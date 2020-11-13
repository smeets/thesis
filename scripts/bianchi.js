let N = 10 // competing stations
let L = 7 // short retry limit
let CWmin = 32
let CWmax = 1024
let W = new Array(L+1).fill(1).map((e,i) => Math.min(Math.pow(2, i) * CWmin, CWmax))
let rate = 1 // channel rate (Mbps)
let D = 8182 // frame size (bit)

const { MAC_HEADER, SERVICE, PHY_HEADER, ACK, DIFS, SIFS, BASIC_RATE, T_SLOT, B0 } = require('./config')

// same
const Ptau = tau => 1.0 - Math.pow(1.0 - tau, N-1)
const PtauInv = P => 1.0 - Math.pow(1.0 - P, 1.0/(N-1))

// no idea
const tauP = P => {
    let den = 0
    for (let i = 0; i <= L; i++) {
        let avg = (W[i] - 1)/2.0
        den += Math.pow(P, i) * avg
    }
    den *= (1 - P)/(1 - Math.pow(P, L+1))
    return 1/(den+1)
}

function solve(NN) {
    N = NN
    let p = 0
    let tau = 0
    let oldp = 0
    var err
    let maxp = Ptau(2.0/(W[0] + 1))
    let minp = Ptau(2.0/(W[L] + 2))
    do {
        oldp = p
        p = maxp*0.5 + minp*0.5
        if (p==oldp) { p *= 0.3; minp = 0; maxp = 1; }
        tau = tauP(p)
        err = tau - PtauInv(p)
        if (err<0) maxp=p; else minp = p;
        //console.log("p:(", minp.toFixed(5), "-", maxp.toFixed(5), ")/2", " tau =", tau.toFixed(5), "err =", err)
    } while (Math.abs(err) > 1e-8)
    return tau
}

function U(NN, tau) {
    N = NN

    const P     = Ptau(tau)            // eq. 2 from felemban
    const Pidle = Math.pow(1 - tau, N) // inv. of Pbusy
    const PS    = N * tau * (1 - P)    // Ps from eq. 2 from felemban
    const Tsucc = (Math.ceil((D+MAC_HEADER+SERVICE)/(rate)) + DIFS + ACK/BASIC_RATE + 2*PHY_HEADER + SIFS + 2)/(1-B0) + T_SLOT
    const Tcoll =  Math.ceil((D+MAC_HEADER+SERVICE)/(rate)) + DIFS + ACK/BASIC_RATE + 2*PHY_HEADER + SIFS + 1 + T_SLOT
    const s = Pidle*T_SLOT + PS*Tsucc + (1-PS-Pidle)*Tcoll
    return PS*Tsucc/s
}

// let tau = solve()

// console.log("> bianchi")
// console.log("N", "=", N, "|", "L", "=", L, "|", "R", "=", rate, "Mbps", "|", "D", "=", D, "bits")
// console.log("W", "=", W)
// console.log("tau", "=", tau)
// console.log("U  ", "=", U(tau))
// console.log("Ps ", "=", N*tau*(1-Ptau(tau))/(1-Math.pow(1 - tau, N)))

module.exports = { solve: solve, U: U, Ptau: Ptau }
