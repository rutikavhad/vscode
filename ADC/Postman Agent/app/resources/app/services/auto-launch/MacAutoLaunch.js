const { app } = require('electron'),
  AutoLunch = require('./AutoLaunch');

/**
 * Class implementing auto launch for Mac
 * Auto launch in Mac is implemented by using the electron {@link https://www.electronjs.org/docs/api/app#appsetloginitemsettingssettings-macos-windows API}
 * @class
 * @implements {AutoLaunch}
 */
class MacAutoLaunch extends AutoLunch {
  constructor () {
    super();
  }

  /**
   * Auto launch preference in Mac can be modified if not in Dev mode
   * @override
   */
  _canModifyAutoLaunch () {
    if (this._isDevMode) {
      pm.logger.info('AutoLaunch: Disabled in developer mode');
    }
    return !this._isDevMode;
  }

  /**
   * Check if the auto launch is enabled
   * @override
   * @returns {Boolean}
   */
  isEnabled () {
    return app.getLoginItemSettings().openAtLogin;
  }

  /**
   * Auto launch in Mac is enabled by using electron API
   * @override
   */
  enable () {
    if (this._canModifyAutoLaunch()) {
      app.setLoginItemSettings({
        openAtLogin: true
      });
      pm.logger.info('AutoLaunch: Enabled');

      // Using inline require to avoid cyclic dependency
      require('../../src/menu').MenuManager.refreshAutoLaunchMenuItem();
      return;
    }
    pm.logger.error('AutoLaunch: Not modifiable.');
  }

  /**
   * Auto launch in Mac is disabled by using the electron {@link https://www.electronjs.org/docs/api/app#appsetloginitemsettingssettings-macos-windows API}
   * @override
   */
  disable () {
    if (this._canModifyAutoLaunch()) {
      app.setLoginItemSettings({
        openAtLogin: false
      });
      pm.logger.info('AutoLaunch: Disabled');
      return;
    }
    pm.logger.error('AutoLaunch: Not modifiable.');
  }

  /**
   * On Mac, we enable auto launch by default when the application runs from the applications folder for the first time.
   * To cover the case where user moves the application to Applications folder when launching the app second time or after,
   * using storage variable 'shouldAutoLaunchMenuBeEnabled'
   * @override
   */
  initialize () {
    if (app.isInApplicationsFolder() === false) {
      return;
    }

    super.initialize();
  }
}

module.exports = MacAutoLaunch;
