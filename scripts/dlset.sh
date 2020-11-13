#!/bin/bash

CONF=$1
TEST=$2
mkdir -p ./datasets/$CONF/$TEST
scp -r allah@192.168.9.194:~/jana/data/$TEST/result.csv ./datasets/$CONF/$TEST/r1.csv
scp -r allah@192.168.9.234:~/jana/data/$TEST/result.csv ./datasets/$CONF/$TEST/r2.csv
scp -r allah@192.168.9.242:~/jana/data/$TEST/result.csv ./datasets/$CONF/$TEST/r3.csv