radio
-----

 - `used_channels` - Channels in use by neighboring BSSs
 - `phy_rate` - (kbps) The actual PHY rate used by the radio to
transmit the most recent data frame.
 - `max_phy_rate` - (kbps) The theoretical maximum PHY rate in which
the radio can transmit frames in its current
configuration.
 - `channel` - Operating channel used by the radio. In case
of automatic channel selection, the chosen
channel is displayed.
 - `channel_width` - Operating channel bandwidth
 - `rts_threshold` - Threshold in bytes that determines for which frames the RTS mechanisms are used.
 - ? `tx_power_adjust` - The value by which the output power is
increased or decreased

radio.monitor
-------------

 - `medium_available` - % medium availability in period
 - `glitch` - failed CRC checks in sample period?
 - `txtime` - Reflects the time spent transmitting in % within a Chanim measurement period

radio.bsslist
-------------
per mac addr

 - `ssid`
 - `channel`
 - `rssi` - (dBm)

accesspoint.station
-------------------
per STA

 - `num_associations` - The amount of associations that this STA has
performed over time with a given BSSID
 - `capabilities` - Indication of the announced/negotiated
WLAN features from a STA
 - `last_disconnect_X` - maybe
 - `rssi` - (dbm) Indication of the current RSSI value recorded
 - `tx_noack_failures` - Indication of the total amount of packets
sent for which the STA did not send an ACK
 - `idle_time` - (seconds) Indication of the total time that a STA
remains idle (no data transmission) while
connected.
 - `assoc_time` - (seconds) Indication of the total time that a given STA is connected to the BSSID

 + average tx/rx bytes/packet/bandwidth counters


