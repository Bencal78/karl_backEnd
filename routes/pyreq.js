var express = require('express');
var router = express.Router();
var controller = require('../controllers/pyreq');


router.get('/', controller.get);
router.get('/return_outfit', controller.return_outfit)
router.get('/return_weather', controller.return_weather)
router.get('/return_outfit_rl', controller.return_outfit_rl)
router.get('/return_outfit_nb', controller.return_outfit_nb)


module.exports = router;
