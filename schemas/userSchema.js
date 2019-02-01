var client = require('../helpers/mongoClient');
var Schema = client.Schema;
var TasteSchema = require('./tasteSchema');
var ClotheSchema = require('./clotheSchema');

var schema = new Schema({
	idGoogle : String,
	firstName : String,
	lastName : String,
	givenName : String,
	email : String,
	age : Number,
	genre : String,
	tastes : [TasteSchema],
	clothes: [ClotheSchema],
	rl_cat_score: Object,
	ts: { type: Date, default: Date.now},
	nb_dict: Object
}, {versionKey: 'version'});

module.exports = schema;
