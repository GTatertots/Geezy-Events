const express = require('express');
const model = require('./model');

var app = express();
const port = 8080;

app.get('/events', function (req, res) {

});

app.get('/events/:eventID', function (req, res) {

});

app.put('/events/:eventID', function (req, res) {

});

app.delete('/events/:eventID', function (req, res) {

});

app.post('/events', function (req, res) {
  const newEvent = model.addEvent({
    name = req.body.name,
    location = req.body.location,
    date = req.body.date,
    time = req.body.time,
    type = req.body.type
  });
  newEvent.then(() => {
    res.status(201).send("event added");
  });
});


app.listen(8080, function () {
        console.log('Server running on port 8080...');
});
