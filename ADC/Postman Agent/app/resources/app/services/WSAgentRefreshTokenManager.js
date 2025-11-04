let _ = require('lodash'),
  uuid = require('uuid');

/**
 * Manager for handling refresh token requests through Websocket Agent
 *
 * @class RefreshTokenManager
 */
class RefreshTokenManager {
  refreshCallbackMap = new Map();
  timeout = 30000; // Refresh Token Timeout in MS

  constructor (socket) {
    this.refreshToken = this.refreshToken.bind(this);

    if (!socket) {
      throw new Error('RefreshTokenManager~constructor: Socket not provided');
    }

    this.socket = socket;

    this.socket.on('oauth2', ({ name, namespace, data }) => {
      if (!(namespace === 'oauth2-refresh-token' && name === 'oauth2-token-refreshed')) {
        return;
      }

      const { refreshId } = data,
        refreshCallback = this.refreshCallbackMap.get(refreshId);

      // Bailout if no callback object is found
      if (!refreshCallback) {
        pm.logger.warn('WSAgent~RefreshTokenManager~refreshToken: No callback found for refreshId', refreshId);

        return;
      }

      // clean up the map as this callback object is no longer needed
      this.refreshCallbackMap.delete(refreshId);

      // if we have an error, call the callback with error
      if (data.error) {
        return refreshCallback(new Error(data.error));
      }

      if (data.accessToken) {
        return refreshCallback(null, data.accessToken);
      }

      pm.logger.error('WSAgent~RefreshTokenManager~refreshToken: No Access Token Received');

      return refreshCallback(new Error('No Access Token Received'));
    });
  }

  cancelRefresh (error) {
    // We will lose the error object over the socket, so we will stringify it
    const errorMessage = _.isString(error) ? error : _.get(error, 'message', 'Could not refresh token');

    this.socket && this.socket.emit('oauth2', {
      name: 'oauth2-cancel-refresh-token',
      namespace: 'oauth2-refresh-token',
      data: {
        error: errorMessage
      }
    });
  }

  async refreshToken (authSessionId, callback) {
    const refreshId = uuid.v4();

    this.refreshCallbackMap.set(refreshId, callback);

    this.socket && this.socket.emit('oauth2', {
      name: 'oauth2-refresh-token',
      namespace: 'oauth2-refresh-token',
      data: {
        authSessionId,
        refreshId
      }
    });

    const timeoutPromise = new Promise((resolve, reject) => {
      // We add a timeout to the refresh token promise to ensure that the request is not
      // hung up on the refresh token call. If the refresh token call takes more than
      // timeout, we abandon the refresh token request.
      setTimeout(() => reject(), this.timeout);
    });

    await timeoutPromise.catch(() => {
      const refreshCallback = this.refreshCallbackMap.get(refreshId);

      // Bailout if no callback is found -> this means that the refresh token call was successful
      // and the callback was already called
      if (!refreshCallback) {
        return;
      }

      // clean up the map as this callback is no longer needed
      this.refreshCallbackMap.delete(refreshId);

      this.cancelRefresh(new Error('Timeout while refreshing token'));

      return refreshCallback(new Error('Timeout while refreshing token'));
    });
  }
}

module.exports = {
  initialize: function (socket) {
    pm.refreshTokenManager = new RefreshTokenManager(socket);
  }
};
