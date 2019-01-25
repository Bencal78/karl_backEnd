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
    switch (func_name) {
      case "return_outfit_quizz_start":
      return_outfit_quizz_start(req, res, next)
      break;

      case "return_outfit":
      return_outfit(req, res, next)
      break;

      case "return_outfit_rl":
      return_outfit_rl(req, res, next)
      break;

      case "return_outfit_nb":
      return_outfit_nb(req, res, next)
      break;

      default:

    }

  }catch (e){
    return next(e);
  }
  return res.status(200);
};

let return_outfit_quizz_start = async (req, res, next) => {
  try{
    try{
      var all_clothes = (await clothes.get());
    }
    catch (e){
      return next(e);
    }

    var clothes_json = {"clothes": all_clothes}
    var clothes_string = JSON.stringify(clothes_json)
    console.log(req.query);
    var py = spawn('python3', ['./python/nodejs_communicator.py', req.query.func_name, clothes_string])// nodejs_communicator
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

let return_outfit_rl = async(req, res, next) => {
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
  if (!("rl_cat_score" in user)){
    user["rl_cat_score"] = {0: {}, 1: {}, 2: {}, 3: {}}
  }
  if (!("tastes" in user)){
    user["last_taste"] = "None"
  }
  else {
    user["last_taste"] = user.tastes.slice(-1)[0]
  }
  var clothes_json = {"clothes": user.clothes, "rl_cat_score": user.rl_cat_score, "last_taste": user.last_taste}

  var clothes_string = JSON.stringify(clothes_json)
  var py = spawn('python3', ['./python/nodejs_communicator.py', req.query.func_name, clothes_string])// nodejs_communicator
  /*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
  py.stdout.on('data', (data) => {
    console.log(((data.toString()).length));
    console.log(Buffer.byteLength(data.toString(), 'utf8'));
    result = JSON.parse(data.toString().replace(/'/g, '"'))
    return res.status(200).json(result["outfit"]);
  });
}

let return_outfit = async(req, res, next) => {
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
	var clothes_json = {"clothes": user.clothes}
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
}


exports.get = get;
