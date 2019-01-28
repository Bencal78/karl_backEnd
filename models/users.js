const util = require('util');
const mongoose = require('mongoose');
const User = require('../schemas/users');
const Taste = require('../schemas/tastes');


exports.create = function(values) {
  return User.create(values, function (err, res) {
    if (err){
      console.log("err :", err);
      return err;
    }
    // saved!
  });
};


exports.get = function(values) {
  var query = User.find(null);
  var fields = Object.keys(values);
  fields.forEach(x => {
      query.where(x, values[x]);
  });
  return query.exec();
};


exports.update = function(body) {
  return User.updateOne({ _id: body._id }, body, function(err, res) {
    // Updated at most one doc, `res.modifiedCount` contains the number
    // of docs that MongoDB updated
  });
};

exports.addTaste = function(body) {
  console.log("body :", body);
  return User.findOne({_id: body._id}, function(err, usr){
    usr.tastes.push(body.tastes)
    usr.save(function(err) {
    });
  });
};

exports.addClothe = function(body) {
  return User.findOne({_id: body._id}, function(err, usr){
    body.clothes.forEach(c => {
      usr.clothes.push(c)
    });
    usr.save(function(err) {
    });
  });
};

exports.delete = function(values) {
  return User.deleteMany(values, function (err) {
    if (err) return handleError(err);
    // deleted User document
  });
};
