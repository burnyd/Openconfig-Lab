

# Requirements
============

* docker/Moby (tested in 17.09.0-ce)
* Arista ceos-lab (tested in 4.21.4F)

All Arista supported YANG models can be found in code [here](https://github.com/aristanetworks/yang)

![Alt text](images/background1.jpg?raw=true "lab")

This lab leverages cEOS and Openconfig components (gnmi/grpc in eos, pyangbind, napalm_yang and streaming telemetry)

I plan to use this as a demo for a few upcoming Arista events as well as some playing.

First please download the arista ceos code and follow the instructions before staring and follow the instructions for ceos lab.  Simply replace the first line in the startup.sh script with CEOS_IMAGE= and the name.  For example, running a docker image on my local mac I have a ceosimage and the tag of 4.21.4F so in the bash shell I am using CEOS_IMAGE=ceosimage:4.21.4F

# Explanation

`configs` This directory simply holds configs of the two ceos devices.
`docker` This directory houses the Dockerfile for the mgt1 ubuntu container which can be found [here](https://cloud.docker.com/u/burnyd/repository/docker/burnyd/ubuntu-oc).

`docs` This directory has random ramblings from me in YAML about Openconfig.  
`images` Not really relevant but random screenshots for this repo.

# Enabling gnmi interface on Arista devices
It is extremely simply on eos to enable gnmi interface this is done on startup with ceos containers.
```console
!
management api gnmi
   transport grpc default
!
```
Check to see if gnmi interface is running.
```console
ceos-1#show management api gnmi
Enabled:            Yes
Server:             running on port 6030, in default VRF
SSL Profile:        none
QoS DSCP:           none
```
# Instructions
```console
git clone https://github.com/burnyd/Openconfig-Lab/ && cd OpenConfig-Lab
source startup.sh
```
This may take some time with ceos-lab to boot up and start.  This should launch the entire lab and look like the following...

![Alt text](images/dockerps.jpg?raw=true "dockerps")

To go attach / exec into the mgt1 ubuntu container please issue the following.

```console
sh-3.2# docker exec -it mgt1 bash
root@b6efac7b7b0f:/#
root@b6efac7b7b0f:/# ping ceos1
PING ceos1 (172.24.0.2) 56(84) bytes of data.
64 bytes from ceos1.mgt (172.24.0.2): icmp_seq=1 ttl=64 time=0.151 ms
```
Everything should be pinagable via their docker name with docker networking on the management network.
