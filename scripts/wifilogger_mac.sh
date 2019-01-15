#!/bin/bash

airport=/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport

echo "timestamp,channel,rssi,mcs"
while x=1; 
do
 ts=$(date +"%Y-%m-%d %T")
 channel=$(${airport} -I | grep channel | sed 's/.*: //g')
 rssi=$(${airport} -I | grep CtlRSSI | sed 's/.*: //g')
 mcs=$(${airport} -I | grep MCS | sed 's/.*: //g')
 echo "${ts},${channel},${rssi},${mcs}"
 sleep 1
done