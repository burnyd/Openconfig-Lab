FROM ubuntu:16.04

RUN apt-get update && apt-get install wget python-pip python-dev git net-tools iputils-ping mtr -y

ADD source.sh /tmp/

#RUN /bin/bash -c "source /tmp/mgt1.sh"

#using this to keep the container
CMD tail -f /dev/null
