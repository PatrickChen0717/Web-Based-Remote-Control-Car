const express = require('express')
const app = express()
const port = 80

app.use('/', express.static('public'));

const fs = require('fs')
var distance = 0;


app.get('/newProject', function(req, res) {

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
            distance = data;
            //console.log(data);
        })

        //console.log("SENT: "+distance);
        res.write("data: " + distance + "\n\n")
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