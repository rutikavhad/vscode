'use strict';

const mongoose = require('mongoose');

const MoviesSchema = new mongoose.Schema({
    Title: { type: String, required: true },
    Year: { type: Number },
    Runtime: { type: String },
    Genre: [String],
    Director: { type: String },
    Writer: [String],
    Actors: [String],
    Plot: { type: String },
    Language: [String],
    Country: { type: String },
    imdbRating: { type: Number },
    imdbVotes: { type: Number },
    imdbID: { type: String },
    BoxOffice: { type: String },
    Production: { type: String },
}, {
    collection: 'movies',
    strict: false,
});

MoviesSchema.index(
    {
        Title: 'text',
        Director: 'text',
        Actors: 'text',
        Plot: 'text'
    },
    { name: 'moviesIndex' }
);

const Movies = mongoose.model('Movies', MoviesSchema);

module.exports = Movies;
