const os = require('os'),
  fs = require('fs'),
  path = require('path'),
  { app } = require('electron'),
  { Originator, Collectors } = require('@postman/app-logger'),

  /**
   * @method getLogPath
   * @description Assigns the logging folder path
   * @return {String}
   */
  getLogPath = () => {
    return path.resolve(app.getPath('userData'), 'logs');
  },

  Logger = {
    init () {
      // Assign logging folder information first
      let FileCollector = Collectors.File,
        ConsoleCollector = Collectors.Console,
        origin = 'main',
        sessionId = process.pid, // set the current process id as sessionId
        collectors = [],
        logPath = getLogPath();

      fs.mkdir(logPath, { recursive: true }, (err) => {
        try {
          if (err) {
            throw err;
          }

          // Set the logging folder information
          app.logPath = logPath;

          // create collectors
          collectors = [
            new FileCollector({
              file: path.resolve(logPath, `${origin}.log`)
            })
          ];

          process.env.PM_BUILD_ENV !== 'production' && collectors.push(new ConsoleCollector());

          // Attach the logger to global
          global.pm.logger = new Originator({ origin, collectors, sessionId });
        }
        catch (e) {
          global.pm.logger = console; // defaults to console

          // Add a helper to create a context object
          // Fallback so modules that assume that pm.logger is using `app-logger` won't misbehave
          global.pm.logger.getContext = function getContext (api, domain) {
            return {
              api,
              domain
            };
          };

          // Don't fail the boot if logger fails
          pm.logger.error('Logger initialization failed', e);
        }
        pm.logger.info(`Booting ${app.name} ${app.getVersion()}, ${os.platform()}-${os.release()} on ${os.arch()}`);
      });
    }
  };

module.exports = Logger;
