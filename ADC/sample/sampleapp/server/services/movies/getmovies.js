'use strict'

const { Movies } = require('../../models');
const { getModelData } = require('../filters');
const {logger, updateData, getQueryFilter}=require('../../../utils');

function getMovies(request, response) {
    try {
        let fdata = request.query ? updateData(request.query) : {};
        fdata.qfilter = getQueryFilter(fdata);
        getModelData(Movies, fdata, response, 'movies', request);
    } catch (error) {
        logger.error(`${error}`);
        return response.send({ success: false, message: `${error}` });
    }
}

module.exports = {
    getMovies: getMovies,
};