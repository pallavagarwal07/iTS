// Function to generate random name for the c file
function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for( var i=0; i < 8; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}


// Import the filesystem
var fs = require('fs');
var spawn = require('child_process').spawnSync;


// Actual code for the server
var express = require('express');
var app = express();
app.use(express.static( __dirname + '/../' ));
// Static files have been served by this point.
// Requests requiring non-existent files pass through.


app.get('/compile_req', function (req, res) {
    // Decode base64 strings
    code = new Buffer(req.query.code, 'base64').toString('ascii');
    input = new Buffer(req.query.input, 'base64').toString('ascii');

    // Write code, input to files
    rand = __dirname + '/' + makeid();
    fs.writeFileSync(rand + '.c', code);
    fs.writeFileSync(rand + '.in', input);

    console.log(code);
    console.log(input);

    ret_val = {
        "gcc_error": "",
        "gcc_warning": "",
        "gcc_out": "",
        "out_ret": "",
        "its_out": "",
        "its_cmd": ""
    };

    gcc = spawn('gcc', ['-Wall', '-o' + rand + '.out', rand+'.c']);

    output = gcc.stdout.toString('utf-8');
    error = gcc.stderr.toString('utf-8');
    console.log('STATUS: ' + gcc.status);

    if(gcc.status == 0)
    {
        if(error.length != 0)
            ret_val.gcc_warning = error.replace(rand, 'code');

        exec = spawn(rand+'.out', [], {
            "input": fs.readFileSync(rand+'.in'),
            "timeout": 2000
        });

        if(exec.signal == "SIGTERM") {
            ret_val.gcc_warning = "TIME LIMIT exceeded in GCC executable";
        }
        else {
            ret_val.gcc_out = exec.stdout.toString('utf-8');
        }
        ret_val.out_ret = exec.status;
    }
    else
        ret_val.gcc_error = error.replace(rand, 'code');
    // End of all things concerned with GCC..

    its = spawn('its', [ '-c'+rand+'.c', '-i'+rand+'.in',
            '-o'+rand+'.txt', '-e'+rand+'.its'], { "timeout": 35000});

    ret_val.its_out = fs.readFileSync(rand+'.txt').toString('utf-8');
    ret_val.its_cmd = fs.readFileSync(rand+'.its').toString('utf-8');

    // Delete all created files
    fs.unlink(rand + '.in');
    fs.unlink(rand + '.out');
    fs.unlink(rand + '.c');
    fs.unlink(rand + '.txt');
    fs.unlink(rand + '.its');

    var MongoClient = require('mongodb').MongoClient;
    MongoClient.connect("mongodb://cimulatordb/codes", function(err, db) {
        if(!err) {
            console.log("We are connected");
        }
        var collection = db.collection('records');
        doc1 = {
            'request' : {
                'input': input,
                'code': code
            },
            'response': ret_val,
            'timestamp': Math.floor(new Date()/1000)

        };
        collection.insert(doc1, function(err){if(!err)console.log("Inserted!");});
    });
    res.send(ret_val);
});

app.get('/bug_report', function (req, res) {
    // Decode base64 strings
    code = new Buffer(req.query.code, 'base64').toString('ascii');
    input = new Buffer(req.query.input, 'base64').toString('ascii');
    name = new Buffer(req.query.name, 'base64').toString('ascii');
    email = new Buffer(req.query.email, 'base64').toString('ascii');
    bug = new Buffer(req.query.bug, 'base64').toString('ascii');

    var MongoClient = require('mongodb').MongoClient;
    MongoClient.connect("mongodb://cimulatordb/codes", function(err, db) {
        if(!err) {
            console.log("We are connected");
        }
        var collection = db.collection('bugs');
        doc1 = {
            'name': name,
            'email': email,
            'bug': bug,
            'code': code,
            'input': input
        };
        collection.insert(doc1, function(err){if(!err)console.log("Inserted!");});
    });
    res.send("thanks");
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});
