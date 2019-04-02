# ubus

 - `$ap_id`: An accesspoint identifier: `ap0`, `ap1`, `ap2`, etc.
 - `$mac_address`: A lower-case MAC: `b8:27:eb:73:7b:ae`
 - `$radio_ssid`: A common name for the network: `El_Dorito`, `Wi-Spy Story 5`
 - `$radio_id`: A radio name: `radio_2G`, `radio_5G`
 - `$interface_id`: network interface name: `wl0`, `wl1`, `wl0_1`

## wireless.accesspoint
[src](wireless.accesspoint.get.json)

`ubus call wireless.accesspoint get`

```json
{
	"$ap_id": {
	    "ssid":         "[string]: $interface_id",
	    "ap_isolation": "[number]: 0, 1",
	    "public":       "[number]: 0, 1",
	    "max_assoc":    "[number]: 0, 8",
	    "uuid":         "[string,32]: uuid-string"
	}
}
```

### wireless.accesspoint.acl
omitted

### wireless.accesspoint.station
[src](wireless.accesspoint.station.get.json)

`ubus call wireless.accesspoint.station get`

```json
{
	"$ap_id": {
		"$mac_address": {
		    "state": "Authenticated Associated Authorized",
		    "flags": "WMM AMPDU",
		    "capabilities": "802.11n 1x1 WMM SGI20 AMPDU LDPC",
		    "authentication": "WPA2PSK",
		    "encryption": "AES",
		    "last_auth_timestamp": "02:08:06-08\/05\/2017",
		    "last_authentication_status": "Success",
		    "last_assoc_timestamp": "02:08:06-08\/05\/2017",
		    "last_assoc_status": "Success",
		    "last_ssid": "$radio_ssid",
		    "last_authentication": "WPA2PSK",
		    "last_encryption": "AES",
		    "num_associations": 54,
		    "last_wpssession_timestamp": "",
		    "last_wps_version": 0,
		    "last_wpahandshake_timestamp": "19:36:44-03\/05\/2017",
		    "last_wpahandshake_status": "Success",
		    "last_authorization_timestamp": "02:08:08-08\/05\/2017",
		    "last_disconnect_timestamp": "02:08:06-08\/05\/2017",
		    "last_disconnect_by": "Station",
		    "last_statistics_timestamp": "11:08:06-10\/05\/2017",
		    "last_rssi": -77,
		    "last_rssi_history": "-78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -79 -79 -79 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -77 -77 -77 -77 -77 -77 -77 -77 -79 -79 -79 -79 -79 -79 -79 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -77 -77 -77 -77 -77 -77 -77 -77 -77 ",
		    "tx_packets": 1131,
		    "tx_bytes": 151308,
		    "tx_noack_failures": 2955,
		    "tx_data_rate": 0,
		    "tx_data_rate_history": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ",
		    "tx_phy_rate": 13000,
		    "tx_phy_rate_coded": "M1",
		    "tx_phy_rate_history": "13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 13000 ",
		    "rx_packets": 108349,
		    "rx_sec_failures": 0,
		    "rx_bytes": 4756821,
		    "rx_data_rate": 0,
		    "rx_data_rate_history": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ",
		    "rx_phy_rate": 1000,
		    "rx_phy_rate_coded": "L1",
		    "rx_phy_rate_history": "1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 ",
		    "rssi": -77,
		    "rssi_history": "-78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 -79 -79 -79 -78 -78 -78 -78 -78 -78 -78 -78 -78 -78 ",
		    "assoc_time": 204369,
		    "idle_time": 2,
		    "ps_on_time": 4658992,
		    "ps_off_on_transistions": 43913,
		    "last_measurement": "11:07:39-10\/05\/2017",
		    "av_txbw_used": 100,
		    "av_rxbw_used": 100,
		    "av_txss_used": 0,
		    "av_rxss_used": 0,
		    "av_rx_phyrate_history": 0,
		    "av_tx_phyrate_history": 0,
		    "av_rx_rate_history": 0,
		    "av_tx_rate_history": 0,
		    "av_rssi": -78,
		    "av_ps_on_time": 18,
		    "ps_on_time_history": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 344 194 0 0 0 0 0 0 0 0 0 0 0 0 "
		}
	}
}
```

