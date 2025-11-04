const electron = require('electron'),
      EventEmitter = require('events'),
      AgentReleaseService = require('./agentReleaseService'),
      version = require('../package.json').version,
      agentHttpService = require('./agentHttpService'),
      agentUpdaterAdapter = require('./agentUpdaterAdapter'),
      SerializedError = require('serialised-error'),
      MenuManager = require('../src/menu').MenuManager,

      UPDATE_DOWNLOADING = 'downloading',
      UPDATE_DOWNLOADED = 'downloaded',
      UPDATE_CHECKING = 'checking',
      UPDATE_NOT_AVILABLE = 'UpdateNotAvailable',
      UPDATE_AVAILABLE = 'UpdateAvailable',
      IDLE = 'idle',
      UPDATE_ERROR = 'error';

function getPlatform () {
  const architecture =
    require('starship').operatingSystemArchitecture ??
    process.arch.replace('ia32', 'x86');

  // TODO: Remove this once we can allow upgrades from x64 to ARM on Windows.
  if (
    process.platform === 'win32' &&
    architecture === 'arm64' &&
    process.arch !== 'arm64'
  ) {
    return 'windows_64';
  }

  return `${
    { darwin: 'osx', linux: 'linux', win32: 'windows' }[process.platform]
  }_${{ arm64: 'arm64', x64: '64', x86: '32' }[architecture]}`;
}

class agentUpdateService extends EventEmitter {
  /**
   * Constructor for agentUpdaterService
   */
  constructor () {
    super();
    this.status = IDLE,
    this.data = null,
    this.version = version;
    this.appId = pm.installationId;
    this.updateServerDomain = pm.config.get('postman_update_server_url');
    this._hasUpdaterInstanceInitialised = false;
    this.connectedClientCount = 0;
  }

  /**
   * This function returns the app release server endpoint to check for updates
   * @param {*} cb
   */
  _getUpdateStatusURL (cb) {
    let updateChannel = AgentReleaseService.getReleaseChannel(),
      appReleaseServerEndpoint = this.updateServerDomain + 'update/status?' + [
        `channel=${updateChannel}`,
        `currentVersion=${this.version}`,
        `platform=${getPlatform()}`
      ].join('&');
    cb(appReleaseServerEndpoint);
  }

  /**
   * Return the current status for the update workflow
   */
  getStatus () {
     return this.status;
  }

  /**
   *  Function to download updated app and update the menuItem to downloading
   * @param {Object} options
   */
  downloadUpdate (options = {}) {
    if (this.getStatus() !== UPDATE_AVAILABLE) {
      return;
    }

    this.status = UPDATE_DOWNLOADING;
    MenuManager.refreshUpdateStatus([
      {
      label: `Downloading update v${this.data.version}...`,
      enabled: false
      }
    ]);

    let data = this.data,
      eventPayload = {
        channel: AgentReleaseService.getReleaseChannel(),
        version: this.version,
        platform: getPlatform(),
        downloadURL: options.downloadURL || (data && data.url),
        updateServerDomain: this.updateServerDomain
      };
    this.updaterInstance.downloadUpdate(eventPayload);
  }

  /**
   * Function to check the version available to update app and set the MenuItem
   * accordingly
   */
  checkForVersionUpdate () {
    this.status = UPDATE_CHECKING,
    this.data = null;

    return new Promise((resolve, reject) => {
      this._getUpdateStatusURL((url) => {
        agentHttpService.request(url).then(({ body, status }) => {

          if (status === 200) {
            this.status = UPDATE_AVAILABLE;
            this.data = body;

            resolve({
              status: this.status,
              data: body
            });
          }
          else if (status === 204) {
            this.status = UPDATE_NOT_AVILABLE;
            this.data = null;

            resolve({
              status: this.status,
              data: null
            });
          }
          else {
            pm.logger.warn(`Error while checking for update, received status code ${status}`);
            this.status = UPDATE_ERROR;
            this.data = null;

            reject({
              status: this.status,
              error: `received status code ${status}`
            });
          }
        }).catch((err) => {
          pm.logger.warn('Error while checking for update', err);
          this.status = UPDATE_ERROR;
          this.data = null;

          reject({
            status: this.status,
            error: new SerializedError(err)
          });
        });
      });
    });
  }

