'use strict';

const express = require('express');
const helmet = require('helmet')
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cookieParser = require('cookie-parser');
const cors = require('cors');

module.exports = function () {
  let server = express(), create, start, close;

create = function (config, db) {
    try {
      let routes = require('./routes');
      const originalSend = server.response.send;

      // Server settings
      server.set('env', config.env);
      server.set('port', config.port);
      server.set('hostname', config.hostname);

      // Returns middleware that parses json
      server.use(helmet());
      server.use(cors());
      server.use(bodyParser.json());
      server.use(bodyParser.urlencoded({ extended: false }));
      server.use(cookieParser());

      server.response.send = function sendOverWrite(body) {
        originalSend.call(this, body);
        this.__custombody__ = body
      }
      //DB connection
      mongoose.connect(db.database, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        autoIndex: true,
      });
      // Set up routes
      routes.init(server);
    } catch (error) {
      throw error;
    }
};

  start = function () {
    try {
      let hostname = server.get('hostname'),
        port = server.get('port');

      server.listen(port, function () {
        console.log('Express server listening on - http://' + hostname + ':' + port);
      });
    } catch (error) {
      throw error;
    }
  };

  close = function (exit, code) {
    try {
      setTimeout(() => {
        exit(code);
      }, 100);
    } catch (error) {
      throw error;
    }
  };
return {
    create: create,
    start: start,
    close: close
  };
};
