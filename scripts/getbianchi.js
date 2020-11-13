const bianchi = require('./bianchi')

const stations = parseInt(process.argv[2])
const payload = parseInt(process.argv[3]) * 8

const tau = bianchi.solve(stations)
const thru = bianchi.U(stations, payload, tau)
const coll = bianchi.Ptau(tau)

console.log(stations, payload, tau, thru, coll)
