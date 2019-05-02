#!/bin/sh
# Copyright (C) 2016  Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

set -e

case `uname -s` in
  (Darwin)
    SED='sed -i ""'
    ;;
  (Linux)
    SED='sed -i'
    ;;
  (*)
    echo >&2 'unsupported platform'
    exit 1
    ;;
esac

curl -s https://api.github.com/repos/openconfig/reference/git/refs/heads/master | jq -r .object.sha > reference_version
version=$(cat reference_version)
echo "Downloading openconfig.proto@$version"
curl -s https://api.github.com/repos/openconfig/reference/contents/rpc/openconfig/openconfig.proto?ref=$version -H "Accept: application/vnd.github.VERSION.raw" > openconfig.proto
# Fix up the import of any.proto (https://github.com/openconfig/reference/issues/24)
$SED "s:github.com/golang/protobuf/ptypes/any:google/protobuf:" openconfig.proto
python -m grpc_tools.protoc -I .:$GOPATH/src --python_out=. --grpc_python_out=. openconfig.proto
