var client = require('../helpers/mongoClient');
var TatsteSchema = require('./tasteSchema');

module.exports = client.model('decision', TatsteSchema);
