import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
import glob
import sys, re
from os import path

testcases = glob.glob(sys.argv[1])

def host2num(a):
	if a == b"localhost" or a == "localhost":
		return 1
	elif a == b"control" or a == "control":
		return 2
	else:
		return 0

testcasecache = {}
def loadcase(casedir):
	global testcasecache
	datafile = path.join(casedir, "txdata.csv")

	if datafile in testcasecache:
		return testcasecache[datafile]

	data = np.genfromtxt(datafile, delimiter=',', converters={0: host2num}, names=True)
	testcasecache[datafile] = data
	return data

def bytestr(size):
	if size > 1e9:
		return "{}gb".format(int(size/1e9))
	elif size > 1e6:
		return "{}mb".format(int(size/1e6))
	elif size > 1e3:
		return "{}kb".format(int(size/1e3))
	else:
		return "{}b".format(int(size))

def testpath(payload, n):
	paystr = bytestr(payload)
	nstr = "{}".format(n)
	for testcase in testcases:
		m = re.search('.*-(.+)-(.+)', testcase)
		if m and m.group(1) == paystr and m.group(2) == nstr:
			return testcase
	return ""

N = [5,10,15,20]
D = [2**i for i in range(16)]
lines = {
	'1b': 'r-',
	'2b': 'r--',
	'4b': 'r-x',
	'8b': 'r-*',
	'16b': 'r-.',
	'32b': 'b-',
	"64b": 'b--',
	"128b": 'b-*',
	"256b": 'b-.',
	"512b": 'g-',
	"1kb": 'g--',
	"2kb": 'g-*',
	"4kb": 'g-.',
	"8kb": 'y-',
	"16kb": 'y--',
	"32kb": 'y-*'
}

# def plot_txtime_vs_host(ax, host):
# 	ax.set_title('{}'.format(host), fontsize=16)
# 	for payload in D:
# 		cases = [loadcase(testpath(payload, n)) for n in N if testpath(payload, n) != ""]
# 		plot = True
# 		for i in range(len(cases)):
# 			for x in cases[i]["tx_bytes"]:
# 				if x < 0:
# 					plot = False
# 					break
# 		if plot and len(cases) > 0:
# 			tx_times = [data["tx_time_50"][np.where(data["host"] == host2num(host))] for data in cases]
# 			ax.plot(N, tx_times, lines[bytestr(payload)], label="{}".format(bytestr(payload)))
# 	ax.set_xlabel('hosts (N)')
# 	ax.set_ylabel('tx time (us)')
# 	ax.tick_params('y', colors='b')

# fig, axs = plt.subplots(1, 2, sharey=True)
# fig.suptitle('wireless media time vs N\n{}'.format(sys.argv[1]), fontsize=16)
# plot_txtime_vs_host(axs[0], "localhost")
# plot_txtime_vs_host(axs[1], "control")
# axs[0].set_xticks(N)
# axs[1].set_xticks(N)
# plt.legend()

fig, ax1 = plt.subplots()
fig.suptitle('scaled and normalized throughput', fontsize=16)
plt.title('{}'.format(sys.argv[1]))
for payload in D:
	mbps = [(8*sum(loadcase(testpath(payload, n))["tx_bytes"])/(60e6)) for n in N if testpath(payload, n) != ""]
	plot = True
	for n in N:
		if not plot:
			break
		if testpath(payload, n) == "":
			continue
		for x in loadcase(testpath(payload, n))["tx_bytes"]:
			if x < 0:
				plot = False
				break
	if plot and len(mbps) > 0:
		# felebam-ekici, at 5 nodes, mbps[0] = 0.68 * capacity
		# then capacity is mbps[0] / 0.68, so we scale everything
		# and see if the curve looks familiar
		fe_scaler = mbps[0] / 0.68
		# fe_scaler = 75
		ax1.plot(N, [d/fe_scaler for d in mbps], lines[bytestr(payload)], label="{}".format(bytestr(payload)))
ax1.plot(N, [0.68, 0.65, 0.62, 0.60], 'c-o', label="felemban")
ax1.set_xlabel('hosts (N)')
ax1.set_ylabel('throughput (mbps)')
ax1.tick_params('y', colors='b')
ax1.set_ylim(bottom=0.0, top=1.0)
plt.xticks(N)
plt.legend()

def plot_relative_data_vs_host(ax, key, host):
	ax.set_title('{}'.format(host), fontsize=16)
	for payload in D:
		cases = [loadcase(testpath(payload, n)) for n in N if testpath(payload, n) != ""]
		plot = True
		for i in range(len(cases)):
			for x in cases[i]["tx_bytes"]:
				if x < 0:
					plot = False
					break
		if plot and len(cases) > 0:
			packets = [data["tx_packets"][np.where(data["host"] == host2num(host))] for data in cases]
			values = [data[key][np.where(data["host"] == host2num(host))] for data in cases]
			relative = [values[i] / packets[i] for i in range(len(N))]
			ax.plot(N, relative, lines[bytestr(payload)], label="{}".format(bytestr(payload)))
	ax.tick_params('y', colors='b')

fig, ax2 = plt.subplots()
fig.suptitle('total relative tx failures vs N\n{}'.format(sys.argv[1]), fontsize=16)
plot_relative_data_vs_host(ax2, 'tx_failed', "localhost")
ax2.set_xlabel('hosts (N)')
ax2.set_ylabel('relative packet drop probability')
ax2.set_xticks(N)
plt.legend()

# fig, ax3 = plt.subplots()
# fig.suptitle('relative tx retries vs N\n{}'.format(sys.argv[1]), fontsize=16)
# plot_relative_data_vs_host(ax3, 'tx_retries', "localhost")
# ax3.set_xlabel('hosts (N)')
# ax3.set_ylabel('relative tx retries')
# ax3.set_xticks(N)

plt.show()
