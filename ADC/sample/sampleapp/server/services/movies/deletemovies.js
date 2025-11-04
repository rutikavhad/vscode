"use strict";

const {Movies} = require("../../models");
const {logger} = require("../../../utils");

async function deleteMovie(request, response) {
  try {
    let params = request.params;

    if (params && !params.id) {
      return response.send({
        success: false,
        message: "Bad request: Movie id missing in request url!",
      });
    }

  
    let filter = {id: params.id};

    await Movies.findOneAndDelete(filter)
      .then((doc) => {
        if (!doc) {
          return response.send({
            success: false,
            message: `No movie details found for id ${params.id}`,
          });
        } else {
          return response.send({
            success: true,
            message: "Movie details deleted successfully!",
          });
        }
      })
      .catch((error) => {
        logger.error(`${error}`);
        return response.send({success: false, message: `${error}`});
      });
  } catch (error) {
    logger.error(`${error}`);
    return response.send({success: false, message: `${error}`});
  }
};

module.exports = {
  deleteMovie: deleteMovie,
};
