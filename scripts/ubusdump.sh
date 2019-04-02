#!/bin/ash

namespaces=$(ubus list)

for ns in namespaces
do
	echo "${ns} objects:"
	ubus -v list ${ns}
done

