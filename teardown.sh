#!/bin/bash

echo "stopping and removing ceos1"
docker stop ceos1 && docker rm ceos1

echo "stopping and removing ceos2"
docker stop ceos2 && docker rm ceos2

echo "stopping and removing mgt1"
docker stop mgt1 && docker rm mgt1

echo "stopping and removing influx"
docker stop influx && docker rm influx

echo "stopping and removing kafka"
docker stop kafka && docker rm kafka

echo "stopping and removing telegraf"
docker stop telegraf && docker rm telegraf

echo "stopping and removing grafana"
docker stop grafana && docker rm grafana

echo "removing networking"
docker network rm peering
docker network rm mgt

echo "finished"
