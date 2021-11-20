var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var PythonShell = require('python-shell');

const PORT = process.env.PORT || 3000;
const users = [];

app.get('/', function(req, res) {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket) {
  socket.on('adduser', function(name) {
    users.push(name);
    socket.on('chat message', function(msg) {
      var options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: './Functionality',
        args: [msg]
      };

      PythonShell.run('classifier.py', options, function(err, results) {
        if (err) throw err;
        console.log(results[0]);
        io.emit('chat message', { msg, result: results[0], name });
      });
    });
  });
});

http.listen(PORT, function() {
  console.log(`Listening on ${PORT}`);
});
