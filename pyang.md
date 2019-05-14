# Pyang

Pyangbind is simply a parser for all openconfig models.  Pyang will turn actual YANG models into python objects ie lists, tupples and dictionaries.

Lets take a look at the bgp model.

```console
sh-3.2# docker exec -it mgt1 bash
pyang -f tree /models/bgp/*
root@b6efac7b7b0f:/# cd /tmp/scripts/
module: openconfig-bgp
  +--rw bgp
     +--rw global
     |  +--rw config
     |  |  +--rw as           oc-inet:as-number
     |  |  +--rw router-id?   oc-yang:dotted-quad
     |  +--ro state
     |  |  +--ro as           oc-inet:as-number
     |  |  +--ro router-id?   oc-yang:dotted-quad
     |  +--rw default-route-distance
```

the bgp_example.py is a good way to reflect the model and how it interacts with the python code.

```console
ocbgp = ocbind.openconfig_bgp(path_helper=ph)
ocbgp.bgp.global_.config.as_ = 1
ocbgp.bgp.global_.config.router_id = "1.1.1.1"
struct =  json.dumps(ocbgp.get(filter=True), indent=4)
```

Lets reflect upon those and compare then to the module above it.

ocbgp.bgp.global_.config.as_ = 1 #This has to be a oc-inet which is a integer
ocbgp.bgp.global_.config.router_id = "1.1.1.1" #This has to be a dotted-quad which is a ipv4 address
```

If either are changed to something that is not the same as the unit should be pyang will bomb and not work properly.  

Lets look at a more complicated example bgp_config.py which will take a python dictionary and turn it into code.  

```console
root@b6efac7b7b0f:/tmp/scripts# python bgp_config.py
{
    "bgp": {
        "global": {
            "config": {
                "as": 65002,
                "router-id": "2.2.2.2"
            }
        },
        "neighbors": {
            "neighbor": {
                "12.12.12.1": {
                    "config": {
                        "neighbor-address": "12.12.12.1",
                        "peer-as": 65001
                    },
                    "neighbor-address": "12.12.12.1"
                }
            }
        }
    }
}
{
    "bgp": {
        "global": {
            "config": {
                "as": 65001,
                "router-id": "1.1.1.1"
            }
        },
        "neighbors": {
            "neighbor": {
                "12.12.12.2": {
                    "config": {
                        "neighbor-address": "12.12.12.2",
                        "peer-as": 65002
                    },
                    "neighbor-address": "12.12.12.2"
                }
            }
        }
    }
}
```

Either way, the key point here is that pynag can parse through and add yang models to code.  The result would be importing any module into python code and then sending it directly to the device.
