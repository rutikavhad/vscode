'use strict';
const { database } = require('./settings');

module.exports = {
  secret: database.secretKey,
  database: database.dbURL
};
