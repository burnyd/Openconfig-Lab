Will add later

This lab leveraging cEOS and Openconfig(gnmi in eos, pyangbind and napalm-yang)

First please download the arista ceos code and follow the instructions before staring.

git clone https://github.com/burnyd/Openconfig-Lab/

Edit the variable file in startup.sh with the correct ceosimage.  For example, my current image is ceosimage:4.21.4F
which can be found by doing a docker image | grep ceos

sh-3.2# docker images | grep ceos
ceosimage                        4.21.4F             5796dd78e5fd        2 days ago          1.54GB

Start the environment.

source startup.sh

This should take a few minutes by the time it is ran you should be able to go into the environment

sh-3.2# docker exec -it mgt1 bash
root@83f132460717:/# git clone https://github.com/burnyd/Openconfig-Lab/

cd Openconfig-Lab/

#Installs all of the napalm, golang, gnmi aplications and openconfig models.
source scripts/source.sh
