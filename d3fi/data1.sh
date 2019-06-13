#!/bin/bash
SL=$1
DEVICE=$2
X=0

echo "time,bytes,packets,dropped,requeued,txretry,txfailed,sndbuf"
while [ 1 == 1 ];
do
	DATA=$(./tcq/tcq 2>&1 | sed -e '/backlog/d' )
	SNDBUF=$(cat /proc/net/udp | grep "${SL}:" | awk '{ q = "0x" substr($5, 1, 8); printf "%d\n", q }')
	TXRETRY=$(ethtool -S $DEVICE | grep 'tx_retries' | awk '{ print $2 }')
	TXFAILED=$(ethtool -S $DEVICE | grep 'tx_retry_failed' | awk '{ print $2 }')

	echo $X, $DATA, $TXRETRY, $TXFAILED, $SNDBUF
	sleep 1s
	X=$(( X + 1 ))
done