#!/bin/bash

MPM=/home/tengqing/Repository/MPM/MPM/build/MPM

parallel_num=8

for i in `seq 42 108`; do
    (
        cd ${i} || exit
        ${MPM} gyroid.mpm > gyroid.log 2>&1
    ) &
    echo "Running ${i}"
    if (( $(jobs | wc -l) >= ${parallel_num} )); then
        wait -n || exit
    fi
done

wait
