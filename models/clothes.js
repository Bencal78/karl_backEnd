const util = require('util');
const mongoose = require('mongoose');
const Clothe = require('../schemas/clothes');


exports.create = function(values) {
  return Clothe.create(values, function (err, res) {
    if (err) return handleError(err);
    // saved!
  });
};

exports.get = function(values) {
  var query = Clothe.find(null);
  var fields = Object.keys(values);
  fields.forEach(x => {
      query.where(x, values[x]);
  });
  return query.exec();
};


exports.update = function(body) {
  return Clothe.updateOne({ _id: body._id }, body, function(err, res) {
    // Updated at most one doc, `res.modifiedCount` contains the number
    // of docs that MongoDB updated
  });
};

exports.delete = function(values) {
  return Clothe.deleteMany(values, function (err) {
    if (err) return handleError(err);
    // deleted clothe document
  });
};
