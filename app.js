// Require express and create an instance of it
var express = require('express');
var bodyParser = require('body-parser')
var app = express();
var path = require('path');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/api/uploads', express.static(path.join(__dirname, 'uploads')));

var clothes = require('./routes/clothes'); //ajouter un truc comme ca quand on crée une nouvelle "class"
var users = require('./routes/users');
app.use('/api/clothes', clothes); //ajouter un truc comme ca quand on crée une nouvelle "class"
app.use('/api/users', users);


module.exports = app;
