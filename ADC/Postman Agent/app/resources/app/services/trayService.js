const { app, Tray, Menu: { buildFromTemplate } } = require('electron'),
      path = require('path'),
      agentEnvironmentService = require('./agentEnvironmentService'),
      iconMapItem = {
        linux_beta: 'postmanlogo-head-blue-beta-linux',

        // TODO: Preview Replace with preview environment icon
        linux_preview: 'postmanlogo-head-blue-beta-linux',
        linux_stage: 'postmanlogo-head-blue-stage-linux',
        linux_prod: 'postmanlogo-head-blue-prod-linux',
        linux_dev: 'postmanlogo-head-blue-beta-linux',
        win32_beta: 'postmanlogo-head-blue-beta-windows',

        // TODO: Preview Replace with preview environment icon
        win32_preview: 'postmanlogo-head-blue-beta-windows',
        win32_stage: 'postmanlogo-head-blue-stage-windows',
        win32_prod: 'postmanlogo-head-blue-prod-windows',
        win32_dev: 'postmanlogo-head-blue-beta-windows',
        darwin_beta: 'postmanlogo-head-blackTemplate',
        darwin_preview: 'postmanlogo-head-blackTemplate',
        darwin_stage: 'postmanlogo-head-blackTemplate',
        darwin_prod: 'postmanlogo-head-blackTemplate',
        darwin_dev: 'postmanlogo-head-blackTemplate'
      };

let tray;

module.exports = {

  setTrayIcon () {
    const iconName = this.getIcon();
        tray = new Tray(path.join(__dirname, '..', 'assets', 'images', `${iconName}.png`));

    // taking name from config file it will have space in app name
    tray.setToolTip(pm.config.get('AppName'));
  },

  getIcon () {
    const environmentName = agentEnvironmentService.getEnvironmentInfo(),
     iconName = iconMapItem[process.platform + '_' + environmentName];

    return iconName;
  },

  refreshContextMenu (prependItems) {
    tray.setContextMenu(buildFromTemplate(prependItems));
  }
};
