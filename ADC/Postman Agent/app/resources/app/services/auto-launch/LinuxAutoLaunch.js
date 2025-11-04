const path = require('path'),
  os = require('os'),
  AutoLaunch = require('./AutoLaunch'),
  fs = require('fs'),
  autoStartDir = `${os.homedir}/.config/autostart`, // the directory where the desktop files with auto start configuration lives
  desktopFilePathForAutoLaunch = `${autoStartDir}/${pm.config.get('AppName')}.desktop`; // the path for auto launch desktop file

  /**
   * @description Using the symbolic link as binary path to be consistent across updates
   * @param {String} appFolder The folder of the binary which created this process
   * @returns {String} the binary path of the App
   */
  function getAppBinaryPath (appFolder) {
    return path.resolve(appFolder, '..', pm.config.get('AppName'));
  }

/**
   * @description Gets the contents of the older version of linux desktop file for auto launch
   *   Having this to check, if the contents of the desktop file needs to be modified
   * @param {String} appBinaryPath the binary path of the App
   * @returns {String}
   */
  function getOldDesktopEntry (appFolder) {
    return `[Desktop Entry]
Name=${pm.config.get('AppName')}
Exec=${getAppBinaryPath(appFolder)}
Type=Application
Categories=GNOME;GTK;Network;`;
  }

  /**
   * @description Gets the contents of the linux desktop file for auto launch
   * @param {String} appBinaryPath the binary path of the App
   * @returns {String}
   */
  function getDesktopEntry (appFolder) {
    return `[Desktop Entry]
Name=${pm.config.get('AppName')}
Exec="${getAppBinaryPath(appFolder)}"
Type=Application
Categories=GNOME;GTK;Network;`;
  }

  /**
   * Refresh tray menu item to reflect the changes on auto launch.
   */
  function refreshTrayMenu () {
    // Using inline require to avoid cyclic dependency
    require('../../src/menu').MenuManager.refreshAutoLaunchMenuItem();
  }

/**
 * Class implementing auto launch for Linux
 * @class
 * @implements {AutoLaunch}
 * To auto launch deskop app on OS Login,
 *   1.Create a .desktop file with the executable path and Icon path.
 *   2.Create autostart folder under ~/.config folder if not present.
 *   3.Create a symbolic link to the .desktop file under autostart folder.
 */
class LinuxAutoLaunch extends AutoLaunch {
  constructor () {
    super();
    this._isInitiallyEnabled = false;
  }

  /**
   * Should be called when the app is ready as we try to refresh the tray menu GUI after enabling
   * @override
   */
  initialize () {
    if (this._isDevMode) {
      return;
    }

    // Check if the desktop entry file exists
    fs.readFile(desktopFilePathForAutoLaunch, 'utf8', (err, data) => {
      if (err) {
        this._isInitiallyEnabled = false;
      } else if (data === getOldDesktopEntry(this._appFolder)) {
          // The app does not start, if the executable path contains spaces.
          // For details, https://postmanlabs.atlassian.net/browse/CFDTN-418.
          // We need to modify the desktop entry, if the contents differ only in the quotes.
          // We shall not modify the desktop entry, if the path varies.
          // Update case: As we use symlink, the path remains same just missing the quotes.
          this.enable();
          this._isInitiallyEnabled = true;
      } else {
        // If the contents are same along with the quotes, just show that the auto launch is enabled without modifying the contents.
        this._isInitiallyEnabled = true;
      }

      // Refresh menu item, after initializing the auto launch
      refreshTrayMenu();
    });
  }

  /**
   * Check if the auto launch is set
   * @override
   */
  isEnabled () {
    return this._isInitiallyEnabled;
  }

  /**
   * Auto launch preference in Linux can be modified if the app symlink is available.
   * @param {Callback} cb call back with boolean parameter.
   * @override
   */
  _canModifyAutoLaunch (cb) {
    if (this._isDevMode) {
      pm.logger.info('AutoLaunch: Disabled in developer mode');
      cb(false);
      return;
    }

    const appBinaryPath = getAppBinaryPath(this._appFolder);

    // In case of symlink being deleted. Auto launch uses symlink as symlink path stays the same across updates.
    fs.access(appBinaryPath, fs.constants.F_OK, (err) => {
      if (err) {
        pm.logger.error(`AutoLaunch: Missing ${pm.config.get('AppName')}, checked: `, appBinaryPath);
        cb(false);
        return;
      }

      cb(true);
    });
  }

  /**
   * Enables auto launch by creating a desktop file at auto start directory
   * @override
   */
  enable () {
    this._canModifyAutoLaunch((mutable) => {
      if (!mutable) {
        pm.logger.error('AutoLaunch: Not modifiable.');
        return;
      }
      fs.mkdir(autoStartDir, { recursive: true }, (err) => {
        if (err) {
          pm.logger.error('AutoLaunch: Failed to create autostart directory.', err);
          this._isInitiallyEnabled = false;
          return refreshTrayMenu();
        }

        fs.writeFile(desktopFilePathForAutoLaunch, getDesktopEntry(this._appFolder), 'utf8', (err) => {
          if (err) {
            pm.logger.error('AutoLaunch: Failed to create autostart desktop file.', err);
            this._isInitiallyEnabled = false;
            return refreshTrayMenu();
          }

          this._isInitiallyEnabled = true;
          pm.logger.info('AutoLaunch: Enabled');
          return refreshTrayMenu();
        });
      });
    });
  }

  /**
   * Disables auto launch by removing the desktop file from auto start directory
   * @override
   */
  disable () {
    this._canModifyAutoLaunch((mutable) => {
      if (!mutable) {
        pm.logger.error('AutoLaunch: Not modifiable.');
        return;
      }

      fs.unlink(desktopFilePathForAutoLaunch, (err) => {
        if (err) {
          if (err.code === 'ENOENT') {
            pm.logger.info('AutoLaunch: Already Disabled.');
            this._isInitiallyEnabled = false;
            return refreshTrayMenu();
          }
          pm.logger.error('AutoLaunch: Failed to delete autostart desktop file.', err);
          this._isInitiallyEnabled = true;
          return refreshTrayMenu();
        }

        this._isInitiallyEnabled = false;
        pm.logger.info('AutoLaunch: Disabled');
        return refreshTrayMenu();
      });
    });
  }
}

module.exports = LinuxAutoLaunch;
