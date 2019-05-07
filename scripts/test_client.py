#!/usr/bin/env python
# Copyright (C) 2016  Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

"""The Python implementation of a gNMI client."""

from __future__ import print_function

import argparse
import logging
import sys
import time

import grpc
import grpc.framework.interfaces.face
import pyopenconfig.gnmi_pb2
import pyopenconfig.resources

#import potsdb
import atexit

from influxdb import InfluxDBClient
import datetime

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('test-client')
logger.setLevel(logging.DEBUG)

#host_ip = "localhost"
#host_port = 80050

influx = 'influx'
client = InfluxDBClient(host=influx, port=8086, username='dan', password='dan', ssl=False, verify_ssl=False)
client.switch_database('OC')

mode = "stream"
nums = 0

"""db_host = '127.0.0.1'
db_port = 4242
metrics = potsdb.Client(db_host, port=db_port)
"""

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT8:%H:%MZ')

def encodePath(path):
    pathStrs = ""
    for pe in path:
        pstr = pe.name
        if pe.key:
             for k, v in pe.key.iteritems():
                  pstr += "[" + str(k) + "=" + str(v) + "]"
        pathStrs = pathStrs + "." + pstr
    return pathStrs[1:]


def saveToInflux(response):
    for update in response.update.update:
        path_metric = encodePath(update.path.elem)
        value = update.val.int_val
        time_now = str(datetime.datetime.now())
        json_data = [
        {
        "measurement": "OC-Data",
        "tags": {
            "host": "server",
            "region": "NYC"
        },
        "time": ""+time_now+"",
        "fields": {
            "value": path_metric
        }
    }
]
        client.write_points(json_data)
        print("Inserted %s using value %s" %(path_metric, value))



def get(stub, path_str, metadata):
    """Get and echo the response"""
    response = stub.Get(pyopenconfig.resources.make_get_request(path_str),
                        metadata=metadata)
    print(response)

def subscribe(stub, path_str, mode, metadata):
    global nums
    """Subscribe and echo the stream"""
    logger.info("start to subscrib path: %s in %s mode" % (path_str, mode))
    subscribe_request = pyopenconfig.resources.make_subscribe_request(path_str=path_str, mode=mode)
    i = 0
    try:
        for response in stub.Subscribe(subscribe_request, metadata=metadata):
            #logger.debug(response)
            #saveToTSDB(response)
            saveToInflux(response)
            i += 1
            nums = i
    except grpc.framework.interfaces.face.face.AbortionError, error: # pylint: disable=catching-non-exception
        if error.code == grpc.StatusCode.OUT_OF_RANGE and error.details == 'EOF':
            # https://github.com/grpc/grpc/issues/7192
            sys.stderr.write('EOF after %d updates\n' % i)
            logger.info('EOF after %d updates\n' % i)
        else:
            raise

    logger.info("Finished streaming, %s updates has been streamed." % i)

def shutdown_hook():
    global nums
    try:
        pass
    except Exception:
        pass
    finally:
        logger.info("%s updates has been streamed." % nums)
        logger.info('existing program')


def run():
    """Main loop"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                        help='OpenConfig server host')
    parser.add_argument('--port', type=int, default=80051,
                        help='OpenConfig server port')
    parser.add_argument('--username', type=str, help='username')
    parser.add_argument('--password', type=str, help='password')
    parser.add_argument('--mode', type=str, default='stream', help='subscription mode')
    parser.add_argument('--debug', type=str, default='on', help='debug level')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--get',
                       help='OpenConfig path to perform a single-shot get')
    group.add_argument('--subscribe',
                       help='OpenConfig path to subscribe to')
    args = parser.parse_args()

    metadata = None
    if args.debug == "off":
        logger.setLevel(logging.INFO)

    if args.username or args.password:
        metadata = [("username", args.username), ("password", args.password)]

    channel = grpc.insecure_channel(args.host + ":" + str(args.port))
    stub = pyopenconfig.gnmi_pb2.gNMIStub(channel)

    atexit.register(shutdown_hook)

    if args.get:
        get(stub, args.get, metadata)
    elif args.subscribe:
        subscribe(stub, args.subscribe, args.mode, metadata)
    else:
        subscribe(stub, '/', metadata)


if __name__ == '__main__':
    run()
