const { shell, app } = require('electron'),
      trayService = require('../services/trayService'),
      autoLaunch = require('../services/auto-launch'),
      applicationName = `${pm.config.get('AppName')} v${app.getVersion()}`, // The current Application name along with the version
      finder = {
        linux: 'File Manager',
        darwin: 'Finder',
        win32: 'Explorer'
      }; // The platform specific file managers


let MenuManager = {},
    UpdateMenuItems = [
      {
        label: 'Check For Updates',
        click: function () {
          MenuManager.handleMenuAction('CheckForUpdateAndDownload');
        }
      }
    ],
    RuntimeMenuItems = [
      {
        label: 'Starting...',
        enabled: false
      }
    ],

    AutoLaunchMenuItem = {
          label: 'Launch at startup',
          type: 'checkbox',
          click: () => autoLaunch.toggle(),
          checked: autoLaunch.isEnabled(),
          enabled: autoLaunch.canModifyConfig()
    };

MenuManager = {
  getBasicMenu: function () {
    return [
      () => {
        return [
          {
            label: 'Open Postman',
            click () {
              shell.openExternal(`${pm.config.get('BuildURL')}`);
            }
          },
          {
            type: 'separator'
          }
        ];
      },
      this.refreshRuntimeMenuItem,
        () => {
          return [
            {
              type: 'separator'
            }
          ];
        },
        () => {
          return [
            {
              type: 'separator'
            }
          ];
        },
        this.refreshUpdateMenuItem,
        () => {
          return [
            {
              type: 'separator'
            },
            {
              label: 'Support',
              click () {
                shell.openExternal('https://go.pstmn.io/desktop-agent-support');
              }
            },
            {
              label: 'Documentation',
              click () {
                shell.openExternal('https://go.pstmn.io/desktop-agent-docs');
              }
            },
            {
              label: 'Developer',
                submenu: [
                 {
                    label: `View Logs in ${finder[process.platform]}`,
                      click () {
                        shell.openPath(app.logPath).then((errorMessage) => {
                          if (errorMessage) {
                            pm.logger.error(`Menu~handleMenuAction: Failed to open logs folder ${errorMessage}`);
                          }
                        });
                      }
                 }
                ]
            },
            {
              type: 'separator'
            },
            {
              label: 'Settings',
                submenu: [
                  AutoLaunchMenuItem
                ]
            },
            {
              type: 'separator'
            },
            {
              label: applicationName,
              enabled: false
            },
            {
              type: 'separator'
            },
            {
              label: 'Quit',
              role: 'quit',
              accelerator: 'Cmd+Q'
            }
          ];
        }
    ];
  },

  refreshRuntimeMenuItem: function (object) {

    if (Array.isArray(object)) {
      RuntimeMenuItems = object;
    }
    return RuntimeMenuItems;
  },

  refreshUpdateMenuItem: function (object) {
    if (Array.isArray(object)) {
      UpdateMenuItems = object;
    }
    return UpdateMenuItems;
  },

  refreshTrayMenu: function () {
    const prependItems = [];
    this.getBasicMenu().map((item) => {
      prependItems.push(...item());
    });
    trayService.refreshContextMenu(prependItems);
  },

  refreshUpdateStatus (menuItems) {
    this.refreshUpdateMenuItem(menuItems);
    this.refreshTrayMenu();
  },

  refreshRuntimeStatus (menuItems) {
    this.refreshRuntimeMenuItem(menuItems);
    this.refreshTrayMenu();
  },

  refreshAutoLaunchMenuItem () {
    AutoLaunchMenuItem.checked = autoLaunch.isEnabled();
    AutoLaunchMenuItem.enabled = autoLaunch.canModifyConfig();
    this.refreshTrayMenu();
  },

  handleMenuAction: function (action) {
    var agentUpdateService = require('../services/agentUpdateService');

    if (action === 'CheckForUpdateAndDownload') {
      agentUpdateService.checkForUpdateAndDownload();
    }
    else if (action === 'Downloadupdate') {
      agentUpdateService.downloadUpdate();
    }
    else if (action === 'RestartApp') {
      agentUpdateService.restartAndUpdate();
    }
  }
};

exports.MenuManager = MenuManager;
