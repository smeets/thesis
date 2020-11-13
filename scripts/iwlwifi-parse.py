import glob
import numpy as np
from os import path

def parse_iw(iwpath):
	timekeys = ["connected time"]
	u64keys = ["rx bytes", "tx bytes", "rx packets", "tx packets", "tx retries", "tx failed"]
	fields = {}
	with open(iwpath, "r") as f:
		if not f.readline().startswith("Station"):
			raise Exception("XXX")
		for line in f:
			key = line[0:line.find(':')].strip()
			val = line[line.find(':')+1:-1].strip()

			if key in timekeys:
				# parse val as "<number> <unit>"
				val = int(val[0:val.find(" ")])
			elif key in u64keys:
				# parse val as "<number>"
				val = int(val)
			else:
				continue

			fields[key] = val

	return fields

def parse_iwstats(dir, host):
	iwbegin = path.join(dir, "iwbegin-{}.txt".format(host))
	iwend = path.join(dir, "iwend-{}.txt".format(host))

	begin = parse_iw(iwbegin)
	end = parse_iw(iwend)
	diff = {}
	for key in end:
		diff[key] = end[key] - begin[key]
	return diff

def parse_dmesg(dmesgpath):
	# [156967.845533] tx_cmd: txq=10 status=SUCCESS (0x00000201) f=1 agg=n rts=0 ack=0 time=99
	txtimes = []
	ackfails = []
	rtsfails = []
	with open(dmesgpath, "r") as f:
		for line in f:
			if not "time=" in line:
				print(line)
				continue
			# allow absolutely no aggregation
			if "agg=y" in line:
				print(dmesgpath, line)
				continue
			time = line[line.index("time=")+5:]
			txtimes.append(int(time))

			ackpos = line.index("ack=")
			ack = line[ackpos+4:line.index(" ", ackpos+4)]
			ackfails.append(int(ack))

			rtspos = line.index("rts=")
			rts = line[rtspos+4:line.index(" ", rtspos+4)]
			rtsfails.append(int(rts))
	return txtimes, ackfails, rtsfails

def scan_hosts(dirx):
	paths = glob.glob(path.join(dirx, "iwend-*.txt"))
	files = [path.relpath(p, dirx) for p in paths]
	hosts = [f[f.index("-")+1:f.index(".txt")] for f in files]
	return hosts

def generate_csv_for_test(dir):
	hosts = scan_hosts(dir)
	hostdata = {}
	headers = dict.fromkeys(["host", "tx time avg", "tx time 50", "ack fails", "ack fails 50", "rts fails", "rts fail 50"])

	for host in hosts:
		stats = parse_iwstats(dir, host)
		for key in stats:
			if not key in headers:
				headers[key] = None
		hostdata[host] = stats

	def set_stats(host, txtime, ackfail, rtsfail):
		txtime_avg, txtime_mid = int(np.mean(txtime)+0.5), int(np.median(txtime)+0.5)
		hostdata[host]["tx time avg"] = txtime_avg
		hostdata[host]["tx time 50"] = txtime_mid

		ackfail_sum, ackfail_mid = int(np.sum(ackfail)+0.5), int(np.median(ackfail)+0.5)
		hostdata[host]["ack fails"] = ackfail_sum
		hostdata[host]["ack fails 50"] = ackfail_mid

		rtsfail_sum, rtsfail_mid = int(np.sum(rtsfail)+0.5), int(np.median(rtsfail)+0.5)
		hostdata[host]["rts fails"] = rtsfail_sum
		hostdata[host]["rts fail 50"] = rtsfail_mid

	local_txtime, local_ackfail, local_rtsfail = parse_dmesg(path.join(dir, "dmesg.txt"))
	if not "localhost" in hostdata:
		hostdata["localhost"] = {}
	set_stats("localhost", local_txtime, local_ackfail, local_rtsfail)

	ctrl_txtime, ctrl_ackfail, ctrl_rtsfail = parse_dmesg(path.join(dir, "dmesg-control.txt"))
	if not "control" in hostdata:
		hostdata["control"] = {}
	set_stats("control", ctrl_txtime, ctrl_ackfail, ctrl_rtsfail)

	headers = headers.keys()
	with open(path.join(dir, "txdata.csv"), "w") as f:
		f.write(",".join(["\"{}\"".format(hdr) for hdr in headers]))
		f.write("\n")
		for host in hostdata:
			data = hostdata[host]
			f.write(host)
			for key in headers:
				if key == "host":
					continue
				f.write(",")
				if key in data:
					f.write(str(data[key]))
				else:
					f.write("0")
			f.write("\n")



# parse_iw("datasets/at-lth/selfspam2/2g-uniform-asap-1b-5", "192.168.10.128")
# scan_hosts("datasets/at-lth/selfspam2/2g-uniform-asap-1b-5")
# generate_csv_for_test("datasets/at-lth/selfspam2/2g-uniform-asap-1b-5")

for testcase in glob.iglob("datasets/at-lth/selfspam2/*"):
	print(path.normpath(testcase))
	generate_csv_for_test(testcase)

