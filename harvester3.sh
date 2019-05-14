#!/bin/bash
starttime=`date +'%Y-%m-%d %H:%M:%S'`
mpiexec -np 2 python3 harvesterControl.py 2 10000000 10000000
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "execution time： "$((end_seconds-start_seconds))"s"