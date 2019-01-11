var client = require('../helpers/mongoClient');
var Schema = client.Schema;
var ClotheSchema = require('./clotheSchema');

var schema = new Schema({
    decision : Boolean,
		clothes: [ClotheSchema]
}, {versionKey: 'version'});

module.exports = schema;