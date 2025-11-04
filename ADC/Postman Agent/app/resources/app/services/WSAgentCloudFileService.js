/**
 * Service for handling cloud files through Websocket Agent
 *
 * @class CloudFileService
 */
class CloudFileService {

  constructor (socket) {
    if (!socket) {
      throw new Error('CloudFileService~constructor: Socket not provided');
    }

    this.socket = socket;
  }

  /**
   * Fetches the file from cloud, stores it in local storage and
   * calls the callback with the file path in the local storage.
   * @param {string} path file path in the cloud
   * @param {function} callback
   */
  fetchFile (path, callback) {
    this.socket.once('remote-file-ws-event', (event) => {
      const { name, data } = event || {};

      if (name === 'remote-file-fetch-failed') {
        return callback(new Error('Cloud file fetch failed'));
      }

      if (name === 'remote-file-fetch-completed') {
        return callback(null, data.filePath);
      }
    });

    this.socket.emit('remote-file-ws-event', {
      name: 'remote-file-fetch-start',
      data: {
        filePath: path
      }
    });
  }
}

module.exports = {
  initialize: function (socket) {
    pm.wsCloudFileService = new CloudFileService(socket);
  }
};
