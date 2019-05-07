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
