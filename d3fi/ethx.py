import socket
import struct
import mtime


def probe_sndbuf(message):
	sent = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
		try:
			sent = sent + sock.sendto(message, socket.MSG_DONTWAIT, ("192.168.9.1", 3000))
		except socket.error:
			sock.close()
			return sent

def time_sendall(message):
	ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	linger = struct.pack('ii', 1, 10)
	ts.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger)

	msglen = len(message)

	sent = 0
	pkts = 0
	start = mtime.monotonic_time()
	bw = 0
	bw_timer = mtime.monotonic_time()
	bw_err_time = 0
	last_pkts = 0
	first_err = 0
	sndbuf = ts.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
	while True:
		try:
			bytez = ts.sendto(message, socket.MSG_DONTWAIT, ("192.168.9.1", 3000))
			if first_err != 0:
				bw_err_time = bw_err_time + (last_err_time - first_err)
				first_err = 0
			sent = sent + bytez
			pkts = pkts + 1
			bw = bw + bytez

			if bw >= sndbuf * 2:
				now = mtime.monotonic_time()
				if now - bw_timer < 5000000:
					continue
				 
				sndbuf = ts.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
				
				avg_bw = round((8*sent/1e6)/((now-start)/1e6), 2)
				now_bw = round((8*bw/1e6)/((now-bw_timer)/1e6), 2)

				# basic access scheme
				# DIFS + T(header) + T(payload) + SIFS + T(ACK)

				chan_bw = 30*1e6 #bps
				payload_xmit_time = ((8*bw) / chan_bw)*1e6      # usec
				
				# sifs (802.11n 5ghz) = 16 us
				# sifs (802.11n 2,4ghz) = 10 us
				# difs (802.11n 5ghz) = 34 us
				# difs (802.11n 2,4ghz) = 28 us
				DIFS = 28
				SIFS = 10

				tpp = (now-bw_timer) / (pkts-last_pkts)     # total time per packet (avg in period)
				avg_tpp = (now-start) / pkts                # total time per packet (avg since start)

				avg_xmit = payload_xmit_time / (pkts-last_pkts)  # payload xmit time per packet (avg)
				real_xmit = ((msglen*8+272+112) / chan_bw) * 1e6 # usec
				real_xmit = real_xmit + 10 + 28

				print int(bw/1e6), "MB /", round((now-bw_timer)/1e6, 2), "sec ( xmit=",int(avg_xmit), "us, real=" ,int(real_xmit), "us, tpp=", int(tpp), "us [", int(avg_tpp), "]) =", now_bw, "mbps [", avg_bw, "],", (pkts-last_pkts), "pkts, SNDBUF =", sndbuf/1e6, "MB, error_time=", int(bw_err_time/1e3), "msec, work_time=", int((now-bw_timer-bw_err_time)/1e3), "msec"
				bw = 0
				last_pkts = pkts
				bw_err_time = 0
				bw_timer = mtime.monotonic_time()

		except socket.error as e:
			last_err_time = mtime.monotonic_time()
			if first_err == 0:
				first_err = last_err_time
			pass
	sndbuf = ts.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
	enqueue = mtime.monotonic_time()
	ts.close()
	closed = mtime.monotonic_time()

	return {
		"data": sent, 
		"send": enqueue - start,
		"exit": closed - enqueue,
		"pkts": pkts,
		"sndbuf": sndbuf
	}

def time_loop(message):
	ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	linger = struct.pack('ii', 1, 10)
	ts.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger)

	sndbuf = ts.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

	data = 0
	pkts = 0
	last_pkts = 0
	last_data = 0
	last_time = mtime.monotonic_time()
	for i in range(1000):
		send = mtime.monotonic_time()
		data = data + ts.sendto(message, ("192.168.1.1", 3000))
		pkts = pkts + 1
		dt = mtime.monotonic_time() - send
		if dt > 5000:
			now = mtime.monotonic_time()
			print data-last_data, "bytes", pkts-last_pkts, "pkts", dt, "us", now-last_time, "us"
			last_data = data
			last_pkts = pkts
			last_time = now
