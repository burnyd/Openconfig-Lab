

# Requirements
============

* docker/Moby (tested in 17.09.0-ce)
* Arista ceos-lab (tested in 4.21.4F)

![Alt text](images/background1.jpg?raw=true "Pi")



Will add later

This lab leveraging cEOS and Openconfig(gnmi in eos, pyangbind and napalm-yang)

First please download the arista ceos code and follow the instructions before staring.

git clone https://github.com/burnyd/Openconfig-Lab/

Edit the variable file in startup.sh with the correct ceosimage.  For example, my current image is ceosimage:4.21.4F
which can be found by doing a docker image | grep ceos
