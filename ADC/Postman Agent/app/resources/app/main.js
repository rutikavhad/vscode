// IMPORTANT: This should be the very first like of application
require('./src/boot');

const path = require('path'),
    async = require('async'),
    os = require('os'),
    _ = require('lodash'),
    { app, Tray, dialog } = require('electron'),
    WebsocketAgent = require('./lib/WebsocketAgent'),
    MenuManager = require('./src/menu').MenuManager,
    RuntimeExecutionService = require('./lib/common/services/RuntimeExecutionService'),
    { createDefaultWorkingDir, populateInstallationId, updateHandlerInit } = require('./src/initHelpers'),
    agentSettings = require('./services/agentSettings'),
    agentUpdateService = require('./services/agentUpdateService'),
    trayService = require('./services/trayService'),
    agentUpdateNotifier = require('./services/agentUpdateNotifier'),
    autoLaunch = require('./services/auto-launch'),

    MOVE_DIALOG_MESSAGE = 'Move to Applications Folder?',
    MOVE_DIALOG_ACTION_BUTTON = 'Move to Applications Folder',
    MOVE_DIALOG_CANCEL_BUTTON = 'Do Not Move',
    MOVE_DIALOG_CHECKBOX_MESSAGE = 'Do not remind me again',
    MOVE_DIALOG_DETAILS = 'I can move myself to the Applications folder if you\'d like. This will ensure that future updates will be installed correctly.';

// The default minimum supported version of TLS in node v10 was v1.
// Once we upgraded Electron to v7 that comes with node v12, the minimum
// support version was changed to v1.2. Due to this, users still using the
// old servers won't be able to use Postman Desktop Agent to send request
// See https://github.com/postmanlabs/postman-app-support/issues/9406
// As a fix, we are overriding this default minimum version of TLS back to v1
require('tls').DEFAULT_MIN_VERSION = 'TLSv1';

if (!app.requestSingleInstanceLock()) {
  pm.logger.info('Postman Agent~Main Could not get the lock, quitting');
  app.exit();
}

// Hide dock icon in MAC
if (process.platform === 'darwin') {
  app.dock.hide();
}

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  pm.logger.error('Postman Agent~Main~UncaughtException', error);

  dialog.showMessageBox({
    title: 'Unexpected Error',
    type: 'error',
    message: 'An Error Has Occurred',
    detail: error.toString(),
    buttons: ['Close']
  });
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (error) => {
  pm.logger.error('Postman Agent~unhandledRejection', error);

  dialog.showMessageBox({
    title: 'Unexpected Error',
    type: 'error',
    message: 'An Error Has Occurred',
    detail: error.toString(),
    buttons: ['Close']
  });
});

/**
 * Emitted when all windows have been closed.
 *
 * If you do not subscribe to this event and all windows are closed,
 * the default behavior is to quit the app; however, if you subscribe,
 * you control whether the app quits or not.
 */
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', function (event) {
  pm.logger.info('Quitting app');
  app.quittingApp = true;

  if (process.platform !== 'linux') {
    agentUpdateService.updaterInstance = null;
    return;
  }

  // Calling `event.preventDefault` stops the default action of an event from happening. We need this logic for linux
  // Since we have to swap the updated app files, if available with the existing app files on linux before quitting the app
  event.preventDefault();
  agentSettings.get('downloadedVersion', (err, downloadedVersion) => {
    if (err) {
      return;
    }
    let currentVersion = app.getVersion();

    // Update has been downloaded if `downloadedVersion` exists
    // Update the app and quit
    if (_.isNil(downloadedVersion) === false && currentVersion !== downloadedVersion) {

      // applyUpdateAndQuit() internally calls swapAndRelaunch.sh
      // Which serves the purpose of applying update & quit the app by killing the parent process
      // If called, any statement after this function call in `before-quit` event will be skipped.
      pm.logger.info('Applying update and quitting the app');
      agentUpdateService.applyUpdateAndQuit();
    }

    // if there is no new downloaded updates to apply
    else {
      app.exit();
    }
  });
});

/**
 * This will show a prompt for moving the current app to applications folder when running on a mac
 */
