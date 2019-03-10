docker run -it mgt1 /bin/bash
docker exec -it mgt1 bash
source /tmp/source.sh 
gnmi  -addr ceos-1:6030 -username admin -password admin get '/'
