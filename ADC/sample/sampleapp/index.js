'use strict';

const config = require('./configs/config');
const db = require('./configs/database');
const server = require('./server');

const app = server();
app.create(config, db);
app.start();
