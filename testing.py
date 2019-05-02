from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import json
import logging
import os
import re
import ssl
import sys
import six
import grpc
try:
  import gnmi_pb2
except ImportError:
  print('ERROR: Ensure you\'ve installed dependencies from requirements.txt\n'
        'eg, pip install -r requirements.txt')
import gnmi_pb2_grpc

__version__ = '0.4'

_RE_PATH_COMPONENT = re.compile(r'''
^
(?P<pname>[^[]+)  # gNMI path name
(\[(?P<key>\w+)   # gNMI path key
=
(?P<value>.*)    # gNMI path value
\])?$
''', re.VERBOSE)

xpath = '/interfaces/interface[name=Ethernet1]/state/counters'
user = 'daniel'
password = 'daniel123'
target = '10.20.30.25'
port = '6030'
mode = 'get'

def _parse_path(p_names):
  gnmi_elems = []
  for word in p_names:
    word_search = _RE_PATH_COMPONENT.search(word)
    if not word_search:  # Invalid path specified.
      raise XpathError('xpath component parse error: %s' % word)
    if word_search.group('key') is not None:  # A path key was provided.
      tmp_key = {}
      for x in re.findall(r'\[([^]]*)\]', word):
        tmp_key[x.split("=")[0]] = x.split("=")[-1]
      gnmi_elems.append(gnmi_pb2.PathElem(name=word_search.group(
          'pname'), key=tmp_key))
    else:
      gnmi_elems.append(gnmi_pb2.PathElem(name=word, key={}))
  return gnmi_pb2.Path(elem=gnmi_elems)

def _path_names(xpath):
  if not xpath or xpath == '/':  # A blank xpath was provided at CLI.
    return []
  return xpath.strip().strip('/').split('/')

def _create_stub(target, port):
  """Creates a gNMI Stub.

  Args:
    target: (str) gNMI Target.
    port: (str) gNMI Target IP port.

  Returns:
    a gnmi_pb2_grpc object representing a gNMI Stub.
  """
  channel = gnmi_pb2_grpc.grpc.insecure_channel(target + ':' + port)
  return gnmi_pb2_grpc.gNMIStub(channel)

def _get(stub, paths, username, password):
  if username:  # User/pass supplied for Authentication.
    return stub.Get(
        gnmi_pb2.GetRequest(path=[paths], encoding='JSON_IETF'),
        metadata=[('username', username), ('password', password)])
  #return stub.Get(gnmi_pb2.GetRequest(path=[paths], encoding='JSON_IETF'))

#paths = _parse_path(_path_names(xpath))
#print(paths)
#esting = _path_names(xpath)
#print(testing)

#stub_test = _create_stub(target, port)
stub = _create_stub(target, port)
paths = _parse_path(_path_names(xpath))
response = _get(stub, paths, user, password)
#print(response)
#print(json.dumps(json.loads(response.notification[0].update[0].val.
#                             json_ietf_val), indent=2))

#print (json.dumps(response, indent=2))

"""
notification {
  update {
    path {
      elem {
        name: "interfaces"
      }
      elem {
        name: "interface"
        key {
          key: "name"
          value: "Ethernet1"
        }
      }
      elem {
        name: "state"
      }
      elem {
        name: "counters"
      }
    }
    val {
      json_ietf_val: "{\"openconfig-interfaces:in-broadcast-pkts\": \"63498\", \"openconfig-interfaces:in-discards\": \"0\", \"openconfig-interfaces:in-errors\": \"0\", \"openconfig-interfaces:in-multicast-pkts\": \"3896304\", \"openconfig-interfaces:in-octets\": \"486001405\", \"openconfig-interfaces:in-unicast-pkts\": \"0\", \"openconfig-interfaces:out-broadcast-pkts\": \"39478\", \"openconfig-interfaces:out-discards\": \"0\", \"openconfig-interfaces:out-errors\": \"0\", \"openconfig-interfaces:out-multicast-pkts\": \"633886\", \"openconfig-interfaces:out-octets\": \"95785052\", \"openconfig-interfaces:out-unicast-pkts\": \"0\"}"
    }
  }
}
"""

print(json.dumps(json.loads(response.notification[0].update[0].val.
                             json_ietf_val), indent=2))
