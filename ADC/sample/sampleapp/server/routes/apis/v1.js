"use strict";
const moviesController=require('../../controllers/apis/movies');
const express=require("express");
let router=express.Router();

router.use('/movies',moviesController);

module.exports=router;