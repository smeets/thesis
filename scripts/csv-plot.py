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
