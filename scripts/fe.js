let N = 3 // competing stations
let L = 7 // short retry limit
let CWmin = 32
let CWmax = 1024
let W = new Array(L+1).fill(1).map((e,i) => Math.min(Math.pow(2, i) * CWmin, CWmax))
let rate = 1 // channel rate (Mbps)
let D = 8182 // frame size (bit)

// same
const Ptau = tau => 1.0 - Math.pow(1.0 - tau, N-1)
const PtauInv = P => 1.0 - Math.pow(1.0 - P, 1.0/(N-1))

// no idea
// 1-P**L+1
const tauP = (P, Pf) => {
    let den = 0
    for (let j = 0; j <= L; j++) {
        let sum = 0
        for (let k = 1; k <= W[j]-1; k++) {
            sum += (W[j] - k)/W[j]
        }
        sum = 1 + sum/(1-Pf)
        sum = sum * Math.pow(P, j)
    }
    den *= (1 - P)
    return (1 - Math.pow(P, L+1))/den
}

function solve_bianchi() {
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

let tau = solve_bianchi()

console.log("Competing stations (N) =", N)
console.log("Short Retry Limit (L) =", L)
console.log("Contention windows =", W)
console.log("Channel bitrate =", rate, "Mbps")
console.log("Payload size =", D, "bits")
console.log("")
console.log("bianchi:", "tau", "=", tau)