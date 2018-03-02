#!/usr/bin/env nodejs
// server.js
// where your node app starts

//functions

// init project
var express = require('express');
var htmlparser = require("htmlparser");
var request = require("request");

var app = express();
var bodyParser = require('body-parser')
var querystring = require('querystring');

const https = require("https");

app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));
app.use(express.static('public'));

// we've started you off with Express, 
// but feel free to use whatever libs or frameworks you'd like through `package.json`.

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public/jquery-3.3.1.min.js'));

// http://expressjs.com/en/starter/basic-routing.html
app.get("/", function (request, response) {
  response.sendFile(__dirname + '/views/index.html');
});

var texts = []
var urls = []

app.post("/forward", function (request, response) {
  
  // get request data and return result from validation engine api
  var data = Object.keys(request.body).map(function(k) { return request.body[k] });
  var wholeid = (data[0]).toString();
  var htmlcode = data[1];
  var textfiltered = htmlcode.replace(/<(?:.|\n)*?>/gm, '').replace('http', ' http');
  textfiltered = textfiltered.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').trim();

  var spaceSplit = textfiltered.split(' ');
  
  texts.push(textfiltered);
  for (var i = 0; i < spaceSplit.length; i++)
  {
    if(spaceSplit[i].substr(0,4) == "http" && spaceSplit[i].substr(0,20) != "https://twitter.com/" && spaceSplit[i].substr(0,21) != "https://facebook.com/")
    {
        //console.log("Inspecting " + spaceSplit[i].trim());
        const request = require("request");
        request.get(spaceSplit[i].trim(), (error, resposta, body) => {
          if (error == null)
          {
            var website = resposta.body;

            var titleTag = website.match(/<title>(.*?)<\/title>/g);

            if (titleTag != null)
            {
              var title = titleTag[0].toString().replace(/<(?:.|\n)*?>/gm, '');
              //console.log("Found that title is " + title);

              var bodyTag = website;
              if (bodyTag != null)
              {
                var bodyText = bodyTag.replace(/\s+/g,' ').replace(/<(?:.|\n)*?>/gm, '').replace('&nbsp;', '').replace('&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').trim();
                //console.log("Found that content is " + bodyText.substr(0,150));
                
                  // Process data and then respond to the Chrome extension with content analysis results
                  resulttext = callEndpoint(title, bodyText);
                      
                  //var resp= {id : (data[0]).toString()};
                
                  var resp = {status: 200, id: (data[0]).toString(), result: resulttext};
                  response.send(resp);
              }
            }
          }
        });
        
      
    }
  }

});

function callEndpoint (title, body){

  var url = "http://localhost:5000/";
  var formData = {"title": title, "body": body};
  
  var express = require('express')
  var cors = require('cors')
  var app = express()

  var response = "";

  app.use(cors())

  request.post({
       method: 'POST',
            url: url,
            json: true,
            form: formData,
            headers: {
                  'Content-Type': 'application/json; Access-Control-Allow-Origin: *'
              }
        },
        function (err, httpResponse, body) {
            console.log(httpResponse.body);
            response = httpResponse.body;
        });
  return response;
}

// listen for requests :)
var listener = app.listen(50000, function () {
  console.log('Your app is listening on port ' + listener.address().port);
});
