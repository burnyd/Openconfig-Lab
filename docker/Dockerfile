FROM ubuntu:16.04

#Create the Working directory where models and all will be /OC
WORKDIR /OC

#Copy contents from the Git repo into the /OC directory
COPY . .

#Install necessary packages
RUN apt-get update && apt-get install wget python-pip python-dev git net-tools iputils-ping mtr vim -y

#Install necessary Python packages
RUN pip install grpcio futures grpcio-tools protobuf influxdb pyangbind

ENV PYBINDPLUGIN /usr/local/lib/python2.7/dist-packages/pyangbind/plugin
#Clone latest Git repos for models and add a symbolic link to models 
RUN git clone https://github.com/openconfig/public.git && ln -s public/release/models/OC models

#Create the python to OC binding.py file which binds yang to Python models.
RUN pyang --split-class-dir ocbind --plugindir /usr/local/lib/python2.7/dist-packages/pyangbind/plugin \
    -p models \
    -f pybind \
    --use-xpathhelper \
    models/interfaces/openconfig-interfaces.yang \
    models/vlan/openconfig-vlan.yang \
    models/openconfig-extensions.yang  \
    models/types/openconfig-yang-types.yang \
    models/types/openconfig-types.yang \
    models/types/openconfig-inet-types.yang \
    models/interfaces/openconfig-interfaces.yang \
    models/interfaces/openconfig-if-ethernet.yang \
    models/interfaces/openconfig-if-aggregate.yang \
    models/interfaces/openconfig-if-ip.yang \
    models/bgp/openconfig-bgp-errors.yang \
    models/bgp/openconfig-bgp-types.yang \
    models/policy/openconfig-policy-types.yang \
    models/policy/openconfig-routing-policy.yang \
    models/bgp/openconfig-bgp-policy.yang \
    models/bgp/openconfig-bgp-common.yang \
    models/bgp/openconfig-bgp-common-multiprotocol.yang \
    models/bgp/openconfig-bgp-common-structure.yang \
    models/bgp/openconfig-bgp-peer-group.yang \
    models/bgp/openconfig-bgp-neighbor.yang \
    models/bgp/openconfig-bgp-global.yang \
    models/bgp/openconfig-bgp.yang \
    models/network-instance/openconfig-network-instance.yang

#using this to keep the container alive.
CMD tail -f /dev/null
