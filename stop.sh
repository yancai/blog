#!/bin/bash

base=`dirname $0`
pidfile=$base/pid

pid=`cat $pidfile`

kill $pid

rm $pidfile
