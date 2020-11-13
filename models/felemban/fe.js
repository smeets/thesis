let N = 10 // competing stations
let L = 7 // short retry limit
let CWmin = 32
let CWmax = 1024
let W = new Array(L+1).fill(1).map((e,i) => Math.min(Math.pow(2, i) * CWmin, CWmax))
let rate = 1 // channel rate (Mbps)
let D = 8184 // frame size (bit)
let MAC_HEADER = 272 // bits
let SERVICE = 24 // bits?
let PHY_HEADER = 192 // bits?
let ACK = 112 // bits?
let DIFS = 128 // us
let SIFS = 28 // us
let BASIC_RATE = 2 // Mbps
let T_SLOT = 50 // us

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
const Ps    = tau => N * tau * (1 - tau)**(N-1)
const Pdrop = tau => Ptau(tau)**(L+1)
const PtauInv = P => 1 - Math.pow(1 - P, 1/(N - 1))

// Pf
const Pei = tau => (1 - tau)**(N - 1)
const Pes = tau => binom(N-1, 1) * tau * (1 - tau)**(N-2)
const Pec = tau => 1 - Pei(tau) - Pes(tau)

const Pss = () => 1 / W[0]
const Psi = () => 1 - Pss()

const Pci = tau => sum(2, N-1, n => Q(tau, n)*Math.pow(1 - 1/CWinv(tau), n))
const Pcs = tau => sum(2, N-1, n => Q(tau, n)*n*(1/CWinv(tau))*(1-1/CWinv(tau))**(n-1))
const Pcc = tau => 1 - Pci(tau) - Pcs(tau)

const Q = (tau, n) => binom(N-1, n) * (tau**n) * (1 - tau)**(N-n-1)
const CWinv = tau => {
    let P = Ptau(tau)
    return sum(0, L, i => (1 - P)*(P**i)*W[i]/(1 - Pdrop(tau)))
}

const Pi = tau => [[Pei(tau), Pes(tau), Pec(tau)],
                   [Psi(tau), Pss(tau), 0       ],
                   [Pci(tau), Pcs(tau), Pcc(tau)]]

const transpose = pi => {
    return [
        [pi[0][0], pi[1][0], pi[2][0]],
        [pi[0][1], pi[1][1], pi[2][1]],
        [pi[0][2], pi[1][2], pi[2][2]]
    ]
}
const dot = (P, A) => {
    let a = [1,1,1]
    a[0] = P[0][0]*A[0] + P[0][1]*A[1] + P[0][2]*A[2]
    a[1] = P[1][0]*A[0] + P[1][1]*A[1] + P[1][2]*A[2]
    a[2] = P[2][0]*A[0] + P[2][1]*A[1] + P[2][2]*A[2]
    return a
}

const solvePf = tau => {
    let pi = Pi(tau)
    let P = transpose(pi)
    let A = [1, 0, 0]
    let A1 = [0, 0, 0]
    let ctr = 0
    let err = (a, b) => Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2])
    while (err(A, A1) > 1e-8) {
        ctr += 1
        A1 = dot(P, A)
        A = dot(P, A1)
    }

    // for (var j = 0; j < 3; j++) {
    //     if (j != 1) process.stderr.write('     ')
    //     else process.stderr.write('pi = ')
    //     for (var i = 0; i < 3; i++) {
    //         process.stderr.write(pi[j][i].toFixed(5).padEnd(8, " "))
    //     }
    //     if (j === 0) process.stderr.write("N   = " + N)
    //     if (j === 1) process.stderr.write("tau = " + tau)
    //     if (j === 2) process.stderr.write("err = " + err())
    //     console.error()
    // }
    // console.error()
    let PI = A[0]
    let Pd = PI
    return 1 - Pd
}
                   
