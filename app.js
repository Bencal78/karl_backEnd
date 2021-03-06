// Require express and create an instance of it
var express = require('express');
var bodyParser = require('body-parser')
var app = express();
var path = require('path');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/api/uploads', express.static(path.join(__dirname, 'uploads')));
//app.use('/api/uploads', express.static('uploads'));

var clothes = require('./routes/clothes'); //ajouter un truc comme ca quand on crée une nouvelle "class"
var users = require('./routes/users');
var pyreq = require('./routes/pyreq')
app.use('/api/clothes', clothes); //ajouter un truc comme ca quand on crée une nouvelle "class"
app.use('/api/users', users);
app.use('/api/pyreq', pyreq);


module.exports = app;
