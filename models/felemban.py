import math
import numpy as np
import sympy as sp
from scipy.special import binom as binomial

def solve_steady_state(p):
    dim = p.shape[0]
    q = (p - np.eye(dim))
    ones = np.ones(dim)
    q = np.c_[q,ones]
    QTQ = np.dot(q, q.T)
    bQT = np.ones(dim)
    return np.linalg.solve(QTQ,bQT)


def sum(fn, limits):
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

    def compute(self, tau0=0.5, epsilon=1e-10):
        """
        Calculate model parameters iteratively.

        Keyword arguments:
        tau0 -- initial guess for tau (0 < tau0 < 1, default 0.5)
        epsilon -- desired precision (default 1e-10)
        """
        
        # p_e (probability exit in idle state) is defined to be 1 in the paper
        pe = 1

        # IEEE specification
        CW_min = 32
        CW_max = 1024
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
            return binomial(N-1, n) * tau**n * (1 - tau)**(N - n - 1)

        while True:
            # Equation (2)
            P = 1 - (1 - tau) ** (N - 1)

            pei = (1 - tau)**(N-1)

            # Equation (3)
            pes = binomial(N-1, 1) * tau * (1 - tau)**(N-2)
            pec = 1 - pei - pes

            pss = 1/W(0)
            psi = 1 - pss

            Pdrop = P**(L+1)

            # Equation (8)
            CW_avg = sum(lambda i: (1-P)*P**i*W(i)/(1-Pdrop), (0, L))

            # Equation (7)
            pci = sum(lambda n: Q(n) * (1 - 1/CW_avg)**n, (2, N-1))

            # Equation (9)
            pcs = sum(lambda n: Q(n) * n * (1/CW_avg) * (1 - 1/CW_avg)**(n-1), (2, N-1))
            
            pcc = 1 - pci - pcs

            # Equation (10)
            pi = np.matrix([
            [pei, pes, pec],
            [psi, pss, 0],
            [pci, pcs, pcc]
            ])

            # pi * A = A
            A = solve_steady_state(pi)

            PI = A[0]

            # Equation (4)
            Pd = PI * pe

            # Equation (5)
            Pf = 1 - Pd

            # Equation (1)
            tau_new = (1 - P**(L+1)) / ((1 - P) * sum(lambda j: (1 + (1/(1-Pf)) * sum(lambda k: (W(j) - k)/W(j), (1,W(j)-1))) * P**j, (0,L)))
            
            # tau_i = alpha*tau_{i-1} + (1-alpha) * tau_new
            tau_old = tau
            tau = alpha * tau + (1 - alpha) * tau_new
            if abs(tau - tau_old) < epsilon: break

        return tau, P, Pf

    def simulate():
        pass
