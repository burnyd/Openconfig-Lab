#!/bin/bash

CEOS_IMAGE=ceosimage:4.21.4F

ping -q -c5 google.com > /dev/null

if [ $? -eq 0 ]
then
	echo "connectivity is there"
else    echo "connectivity is not there"
        exit 1
fi

echo "creating containers"
docker create --name=ceos1 --privileged -p 6031:6030 -e CEOS=1 -e container=docker -e EOS_PLATFORM=ceoslab -e SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 -e ETBA=1 -e INTFTYPE=eth -i -t $CEOS_IMAGE /sbin/init
docker create --name=ceos2 --privileged -p 6032:6030 -e CEOS=1 -e container=docker -e EOS_PLATFORM=ceoslab -e SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 -e ETBA=1 -e INTFTYPE=eth -i -t $CEOS_IMAGE /sbin/init
docker create --name=mgt1 -it burnyd/ubuntu-oc:latest
docker create --name=influx -it -p 8083:8083 -p 8086:8086 -p 8088:8088 -p 8089:8089 -e INFLUXDB_DB=OC -e INFLUXDB_ADMIN_USER=dan -e INFLUXDB_ADMIN_PASSWORD=dan -e INFLUXDB_USER=dan -e INFLUXDB_USER_PASSWORD=dan $PWD/scripts/influxdb.conf:/etc/influxdb/influxdb.conf influxdb
docker create --name=grafana -it -p 3000:3000 grafana/grafana
docker create --name=zookeeper -it -p 2181 -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper
docker create --name=kafka -it -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka
docker create --name=telegraf -it -v $PWD/scripts/telegraf.conf:/etc/telegraf/telegraf.conf telegraf

echo "creating networking"
docker network create peering
docker network create mgt
docker network connect peering ceos1
docker network connect peering ceos2
docker network connect mgt mgt1
docker network connect mgt ceos1
docker network connect mgt ceos2
docker network connect mgt influx
docker network connect mgt zookeeper
docker network connect mgt kafka
docker network connect mgt telegraf
docker network connect mgt grafana

echo "starting ceos containers this may take a while"
docker start ceos1
docker start ceos2

sleep 180s

echo "Starting infrastructure containers"

docker start mgt1
docker start influx
docker start zookeeper
docker start kafka
docker start telegraf
docker start grafana

echo "copying over configs"
docker cp ./configs/ceos-1/startup-config ceos1:/mnt/flash/startup-config
docker cp ./configs/ceos-2/startup-config ceos2:/mnt/flash/startup-config
docker exec -it ceos1 Cli -p 15 -c "copy start run"
docker exec -it ceos2 Cli -p 15 -c "copy start run"

#echo "Creating influx OC DB"
#curl -XPOST 'http://localhost:8086/query?u=myusername&p=mypassword' --data-urlencode 'q=CREATE DATABASE "OC"'
#docker exec -it influx influx -execute 'CREATE DATABASE OC'

docker exec -it influx influx -execute 'CREATE USER dan WITH PASSWORD 'dan' WITH ALL PRIVILEGES'
docker exec -it influx influx -execute 'GRANT ALL ON OC to dan'
#echo "Creating influx user"
#curl "http://localhost:8086/query" --data-urlencode "q=CREATE USER dan WITH PASSWORD 'dan' WITH ALL PRIVILEGES"

echo "********** To enter the lab please docker exec -it mgt1 bash *********"
