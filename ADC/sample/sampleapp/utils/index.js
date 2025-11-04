'use strict';

const _ = require("lodash");
const {logger}=require('./logger');

function updateData(obj) {
    try {
        let keys = _.keys(obj);
        let fobj = {};
        _.forEach(keys, function(key) {
            if (!isNaN(obj[key])) {
                fobj[key] = parseInt(obj[key]);
            } else {
                fobj[key] = obj[key];
            }
        })
        return fobj;
    } catch (error) {
        throw error
    }
}
// return query filter parameter object
function getQueryFilter(filter) {
    try {
        let ingoreKeys = ['limit', 'order', 'page', 'query'];
        let keys = _.keys(filter);
        let qfilter = {};
        _.forEach(keys, function(key) {
            if (ingoreKeys.indexOf(key) == -1) {
                qfilter[key] = filter[key];
            }
        });
        return qfilter;
    } catch (error) {
        throw error;
    }
}

// remove empty fields from object
function removeEmptyFields(obj) {
    for (var k in obj) {
        if (!obj[k] || typeof obj[k] !== "object") {
            if (obj[k] === null || obj[k] === undefined || obj[k] === "") {
                delete obj[k];
            }
            continue
        }
        removeEmptyFields(obj[k]);
        if (Object.keys(obj[k]).length === 0) {
            delete obj[k];
        }
    }
    return obj;
}

module.exports = {
  updateData: updateData,
  logger: logger,
  getQueryFilter: getQueryFilter,
  removeEmptyFields: removeEmptyFields
};