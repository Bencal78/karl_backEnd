var express = require('express');
var router = express.Router();
var controller = require('../controllers/users');

router.post('/', controller.create);

router.get('/', controller.get);

router.put('/', controller.update);

router.put('/addTaste/', controller.addTaste);

router.put('/deleteTaste/', controller.deleteTaste);

router.put('/addClothe/', controller.addClothe);

router.put('/deleteClothe/', controller.deleteClothe);

router.delete('/', controller.del);


module.exports = router;
