let N = 10 // competing stations
let L = 7 // short retry limit
let CWmin = 32
let CWmax = 1024
let W = new Array(L+1).fill(1).map((e,i) => Math.min(Math.pow(2, i) * CWmin, CWmax))
let rate = 1 // channel rate (Mbps)
let D = 8182 // frame size (bit)
let { MAC_HEADER, SERVICE, PHY_HEADER, ACK, DIFS, SIFS, BASIC_RATE, T_SLOT, B0 } = require('./config')

function sum(from, to, fn) {
    let s = 0
    for (var x = from; x <= to; x++)
        s += fn(x)
    return s
}

var binomials = [
    [1],
    [1,1],
    [1,2,1],
    [1,3,3,1],
    [1,4,6,4,1],
    [1,5,10,10,5,1],
    [1,6,15,20,15,6,1],
    [1,7,21,35,35,21,7,1],
    [1,8,28,56,70,56,28,8,1],
];

// step 2: a function that builds out the LUT if it needs to.
function binom(n,k) {
    while(n >= binomials.length) {
      let s = binomials.length;
      let nextRow = [];
      nextRow[0] = 1;
      for(let i=1, prev=s-1; i<s; i++) {
        nextRow[i] = binomials[prev][i-1] + binomials[prev][i];
      }
      nextRow[s] = 1;
      binomials.push(nextRow);
    }
    return binomials[n][k];
}

// same
const Ptau  = tau => 1 - (1 - tau)**(N-1)
const Pbusy = tau => 1 - (1 - tau)**(N)
const Ps    = tau => N * tau * (1 - Ptau(tau))
const Pdrop = tau => Ptau(tau)**(L+1)
const PtauInv = P => 1 - Math.pow(1 - P, 1/(N - 1))

// Pf
const Pei = tau => Math.pow(1 - tau, N - 1)
const Pes = tau => binom(N-1, 1) * tau * (1 - tau)**(N-2)
const Pec = tau => 1 - Pei(tau) - Pes(tau)

const Pss = () => 1 / W[0]
const Psi = () => 1 - Pss()

const Pci = tau => sum(2, N-1, n => Q(tau, n)*Math.pow(1 - 1/CWinv(tau), n))
const Pcs = tau => sum(2, N-1, n => Q(tau, n)*n*(1/CWinv(tau))*(1-1/CWinv(tau))**(n-1))
const Pcc = tau => 1 - Pci(tau) - Pcs(tau)

const Q = (tau, n) => binom(N - 1, n) * (tau**n) * (1 - tau)**(N-n-1)
const CWinv = tau => {
    let P = Ptau(tau)
    return sum(0, L, i => (1 - P)*(P**i)*W[i]/(1 - Pdrop(tau)))
}

const Pi = tau => [[Pei(tau), Pes(tau), Pec(tau)],
                   [Psi(tau), Pss(tau), 0       ],
                   [Pci(tau), Pcs(tau), Pcc(tau)]]

const solvePf = tau => {
    let pi = Pi(tau)
    
    let PI = 1.0
    let PS = 0.0
    let PC = 0.0

    let PIo = 0
    let PSo = 0
    let PCo = 0

    let err = () => Math.abs(PI-PIo)+Math.abs(PS-PSo)+Math.abs(PC-PCo)
    while (err() > 1e-8) {
        // 
        // Pei Pes Pec    PI    Pei*PI + Pes*PS + Pec*PC
        // Psi Pss 0.0  x PS  = Psi*PI + Pss*PS + 0.0*PC
        // Pci Pcs Pcc    PC  = Pci*PI + Pcs*PS + Pcc*PC
        //

        PIo = PI; PSo = PS; PCo = PC;
        PI = pi[0][0]*PIo + pi[0][1]*PSo + pi[0][2]*PCo
        PS = pi[1][0]*PIo + pi[1][1]*PSo + pi[1][2]*PCo
        PC = pi[2][0]*PIo + pi[2][1]*PSo + pi[2][2]*PCo

    }

    for (var j = 0; j < 3; j++) {
        if (j != 1) process.stderr.write('     ')
        else process.stderr.write('pi = ')
        for (var i = 0; i < 3; i++) {
            process.stderr.write(pi[j][i].toFixed(5).padEnd(8, " "))
        }
        if (j === 0) process.stderr.write("N   = " + N)
        if (j === 1) process.stderr.write("tau = " + tau)
        if (j === 2) process.stderr.write("err = " + err())
        console.error()
    }
    console.error()

    return PI
}
                   
