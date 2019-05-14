

# Requirements

Make sure to first read the README in the repo which will build the lab environment before proceeding.

``console
git clone https://github.com/burnyd/Openconfig-Lab/ && cd OpenConfig-Lab
source startup.sh
```

# Google gnxi python grpc interface

[Google GNXI project](https://github.com/google/gnxi)

The Google python gnmi interface is quite nice for anyone who knows python.  This will allow for python to use a Google protobuf file which is located in the scripts directory.

To test to make sure that the gnmi client is working properly the test simply sends a grpc stream to ceos1 and pulls back the path for interface counters of Ethernet1.

```console
sh-3.2# docker exec -it mgt1 bash
root@b6efac7b7b0f:/# cd /tmp/scripts/
root@b6efac7b7b0f:/tmp/scripts# python gnmitest.py
{
  "openconfig-interfaces:in-octets": "2363",
  "openconfig-interfaces:in-errors": "0",
  "openconfig-interfaces:in-multicast-pkts": "15",
  "openconfig-interfaces:out-octets": "15315",
  "openconfig-interfaces:in-broadcast-pkts": "28",
  "openconfig-interfaces:out-multicast-pkts": "115",
  "openconfig-interfaces:in-unicast-pkts": "0",
  "openconfig-interfaces:out-unicast-pkts": "0",
  "openconfig-interfaces:out-broadcast-pkts": "5",
  "openconfig-interfaces:out-discards": "0",
  "openconfig-interfaces:out-errors": "0",
  "openconfig-interfaces:in-discards": "0"
}
```

The gnmicli from the actual google repo will take arguments for the CLI so lets check the bgp path for example of ceos2.

```console
sh-3.2# docker exec -it mgt1 bash
root@b6efac7b7b0f:/# cd /tmp/scripts/
root@b6efac7b7b0f:/tmp/scripts# python gnmicli.py -n -m get -t ceos2 -p 6030 -user admin -pass admin -x /network-instances/network-instance[name=default]/protocols/protocol[name=BGP][identifier=BGP]

{
  "openconfig-network-instance:name": "BGP",
  "openconfig-network-instance:isis": {
    "global": {
```
Now that we know this is working lets go ahead and kick off the streaming client


```console
root@b6efac7b7b0f:/tmp/scripts# python subscribe.py --host ceos1 --port 6030 --username admin --password admin --subscribe "interfaces/interface[name=Ethernet1]/state/counters"
INFO:test-client:start to subscrib path: interfaces/interface[name=Ethernet1]/state/counters in stream mode
[name: "interfaces"
, name: "interface"
key {
  key: "name"
  value: "Ethernet1"
}
, name: "state"
, name: "counters"
]
Inserted interfaces.interface[name=Ethernet1].state.counters.in-broadcast-pkts using value 88

Inserted interfaces.interface[name=Ethernet1].state.counters.in-discards using value 0

Inserted interfaces.interface[name=Ethernet1].state.counters.in-errors using value 0

Inserted interfaces.interface[name=Ethernet1].state.counters.in-multicast-pkts using value 19
```

This python file will simply insert data into the kafka stream it will then be inserted from the consumer of it which is telegraf and inserted into grafana

# Log into Grafana

Open up your browser and try http://127.0.0.1:3000

```console
username: admin
password: admin
```

Click on the add source button.  

server is influx database is OC username / password are dan/dan

![Graph Source](images/addsource.jpg?raw=true "addsource")

Once this is finished select a new graph.

Grafana is nice because it will tab complete for all units that are within Influx.

![Eth1](images/eth1graph.jpg?raw=true "eth1graph")

Select the following just like the output above and this should give exactly that.
