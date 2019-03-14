echo "Installing go and setting env variables for Go"
wget https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz -P /opt/

sleep 3

tar -C /usr/local -xzf /opt/go1.9.1.linux-amd64.tar.gz
echo Adding Golang variables...
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$(go env GOPATH)/bin
export GOPATH=$(go env GOPATH)
echo Finished....

echo gnmi client..
go get github.com/aristanetworks/goarista/cmd/gnmi

echo Finished

echo installing pyangbind and napalm components

pip install pyangbind napalm napalm-yang

echo Adding pyangbind env
export PYBINDPLUGIN=`/usr/bin/env python -c \
	'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`

git clone https://github.com/openconfig/public.git
ln -s public/release/models models

set -e

pyang --split-class-dir ocbind --plugindir $PYBINDPLUGIN \
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
    models/vlan/openconfig-vlan-types.yang \
    models/vlan/openconfig-vlan.yang \
    models/interfaces/openconfig-if-ip.yang  \
    models/bgp/openconfig-bgp.yang \
    models/bgp/openconfig-bgp-policy.yang \
    models/bgp/openconfig-bgp-common.yang \
    models/bgp/openconfig-bgp-common-multiprotocol.yang \
    models/bgp/openconfig-bgp-common-structure.yang \
    models/bgp/openconfig-bgp-peer-group.yang \
    models/bgp/openconfig-bgp-neighbor.yang \
    models/bgp/openconfig-bgp-global.yang \
    models/bgp/openconfig-bgp.yang 
