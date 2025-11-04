const uuid = require('uuid');

/**
 * Service to handle requests for resolution of an HTTP request from an ID
 *
 * @class RequestResolutionService
 */
class RequestResolutionService {
  constructor (socket) {
    this.resolveRequest = this.resolveRequest.bind(this);

    if (!socket) {
      throw new Error('RequestResolutionService~constructor: Socket not provided');
    }

    this.socket = socket;
  }

  resolveRequest ({ executionInfo, collection }) {
    return (async function (requestId, referencedRequestContext, callback) {
      let eventId = uuid.v4(),
        timeoutId;

      const resolutionRequestEventHandler = ({ name, data }) => {
        if (name === 'request-resolved' && data.eventId === eventId || data.requestId === requestId) {
          if (timeoutId) {
            clearTimeout(timeoutId);
          }

          if (data.error) {
            return callback(new Error(data.error));
          }

          if (data.requestCollection) {
            return callback(null, data.requestCollection);
          }

          pm.logger.error('WSAgent~RequestResolutionService~resolveRequest: No collection JSON or error received post resolution');

          return callback(new Error('No collection JSON or error received post resolution'));
        }
      };

      this.socket.once('request-resolution-ws-event', resolutionRequestEventHandler);

      this.socket && this.socket.emit('request-resolution-ws-event', {
        name: 'resolve-request',
        data: {
          requestId,
          id: eventId,
          executionInfo,
          referencedRequestContext,

          // The collection payload can get very heavy, only sending what we need
          collection: { info: collection.info, item: collection.item.map((requestItem) => ({ id: requestItem.id })) }
        }
      });

      timeoutId = setTimeout(() => {
        callback(new Error('Request resolution timed out'));
        this.socket.off('request-resolution-ws-event', resolutionRequestEventHandler);
      }, 30_000);
    }).bind(this);
  }
}

module.exports = {
  initialize: function (socket) {
    pm.requestResolutionService = new RequestResolutionService(socket);
  }
};
