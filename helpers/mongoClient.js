var mongoose = require('mongoose');
var config = require('../config/database');

mongoose.connect(`mongodb://${config.username}:${config.password}@${config.databaseAddress}:${config.port}/karl`, { useNewUrlParser: true });
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  // we're connected!
  console.log("Connection to mongoDB established");
});

module.exports = mongoose;
