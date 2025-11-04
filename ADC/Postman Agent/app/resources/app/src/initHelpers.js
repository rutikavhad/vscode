const agentSettings = require('../services/agentSettings'),
      { v4: uuidv4 } = require('uuid'),
      { createDefaultDir } = require('./workingDir'),
      agentUpdateService = require('../services/agentUpdateService'),
      initializeUpdater = require('@postman-app/app-updater').init,
      agentUpdaterAdapter = require('../services/agentUpdaterAdapter'),
      agentUpdateNotifier = require('../services/agentUpdateNotifier'),
      trayService = require('../services/trayService');

/**
 *
 * @param {Function} cb
 */
function populateInstallationId (cb) {
  agentSettings.get('installationId', (err, id) => {
    let installationId,
      firstLoad = false;

    if (id) {
      installationId = id;

      // Logging if error occurred even when installationId was fetched
      err && pm.logger.warn('initHelper~populateInstallationId: Got installationId:', id, 'from agentSettings but with an error', err);
    } else {
      // Logging if id was still not available when no error occurred
      !err && pm.logger.warn('Postman Agent~Main~populateInstallationId: Failed to get installationId from agentSettings but with no error');

      // Logging if error occurs and id was not fetched
      err && pm.logger.warn('Postman Agent~Main~populateInstallationId: Failed to get installationId from agentSettings with an error', err,
        '\n Generating new installationId');

      // This means it is the first time app is loading.
      firstLoad = true;
      installationId = uuidv4();
      agentSettings.set('installationId', installationId);
    }

    // Assign the values in app so that the renderers can make use of it.
    pm.firstLoad = firstLoad;
    pm.installationId = installationId;

    return cb();
  });
}

/**
 *  Try creating the default working directory
 * @param {Function} cb
 */
function createDefaultWorkingDir (cb) {
  agentSettings.get('createdDefaultWorkingDir', (err, created) => {
    if (err) {
      pm.logger.error('InitHelpers~createDefaultWorkingDir - Error while trying to get from agentSettings', err);
    }

    if (created) {
      pm.logger.info('InitHelpers~createDefaultWorkingDir - Default working dir creation already attempted');
      return cb();
    }

    // Record the attempt regardless of success of the creation. Prevents unnecessary attempts in
    // future.
    // @todo update the only update once successful when robust file system APIs are in place
    agentSettings.set('createdDefaultWorkingDir', true);

    createDefaultDir((err) => {
      // Ignore any errors, this is single attempt flow
      if (err) {
        // Logging just for debugging
        pm.logger.error('InitHelper~createDefaultWorkingDir - Error while creating default working dir', err);
      }

      // Ignore the error, its not very critical
      return cb();
    });
  });
}

/**
 * This function initialises app-updater logic and attach listerners for different update states
 *
 * @param {*} cb
 */
function updateHandlerInit (cb) {

  const updaterInstance = initializeUpdater({ adapter: agentUpdaterAdapter });

  // If no updater found for the OS, consider it as not as error, just go through it
  if (!updaterInstance) {
    pm.logger.warn('UpdaterHandler~init - Updater not found for the os');
    cb && cb();
    return;
  }

  updaterInstance.init((err) => {
    if (err) {
      pm.logger.error('UpdateHandler~init - Failed', err);
      cb(err);
    }
    pm.logger.info('UpdateHandler~init - Success');
    agentUpdateService.updaterInstance = updaterInstance;
    agentUpdateService.attachUpdaterListeners();
    cb();
  });
}

module.exports = {
  populateInstallationId,
  createDefaultWorkingDir,
  updateHandlerInit
};
