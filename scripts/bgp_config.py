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

eos_bgp = {'ceos1': {'AS': '65001', 'PEER_AS': '65002', 'ROUTER_ID': '1.1.1.1', 'PEER': '12.12.12.2'}, 'ceos2': {'AS': '65002', 'PEER_AS': '65001', 'ROUTER_ID': '2.2.2.2', 'PEER': '12.12.12.1'}}


def main():
  for k,v in eos_bgp.iteritems():
    ocbgp = ocbind.openconfig_bgp(path_helper=ph)
    ocbgp.bgp.global_.config.as_ = v['AS']
    ocbgp.bgp.global_.config.router_id = v['ROUTER_ID']
    ocbgp.bgp.neighbors.neighbor.add(str(v['PEER']))
    ocbgp.bgp.neighbors.neighbor[str(v['PEER'])].config.peer_as = v['PEER_AS']
    struct = json.dumps(json.loads(pybindJSON.dumps(ocbgp)), indent=4, sort_keys=True)
    print struct
    with open(k, 'w') as f:
      f.write(struct)

main()
