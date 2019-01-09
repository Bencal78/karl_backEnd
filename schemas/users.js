var client = require('../helpers/mongoClient');
var UserSchema = require('./userSchema');

module.exports = client.model('users', UserSchema);
