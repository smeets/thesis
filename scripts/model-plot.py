import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import sys

N, Bi, BiP, Fe, FeP, U, P, C = np.loadtxt(sys.argv[1], delimiter=',', unpack=True, skiprows=1)


fig, (col, thr) = plt.subplots(2, sharex=True)

fig.suptitle("comparison of felemban and reimplementation in basic access mode")

# fig.subplots_adjust(hspace=0)
col.set_xlabel('competing stations (N)')
col.set_ylabel('collision probability (P)')

thr.set_ylabel('normalized throughput (U)')
thr.set_xlabel('competing stations (N)')

# cad.set_ylabel('channel access delay (s)')
# cad.set_xlabel('competing stations (N)')

col.label_outer()
thr.label_outer()

legendP = []
legendL = []

def plot(ax, var, lbl, opt):
    p = ax.plot(N, var, opt)
    if len(legendP) < 2:
        legendP.append(p[0])
        legendL.append(lbl)

plot(thr, Fe, 'felemban', 'b*-')
plot(thr, U,  'our impl.', 'r*-')

plot(col, FeP, 'felemban', 'b*-')
plot(col, P,   'our impl.', 'r*-')

# plot(cad, C, 'reimpl.', 'y*--')


plt.legend()
# box = thr.get_position()
# thr.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# col.set_position([box.x0, box.y0, box.width * 0.7, box.height])
plt.legend(legendP, legendL)

# fig.tight_layout()
# plt.show()

plt.savefig(sys.argv[2])
