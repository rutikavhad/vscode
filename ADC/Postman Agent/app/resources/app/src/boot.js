let config = require('../config.json'),
  initializeLogger = require('../services/Logger').init;

if (!global.pm) {
  global.pm = {};
}

global.pm.config = {
  get: (key) => config[key],
  overrideConfig: (overrides) => {
    config = Object.assign({}, config, overrides);
  },
  resetConfig: () => {
    config = require('../config.json');
  }
};

global.pm.logger = console; // Have console logs until the logger is initialized.
initializeLogger(); // Initialize logger and set it to pm.logger
