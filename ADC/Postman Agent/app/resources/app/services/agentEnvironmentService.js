const { app } = require('electron'),
  environmentMap = {
    'PostmanAgentBeta': 'beta',
    'PostmanAgentPreview': 'preview',
    'PostmanAgentStage': 'stage',
    'PostmanAgent': 'prod'
  };

module.exports = {
  getEnvironmentInfo () {
    const appName = app.getName();
    return environmentMap[appName] || 'dev';
  }
};
