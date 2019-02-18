import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import csv

data = {
    'time': [],
    'utxb': [],
    'utxp': [],
    'urxb': [],
    'urxp': [],
    # 'qtxb': [],
    # 'qtxp': [],
    # 'qrxb': [],
    # 'qrxp': []
}

with open(sys.argv[1]) as csvfile:
    txrx_data = csv.reader(csvfile)
    for time, utxb, utxp, urxb, urxp in txrx_data:
        data['time'].append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
        data['utxb'].append(utxb)
        data['utxp'].append(utxp)
        data['urxb'].append(urxb)
        data['urxp'].append(urxp)

print(data['utxb'])

legendP = []
legendL = []

def plot(var, lbl, opt):
    x = plt.plot_date(data['time'], var, opt)
    legendP.append(x[0])
    legendL.append(lbl)

# plot(data['utxp'], 'ubus tx [p]', 'y+')
plot(data['urxp'], 'ubus rx [p]', 'yx')
# plot(data['qtxp'], 'qcs tx [p]', 'rx')
# plot(data['qrxp'], 'qcs rx [p]', 'r*')

# emptyPlot(b, "", ' ')

# plot(data['utxb'], 'ubus tx [b]', 'y+--')
plot(data['urxb'], 'ubus rx [b]', 'bx--')
# plot(data['qtxb'], 'qcs tx [b]', 'r+--')
# plot(data['qrxb'], 'qcs rx [b]', 'r+--')


plt.legend(legendP, legendL)
# box = b.get_position()
# b.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# p.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# plt.legend(legendP, legendL, loc='center left', bbox_to_anchor=(1.125, 0.5))

# fig.tight_layout()
plt.show()
