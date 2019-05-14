# Napalm-YANG

Napalm Yang is a very powerful parser which will connect to a device and add running config of the device back to openconfig JSON structure.  

In this example the Napalm-Openconfig-Interfaces.py file will connect to ceos1 and pullback interface information.

```console
root@b6efac7b7b0f:/tmp/scripts# cat /tmp/scripts/Napalm-Openconfig-Interfaces.py
from napalm import get_network_driver
import napalm_yang
from json import dumps

eos_driver = get_network_driver('eos')
eos_device = {'username': 'admin', 'password': 'admin', 'hostname': 'ceos1'}

with eos_driver(**eos_device) as d:
  running_config = napalm_yang.base.Root()
  running_config.add_model(napalm_yang.models.openconfig_interfaces)
  running_config.parse_config(device=d)

print dumps(running_config.get(filter=True), indent=4)
root@b6efac7b7b0f:/tmp/scripts# python Napalm-Openconfig-Interfaces.py
```

Output

```console
{
    "interfaces": {
        "interface": {
            "Ethernet1": {
                "name": "Ethernet1",
                "routed-vlan": {
                    "ipv4": {
                        "config": {
                            "enabled": True
                        },
                        "addresses": {
                            "address": {
                                "12.12.12.1": {
                                    "ip": "12.12.12.1",
                                    "config": {
                                        "ip": "12.12.12.1",
                                        "prefix-length": 24,
                                        "secondary": False
                                    }
                                }
                            }
                        }
                    }
                },
```
