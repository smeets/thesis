import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import csv

data = {
    'time': [],
    'rssi': [],
    'utxb': [],
    'utxp': [],
    'urxb': [],
    'urxp': [],
    'qtxb': [],
    'qtxp': [],
    'qrxb': [],
    'qrxp': []
}

# time,tx_bytes,tx_pkts,tx_discard,tx_wifi_sent_be,tx_wifi_sent_bk,tx_wifi_sent_vi,tx_wifi_sent_vo,tx_wifi_drop_be,tx_wifi_drop_bk,tx_wifi_drop_vi,tx_wifi_drop_vo,tx_err,tx_unicast,tx_multicast,tx_broadcast,tx_phy_rate,tx_mgmt,tx_mcs_index,tx_nss,tx_bw,tx_sgi,rx_bytes,rx_pkts,rx_discard,rx_err,rx_unicast,rx_multicast,rx_broadcast,rx_unknown,rx_phy_rate,rx_mgmt,rx_ctrl,rx_mcs_index,rx_nss,rx_bw,rx_sgi,hw_noise,snr,rssi,bw

with open(sys.argv[1]) as csvfile:
    txrx_data = csv.reader(csvfile)
    for time, rssi in txrx_data:
        data['time'].append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
        data['rssi'].append(rssi)

legendP = []
legendL = []

def plot(var, lbl, opt):
    x = plt.plot_date(data['time'], var, opt)
    legendP.append(x[0])
    legendL.append(lbl)

plot(data['rssi'], 'rssi [router]', 'yx-')

plt.legend(legendP, legendL)
# box = b.get_position()
# b.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# p.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# plt.legend(legendP, legendL, loc='center left', bbox_to_anchor=(1.125, 0.5))

# fig.tight_layout()
plt.show()
