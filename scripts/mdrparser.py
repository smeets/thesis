from xml.dom import minidom
from datetime import datetime

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# 2019-01-17T14:33:21.738
# yyyy-mm-dd HH:MM:SS.N
class MdrParser:

    """"""
    def __init__(self, file):
        self.xmldoc = minidom.parse(file)
        self.read_head = 0

    def FREQUENCIES(self, frequencies):
        vals = getText(frequencies.childNodes).split('; ')
        vals.pop()
        return list(map(lambda k: str(int(int(k)/1e6)), vals))

    def VALUES(self, values):
        vals = getText(values.childNodes).split('; ')
        vals.pop()
        return vals

    def DATE(self, date):
        return datetime.strptime(getText(date.childNodes), "%Y-%m-%dT%H:%M:%S.%f")

    def SWEEP(self, sweep):
        return {
            'time' : self.DATE(sweep.getElementsByTagName('StartDate')[0]),
            'values': self.VALUES(sweep.getElementsByTagName('Values')[0])
        }

    def SWEEPS(self, sweeps):
        return [self.SWEEP(sweep) for sweep in sweeps]

    def all(self):
        mcs = self.xmldoc
        
        sweeps = mcs.getElementsByTagName('Sweep')
        freqs = sweeps[0].getElementsByTagName('Frequencies')[0]

        return {
            "freqs": self.FREQUENCIES(freqs),
            "sweeps": self.SWEEPS(sweeps)
        }

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("usage: {} datasets/raw/measure.mdr".format(sys.argv[0]))
        sys.exit(1)

    a = MdrParser(sys.argv[1]).all()
    
    # x1 y1 z1
    # x2 y2 z2
    
    # x = time
    # y = freq
    # z = value

    print(len(a["freqs"]))
    print(len(a["sweeps"]))

    # print("time," + ','.join(a["freqs"]))
    # incr = 0
    # for s in a["sweeps"]:
    #     vals = [str(incr*4)]
    #     vals.extend(s["values"])
    #     print(",".join(vals))
    #     incr = incr + 1

