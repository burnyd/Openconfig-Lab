echo "Installing go and setting env variables for Go"
wget https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz -P /opt/

sleep 3

sudo tar -C /usr/local -xzf /opt/go1.9.1.linux-amd64.tar.gz
echo Adding Golang variables...
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$(go env GOPATH)/bin
export GOPATH=$(go env GOPATH)
echo Finished....

echo gnmi client..
go get github.com/aristanetworks/goarista/cmd/gnmi

echo Finished

echo installing pyangbind

pip install pyangbind

echo Adding pyangbind env
export PYBINDPLUGIN=`/usr/bin/env python -c \
	'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`
