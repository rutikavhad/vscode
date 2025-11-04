"use strict";

const {Movies} = require("../../models");
const {logger, sendPolicyMail} = require("../../../utils");
const customId = require("custom-id");

async function saveMovies(request, response) {
	try {
		const params = request.body;
		if (params) {
			let keys = Object.keys(params);
			let mandetoryKeys = [
        "name"
      ];
			let plst = keys
				.map((key) => {
					let val = params[key];
					if ((mandetoryKeys.indexOf(key) > -1 && val === "") || val === null) {
						return key;
					}
				})
				.filter((item) => {
					return item && item != "";
				});
			if (plst.length) {
				let msg = `Bad Request: ${plst.join(",")} should not be empty fields!`;
				return response.send({success: false, message: msg});
			}
		}
		const cuId = customId({
			name: params.name,
			date: Date.now(),
			randomLength: 2,
		});

		
		params.id = `PY${cuId}`;
		Movies.findOneAndUpdate(params, {$set: params}, {upsert: true})
			.then((doc) => {
				if (doc) {
					logger.error(`${doc}`);
					return response.send({
						success: false,
						message: "Something wrong, Please try again!",
					});
				} else {
					return response.send({
						success: true,
						message: "Movie details saved successfully!",
					});
				}
			})
			.catch((error) => {
				logger.error(`${error}`);
				return response.send({success: false, message: `${error}`});
			});
		// }
	} catch (error) {
		logger.error(`${error}`);
		return response.send({success: false, message: `${error}`});
	}
}

module.exports = {
	saveMovies: saveMovies,
};
