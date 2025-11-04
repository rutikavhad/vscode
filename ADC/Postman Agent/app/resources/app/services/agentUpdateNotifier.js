const agentUpdaterService = require('./agentUpdateService'),
      agentUpdaterConstants = agentUpdaterService.constants,

      AUTO_UPDATE_TIMER = 24 * 3600 * 1000; // 24 hours

module.exports = {

  initialize () {
    setInterval(() => {
      // If update status is already downloaded, downloading or checking don't check for new updates
      var status = agentUpdaterService.getStatus(),
          statusNotAllowed = [
            agentUpdaterConstants.UPDATE_DOWNLOADED,
            agentUpdaterConstants.UPDATE_DOWNLOADING,
            agentUpdaterConstants.UPDATE_CHECKING
          ];

      if (statusNotAllowed.includes(status)) {
        return;
      }

      agentUpdaterService.checkForUpdateAndDownload();
    }, AUTO_UPDATE_TIMER);
  }
};
