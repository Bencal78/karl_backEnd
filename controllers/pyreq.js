var fs = require("fs");
var spawn = require('child_process').spawn
var model = require('../models/clothes');

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
      var clothes = (await model.get({_id: id}));
  	}
  	catch (e){
      	return next(e);
  	}
  	console.log(clothes)
	var py    = spawn('python', ['./python/test.py', func_name])//, contents, nodejs_communicator
	
	/*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
	py.stdout.on('data', (data) => {
		//res = JSON.parse(data.toString().replace(/'/g, '"'))
		res = data.toString()
  		console.log(res)//.clothes
	});

  }catch (e){
      return next(e);
  }
  return res.status(200);
};

exports.get = get;
