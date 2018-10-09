#!/bin/bash

# set python home
PY_HOME=""
if [ -n "$PY_HOME" ] ; then
    py=$PY_HOME/python
else
    py=python
fi

base=`dirname $0`

nohup $py -m http.server 9000 -d static > $base/out.log &

echo $! > $base/pid
