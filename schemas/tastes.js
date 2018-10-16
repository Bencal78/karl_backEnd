var client = require('../helpers/mongoClient');
var Schema = client.Schema;

var schema = new Schema({
    decision : Boolean,
		clothes: [String]
}, {versionKey: 'version'});

module.exports = schema;
