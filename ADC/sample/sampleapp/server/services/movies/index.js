const { getMovies } = require('./getmovies');
const {deleteMovie}=require('./deletemovies');
const { saveMovies } = require('./createmovies');
const { updateMovies } = require('./updatemovies');
module.exports = {
    getMovies: getMovies,
    deleteMovie: deleteMovie,
    saveMovies: saveMovies,
    updateMovies: updateMovies,
};