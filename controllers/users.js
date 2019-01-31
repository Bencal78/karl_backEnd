var model = require('../models/users');

const create = async (req, res, next) => {
  try{
      var response = (await model.create(req.body));
  }catch(e){
      next(e);
  }
  return res.status(200).json({message: 'created.'});
};

const get = async (req, res, next) => {
  try{
      var response = (await model.get(req.query));
  }catch (e){
      return next(e);
  }
  return res.status(200).json(response);
};


const update = async (req, res, next) => {
  id = req.body._id;
  if(id) {
    return model.get({_id: id}).then(result => {
        if (result && result.length > 0) {
            return model.update(req.body).then(Updated => {
                return res.status(200).json({message: 'success.'});
            });
        } else return res.status(400).json({error: 'Invalid data.'});
    }).catch(function(e){
        next(e);
    });
  }
};

const addTaste = async (req, res, next) => {
  id = req.body._id;
  tastes = req.body.tastes;
  console.log("type of tastes :", typeof(tastes));
  if(id && tastes) {
    return model.get({_id: id}).then(result => {
        if (result && result.length > 0) {
            return model.addTaste(req.body).then(Updated => {
                return res.status(200).json({message: 'success.'});
            });
        } else return res.status(400).json({error: 'Invalid data.'});
    }).catch(function(e){
        next(e);
    });
  }
};

const addClothe = async (req, res, next) => {
  id = req.body._id;
  clothes = req.body.clothes;
  console.log("type of clothes :", typeof(clothes));
  if(id && clothes) {
    if(!Array.isArray(clothes)){
      let temp = [];
      temp.push(clothes);
      clothes = temp;
    }
    return model.get({_id: id}).then(result => {
        if (result && result.length > 0) {
            return model.addClothe(req.body).then(Updated => {
                return res.status(200).json({message: 'success.'});
            });
        } else return res.status(400).json({error: 'Invalid data.'});
    }).catch(function(e){
        next(e);
    });
  }
};

const deleteClothe = async (req, res, next) => {
  id = req.body._id;
  clothes = req.body.clothes;
  console.log("type of clothes :", typeof(clothes));
  if(id && clothes) {
    if(!Array.isArray(clothes)){
      let temp = [];
      temp.push(clothes);
      clothes = temp;
    }
    return model.get({_id: id}).then(result => {
        if (result && result.length > 0) {
            return model.deleteClothe(req.body).then(Updated => {
                return res.status(200).json({message: 'success.'});
            });
        } else return res.status(400).json({error: 'Invalid data.'});
    }).catch(function(e){
        next(e);
    });
  }
};

const del = async (req, res, next) => {
  try{
      var checkIfUserExist = (await model.get(req.body));
  }catch(e) {
      return next(e);
  }
  if(checkIfUserExist && checkIfUserExist.length > 0){
      try {
          var response = (await model.delete(req.body));
      } catch (e) {
          return next(e);
      }
      return res.status(200).json({message: 'deleted'});
  } else {
      return res.status(400).json({error: 'Invalid user data.'});
  }
};


exports.create = create;
exports.get = get;
exports.update = update;
exports.del = del;
exports.addTaste = addTaste;
exports.addClothe = addClothe;
exports.deleteClothe = deleteClothe;
