const fs = require('fs');
const path = require('path');
let rawdata = fs.readFileSync(path.resolve(__dirname, 'settings.json'));
let settings = JSON.parse(rawdata);

module.exports = settings;