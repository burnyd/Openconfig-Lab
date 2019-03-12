#!/usr/bin/env python

import sys
import os
sys.path.append("pyangbind/pyangbind/")
import pyangbind.lib.pybindJSON as pybindJSON
import pyangbind.lib.xpathhelper as xpathhelper
import json
import ocbind
from pyangbind.lib.serialise import pybindJSONDecoder
ph = xpathhelper.YANGPathHelper()

eos_bgp = {'ceos1': {'AS': '65001', 'PEER_AS': '65002', 'ROUTER_ID': '1.1.1.1', 'PEER': '12.12.12.2'}, 'ceos2': {'AS': '65002', 'PEER_AS': '65001', 'ROUTER_ID': '2.2.2.2', 'PEER': '12.12.12.22'}}


func main():
for bgp_results in eos_bgp:
    ocbgp = ocbind.openconfig_bgp(path_helper=ph)
    ocbgp.bgp.global_.config.as_ = bgp_results['AS']
    ocbgp.bgp.global_.config.router_id = bgp_results['ROUTER_ID']
    ocbgp.bgp.neighbors.neighbor.add(bgp_results['PEER'])
    ocbgp.bgp.neighbors.neighbor[bgp_results['PEER']].config.peer_as = bgp_results['PEER_AS']
    struct =  json.dumps(ocbgp.get(filter=True), indent=4)
    print struct
    with open(bgp_results, 'w') as f:
      f.write(struct)

main()
