var http = require('http')
var fs   = require('fs')

var backlog = Buffer.alloc(0)
var csvHeader = undefined
process.stdin.on('data', function (chunk, other) {
	if (!csvHeader) {
		var head_end = chunk.indexOf("\n")
		csvHeader = chunk.slice(0, head_end + 1)
		chunk = chunk.slice(head_end + 1)
		console.log("header:", csvHeader.toString())
	}
	backlog = Buffer.concat([backlog, chunk])
})

function sendfile(res, filename, content_type) {
	res.statusCode = 200
	res.setHeader('Content-Type', content_type)
	fs.createReadStream(filename).pipe(res)
}

function senddata(res) {
	res.statusCode = 200
	res.setHeader('Content-Type', "text/csv")
	res.setHeader('Content-Length', csvHeader.byteLength + backlog.byteLength)
	res.write(csvHeader)
	res.end(backlog)
	console.log('fetch', backlog.byteLength, 'bytes')
	backlog = Buffer.alloc(0)
}

function sendfail(res) {
	res.statusCode = 404
	res.end("not found")
}

http.createServer(function (req, res) {
	
	switch (req.url) {
	case "/": 		   sendfile(res, "index.html", "text/html"); break
	case "/manyplots": sendfile(res, "manyplots.html", "text/html"); break
	case "/queueplot": sendfile(res, "queueplot.html", "text/html"); break
	case "/d3.v3.min.js": sendfile(res, "d3.v3.min.js", "application/javascript"); break
	case "/data":      senddata(res); break
	default:           sendfail(res);
	}

}).listen(8080, function () {
	console.log('serving @ localhost:8080')
})