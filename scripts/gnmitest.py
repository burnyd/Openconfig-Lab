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
target = '10.20.30.24'
port = '6030'
#mode = 'get'
mode = 'subscribe'

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
  """Parses the xpath names.

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

def _subscribe(stub, paths, username, password):
    mysubs = []
    for path in xpath:
        mypath = path_from_string(path)
        #mysub = gnmi_pb2.Subscription(path=mypath, mode=opt.mode, suppress_redundant=opt.suppress, sample_interval=opt.interval*1000000000, heartbeat_interval=opt.heartbeat)
        mysub = gnmi_pb2.Subscription(path=mypath, mode='2', sample_interval=10*1000000000)
        mysubs.append(mysub)

    if username:
        #mysblist = gnmi_pb2.SubscriptionList(prefix=myprefix, mode=opt.mode, allow_aggregation=opt.aggregate, encoding=opt.encoding, subscription=mysubs, use_aliases=opt.use_alias, qos=myqos)
        mysblist = gnmi_pb2.SubscriptionList(prefix=None, mode=0, encoding=JSON_IETF, subscription=mysubs, qos=None)
        mysubreq = gnmi_pb2.SubscribeRequest( subscribe=mysblist )

def main():
  #metadata=[('username', username), ('password', password)]
  paths = _parse_path(_path_names(xpath)) #This is the actual path this uses for OC in JSON format.  This actually gets path lists from the created proto/python file.
  stub = _create_stub(target, port)
  if mode == 'get':
    response = _get(stub, paths, user, password)
    print(json.dumps(json.loads(response.notification[0].update[0].val.
                                 json_ietf_val), indent=2))

  elif mode == 'subscribe':
    #responses = stub.Subscribe(req_iterator, options.timeout, metadata=metadata)
    metadata=[('username', user), ('password', password)]
    responses = stub.Subscribe(_subscribe, metadata=metadata)
    for response in responses:
        if response.HasField('sync_response'):
            log.debug('Sync Response received\n'+str(response))
            secs += time.time() - start
            start = 0
            if options.stats:
                log.info("%d updates and %d messages within %1.2f seconds", upds, msgs, secs)
                log.info("Statistics: %5.0f upd/sec, %5.0f msg/sec", upds/secs, msgs/secs)
            elif response.HasField('error'):
                log.error('gNMI Error '+str(response.error.code)+' received\n'+str(response.error.message))
            elif response.HasField('update'):
                if start==0:
                    start=time.time()
                msgs += 1
                upds += len(response.update.update)
                if not options.stats:
                    log.info('Update received\n'+str(response))
            else:
                log.error('Unknown response received:\n'+str(response))



if __name__ == '__main__':
  main()

