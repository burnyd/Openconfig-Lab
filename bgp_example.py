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


ocbgp = ocbind.openconfig_bgp(path_helper=ph)
ocbgp.bgp.global_.config.as_ = 1
ocbgp.bgp.global_.config.router_id = "1.1.1.1"
struct =  json.dumps(ocbgp.get(filter=True), indent=4)

print struct

with open('simple.json', 'w') as f:
  f.write(struct)
I
