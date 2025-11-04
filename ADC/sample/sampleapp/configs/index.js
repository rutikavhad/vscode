'use strict';
const _ = require("lodash");
const env=process.env.NODE_ENV||"production";
const envConfig=require("./"+env);
const defaultConfig={};
module.exports = _.merge(defaultConfig, envConfig);
