import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
import sys

time, tx_bytes, tx_pkts, tx_discard, tx_wifi_sent_be, tx_wifi_sent_bk, tx_wifi_sent_vi, tx_wifi_sent_vo, tx_wifi_drop_be, tx_wifi_drop_bk, tx_wifi_drop_vi, tx_wifi_drop_vo, tx_err, tx_unicast, tx_multicast, tx_broadcast, tx_phy_rate, tx_mgmt, tx_mcs_index, tx_nss, tx_bw, tx_sgi, rx_bytes, rx_pkts, rx_discard, rx_err, rx_unicast, rx_multicast, rx_broadcast, rx_unknown, rx_phy_rate, rx_mgmt, rx_ctrl, rx_mcs_index, rx_nss, rx_bw, rx_sgi, hw_noise, snr, rssi, bw = np.loadtxt(sys.argv[1], delimiter=',', unpack=True, skiprows=1)

rx_bytes = rx_bytes - rx_bytes[0]
tx_bytes = tx_bytes - tx_bytes[0]

fig, ax1 = plt.subplots()
p1 = ax1.plot(time, rx_bytes, 'b-')
ax1.set_xlabel('sample (n)')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()

legendP = [p1[0]]
legendL = ['rx_bytes']
def plot(var, lbl, opt):
    p = ax2.plot(time, var, opt)
    legendP.append(p[0])
    legendL.append(lbl)

plot(rssi, 'rssi', 'r-')
plot(hw_noise, 'hw_noise', 'g-')
plot(snr, 'snr', 'y-')


plt.legend(legendP, legendL)

fig.tight_layout()
plt.show()