## wireless.radio
[src](wireless.radio.get.json)

`ubus call wireless.radio get`

```json
{
	"RADIO NAME": {
	    "max_phy_rate": 130000,
	    "phy_rate":                  "[number]: 48000",
	    "supported_frequency_bands": "[string]: 2.4GHz, 5GHz",
	    "supported_standards":       "[string]: bgn, anc",
	    "standard":                  "[string]: bgn, anc",
	    "band":                      "[string]: 2.4GHz, 5GHz",
	    "allowed_channels":          "[string]: channel_id+",
	    "used_channels":             "[string]: channel_id+",
	    "requested_channel":         "[string]: auto",
	    "channel":                   "[number]: channel_id",
	    "channel_width": 			 "[string]: 20MHz, 80MHz",
	    "beacon_period": 100,
	    "dtim_interval": 1,
	    "rts_threshold": 2347,
	    "rateset": [
	    	"1(b) 2(b) 5.5(b) 6 9 11(b) 12 18 24 36 48 54 ",
	    	"6(b) 9 12(b) 18 24(b) 36 48 54 "
	    ],
	    "frame_bursting": 0,
	    "sgi": 0,
	    "cdd": "off",
	    "stbc": 0,
	    "ldpc": 0,
	    "advanced_qam": 0,
	    "ampdu": 1,
	    "amsdu": 0,
	    "amsdu_in_ampdu": 0,
	    "txbf": ["off", "auto"],
	    "mumimo": ["off", "auto"],
	    "interference_mode": "auto",
	    "interference_channel_list": ["1 2 3 4 5 6 7 8 9 10 11 12 13", ""],
	    "ht_security_restriction": 1,
	    "max_target_power": ["15.75", "0.0"],
	    "max_target_power_adjusted": ["15.75", "0.0"],
	    "tx_power_adjust": "0",
	    "tx_power_overrule_reg": 0,
	    "sta_minimum_mode": "none",
	    "remotely_managed": 0,
	    "integrated_ap": 1,
	    "max_boot_cac": 0,
	    "ocac": 0,
	    "driver_version": ["7.14.89.14", "37.4.15.62"]
	}
}
```

### wireless.radio.acs
omitted

### wireless.radio.bsslist
[src](wireless.radio.bsslist.get.json)

`ubus call wireless.radio.bsslist get`

```json
{
	"$radio_id": {
        "$mac_address": {
		    "ssid":       "[string]: $radio_ssid",
		    "channel":    "[number]: 9",
		    "chan_descr": "[string]: 9",
		    "rssi":       "[number, dBm?]: -58",
		    "sec":        "[string]: OPEN, WPAWPA2PSK",
		    "cap":        "[string, bitset?]: 0428"
		}
    }
}
```

### wireless.radio.monitor
[src](wireless.radio.monitor.get.json)

`ubus call wireless.radio.monitor get`

```json
{
    "$radio_id": {
        "last_measurement": "11:14:39-10\/05\/2017",
        "measurement_interval": 30,
        "medium_available": 93,
        "glitch": 349,
        "txtime": 3,
        "rxtime_inside_bss": 0,
        "rxtime_outside_bss": 1,
        "probe_request": {
            "$mac_address": {
                "age": 59,
                "rssi": -75
            }
        }
    }
}
```

### wireless.radio.stats
[src](wireless.radio.stats.get.json)

`ubus call wireless.radio.stats get`

```json
{
    "$radio_id": {
        "tx_packets": 43041028,
        "tx_unicast_packets": 38267271,
        "tx_broadcast_packets": 2431051,
        "tx_multicast_packets": 2342706,
        "tx_errors": 0,
        "tx_discards": 0,
        "tx_bytes": 3049093135,
        "rx_packets": 16876400,
        "rx_unicast_packets": 16330109,
        "rx_broadcast_packets": 154651,
        "rx_multicast_packets": 391640,
        "rx_errors": 0,
        "rx_discards": 0,
        "rx_bytes": 3245298511
    }
}
```