// no idea
// 1-P**L+1
const tauP = (P, Pf) => {
    let den = 0
    let pf1 = 1/(1-Pf)
    for (let j = 0; j <= L; j++) {
        let s = 1 + pf1*sum(1, W[j] - 1, k => (W[j] - k)/W[j])
        den += s * Math.pow(P, j)
    }
    return (1 - Math.pow(P, L+1))/(den*(1 - P))
}

function solve() {
    let tau = 0
    let err = 0

    do {
        let pf = solvePf(tau)
        let p  = Ptau(tau)

        let tauNew = tauP(p, pf)
        let tauNext = 0.5 * tau + 0.5 * tauNew
        
        err = tauNext - tau
        tau = tauNext
    } while (Math.abs(err) > 1e-8)

    return tau
}

function U(tau) {

 //    slot_idle=50
 // # IEEE frame sizes
 //        MAC = 272 * 8       # bits
 //        PHY = 128 * 8       # bits
 //        ACK = 112 * 8 + PHY # bits
 //        RTS = 160 * 8 + PHY # bits
 //        CTS = 112 * 8 + PHY # bits

 //        # IEEE guard times
 //        DIFS = 128*1e-6 # s
 //        SIFS = 28*1e-6 # s
    MAC_HEADER = 272 
    PHY_HEADER = 128
    ACK        = 112 + PHY_HEADER

    SIFS = 0 * 1e-6
    DIFS = 0 * 1e-6

    const Tack = ACK / (rate * 1e6)
    const Th = (MAC_HEADER+PHY_HEADER)/(rate * 1e6)
    const Ti = 50*1e-6
    const Tp = D/(rate * 1e6)

    const Ts = DIFS + Th + Tp + SIFS + Tack
    const Tc = Ts

    const PsTp = Ps(tau) * Tp                // P(send) * Time(payload)
    const PsTs = Ps(tau) * Ts                // P(send) * Time(send)
    const PcTc = (Pbusy(tau) - Ps(tau)) * Tc // P(coll) * Time(collision)
    const PiTi = (1 - Pbusy(tau)) * Ti       // P(idle) * Time(idle)

    return PsTp / (PcTc + PsTs + PiTi)
}

console.log("N", "bianchi", "felemban", "reimpl")
        // 5    10    15    20    25    30    35    40    45    50    55    60
var FeU = [0.7, 0.69, 0.67, 0.65, 0.63, 0.62, 0.61, 0.60, 0.59, 0.58, 0.57, 0.56]
var FeC = [0.1, 0.18, 0.23, 0.28, 0.30, 0.32, 0.35, 0.38, 0.40, 0.42, 0.43, 0.45]

var bianchi = require('./bianchi')

for (N = 5; N <= 60; N = N + 5) {
    let tau = solve()
    let bTau = bianchi.solve(N)

    process.stdout.write(N.toString())
    process.stdout.write(",")
    process.stdout.write(bianchi.U(bTau).toString())
    process.stdout.write(",")
    process.stdout.write(bianchi.Ptau(bTau).toString())
    process.stdout.write(",")
    process.stdout.write(FeU[N/5 - 1].toString())
    process.stdout.write(",")
    process.stdout.write(FeC[N/5 - 1].toString())
    process.stdout.write(",")
    process.stdout.write(U(tau).toString())
    process.stdout.write(",")
    process.stdout.write(Ptau(tau).toString())
    process.stdout.write("\n")
}


// console.log("> felemban")
// console.log("N", "=", N, "|", "L", "=", L, "|", "R", "=", rate, "Mbps", "|", "D", "=", D, "bits")
// console.log("W", "=", W)

// console.log("tau", "=", tau)
// console.log("U  ", "=", U(tau), "~0.7")
// console.log("Ps ", "=", N*tau*(1-Ptau(tau))/(1-Math.pow(1 - tau, N)))
// console.log("C% ", "=", Ptau(tau))

module.exports = { solve: solve, U: U }
