var fs = require("fs");
var spawn = require('child_process').spawn
var clothes = require('../models/clothes');
var users = require('../models/users');
var request = require('request-promise');

const get = async (req, res, next) => {

};

const return_outfit = async (req, res, next) => {
  try{
    var func_name = 'return_outfit'

  	var id = req.query.id
  	if(!id){
  		return res.status(404).json({"message": "Cannot return outfit without id"})
  	}
  	try{
  		var user = (await users.get({_id: id}))[0];
    	}
  	catch (e){
      	return next(e);
    	}
    conditions = await return_weather_python(req, res, next)
    if (conditions){
      py_conditions = conditions.python
    }
    else {
      py_conditions = false
    }
    console.log(py_conditions);
  	var user = user.toJSON()
    if (!("clothes" in user)){
      return res.status(501).json({"error": "no field 'clothes' for this user : "+id+". Cannot create an outfit without clothes"});
    }
    else{
      if (user["clothes"].length == 0){
        return res.status(501).json({"error": "field 'clothes' empty for this user : "+id+". Cannot create an outfit without clothes"});
      }
    }
  	var clothes_json = {"clothes": user.clothes, "conditions": py_conditions}
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

const return_outfit_rl = async(req, res, next) => {

  var func_name = 'return_outfit_rl'
  var id = req.query.id
  // get requested id
  if(!id){
    return res.status(404).json({"message": "Cannot return outfit without id"})
  }
  // get user from MongoDB
  try{
    var user = (await users.get({_id: id}))[0];
  }
  catch (e){
    return next(e);
  }
  // user tojson
  var user = user.toJSON()
  // request for weather conditions
  conditions = await return_weather_python(req, res, next)
  if (conditions){
    py_conditions = conditions.python
  }
  else {
    py_conditions = false
  }
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

  var args_json = {"clothes": user.clothes, "rl_cat_score": user.rl_cat_score, "tastes": tastes, "conditions": py_conditions}
  var args_string = JSON.stringify(args_json)
  var py = spawn('python3', ['./python/nodejs_communicator.py', func_name, args_string])// nodejs_communicator
  /*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
  let result = '';
  py.stdout.on('data', data => {
      result += data.toString();
  });
  py_res = py.stdout.on('end', () => {
    try {
      // If JSON handle the data
      console.log(result);
      py_res = JSON.parse(result.replace(/'/g, '"'))
      console.log(py_res)
      if ("clothes" in py_res){
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

const return_outfit_nb = async (req, res, next) => {
  return res.status(501)
}

const return_weather = async(req, res, next) => {
  if (!("lat" in req.query)){
    return null
  }
  if (!("long" in req.query)){
    return null
  }
  let apiKey = 'a79c0ff7696c4832dd331a688434f96e';
  let url = `http://api.openweathermap.org/data/2.5/weather?lat=${req.query.lat}&lon=${req.query.long}&appid=${apiKey}`
  let kelvin_to_celsius_const = 273.15

  conditions = await request(url).then(body => {
    try{
      body_json = JSON.parse(body);
      temperature = body_json.main.temp - kelvin_to_celsius_const
      weather = body_json["weather"][0]['main']
      conditions = {"python": {"temperature": temperature, "weather": weather}, "android": body_json}
      return conditions
    }catch(e){
      console.log(e)
    }
  }).catch(err => {
    console.log(err);
  })
  return res.status(200).json(conditions)
}

let return_weather_python = async(req, res, next) => {
  if (!("lat" in req.query)){
    return null
  }
  if (!("long" in req.query)){
    return null
  }
  let apiKey = 'a79c0ff7696c4832dd331a688434f96e';
  let url = `http://api.openweathermap.org/data/2.5/weather?lat=${req.query.lat}&lon=${req.query.long}&appid=${apiKey}`
  let kelvin_to_celsius_const = 273.15

  conditions = await request(url).then(body => {
    try{
      body_json = JSON.parse(body);
      temperature = body_json.main.temp - kelvin_to_celsius_const
      weather = body_json["weather"][0]['main']
      conditions = {"python": {"temperature": temperature, "weather": weather}, "android": body_json}
      return conditions
    }catch(e){
      console.log(e)
    }
  }).catch(err => {
    console.log(err);
  })
  return conditions
}


exports.get = get;
exports.return_outfit = return_outfit
exports.return_outfit_rl = return_outfit_rl
exports.return_weather = return_weather
exports.return_outfit_nb = return_outfit_nb
