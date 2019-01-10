import math
import numpy as np

from scipy.special import binom as binomial
from numpy.linalg import norm

"""
Solve the steady state via the power method.
"""
def solve_steady_state(pi, epsilon=1e-8, max_iter=1e5):
    P = pi.T
    size = P.shape[0]
    A = np.zeros(size)
    A[0] = 1
    i = 0

    while True:
        A1 = P.dot(A)
        A = P.dot(A1)

        n = norm(A - A1, 1)
        i += 1
        if n <= epsilon or i >= max_iter:
            return A

def suml(fn, limits):
    lo, hi = limits
    val = 0
    for i in range(lo, hi+1):
        val = val + fn(i)
    return val

class Felemban():
    """
    Felemban distributed coordination function model.

    from models.felemban import Felemban
    x = Felemban()
    x.setup(*x.compute())
    x.simulate()
    """
    def __init__(self, L=10, N=3):
        self.L = L
        self.N = N
        self.setup(tau=0, P=0, Pf=0)

    def setup(self, tau, P, Pf):
        """
        Set model parameters. Parameters can be derived from the compute method.

        Keyword arguments:
        tau -- packet transmission probability
        P -- packed dropped probability
        Pf -- packet freeze probability
        """

        self.tau = tau
        self.P = P
        self.Pf = Pf

    def compute(self, tau0=0.5, epsilon=1e-6, CW_min=32, CW_max=1024):
        """
        Calculate model parameters iteratively.

        Keyword arguments:
        tau0 -- initial guess for tau (0 < tau0 < 1, default 0.5)
        epsilon -- desired precision (default 1e-6)
        CW_min -- ieee specified congestion window size (default=32)
        CW_max -- ieee specified congestion window size (default=1024)
        """

        # p_e (probability exit in idle state) is defined to be 1 in the paper
        pe = 1

        # IEEE specification
        m = int(math.log(CW_max/CW_min, 2))

        L = self.L
        N = self.N

        # guess initial value of tau
        tau = tau0

        # alpha is specified in paper to 0.5
        alpha = 0.5

        def W(j):
            assert(j >= 0)
            assert(j <= L)
            return 2**j*CW_min if j < m else 2**m*CW_min

        # Equation (6)
        def Q(n):
            return binomial(N-1, n) * (tau**n) * (1 - tau)**(N - n - 1)

        while True:
            # Equation (2)
            P = 1 - (1 - tau) ** (N - 1)
            Pdrop = P**(L+1)

            pei = (1 - tau)**(N-1)

            # Equation (3)
            pes = binomial(N-1, 1) * tau * (1 - tau)**(N-2)
            pec = 1 - pei - pes

            pss = 1/W(0)
            psi = 1 - pss

            # Equation (8)
            CW_avg = suml(lambda i: (1-P) * (P**i) * W(i)/(1-Pdrop), (0, L))

            # Equation (7)
            pci = suml(lambda n: Q(n) * (1 - 1/CW_avg)**n, (2, N-1))

            # Equation (9)
            pcs = suml(lambda n: Q(n) * n * (1/CW_avg) * (1 - 1/CW_avg)**(n-1), (2, N-1))

            pcc = 1 - pci - pcs

            # Equation (10)
            pi = np.array([
            [pei, pes, pec],
            [psi, pss, 0],
            [pci, pcs, pcc]
            ])

            # A = [ Pi Ps Pc ]
            A = solve_steady_state(pi, epsilon)
            PI = A[0]

            # Equation (4)
            Pd = PI * pe

            # Equation (5)
            Pf = 1 - Pd

            # Equation (1)
            #tau_newp =(1 - P**(L+1)) / ((1 - P) * sum([1 + (1/(1-Pf)) * sum([(W(j) - k)/W(j) for k in range(1,W(j))]) * P**j for j in range(0,L+1)]))
            tau_new = (1 - P**(L+1)) / ((1 - P) * suml(lambda j: (1 + (1/(1-Pf)) * suml(lambda k: (W(j) - k)/W(j), (1,W(j)-1))) * P**j, (0,L)))

            # tau_i = alpha*tau_{i-1} + (1-alpha) * tau_new
            tau_old = tau
            tau = alpha * tau_old + (1 - alpha) * tau_new
            if abs(tau - tau_old) <= epsilon: 
                break

        return tau, P, Pf

    def U(self, bps=1e6, access_mode="basic", payload=8192, slot_idle=50):
        """
        Normalized channel throughput.

        Keyword arguments:
        bps -- channel bit rate in bits per second (default=1Mbps)
        access_mode -- either "basic" or "rts" (default="basic")
        payload -- size of packet without headers, in bits (default=8192)
        slot_idle -- time of an idle slot, in microseconds (default=50)
        """
        channel_bit_rate = bps

        # IEEE frame sizes
        MAC = 272 * 8       # bits
        PHY = 128 * 8       # bits
        ACK = 112 * 8 + PHY # bits
        RTS = 160 * 8 + PHY # bits
        CTS = 112 * 8 + PHY # bits

        # IEEE guard times
        DIFS = 128*1e-6 # s
        SIFS = 28*1e-6 # s

        # Transmission duration of RTS, CTS and ACK packets
        TRTS = RTS / channel_bit_rate # s
        TCTS = CTS / channel_bit_rate # s
        TACK = ACK / channel_bit_rate # s

        # P(channel is busy)
        Pb = 1 - (1 - self.tau)**self.N

        # P(begin successful transmission)
        Ps = self.N*self.tau*(1 - self.tau)**(self.N-1)

        # Transmission duration of headers
        Th = (MAC + PHY) / channel_bit_rate # s

        # Transmission duration of payload
        Tp = payload / channel_bit_rate # s

        # Duration of idle time slot
        Ti = slot_idle*1e-6 # s

        if access_mode == "rts":
            # use rts/cts access mechanism
            Ts = DIFS + TRTS + SIFS + TCTS + SIFS + Th + Tp + SIFS + TACK
            Tc = DIFS + TRTS + SIFS + TCTS
        elif access_mode == "basic":
            # basic access mechanism
            Ts = Tc = DIFS + Th + Tp + SIFS + TACK
        else:
            # wat
            pass
        print("Pb={}\nPs={}\nTh={}\nTp={}\nTi={}\n".format(Pb, Ps, Th, Tp, Ti))
        return (Ps*Tp)/((Ps*Ts) + (Pb-Ps)*Tc + (1-Pb)*Ti)

Felemban().compute()
