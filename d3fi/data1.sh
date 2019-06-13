#!/bin/bash
DEVICE=$1
INODE=$2
X=0

echo "time,sent,bytes,packets,dropped,requeued,txretry,txfailed,txrate,xmit,sndbuf"
while [ 1 == 1 ];
do
	DATA=$(./tcq/tcq 2>&1 | sed -e '/sent/d' )
	SNDBUF=$(cat /proc/net/udp | grep "$INODE" | awk '{ q = "0x" substr($5, 1, 8); printf "%d\n", q }')
	ETHSTATS=$(ethtool -S $DEVICE | awk '/tx_retries/ {RETRY=$2} /tx_retry_failed/{FAILED=$2} /txrate/{RATE=$2} /tx_packets/{SENT=$2} END{ print RETRY ", " FAILED ", " RATE ", " SENT }')

	echo $X, $DATA, $ETHSTATS, $SNDBUF
	sleep 1s
	X=$(( X + 1 ))
done