function promptMoveToApplicationsFolder (cb) {
  shouldShowMovePrompt((shouldShow) => {
    if (!shouldShow) {
      return cb();
    }

    pm.logger.info('Main~promptMoveToApplicationsFolder - Postman Agent is not in applications folder, showing a prompt to move it there');

    dialog.showMessageBox({
      type: 'question',
      buttons: [MOVE_DIALOG_ACTION_BUTTON, MOVE_DIALOG_CANCEL_BUTTON],
      defaultId: 0, // Does not change the default selected button as mentioned in docs but only specifies the primary button (changes the color to blue)
      message: MOVE_DIALOG_MESSAGE,
      detail: MOVE_DIALOG_DETAILS,
      checkboxLabel: MOVE_DIALOG_CHECKBOX_MESSAGE
    }).then((result) => {
      // if the checkbox was checked, we need to wait for persisting this setting and then move the app
      if (result.checkboxChecked) {
        agentSettings.set('doNotRemindMoveToApplications', true, (err) => {
          result.response === 0 && app.moveToApplicationsFolder();
        });
        return cb();
      }

      // otherwise, if checkbox was not checked we can directly go ahead and start the move
      if (result.response !== 0) {
        return cb();
      }

      // not calling the callback here since we the current app will be quitting anyway
      // no point showing the splash screen
      app.moveToApplicationsFolder();
    });
  });
}

/**
 * Determines whether to show the prompt for moving the current app to applications folder
 */
function shouldShowMovePrompt (cb) {
  if (process.env.PM_BUILD_ENV === 'development' ||
      process.env.SKIP_MOVE_PROMPT === 'true' ||
      os.type() !== 'Darwin' ||
      app.isInApplicationsFolder()) {
    return cb(false);
  }

  agentSettings.get('doNotRemindMoveToApplications', (err, doNotRemind) => {
    if (err) {
      pm.logger.info('Main~shouldShowMovePrompt - Error while trying to get "mode" from agentSettings', err);
      return cb(false);
    }

    doNotRemind && pm.logger.info('Main~shouldShowMovePrompt - Not showing the prompt since user has chosen not to be reminded again');
    return cb(!doNotRemind);
  });
}

/**
 * Start the application
 */
function onReady () {

  promptMoveToApplicationsFolder(() => {
    agentSettings.set('downloadedVersion', null);

    trayService.setTrayIcon();

    // Start the websocket server
    WebsocketAgent.start(RuntimeExecutionService(), (err, server, io) => {
      let port,
        count = 0,
        update = () => {
          agentUpdateService.updateConnectedClientCount(count);

          MenuManager.refreshRuntimeStatus([
            {
              label: count ? `Connected (${count})` : 'Disconnected',
              enabled: false
            },
            {
              label: 'Listening on port ' + port,
              enabled: false
            }
          ]);
        };

      agentUpdateService.on('update_downloaded', ({ version }) => {
        io.sockets.emit('update_downloaded', { version });
      });

      io.on('connection', (socket) => {
        // Update the tray when a new connection is made
        count++;
        update();

        // Update the tray when a disconnection happens
        socket.on('disconnect', () => {
          count--;
          update();
        });
      });

      server.on('listening', () => {
        port = server.address().port;

        // Update the tray with the status
        update();
      });

      server.on('close', async () => {

        MenuManager.refreshRuntimeStatus([
          {
            label: 'Stopped',
            enabled: false
          }
        ]);
      });

      server.on('error', (err) => {

        MenuManager.refreshRuntimeStatus([
          {
            label: 'Error - ' + err.code,
            enabled: false
          }
        ]);
      });

      if (pm.config.get('ENV') !== 'dev') {
        // Initializing agent update Notifier after app loads to check for updates every 24 hrs
        agentUpdateNotifier.initialize();

        // Electron's documentation advises a 10-second timeout to avoid locking issues.
        // See this: https://www.electronjs.org/docs/latest/api/auto-updater#:~:text=by%20setting%20a%2010%2Dsecond%20timeout%20on%20your%20update%20checks
        // Note that while they don't say that, it can also apply to launches other than the first one.
        setTimeout(() => {
          // Checking for updates on app launch
          agentUpdateService.checkForUpdateAndDownload();
        }, 10000);
      }
    });
  });

  // Initialize auto launch enabler
  autoLaunch.initialize();
}

async.series([
  (next) => populateInstallationId(next),
  (next) => createDefaultWorkingDir(next),
  (next) => updateHandlerInit(next)
], (err) => {
  if (err) {
    // Booting failed! We cannot continue so shut down business
    throw err;
  }

  app.isReady() ? onReady() : app.on('ready', onReady);
});
