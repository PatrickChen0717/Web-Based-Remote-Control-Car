
const res = require('express/lib/response');
const port = 80;



const fs = require('fs')
var distance1 = 0;
var distance2 = 0;
var distance3 = 0;
var distance4 = 0;
var express = require('express'); 
var bodyParser = require('body-parser'); 
var app = express(); 



app.use('/', express.static('public'));
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false })); 
  
app.post("/postdata", (req, res) => { 
        
    var left = req.body.leftdist; 
    var right = req.body.rightdist; 
    var front = req.body.frontdist; 
    var back = req.body.backdist; 
    console.log( left ,right ,front ,back);
    
    

    fs.writeFile('./public/leftData.txt', String(left), err => {
        if (err) {
        console.error(err)
        return
        }
        //file written successfully
    })
    fs.writeFile('./public/rightData.txt', String(right), err => {
        if (err) {
        console.error(err)
        return
        }
        //file written successfully
    })
    fs.writeFile('./public/frontData.txt', String(front), err => {
        if (err) {
        console.error(err)
        return
        }
        //file written successfully
    })
    fs.writeFile('./public/backData.txt', String(back), err => {
        if (err) {
        console.error(err)
        return
        }
        //file written successfully
    })
    
    res.send("process complete"); 
}); 
 

app.get("/getdata", (req, res) => { 
    var data= { // this is the data you're sending back during the GET request 
        direction: "forward",
    } 
    res.status(200).json(data) 
}); 


app.get('/left', function(req, res) {

    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    });

    var interval = setInterval(function(){

        fs.readFile('./public/leftData.txt', 'utf-8', (err, data) => {
            //if (err) throw err;
          
            // Converting Raw Buffer to text
            // data using tostring function.
            distance1 = data;
            //console.log(data);
        })

        //console.log("SENT: "+distance);
        res.write("data: " + distance1 + "\n\n")
    }, 10);

    // close
    res.on('close', () => {
        clearInterval(interval);
        res.end();
    });
}) 

app.get('/right', function(req, res) {

    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    });

    var interval = setInterval(function(){

        fs.readFile('./public/rightData.txt', 'utf-8', (err, data) => {
            //if (err) throw err;
          
            // Converting Raw Buffer to text
            // data using tostring function.
            distance2 = data;
            //console.log(data);
        })

        //console.log("SENT: "+distance);
        res.write("data: " + distance2 + "\n\n")
    }, 10);

    // close
    res.on('close', () => {
        clearInterval(interval);
        res.end();
    });
}) 

app.get('/front', function(req, res) {

    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    });

    var interval = setInterval(function(){

        fs.readFile('./public/frontData.txt', 'utf-8', (err, data) => {
            //if (err) throw err;
          
            // Converting Raw Buffer to text
            // data using tostring function.
            distance3 = data;
            //console.log(data);
        })

        //console.log("SENT: "+distance);
        res.write("data: " + distance3 + "\n\n")
    }, 10);

    // close
    res.on('close', () => {
        clearInterval(interval);
        res.end();
    });
}) 

app.get('/back', function(req, res) {

    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    });

    var interval = setInterval(function(){

        fs.readFile('./public/backData.txt', 'utf-8', (err, data) => {
            //if (err) throw err;
          
            // Converting Raw Buffer to text
            // data using tostring function.
            distance4 = data;
            //console.log(data);
        })

        //console.log("SENT: "+distance);
        res.write("data: " + distance4 + "\n\n")
    }, 10);

    // close
    res.on('close', () => {
        clearInterval(interval);
        res.end();
    });
}) 



app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`)
})

 