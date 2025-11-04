"use strict";

const {Movies} = require("../../models");
const {logger, removeEmptyFields, sendPolicyMail} = require("../../../utils");

async function updateMovies(request, response) {
	try {
		let obj = request.body;
		let params = request.params;
		if (params && !params.id) {
			return response.send({
				success: false,
				message: "Bad request: Movie id missing in request url!",
			});
		}

		if (params.id.length < 10) {
			return response.send({
				success: false,
				message: `No Policy details found with id ${params.id}`,
			});
		}

		let filter = {id: params.id};
		
		obj = removeEmptyFields(obj);
		
		if (Object.keys(obj).length) {
			await Movies.findOneAndUpdate(filter, {$set: obj}, {upsert: true})
				.then((doc) => {
					if (!doc) {
						return response.send({
							success: false,
							message: `No movie details found with id ${params.id}`,
						});
					} else {
						sendPolicyMail(params);
						return response.send({
							success: true,
							message: "Movie details updated successfully!",
						});
					}
				})
				.catch((error) => {
					logger.error(`${error}`);
					return response.send({success: false, message: `${error}`});
				});
		} else {
			return response.send({
				success: false,
				message: "Movie details fields should not be empty!",
			});
		}
	} catch (error) {
		logger.error(`${error}`);
		return response.send({success: false, message: `${error}`});
	}
}

module.exports = {
	updateMovies: updateMovies,
};
