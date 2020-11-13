import glob
import numpy as np
from os import path

def parse_iw(iwpath):
    timekeys = ["connected time"]
    u64keys = ["rx bytes", "tx bytes", "rx packets", "tx packets", "tx retries", "tx failed"]
    ratekeys = ["tx bitrate"]
    fields = {}
    with open(iwpath, "r") as f:
        if not f.readline().startswith("Station"):
            raise Exception("XXX")
        for line in f:
            #   tx bitrate: 144.4 MBit/s MCS 15 short GI

            key = line[0:line.find(':')].strip()
            val = line[line.find(':')+1:-1].strip()

            if key in timekeys:
                # parse val as "<number> <unit>"
                val = int(val[0:val.find(" ")])
            elif key in u64keys:
                # parse val as "<number>"
                val = int(val)
            elif key in ratekeys:
                val = float(val[0:val.find("MBit/s")-1])
            else:
                continue

            fields[key] = val

    return fields

#
# tweak as necessary
#
for testcase in glob.iglob("datasets/at-lth/selfspam2/*"):
    testcase = path.normpath(testcase)
    bitrates = []
    for iw_path in glob.iglob(path.join(testcase, 'iwbegin-*.txt')):
        if "localhost" in iw_path:
            continue
        if "control" in iw_path:
            continue
        iw_path = path.normpath(iw_path)
        iw = parse_iw(iw_path)
        bitrates.append(iw["tx bitrate"])
    print(testcase, np.mean(bitrates))

#
# then use something to mix & match
#
# See if there is a difference between start and end txrates in N=20 tests:
#    cat begin_pionly.txt end_pionly.txt | sort | rg -e -20
#