// no idea
// 1-P**L+1
const tauP = (P, Pf) => {
    let den = 0
    let pf1 = 1/(1-Pf)
    for (let j = 0; j <= L; j++) {
        let s = pf1 * sum(1, W[j] - 1, k => (W[j] - k)/W[j])
        den += (1 + s) * (P**j)
    }
    return (1 - P**(L+1))/((1-P) * den)
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

const TP   = () => (D + MAC_HEADER + SERVICE) / rate
const TACK = () => ACK/BASIC_RATE
// https://en.wikipedia.org/wiki/DCF_Interframe_Space
//            b   a   g   n24   n50/ac\
// slot [us]  20  9   9   9     9
// sifs [us]  10  16  10  10    16
const TI   = () => 50
const TS   = () => {
    return TP() + DIFS + TACK() + 2*PHY_HEADER + SIFS + T_SLOT
}
const TC   = TS

function U(tau) {
    const Ti = TI()
    const Tp = D/rate                          // us

    const PsTp = Ps(tau) * Tp                  // P(send) * Time(payload)
    const PsTs = Ps(tau) * TS()                // P(send) * Time(send)
    const PcTc = (Pbusy(tau) - Ps(tau)) * TC() // P(coll) * Time(collision)
    const PiTi = (1 - Pbusy(tau)) * Ti         // P(idle) * Time(idle)

    return PsTp / (PcTc + PsTs + PiTi)
}

function CAD(tau) {
    let DI = TI()
    let DS = (1 / (1 - Pss())) * TS() + DI
    let DC = sum(0, L, i => i * Math.pow(Pcc(tau), i)) * TC() + 
             (Pcs(tau) / (1-Pcc(tau))) * DS +
             (Pci(tau) / (1-Pcc(tau))) * DI
    
    let Pd = 1 - solvePf(tau)
    let Fb = (Pei(tau)/Pd)*DI + 
             (Pes(tau)/Pd)*DS + 
             (Pec(tau)/Pd)*DC
    
    let pnb = 1
    let Ft = (1 - CWinv(tau)) * ((Pei(tau)/pnb)*DI + 
                                 (Pes(tau)/pnb)*DS +
                                 (Pec(tau)/pnb)*DC)

    let F = (1 - tau)* Fb + tau * Ft
    let T = (1 / (1 - Pdrop(tau))) *
            sum(0, L, i => (1-Ptau(tau))*Ptau(tau)**i * (TS() + TC() + sum(0, i, j => ((W[j]-1)/2) * F)))
    // console.log("N = ", N)
    // console.log('? = ', (1 / (1 - Pdrop(tau))), Pdrop(tau))
    // console.log('s = ', sum(0, L, i => (1-Ptau(tau))*Math.pow(Ptau(tau), i) * (TS() + i*TC() + sum(0, i, j => ((W[j]-1)/2) * F))))
    return T
}

// N=5
// console.log(CAD(solve()))
// return
let hdr = ["N", "U[f]", "P[f]", "U", "P", "C"]

console.log(hdr.join(','))

        // 5    10    15    20    25    30    35    40    45    50    55    60
var FeU = [0.68, 0.65, 0.62, 0.60, 0.58, 0.56, 0.55, 0.54, 0.53, 0.52, 0.51, 0.50]
var FeC = [0.1, 0.18, 0.24, 0.28, 0.31, 0.34, 0.36, 0.38, 0.40, 0.42, 0.43, 0.44]

// var bianchi = require('./bianchi')

for (N = 5; N <= 60; N = N + 5) {
    let tau = solve()
    // let bTau = bianchi.solve(N)

    process.stdout.write(N.toString())
    // process.stdout.write(",")
    // process.stdout.write(bianchi.U(bTau).toString())
    // process.stdout.write(",")
    // process.stdout.write(bianchi.Ptau(bTau).toString())
    process.stdout.write(",")
    process.stdout.write(FeU[N/5 - 1].toString())
    process.stdout.write(",")
    process.stdout.write(FeC[N/5 - 1].toString())
    process.stdout.write(",")
    process.stdout.write(U(tau).toString())
    process.stdout.write(",")
    process.stdout.write(Ptau(tau).toString())
    process.stdout.write(",")
    process.stdout.write(CAD(tau).toString())
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
