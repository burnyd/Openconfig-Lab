#!/bin/bash

echo "stopping and removing ceos1"
docker stop ceos1 && docker rm ceos1

echo "stopping and removing ceos2"
docker stop ceos1 && docker rm ceos1

echo "stopping and removing mgt1"
docker stop mgt1 && docker rm mgt1

echo "removing networking"
docker network rm peering
docker network rm mgt

echo "finished"
