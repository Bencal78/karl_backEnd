var client = require('../helpers/mongoClient');
var clotheSchema = require('./clotheSchema');

module.exports = client.model('cloths', clotheSchema);
