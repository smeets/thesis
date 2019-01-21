class LogParser:
    def PARAMS():
        return ["tx_bytes", "tx_pkts", "tx_discard", "tx_wifi_sent_be", "tx_wifi_sent_bk", "tx_wifi_sent_vi", "tx_wifi_sent_vo", "tx_wifi_drop_be", "tx_wifi_drop_bk", "tx_wifi_drop_vi", "tx_wifi_drop_vo", "tx_err", "tx_unicast", "tx_multicast", "tx_broadcast", "tx_phy_rate", "tx_mgmt", "tx_mcs_index", "tx_nss", "tx_bw", "tx_sgi", "rx_bytes", "rx_pkts", "rx_discard", "rx_err", "rx_unicast", "rx_multicast", "rx_broadcast", "rx_unknown", "rx_phy_rate", "rx_mgmt", "rx_ctrl", "rx_mcs_index", "rx_nss", "rx_bw", "rx_sgi", "hw_noise", "snr", "rssi", "bw"]

    """"""
    def __init__(self, content):
        self.content = content
        self.read_head = 0

    def read(self, n=1):
        s = self.content[self.read_head:self.read_head+n]
        self.read_head = self.read_head + n
        return s

    def peek(self):
        return self.content[self.read_head]

    def done(self):
        return self.read_head == len(self.content)

    def read_float(self):
        mark = self.read_head
        valid = "-.0123456789"
        while self.peek() in valid and not self.done():
            self.read()
        return float(self.content[mark:self.read_head])

    def skip_whitespace(self):
        while not self.done() and (self.peek() == '\n' or self.peek() == ' '):
            self.read()

    def read_to_whitespace(self):
        mark = self.read_head
        while not self.done() and not (self.peek() == ' ' or self.peek() == '\n'):
            self.read()
        return self.content[mark:self.read_head]

    def expect(self, what):
        s = self.read(len(what))
        if s != what:
            raise ValueError("EXPECTED %s BUT GOT %s AT %d\n%s" % (what, s, self.read_head-len(what), self.content[self.read_head-30:self.read_head]))

    def PARAM(self):
        # tx_bytes     : 33
        name = self.read_to_whitespace()

        self.skip_whitespace()       
        if self.done() or self.peek() != ':':
            return name,-1234

        # optional value
        self.skip_whitespace()
        self.expect(':')
        self.expect(' ')
        value = self.read_float()
        self.expect('\n')
        return name,value

    def SECTION_TIME(self):
        mark = self.read_head
        while self.read() != '\n':
            pass
        time = self.content[mark:self.read_head-1].strip()
        return time

    def SECTION_DATA(self):
        mark = self.read_head
        data = {}
        nbr = 40
        while nbr > 0 and not self.done():
            name,value = self.PARAM()
            data[name] = value
            nbr = nbr - 1
        return data

    def SECTION(self):
        time = self.SECTION_TIME()
        self.skip_whitespace()
        data = self.SECTION_DATA()
        return time,data

    def all(self):
        sections = []
        while not self.done():
            time,data = self.SECTION()
            sections.append((time,data))
            self.skip_whitespace()
        return sections

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("usage: {} datasets/raw/measure.txt".format(sys.argv[0]))
        sys.exit(1)

    f = open(sys.argv[1], "r")
    a = LogParser(f.read()).all()

    params = LogParser.PARAMS()

    print('time,' + ','.join(params))
    i = 0
    for time,data in a:
        vals = [str(i)]
        vals.extend(map(lambda k: str(data[k]), params))
        print(",".join(vals))
        i = i + 1


