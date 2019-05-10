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

#xpath = '/interfaces/interface[name=Ethernet1]/state/counters'
xpath = '/network-instances/network-instance[name=default]/protocols/protocol[name=BGP][identifier=BGP]/'
user = 'admin'
password = 'admin'
target = '127.0.0.1'
port = '6031'
mode = 'get'

def _parse_path(p_names):
  """Parses a list of path names for path keys.

  Args:
    p_names: (list) of path elements, which may include keys.

  Returns:
    a gnmi_pb2.Path object representing gNMI path elements.

  Raises:
    XpathError: Unabled to parse the xpath provided.

    p_names will get passed in a list for examples ['interfaces', 'interface[name=Ethernet1]', 'state', 'counters']

    I think this is where it actually calls everything and returns back paths from the function of what is actually available.

  """
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
  """
  All this really does is add the devices into a python list!
  Parses the xpath names.

  This takes an input string and converts it to a list of gNMI Path names. Those
  are later turned into a gNMI Path Class object for use in the Get/SetRequests.
  Args:
    xpath: (str) xpath formatted path.

  Returns:
    list of gNMI path names.
  """
  if not xpath or xpath == '/':  # A blank xpath was provided at CLI.
    return []
  return xpath.strip().strip('/').split('/')  # Remove leading and trailing '/'. For example it turns it into  ['interfaces', 'interface[name=Ethernet1]', 'state', 'counters']


def _get_val(json_value):
  """Get the gNMI val for path definition.

  Args:
    json_value: (str) JSON_IETF or file.

  Returns:
    gnmi_pb2.TypedValue()
  """
  val = gnmi_pb2.TypedValue()
  if '@' in json_value:
    try:
      set_json = json.loads(six.moves.builtins.open(
          json_value.strip('@'), 'rb').read())
    except (IOError, ValueError) as e:
      raise JsonReadError('Error while loading JSON: %s' % str(e))
    val.json_ietf_val = json.dumps(set_json)
    return val
  coerced_val = _format_type(json_value)
  type_to_value = {bool: 'bool_val', int: 'int_val', float: 'float_val',
                   str: 'string_val'}
  if type_to_value.get(type(coerced_val)):
    setattr(val, type_to_value.get(type(coerced_val)), coerced_val)
  return val

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
  """Create a gNMI GetRequest.

  Args:
    stub: (class) gNMI Stub used to build the secure channel.
    paths: gNMI Path
    username: (str) Username used when building the channel.
    password: (str) Password used when building the channel.

  Returns:
    a gnmi_pb2.GetResponse object representing a gNMI GetResponse.
  """
  if username:  # User/pass supplied for Authentication.
    return stub.Get(
        gnmi_pb2.GetRequest(path=[paths], encoding='JSON_IETF'),
        metadata=[('username', username), ('password', password)])
  return stub.Get(gnmi_pb2.GetRequest(path=[paths], encoding='JSON_IETF'))

def path_from_string(path='/'):
    mypath = []

    for e in list_from_path(path):
        eName = e.split("[", 1)[0]
        eKeys = re.findall('\[(.*?)\]', e)
        dKeys = dict(x.split('=', 1) for x in eKeys)
        mypath.append(gnmi_pb2.PathElem(name=eName, key=dKeys))

    return gnmi_pb2.Path(elem=mypath)

def main():
  #metadata=[('username', username), ('password', password)]
  paths = _parse_path(_path_names(xpath))
  #This prints out the entire elem path with the list broken up
  stub = _create_stub(target, port)
  #This is easy to understand it simply creates the connection
  if mode == 'get':
    response = _get(stub, paths, user, password)
    #This is where it actually talks with the device and begins to pull things back it looks like the following
    """
        val {
      json_ietf_val: "{\"openconfig-interfaces:in-broadcast-pkts\": \"63498\", \"openconfig-interfaces:in-discards\": \"0\", \"openconfig-interfaces:in-errors\": \"0\", \"openconfig-interfaces:in-multicast-pkts\": \"3895875\", \"openconfig-interfaces:in-octets\": \"485946640\", \"openconfig-interfaces:in-unicast-pkts\": \"0\", \"openconfig-interfaces:out-broadcast-pkts\": \"39478\", \"openconfig-interfaces:out-discards\": \"0\", \"openconfig-interfaces:out-errors\": \"0\", \"openconfig-interfaces:out-multicast-pkts\": \"633859\", \"openconfig-interfaces:out-octets\": \"95779841\", \"openconfig-interfaces:out-unicast-pkts\": \"0\"}"
    }
  }
}"""
    print(json.dumps(json.loads(response.notification[0].update[0].val.
                                 json_ietf_val), indent=2))

if __name__ == '__main__':
  main()
