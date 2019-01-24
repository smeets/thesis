import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import sys

N, Bi, BiC, Fe, FeC, U, C = np.loadtxt(sys.argv[1], delimiter=',', unpack=True, skiprows=1)

fig, col = plt.subplots()
fig.suptitle("comparison of felemban and reimplementation in basic access mode")

col.set_xlabel('competing stations (N)')
col.set_ylabel('collision probability (P)')
col.set_ylim((0, 1))
col.set_xlim((0, 65))

thr = col.twinx()
thr.set_ylabel('normalized throughput (U)')
thr.set_ylim((0, 1))
thr.set_xlim((0, 65))


legendP = []
legendL = []
def emptyPlot(ax, lbl, opt):
    p = ax.plot(0, 0, opt)
    legendP.append(p[0])
    legendL.append(lbl)

def plot(ax, var, lbl, opt):
    p = ax.plot(N, var, opt)
    legendP.append(p[0])
    legendL.append(lbl)

emptyPlot(thr, "throughput", 'k-')
emptyPlot(col, "collision %", 'k--')

emptyPlot(col, "", ' ')

plot(thr, Bi, 'bianchi', 'cx-')
plot(thr, Fe, 'felemban', 'b*-')
plot(thr, U, 'smeets', 'ro-')

emptyPlot(col, "", ' ')

plot(col, BiC, 'bianchi', 'cx--')
plot(col, FeC, 'felemban', 'b*--')
plot(col, C, 'smeets', 'ro--')


#plt.legend(legendP, legendL)
box = thr.get_position()
thr.set_position([box.x0, box.y0, box.width * 0.7, box.height])
col.set_position([box.x0, box.y0, box.width * 0.7, box.height])
plt.legend(legendP, legendL, loc='center left', bbox_to_anchor=(1.125, 0.5))

# fig.tight_layout()
#plt.show()

plt.savefig(sys.argv[2])
