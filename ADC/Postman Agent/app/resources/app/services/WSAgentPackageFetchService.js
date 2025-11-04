const uuid = require('uuid');

/**
 * Service for handling packages through Websocket Agent
 *
 * @class PackageFetchService
 */
class PackageFetchService {

  constructor (socket) {
    if (!socket) {
      throw new Error('PackageFetchService~constructor: Socket not provided');
    }

    this.socket = socket;
  }

  /**
   * Fetches packages using WebSocket communication.
   *
   * @param {Array} packages - The packages to fetch.
   * @param {Function} callback - The callback function to be called when the fetch is completed or failed.
   */
  fetchPackage (packages, collectionId, callback) {
    let timeoutId;

    const id = uuid.v4(),
      eventHandler = (event) => {
      const { name, data } = event || {};

      if (name === 'package-fetch-failed' && data.id === id) {
        clearTimeout(timeoutId);
        return callback(new Error('Cloud file fetch failed'));
      }

      if (name === 'package-fetch-completed' && data.id === id) {
        clearTimeout(timeoutId);
        return callback(null, data.packages, data.packageErrors);
      }
    };


    this.socket.once('package-ws-event', eventHandler);

    timeoutId = setTimeout(() => {
      callback(new Error('Package fetch timed out'));
      this.socket.off('package-ws-event', eventHandler);
    }, 60000);


    this.socket.emit('package-ws-event', {
      name: 'package-fetch-start',
      data: {
        packages,
        id,
        collectionId
      }
    });
  }
}

module.exports = {
  initialize: function (socket) {
    pm.wsPackageFetchService = new PackageFetchService(socket);
  }
};
