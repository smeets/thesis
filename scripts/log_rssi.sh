#!/bin/ash

while [[ 1 -eq 1 ]]; do
	rssi=$(ubus call wireless.accesspoint.station get \
	'{ "macaddr": "xaxa" }' \
	| grep rssi \
	| sed 's/.*"rssi": //')
	echo "$(date),$rssi"
	sleep 1s
done