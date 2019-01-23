var fs = require("fs");
var spawn = require('child_process').spawn
var clothes = require('../models/clothes');
var users = require('../models/users');

const get = async (req, res, next) => {
  try{

      	var func_name = req.query.func_name
	if(!func_name){
		return res.status(404)
	}
	var id = req.query.id
	if(!id){
		return res.status(404)
	}
	try{
		var user = (await users.get({_id: id}))[0];
  	}
  	catch (e){
      	return next(e);
  	}
  	var user = user.toJSON()
  	var clothes_json = {"clothes": user.clothes, "rl_cat_score": user.rl_cat_score, "tastes": user.tastes.slice(-1)[0]}
  	var clothes_string = JSON.stringify(clothes_json)
	var py = spawn('python3', ['./python/nodejs_communicator.py', func_name, clothes_string])// nodejs_communicator
	/*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
	py.stdout.on('data', (data) => {
		result = JSON.parse(data.toString().replace(/'/g, '"'))
  		return res.status(200).json(result);
	});

  }catch (e){
      return next(e);
  }
  return res.status(200);
};

exports.get = get;
