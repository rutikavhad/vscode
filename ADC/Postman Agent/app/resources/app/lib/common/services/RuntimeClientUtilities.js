const { promisify } = require('util');
const PostmanFs = require('../utils/postmanFs');
const getSystemProxy = require('../../utils/getSystemProxy');

const PROXY_ENV_LOWER_CASE = {
  http_proxy: process.env.http_proxy,
  https_proxy: process.env.https_proxy,
  no_proxy: process.env.no_proxy
};

const PROXY_ENV_UPPER_CASE = {
  http_proxy: process.env.HTTP_PROXY,
  https_proxy: process.env.HTTPS_PROXY,
  no_proxy: process.env.NO_PROXY
};

const LARGE_TIMEOUT = 1000000000; // 1 billion milliseconds, effectively no timeout

class RuntimeClientUtilities {
  constructor (defaultWorkingDir) {
    this.defaultWorkingDir = defaultWorkingDir;
  }

  async loadFile (path, { cwd, encoding } = { cwd: undefined, encoding: undefined }) {
    const postmanFs = new PostmanFs(cwd || this.defaultWorkingDir);
    const buffer = await promisify(postmanFs.readFile.bind(postmanFs))(path);

    return encoding ? buffer.toString(encoding) : buffer;
  }

  async loadSecureContext (config, options) {
    const [ca, cert, key, pfx] = await Promise.all([
      config.ca ? this.loadFile(config.ca, options) : undefined,
      config.cert ? this.loadFile(config.cert, options) : undefined,
      config.key ? this.loadFile(config.key, options) : undefined,
      config.pfx ? this.loadFile(config.pfx, options) : undefined,
    ]);

    return { ca, cert, key, pfx, passphrase: config.passphrase };
  }

  async loadSystemProxy (url) {
    return new Promise((resolve, reject) => {
      getSystemProxy(url, (error, proxyConfig) => {
        if (error) return reject(error);
        resolve(proxyConfig?.getProxyUrl());
      });
    });
  }

  formatHostname (hostname) {
    return hostname.replace(/^\.*/, '.').toLowerCase();
  }

  parseNoProxyZone (zone) {
    zone = zone.trim().toLowerCase();
    const zoneParts = zone.split(':', 2);
    const zoneHost = this.formatHostname(zoneParts[0]);
    const zonePort = zoneParts[1];
    const hasPort = zone.indexOf(':') > -1;
    return { hostname: zoneHost, port: zonePort, hasPort: hasPort };
  }

  uriInNoProxy (uri, noProxy) {
    const port = uri.port || (uri.protocol === 'https:' ? '443' : '80');
    const hostname = this.formatHostname(uri.hostname);
    const noProxyList = noProxy.split(',');
    return noProxyList.map((zone) => this.parseNoProxyZone(zone)).some((noProxyZone) => {
      const isMatchedAt = hostname.indexOf(noProxyZone.hostname);
      const hostnameMatched = (
        isMatchedAt > -1 && (isMatchedAt === hostname.length - noProxyZone.hostname.length)
      );
      if (noProxyZone.hasPort) {
        return (port === noProxyZone.port) && hostnameMatched;
      }
      return hostnameMatched;
    });
  }

  loadEnvProxy (uri) {
    const noProxy = PROXY_ENV_UPPER_CASE.no_proxy ?? PROXY_ENV_LOWER_CASE.no_proxy ?? '';

    if (noProxy === '*') {
      return null;
    }

    if (noProxy !== '' && this.uriInNoProxy(uri, noProxy)) {
      return null;
    }

    if (uri.protocol === 'http:') {
      return PROXY_ENV_UPPER_CASE.http_proxy ?? PROXY_ENV_LOWER_CASE.http_proxy ?? null;
    }
    if (uri.protocol === 'https:') {
      return PROXY_ENV_UPPER_CASE.https_proxy ?? PROXY_ENV_LOWER_CASE.https_proxy ?? null;
    }
    return null;
  }

  /**
   * Helper function to create timeout options
   * @param {number} timeoutValue - The timeout value from settings
   * @returns {Object} - Timeout configuration object
   */
  createTimeoutOptions (timeoutValue) {
    // If timeout is 0, undefined, or null, use infinite timeout
    if (!timeoutValue || timeoutValue <= 0) {
      pm.logger.info(`MCPClient: Using large timeout (${LARGE_TIMEOUT}ms)`);
      return {
        resetTimeoutOnProgress: true,
        maxTotalTimeout: LARGE_TIMEOUT,
        timeout: LARGE_TIMEOUT
      };
    }

    // Use the configured timeout value
    pm.logger.info(`MCPClient: Using timeout of ${timeoutValue}ms`);
    return {
      resetTimeoutOnProgress: true,
      maxTotalTimeout: timeoutValue,
      timeout: timeoutValue
    };
  }
}

module.exports = RuntimeClientUtilities;
