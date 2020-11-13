import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
import sys
from mdrparser import MdrParser

samples = MdrParser(sys.argv[1]).all()

attenuation = 6 # -6dB

f = list(map(lambda f: int(f), samples["freqs"]))
s = list(map(lambda k: list(map(lambda v: float(v)+attenuation, k["values"])), samples["sweeps"]))

s = s[0:70]

S = np.matrix(s).T

fig, ax = plt.subplots()

ax.set_yticks(list(np.arange(0, len(f), 10)))
ax.set_yticklabels(f[0::10])
# ax.set_xticks(np.arange(0, len(S), 8))
# ax.set_xticklabels(np.arange(0, len(S), 8))

# fig.set_size_inches(6, 11.25)

plot = ax.imshow(S, cmap='hot', interpolation='nearest', label="hej", origin="lower")
ax.set_xlabel('Sample')
ax.set_ylabel('Frequency (Hz)')
fig.suptitle('RSSI Evaluation\nunder saturation'.format(sys.argv[1]), fontsize=16)
cbar = fig.colorbar(plot, orientation="horizontal");
cbar.ax.set_xlabel("RSSI (dBm)")
plt.legend()
plt.show()

#call_qcsapi get_node_stats wds0 0
