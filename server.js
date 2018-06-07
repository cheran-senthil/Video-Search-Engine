var PythonShell = require('python-shell');
var bodyParser = require('body-parser');
var express = require('express')
var path = require('path')
var server = express()

PythonShell.run('clearHistory.py', function() {
	console.log("History cleared");
});

server.use(bodyParser.urlencoded({
	extended: true
}))

server.get('/', function(req, res) {
	res.sendFile(path.join(__dirname + '/index.html'))
})

server.post('/search/', function(req, res) {
	var options = {
		mode: 'text',
		args: [req.body.search]
	};
	PythonShell.run('search.py', options, function(err) {
		res.sendFile(path.join(__dirname + '/temp.html'))
	});
})

server.post('/video/', function(req, res) {
	var options = {
		mode: 'text',
		args: [req.body.Video]
	};
	console.log(req.body.Video)
	PythonShell.run('info.py', options, function() {
		res.sendFile(path.join(__dirname + '/temp.html'))
	});
})

server.post('/history/', function(req, res) {
	PythonShell.run('history.py', function() {
		res.sendFile(path.join(__dirname + '/temp.html'))
	});
})

server.listen(8080)
