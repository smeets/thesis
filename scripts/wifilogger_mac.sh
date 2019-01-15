#!/bin/bash

airport=/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport

echo "timestamp,rssi"
while x=1; 
do 
 rssi=$(${airport} -I | grep CtlRSSI | sed 's/.*: //g')
 ts=$(date +"%Y-%m-%d %T")
 echo "${ts},${rssi}"
 sleep 1
done