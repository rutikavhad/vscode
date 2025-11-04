const path = require('path'),
  fs = require('fs'),
  { app } = require('electron'),
  AutoLunch = require('./AutoLaunch');

/**
 * Class implementing auto launch for Windows
 * Auto launch in Windows is implemented by using the electron {@link https://www.electronjs.org/docs/api/app#appsetloginitemsettingssettings-macos-windows API}
 * @class
 * @implements {AutoLaunch}
 */
class WindowsAutoLaunch extends AutoLunch {
  constructor () {
    super();

    // Using the shortcut as executable path to be consistent across updates
    this._appExePath = path.resolve(this._appFolder, '..', `${pm.config.get('AppName')}.exe`);
  }

  /**
   * Auto launch preference can be changed in windows, if shortcut for the executable is available
   * @override
   */
  _canModifyAutoLaunch (cb) {
    if (this._isDevMode) {
      pm.logger.info('AutoLaunch: Disabled in developer mode');
      cb(false);
      return;
    }

    // In case of shortcut being deleted. Auto launch uses shortcut as shortcut path stays the same across updates
    fs.access(this._appExePath, fs.constants.F_OK, (err) => {
      if (err) {
        pm.logger.error(`AutoLaunch: Missing ${pm.config.get('AppName')}.exe, checked: `, this._appExePath);
        cb(false);
        return;
      }
      cb(true);
    });
  }

  /**
   * Check if auto launch is enabled
   * @override
   * @returns {Boolean}
   */
  isEnabled () {
    const loginItemSettings = app.getLoginItemSettings({
      path: this._appExePath
    });
    return loginItemSettings.openAtLogin;
  }

  /**
   * Enable the auto launch
   * @override
   */
  enable () {
    this._canModifyAutoLaunch((mutable) => {
      if (mutable) {
        app.setLoginItemSettings({
          openAtLogin: true,
          path: this._appExePath
        });
        pm.logger.info('AutoLaunch: Enabled');

        // Using inline require to avoid cyclic dependency
        require('../../src/menu').MenuManager.refreshAutoLaunchMenuItem();
        return;
      }
      pm.logger.error('AutoLaunch: Not modifiable.');
    });
  }

  /**
   * Disable the auto launch
   * @override
   */
  disable () {
    if (this._isDevMode) {
      pm.logger.info('AutoLaunch: Disabled in developer mode');
      return;
    }
    app.setLoginItemSettings({
      openAtLogin: false,
      path: this._appExePath
    });
    pm.logger.info('AutoLaunch: Disabled');
    return;
  }

  /**
   * As we have uninstaller for Windows, we clean it up while uninstalling the app
   * @override
   */
  _disableOnUninstall () {
    if (process.argv[1] === '--squirrel-uninstall') {
      this.disable();
      pm.logger.info('AutoLaunch: Disabled on the Uninstall.');
    }
  }
}

module.exports = WindowsAutoLaunch;
