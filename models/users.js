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

exports.deleteClothe = function(body, user) {
  return User.findOne({_id: body._id}, function(err, usr){
    body.clothes.forEach(c => {
      //First delete the clothe from user clothes
      clothes_to_remove = []
      usr.clothes.forEach(clothe => {
        if(clothe._id == c._id.$oid){
          clothes_to_remove.push(clothe)
        }
      });
      clothes_to_remove.forEach(clothe => {
        var index = usr.clothes.indexOf(clothes);
        if (index > -1) {
          usr.clothes.splice(index, 1);
        }
      })
      var index = usr.clothes.indexOf(c);
      if (index > -1) {
        usr.clothe.splice(index, 1);
      }
      //Then delete all tastes that contain the clothe
      tastes_to_remove = []
      usr.tastes.forEach(t => {
        t.clothes.forEach(clothe => {
          if(clothe._id == c._id.$oid){
            tastes_to_remove.push(t);
          }
        });
      });
      tastes_to_remove.forEach(t => {
        var index = usr.tastes.indexOf(t);
        if (index > -1) {
          usr.tastes.splice(index, 1);
        }
      });
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
