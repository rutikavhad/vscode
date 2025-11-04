'use strict'

const express = require('express');
const { getMovies, deleteMovie, saveMovies, updateMovies } = require('../../services/movies');
let router = express.Router();

router.get('/', getMovies);
router.delete('/:id', deleteMovie);
router.post('/', saveMovies);
router.put('/:id', updateMovies);

module.exports = router;  