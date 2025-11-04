const { app } = require('electron'),
  agentSettings = require('../agentSettings'),
  path = require('path');

/**
 * An abstract class implementing common agent methods
 * @requires pm.logger
 * @requires pm.config
 * @requires agentSettings
 * @abstract
 * @class
 * @
 */
class AutoLaunch {
  constructor () {
    this._isDevMode = (pm.config.get('ENV') === 'dev');
    this._appFolder = path.dirname(process.execPath);
    this._disableOnUninstall();
  }

  /**
   * Check if the auto launch is enabled
   * @returns {Boolean}
   */
  isEnabled () { }

  /**
   * toggles auto launch
   */
  toggle () {
    this.isEnabled() ? this.disable() : this.enable();
  }

  /**
   * Launch on startup feature depends on the path of the application
   * Enabling launch on startup for an application from two different locations will create two entries for same app
   * On Mac, we restrict the user from enabling the auto launch until app is moved to Applications folder
   * @returns {Boolean}
   */
  canModifyConfig () {
    return this._isDevMode ? false : (process.platform !== 'darwin' || app.isInApplicationsFolder());
  }

  /**
   * Determines if the auto launch preference can be modified
   * @param {Callback} cb call back with parameter passed as boolean.
   */
  _canModifyAutoLaunch (cb) { }

  /**
   * Enables auto launch
   */
  enable () { }

  /**
   * Disables auto launch
   */
  disable () { }

  /**
   * @description Initialize the auto launch service
   * Enables the auto launch after installing the application
   * This depends on the platform. Override when necessary.
   */
  initialize () {
    if (this._isDevMode) {
      return;
    }

    agentSettings.get('isAutoLaunchDefaultBehaviourSet', (error, shouldMenuBeEnabled) => {
      if (error) {
        pm.logger.error('AutoLaunch~initialize - Failed to load isAutoLaunchDefaultBehaviourSet: ' + shouldMenuBeEnabled);
        return;
      }

      if (!shouldMenuBeEnabled) {
        this.enable();
        pm.logger.info('AutoLaunch: Enabled as the default behaviour.');
        agentSettings.set('isAutoLaunchDefaultBehaviourSet', true, (error) => {
          if (error) {
            pm.logger.error('AutoLaunch~initialize - Failed to set isAutoLaunchDefaultBehaviourSet: ' + shouldMenuBeEnabled);
            return;
          }

          pm.logger.info('AutoLaunch: isAutoLaunchDefaultBehaviourSet is set and persisted.');
        });
      }
    });
  }

  /**
   * Enabling launch on startup leaves a ghosted entry in login/startup items
   * As we have uninstaller for Windows, we clean it up while uninstalling the app
   * This needs to be called initially even before the tray is created.
   */
  _disableOnUninstall () { }
}

module.exports = AutoLaunch;