  /**
   * Function to check for version update and download the updated version available.
   */
  checkForUpdateAndDownload () {
    MenuManager.refreshUpdateStatus([
      {
        label: 'Checking For Update...',
        enabled: false
      }
    ]);

    this.checkForVersionUpdate().then((result) => {
      if (result.status === UPDATE_AVAILABLE) {
        this.downloadUpdate(result.data);
      }
      else if (result.status === UPDATE_NOT_AVILABLE) {
        MenuManager.refreshUpdateStatus([
          {
            label: 'Check for Updates',
            click: function () {
              MenuManager.handleMenuAction('CheckForUpdateAndDownload');
            }
          },
          {
            label: 'You are up to date!',
            enabled: false
          }
        ]);
      }
    }).catch((result) => {
      pm.logger.warn('Error while checking for update', result.error);
      this.status = UPDATE_ERROR;
      this.data = null;

      MenuManager.refreshUpdateStatus([
        {
          label: 'Check For Updates',
          click: function () {
            MenuManager.handleMenuAction('CheckForUpdateAndDownload');
          }
        },
        {
          label: 'Error! Please try again',
          enabled: false
        }
      ]);
    });
  }

  /**
   * Quit and Restart the app
   */
  restartAndUpdate (opts) {
    // Marking restart flag as true to relaunch the app after applying updates
    const force = opts?.force ?? true;
    if (force || (!force && this.connectedClientCount === 1)) {
      this.updaterInstance.restartAppToUpdate({ restart: true });
    }
  }

  /**
   * Apply update before quit
   */
  applyUpdateAndQuit () {
    // Marking restart flag as false to prevent relaunching the app after applying updates
    this.updaterInstance.restartAppToUpdate({ restart: false });
  }

  /**
   * @method handleOnUpdateDownloaded
   * @param {Object} event
   * @param {String=} notes
   * @param {String=} name
   * @param {String=} date
   * @param {String=} URL
   * @param {String=} downloadVersion
   */
  handleOnUpdateDownloaded (event, notes, name, date, URL, downloadVersion) {
    this.status = UPDATE_DOWNLOADED;
    this.emit('update_downloaded', { version: this.data?.version });

    // Note: downloadVersion is not returning a string value from the api.
    // It should have written the downloaded version like x.y.z but it is returning function
    // So,taking version from properties
    agentUpdaterAdapter.setDownloadedVersion(this.data.version);

    MenuManager.refreshUpdateStatus([
      {
        label: `Update downloaded v${this.data.version}`,
        enabled: false
      },
      {
        label: 'Install update && restart',
        click: function () {
          MenuManager.handleMenuAction('RestartApp');
        }
      }
    ]);
  }

  /**
   * @method handleOnUpdateNotAvailable
   */
  handleOnUpdateNotAvailable () {
    this.status = UPDATE_NOT_AVILABLE;
    this.data = null;

    MenuManager.refreshUpdateStatus([
      {
        label: 'Check For Updates',
        click: function () {
          MenuManager.handleMenuAction('CheckForUpdateAndDownload');
        }
      },
      {
        label: 'You are up to date!',
        enabled: false
      }
    ]);
  }

  /**
   *
   * @param {Error} error
   * @param {Object=} updateData
   */
  handleOnUpdateError (error, updateData) {
    this.status = UPDATE_ERROR;
    this.data = null;

    MenuManager.refreshUpdateStatus([
      {
        label: 'Check For Updates',
        click: function () {
          MenuManager.handleMenuAction('CheckForUpdateAndDownload');
        }
      },
      {
        label: 'Error! Please try again',
        enabled: false
      }
    ]);
  }

  /**
   * @method handleOnVersionUpdate
   * @param {?String} lastKnownVersion
   * @param {String} currentVersion
   */
  handleOnVersionUpdate (lastKnownVersion, currentVersion) {
    MenuManager.refreshUpdateStatus([
      {
        label: 'Check For Updates',
        enabled: false
      },
      {
        label: 'Version Updated to ...',
        enabled: false
      }
    ]);
  }

  /**
   * @method handleAppQuitting
   * @description This will be called when the updater quits the app.
   */
  handleAppQuitting () {
    electron.app.quittingApp = true;
  }

  attachUpdaterListeners () {
    if (this._hasUpdaterInstanceInitialised) {
      return;
    }
    this.updaterInstance.on('updateDownloaded', this.handleOnUpdateDownloaded.bind(this));
    this.updaterInstance.on('updateNotAvailable', this.handleOnUpdateNotAvailable.bind(this));
    this.updaterInstance.on('beforeAppQuit', this.handleAppQuitting.bind(this));
    this.updaterInstance.on('versionUpdated', this.handleOnVersionUpdate.bind(this));
    this.updaterInstance.on('error', this.handleOnUpdateError.bind(this));
    this._hasUpdaterInstanceInitialised = true;
  }

  updateConnectedClientCount (count) {
    this.connectedClientCount = count;
  }
}

let agentUpdaterService = new agentUpdateService();
    agentUpdaterService.constants = {
      UPDATE_DOWNLOADING,
      UPDATE_DOWNLOADED,
      UPDATE_CHECKING,
      UPDATE_NOT_AVILABLE,
      UPDATE_AVAILABLE,
      IDLE,
      UPDATE_ERROR
    };

module.exports = agentUpdaterService;
