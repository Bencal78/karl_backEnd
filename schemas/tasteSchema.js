var client = require('../helpers/mongoClient');
var Schema = client.Schema;
var ClotheSchema = require('./clotheSchema');

var schema = new Schema({
    decision : Boolean,
		clothes: [ClotheSchema],
    rl_used: Boolean,
    nb_used: Boolean,
    ts: { type: Date, default: Date.now}
}, {versionKey: 'version', timestamps: true});

module.exports = schema;
