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
docker create --name=ceos1 --privileged -e CEOS=1 -e container=docker -e EOS_PLATFORM=ceoslab -e SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 -e ETBA=1 -e INTFTYPE=eth -i -t $CEOS_IMAGE /sbin/init
docker create --name=ceos2 --privileged -e CEOS=1 -e container=docker -e EOS_PLATFORM=ceoslab -e SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 -e ETBA=1 -e INTFTYPE=eth -i -t $CEOS_IMAGE /sbin/init
docker create --name=mgt1 -it burnyd/ubuntu-oc

echo "creating networking"
docker network create peering
docker network create mgt
docker network connect peering ceos1
docker network connect peering ceos2
docker network connect peering mgt
docker network connect mgt mgt1
docker network connect mgt ceos1
docker network connect mgt ceos2

echo "starting containers this may take a while"
docker start ceos1
docker start ceos2
docker start mgt1

sleep 240s

echo "copying over configs"
docker cp ./configs/ceos-1/startup-config ceos1:/mnt/flash/startup-config
docker cp ./configs/ceos-2/startup-config ceos2:/mnt/flash/startup-config
docker exec -it ceos1 Cli -p 15 -c "copy start run"
docker exec -it ceos2 Cli -p 15 -c "copy start run"
