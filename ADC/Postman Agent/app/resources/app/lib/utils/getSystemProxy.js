var ProxyConfig = require('postman-collection').ProxyConfig,
    CloudProxyManager = require('../services/CloudProxyManager'),
    HTTP_PROTOCOL = 'http',
    HTTPS_PROTOCOL = 'https',
    ALLOWED_PROTOCOLS = [HTTP_PROTOCOL, HTTPS_PROTOCOL],
    ALLOWED_PROTOCOLS_REGEX = ALLOWED_PROTOCOLS.join('|'),
    PROTOCOL_SEPARATOR = '://',
    HTTP_PROTOCOL_SEPARATOR = HTTP_PROTOCOL + PROTOCOL_SEPARATOR,
    HTTPS_PROTOCOL_SEPARATOR = HTTPS_PROTOCOL + PROTOCOL_SEPARATOR;

/**
 *  @param {PostmanUrl} url resolved request url
 *  @param {function} cb callback
 *
 * @returns {undefined}
 */
module.exports = (url, cb) => {
  var session = require('electron').session.defaultSession,
      regexes = {
        // Updated regex to match both PROXY and SOCKS formats
        hostPortMatcher: /(PROXY|SOCKS\d*)\s+(([^:]+):(\d+))/,
        validUrlTester: '^(' + ALLOWED_PROTOCOLS_REGEX + ')://'
      },
      sanitizedUrl = (url.match(regexes.validUrlTester)) ? url : HTTP_PROTOCOL_SEPARATOR + url,
      protocol = sanitizedUrl.split('://')[0],
      match,
      host,
      port,
      proxyProtocol,
      authenticate,
      username,
      password;

  try {
    CloudProxyManager.resolveProxy(sanitizedUrl, (err, value, authInfo) => {
      if (err) {
        cb(err);
      }

      if (value === 'DIRECT') {
        return cb(null, undefined);
      }

      /**
        Electron return: 'DIRECT' || 'PROXY [host]:port;PROXY [host]:port;...' || 'SOCKS [host]:port;SOCKS4 [host]:port;...'
        Using a regex we separate out the proxy protocol, host and port
        Having protocol in host is invalid (Should we strip-out the protocol for the user?)
      */
      // value = 'PROXY [http://0.0.0.0]:8080;DIRECT;PROXY 0.0.0.0:8081' or 'SOCKS5 127.0.0.1:1080'
      match = value.match(regexes.hostPortMatcher);

      if (!match) {
        // System proxy defined has invalid syntax
        pm.logger.warn('getSystemProxy - System proxy defined has invalid syntax');
        return cb(null, undefined);
      }

      proxyProtocol = match[1]; // 'PROXY', 'SOCKS', 'SOCKS4', 'SOCKS5', etc.
      host = match[3];
      port = parseInt(match[4], 10);
      if (authInfo) {
        authenticate = true;
        username = authInfo.username;
        password = authInfo.password;
      }

      const ProxyConfigDefinition = {
        host: host,
        port: port,
        protocols: [protocol],
        authenticate: authenticate,
        username: username,
        password: password
      };

      if (proxyProtocol && proxyProtocol.startsWith('SOCKS')) {
        ProxyConfigDefinition.protocol = proxyProtocol.toLowerCase();
      }

      return cb(null, new ProxyConfig(ProxyConfigDefinition));
    });
  }
  catch (e) {
    return cb(e);
  }
};
