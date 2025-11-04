'use strict';

const winston = require('winston');
const rfs = require('rotating-file-stream');

// create a rotating write stream
let activityLogStream = rfs.createStream('activity.log', {
    interval: '1d', // rotate daily
    path: './log/'
});

module.exports = {
    logger: new winston.createLogger({
        transports: [
            new winston.transports.Stream({
                stream: activityLogStream,
                format: winston.format.combine(
                    winston.format.timestamp(),
                    winston.format.json()
                ),
            })
        ],
        exitOnError: false
    })
};