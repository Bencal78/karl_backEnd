var client = require('../helpers/mongoClient');
var Schema = client.Schema;

var schema = new Schema({
  name : String,
  category : String,
  bodyparts: [ Number ],
  colors: [ String ],
  fabrics: String,
  temperature: Number,
  pattern: String,
  layer: Number,
  rl_score: Number,
}, {versionKey: 'version'});

module.exports = schema;
