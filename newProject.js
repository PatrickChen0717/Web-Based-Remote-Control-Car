


// import the library and set up the module and initiate the variables 
const res = require('express/lib/response');
const port = 80;



const fs = require('fs')
const Jimp = require("jimp");
var distance1 = 0;
var distance2 = 0;
var distance3 = 0;
var distance4 = 0;
var express = require('express'); 
var bodyParser = require('body-parser'); 
var app = express(); 
var data_html;


app.use('/', express.static('public'));
app.use(bodyParser.json({limit:'50mb'})); 
app.use(bodyParser.urlencoded({ limit:'50mb',extended: true })); 
app.post("/postdata", (req, res) => {     // a route to respond the post request from the respberry pi  
        
    var left = req.body.leftdist; 
    var right = req.body.rightdist; 
    var front = req.body.frontdist; 
    var back = req.body.backdist; 


    console.log(left,right,front,back);
    

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

app.post("/postimg",(req,res)=>{    // the route to handle the img-post request from the respberry pi 

    var img = req.body.image;
    if(img!=""){
        console.log('recieving umg');
        const buffer = Buffer.from(img, "base64");
        Jimp.read(buffer, (err, res) => {
             if (err) throw new Error(err);
             res.quality(15).write("./public/resized.jpg");
        });
        console.log('recieving done ');
    }
    res.send("process complete"); 
});

app.post("/instruc", (req, res) => {   // the route to handle the instruction-post request from the web browser
        
    data_html= req.body.direction; 
   console.log( data_html );
    
    res.send("process complete"); 
}); 


app.get("/getdata", (req, res) => {  // the route to handle the get request from the respberry pi 
    var data= { // this is the data you're sending back during the GET request 
        direction: "forward",
    } 
    var sendup={
        direction:data_html,
    }
    if(data_html!=null){
    res.status(200).json(sendup) 
    }
    else{
        res.status(200).json(data)
    }
}); 

app.get('/public/resized.jpg', (req, res) => {   // the route to push the img to the browser
    
    res.sendFile('/home/a14root/web/public/resized.jpg')
  });


app.get('/left', function(req, res) {   //the event handler that reads from local txt and sends the text to the front html

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

app.get('/right', function(req, res) {  //the event handler that reads from local txt and sends the text to the front html


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

app.get('/front', function(req, res) {  //the event handler that reads from local txt and sends the text to the front html


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

app.get('/back', function(req, res) {     //the event handler that reads from local txt and sends the text to the front html

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



app.listen(port, () => {  // listen to the port for connection 
  console.log(`Listening at http://localhost:${port}`)
})

 