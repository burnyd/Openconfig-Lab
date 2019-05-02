# Copyright (C) 2016  Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

"""Common resources used by gRPC OpenConfig clients and servers."""

import pyopenconfig.gnmi_pb2
import re


def make_path(path_str):
    """Create a Path object from a string path"""
    element = path_str.split('/')
    path = pyopenconfig.gnmi_pb2.Path(element=element)
    return path

def make_new_path(path_str):
    """Create a Path object from a string path"""
    element = path_str.split('/')
    pathElements = make_pathelements(element)
    print pathElements
    path = pyopenconfig.gnmi_pb2.Path(elem=pathElements)
    return path

def make_pathelements(element):
    pathElements = []
    for e in element:
        if '[' in e and ']' in e:
            name = e[:e.find('[')]
            dicts = re.findall(r'\[([^]]*)\]', e)
            key = {}
            for d in dicts:
                k = d[:d.find('=')]
                v = d[d.find('=')+1:]
                key[k]=v 
            pathElement = pyopenconfig.gnmi_pb2.PathElem(name=name,key=key)
            pathElements.append(pathElement)
        else:
            pathElement = pyopenconfig.gnmi_pb2.PathElem(name=e)
            pathElements.append(pathElement)
    return pathElements
        


def make_get_request(path_str='/'):
    """Create a subscribe request from a string path"""
    path = make_path(path_str)
    return pyopenconfig.gnmi_pb2.GetRequest(path=[path])


def make_subscribe_request(path_str='/', mode='stream'):
    """Create a subscribe request from a string path"""
    path = make_new_path(path_str)
    subscription = pyopenconfig.gnmi_pb2.Subscription(path=path)
    if mode == "once":
        mode = 1
    elif mode == "poll":
        mode = 2
    else:
        mode = 0
    subscription_list = pyopenconfig.gnmi_pb2.SubscriptionList(subscription=[subscription],mode=mode)
    yield pyopenconfig.gnmi_pb2.SubscribeRequest(subscribe=subscription_list)
