const platformMap = {
  darwin: require('./MacAutoLaunch'),
  win32: require('./WindowsAutoLaunch'),
  linux: require('./LinuxAutoLaunch')
},
  autoLaunch = new platformMap[process.platform]();

module.exports = autoLaunch;
