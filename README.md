

# Requirements
============

* docker/Moby (tested in 17.09.0-ce)
* Arista ceos-lab (tested in 4.21.4F)

All Arista supported YANG models can be found in code [here](https://github.com/aristanetworks/yang)

![Alt text](images/background1.jpg?raw=true "Pi")

This lab leveraging cEOS and Openconfig components (gnmi/grpc in eos, pyangbind, napalm_yang and streaming telemetry)

I plan to use this as a demo for a few upcoming Arista events as well as some playing.

First please download the arista ceos code and follow the instructions before staring and follow the instructions for ceos lab.  Simply replace the first line in the startup.sh script with CEOS_IMAGE= and the name.  For example, running a docker image on my local mac I have a ceosimage and the tag of 4.21.4F so in the bash shell I am using CEOS_IMAGE=ceosimage:4.21.4F

# Explanation

`configs` This directory simply holds configs of the two ceos devices.
`docker` This directory houses the Dockerfile for the mgt1 ubuntu container which can be found [here](https://cloud.docker.com/u/burnyd/repository/docker/burnyd/ubuntu-oc).
`docs` This directory has random ramblings from me in YAML about Openconfig.  
`images` Not really relevant but random screenshots for this repo.



git clone https://github.com/burnyd/Openconfig-Lab/

Edit the variable file in startup.sh with the correct ceosimage.  For example, my current image is ceosimage:4.21.4F
which can be found by doing a docker image | grep ceos
