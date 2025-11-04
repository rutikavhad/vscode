"use strict";
const _ = require("lodash");
const {logger, updateData} = require("../../../utils");
const {Movies} = require("../../models");

function getFilterData(request, response) {
	try {
		let filter = request.query ? updateData(request.query) : {};
		if (filter && filter.type) {
			let type = filter.type;
			switch (type) {
				case "movies":
					getModelData(Movies, filter, response, type, request);
					break;
				default:
					break;
			}
		} else {
			logger.debug("request params: " + JSON.stringify(filter));
			return response.send({
				success: false,
				message: "Error: Bad Request, fiter type missing",
			});
		}
	} catch (error) {
		logger.error(`${error}`);
		return response.send({success: false, message: `${error}`});
	}
}

async function getModelData(model, filter, response, type, request) {
	try {
		let order = 1;
		let offset = 0;
		let limit = 100;
		let page_no = 0;
		let qfilter = {};
		if (filter && filter.order) {
			order = filter.order == "asc" ? 1 : -1;
		}

		if (filter && filter.query) {
			qfilter = {$text: {$search: filter.query, $caseSensitive: false}};
		} else if (filter && filter.qfilter) {
			qfilter = filter.qfilter;
		}

		if (filter && filter.limit) {
			limit = parseInt(filter.limit);
		}

		if (filter && filter.page) {
			page_no = parseInt(filter.page);
		}

		offset = page_no > 1 ? page_no * limit : 0;
		if (model) {
			let result = await model
				.aggregate([
					{$match: qfilter},
					{$skip: offset},
					{$sort: {createdAt: order}},
					{$limit: limit},
				])
				.then((docs) => {
					return docs;
				});
			let resp = {
				list: result,
				page: page_no,
				next_page: 0,
			};
			if (result) {
				if (result.length == limit) {
					resp.next_page = page_no + 1;
				}
				logger.debug(`${resp}`);

				return response.send({
					success: true,
					data: resp,
					message: `${type} list get suucessfully!`,
				});
			} else {
				return response.send({
					success: true,
					data: resp,
					message: "No Data Found!",
				});
			}
		} else {
			logger.debug("request params: " + JSON.stringify(filter));
			return response.send({
				success: false,
				message: "Error: Bad Request, data model missing",
			});
		}
	} catch (error) {
		logger.error(`${error}`);
		return response.send({success: false, message: `${error}`});
	}
}

module.exports = {
	getFilterData: getFilterData,
	getModelData: getModelData,
};
