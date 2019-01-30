var fs = require("fs");
var spawn = require('child_process').spawn
var clothes = require('../models/clothes');
var users = require('../models/users');
var request = require('request');

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
        message = return_outfit(req, res, next)
        break;

      case "return_outfit_rl":
        message = return_outfit_rl(req, res, next)
        break;

      case "return_weather":
        message = return_weather(req)
        break;

      case "return_outfit_nb":
        return_outfit_nb(req, res, next)
        break;

      default:

    }

  }catch (e){
    return next(e);
  }
  return res.status(200).json(message);
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
  // get requested id
  if(!id){
    return res.status(404)
  }
  // get user from MongoDB
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
    tastes = false;
  }
  else {
    tastes = user["tastes"]
  }
  if (!("clothes" in user)){
    return res.status(501).json({"error": "no field 'clothes' for this user : "+id+". Cannot create an outfit without clothes"});
  }
  else{
    if (user["clothes"].length == 0){
      return res.status(501).json({"error": "field 'clothes' empty for this user : "+id+". Cannot create an outfit without clothes"});
    }
  }


  var args_json = {"clothes": user.clothes, "rl_cat_score": user.rl_cat_score, "tastes": tastes}
  var args_string = JSON.stringify(args_json)
  var py = spawn('python3', ['./python/nodejs_communicator.py', req.query.func_name, args_string])// nodejs_communicator
  /*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
  let result = '';
  py.stdout.on('data', data => {
      result += data.toString();
  });
  py_res = py.stdout.on('end', () => {
    try {
      // If JSON handle the data
      py_res = JSON.parse(result.replace(/'/g, '"'))
      if ("clothes" in py_res){
        console.log(py_res["clothes"]);
        user.clothes = py_res["clothes"]
      }
      if ("rl_cat_score" in py_res){
        user.rl_cat_score = py_res["rl_cat_score"]
      }
      if ("tastes" in py_res){
        user.tastes = py_res["tastes"]
      }
      if ("outfit" in py_res){
        outfit = py_res["outfit"]
      }
      else{
        return res.status(500).json({"error": "no outfit returned (python issue)"});
      }
      try{
        users.update(user);
      }
      catch (e){
        return next(e);
      }
      return res.status(200).json({"outfit": outfit});

    }catch (e) {
      // Otherwise treat as a log entry
      console.log(e);
    }
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

let return_weather_conditions = async() => {
  let apiKey = 'a79c0ff7696c4832dd331a688434f96e';
  let url = `http://api.openweathermap.org/data/2.5/weather?lat=${req.query.lat}&lon=${req.query.long}&appid=${apiKey}`
  let kelvin_to_celsius_const = 273.15

  request(url, function (err, response, body) {
    if(err){
      console.log('error:', error);
    } else {
      try{
        body_json = JSON.parse(body);
        temperature = body_json.main.temp - kelvin_to_celsius_const
        weather = body_json["weather"][0]['main']
        conditions = {"temperature": temperature, "weather": weather}
        return conditions
      }catch(e){
        console.log(e)
      }
    }
  });

}


exports.get = get;
