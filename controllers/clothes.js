var model = require('../models/clothes');

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
  let body = req.body;
  if(Array.isArray(body)){
    let res_arr = []
    let id;
    body.forEach(b => {
      id = b._id;
      res_arr.push(model.get({_id: id}).then(result => {
            if (result && result.length > 0) {
                return model.update(b).then(Updated => {
                    return "200";
                });
            } else return "400";
        }).catch(function(e){
            next(e);
      }));
    });
    return res.status(202).json({message: "updated", promises: res_arr});
  }
  else{
    id = body._id;
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
  }
};

const del = async (req, res, next) => {
  try{
      var checkIfClotheExist = (await model.get(req.body));
  }catch(e) {
      return next(e);
  }
  if(checkIfClotheExist && checkIfClotheExist.length > 0){
      try {
          var response = (await model.delete(req.body));
      } catch (e) {
          return next(e);
      }
      return res.status(200).json({message: 'deleted'});
  } else {
      return res.status(400).json({error: 'Invalid clothe data.'});
  }
};


exports.create = create;
exports.get = get;
exports.update = update;
exports.del = del;
