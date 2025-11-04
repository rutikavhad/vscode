const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { SSEClientTransport } = require('@modelcontextprotocol/sdk/client/sse.js');
const { StdioClientTransport, getDefaultEnvironment } = require('@modelcontextprotocol/sdk/client/stdio.js');
const { StreamableHTTPClientTransport } = require('@modelcontextprotocol/sdk/client/streamableHttp.js');
const { createMiddleware, applyMiddlewares } = require('@modelcontextprotocol/sdk/client/middleware.js');
const { Agent, ProxyAgent } = require('undici');
const { authorizeRequest } = require('postman-runtime/lib/authorizer');
const collectionSDK = require('postman-collection');
const _ = require('lodash');
const tls = require('tls');
const stripJSONComments = require('strip-json-comments');
const EventChannel = require('../channels/EventChannel');
const RuntimeClientUtilities = require('./RuntimeClientUtilities');
const { buildRequest, buildResponse, addToHistory, createHistory, getLocationHeader, resolveLocation } = require('../utils/requestLogging');
const { v4: uuidv4 } = require('uuid');

// Use dynamic import for ESM module
let shellEnv;
(async () => {
  const shellEnvModule = await import('shell-env');
  shellEnv = shellEnvModule.shellEnv;
})();
const {
  CancelledNotificationSchema,
  LoggingMessageNotificationSchema,
  ResourceUpdatedNotificationSchema,
  ResourceListChangedNotificationSchema,
  ToolListChangedNotificationSchema,
  PromptListChangedNotificationSchema,
  JSONRPCMessageSchema,
  ElicitRequestSchema,
  CreateMessageRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');


const NOTIFICATION_SCHEMAS = [
  CancelledNotificationSchema,
  LoggingMessageNotificationSchema,
  ResourceUpdatedNotificationSchema,
  ResourceListChangedNotificationSchema,
  ToolListChangedNotificationSchema,
  PromptListChangedNotificationSchema,
];

// Used when timeout is 0 or undefined
const MAX_REDIRECTS = 4;

class MCPClient {
  constructor (cwd) {
    this._PATH = null;
    this.cwd = cwd;
    this.runtimeUtilities = new RuntimeClientUtilities(cwd);
    this.requestIdToClientMap = new Map();
    this.requestIdToAbortControllerMap = new Map();
  }

  // #region Connect

  // TODO: Update jsdoc types
  async connect (request, fresh = true) {
    const eventChannel = new EventChannel();
    const abortController = new AbortController();

    this.requestIdToAbortControllerMap.set(request.requestId, abortController);

    eventChannel.on('cancel', async ({ forceClose = false }) => {
      abortController.abort();

      this.requestIdToAbortControllerMap.delete(request.requestId);

      if (forceClose) {
        emit(eventChannel, 'aborted', {
          message: 'Connection aborted',
        });

        await this.disconnect(request.requestId);
        eventChannel.destroy();
      }
    });

    this.startConnection(request, fresh, eventChannel).then((requestId) => {
      pm.logger.info('MCPClient~connect: Getting tools');
      this.getTools(request.requestId).then(([error, tools]) => {
        if (error) {
          pm.logger.error(`MCPClient~connect: Error getting tools: ${error.message}`);
        } else {
          pm.logger.info('MCPClient~connect: Successfully fetched tools');
          emit(eventChannel, 'get-tools', tools);
        }
      });

      pm.logger.info('MCPClient~connect: Getting resources');
      this.getResources(requestId).then(([error, resources]) => {
        if (error) {
          pm.logger.error(`MCPClient~connect: Error getting resources: ${error.message}`);
        } else {
          pm.logger.info('MCPClient~connect: Successfully fetched resources');
          emit(eventChannel, 'get-resources', resources);
        }
      });

      pm.logger.info('MCPClient~connect: Getting prompts');
      this.getPrompts(requestId).then(([error, prompts]) => {
        if (error) {
          pm.logger.error(`MCPClient~connect: Error getting prompts: ${error.message}`);
        } else {
          pm.logger.info('MCPClient~connect: Successfully fetched prompts');
          emit(eventChannel, 'get-prompts', prompts);
        }
      });

      pm.logger.info('MCPClient~connect: Getting resource templates');
      this.getResourceTemplates(requestId).then(([error, resourceTemplates]) => {
        if (error) {
          pm.logger.error(`MCPClient~connect: Error getting resource templates: ${error.message}`);
        } else {
          pm.logger.info('MCPClient~connect: Successfully fetched resource templates');
          emit(eventChannel, 'get-resource-templates', resourceTemplates);
        }
      });
    }).catch(() => {
      // no-op, error handling is done in startConnection
    });

    return eventChannel;
  }

  async startConnection (request, fresh = true, eventChannel, abortSignal = null) {
    const { requestId, transport: transportFromRequest, settings } = request;
    const { requestTimeout: maxTotalTimeout } = settings ?? {};
    let signal = this.requestIdToAbortControllerMap.get(requestId)?.signal ?? abortSignal;

    if (!signal || signal?.aborted) {
      const abortController = new AbortController();
      this.requestIdToAbortControllerMap.set(requestId, abortController);
      signal = abortController.signal;
    }

    let transport = transportFromRequest === 'sse' ? 'streamableHTTP' : 'stdio';

    const notificationHandler = (notification) => {
      emit(eventChannel, 'received-notification', {
        notification,
      });
    };

    const elicitationRequestHandler = (request, extra) => {
      const clientDetails = this.requestIdToClientMap.get(requestId) || {};
      const { pendingRequests = new Map() } = clientDetails;
      const { signal, requestId: elicitationRequestId } = extra;

      if (!clientDetails.pendingRequests) {
        clientDetails.pendingRequests = pendingRequests;
      }

      // Store the elicitation requestId
      pendingRequests.set(elicitationRequestId, { signal });

      return new Promise((resolve, reject) => {
         signal?.addEventListener('abort', () => {
          pendingRequests.delete(elicitationRequestId);

          // Emitting this so the app is aware of this happening
          emit(eventChannel, 'request-aborted', {
            message: `Elicitation request id: ${elicitationRequestId} was canceled.`,
            elicitationRequestId,
          });
        });

        eventChannel.on('elicitation-response', (event) => {
          const { relatedRequestId, result } = event;

          if (relatedRequestId === elicitationRequestId) {
            pendingRequests.delete(elicitationRequestId);
            resolve(result);
          }
        });

        emit(eventChannel, 'received-data', {
          method: 'elicitation/create',
          data: {
            id: elicitationRequestId,
            ...request,
          },
        });
      });
    };

    const samplingRequestHandler = (request, extra) => {
      const clientDetails = this.requestIdToClientMap.get(requestId) || {};
      const { pendingRequests = new Map() } = clientDetails;
      const { signal, requestId: samplingRequestId } = extra;

      if (!clientDetails.pendingRequests) {
        clientDetails.pendingRequests = pendingRequests;
      }

      // Store the sampling requestId
      pendingRequests.set(samplingRequestId, { signal });

      return new Promise((resolve, reject) => {
         signal?.addEventListener('abort', () => {
          pendingRequests.delete(samplingRequestId);

          // Emitting this so the app is aware of this happening
          emit(eventChannel, 'request-aborted', {
            message: `Sampling request id: ${samplingRequestId} was canceled.`,
            samplingRequestId,
          });
        });

        eventChannel.on('sampling-response', (event) => {
          const { relatedRequestId, result } = event;

          if (relatedRequestId === samplingRequestId) {
            pendingRequests.delete(samplingRequestId);
            resolve(result);
          }
        });

        eventChannel.on('sampling-declined', (event) => {
          const { relatedRequestId } = event;

          if (relatedRequestId === samplingRequestId) {
            pendingRequests.delete(samplingRequestId);
            reject(new Error('Sampling request declined'));
          }
        });

        emit(eventChannel, 'received-data', {
          method: 'sampling/createMessage',
          data: {
            id: samplingRequestId,
            ...request,
          },
        });
      });
    };

    try {
      let client = await this.createOrGetClient(request, fresh);
      let protocolTransport, error;

      if (transport === 'stdio') {
        [error, protocolTransport] = await this.generateStdioTransport(request, eventChannel);
      } else if (transport === 'streamableHTTP') {
        [error, protocolTransport] = await this.generateHTTPTransport(request, eventChannel, transport);
      } else {
        throw new Error(`Unsupported transport: ${transport}`);
      }

      if (error) {
        throw error;
      }

      // Override the default notification handlers to emit events to the event channel
      updateNotificationHandlers(NOTIFICATION_SCHEMAS, client, notificationHandler);
      client.setRequestHandler(ElicitRequestSchema, elicitationRequestHandler);
      client.setRequestHandler(CreateMessageRequestSchema, samplingRequestHandler);

      pm.logger.info(`MCPClient~connect: Connecting to MCP server with transport: ${transport}`);

      try {
        // Connect to the MCP server
        await client.connect(protocolTransport, {
          ...this.runtimeUtilities.createTimeoutOptions(maxTotalTimeout),
          signal,
        });
      } catch (error) {
        // Make sure we close the client before trying to connect again
        await client.close?.();

        const statusCodeRegex = /http\s+401/i;

        if (signal?.aborted) {
          emit(eventChannel, 'aborted', {
            message: 'Connection aborted',
          });
          return;
        }

        if (statusCodeRegex.test(error.message)) {
          error.code = 401;
          throw error;
        }

        if (transport === 'stdio') {
          throw error;
        }

        let err;
        transport = 'sse';

        // If we tried http and it failed, try sse
        if (transport === 'sse') {
          [err, protocolTransport] = await this.generateHTTPTransport(request, eventChannel, transport);
        }

        if (err || transport === 'stdio') {
          throw err;
        }

        pm.logger.info('MCPClient~connect: Attempting to connect to MCP server with transport: sse');
        client = await this.createOrGetClient(request, fresh);

        // Before we try to connect again we attach the notification handlers again
        updateNotificationHandlers(NOTIFICATION_SCHEMAS, client, notificationHandler);
        client.setRequestHandler(ElicitRequestSchema, elicitationRequestHandler);

        await client.connect(protocolTransport, {
          ...this.runtimeUtilities.createTimeoutOptions(maxTotalTimeout),
          signal,
        });
      }

      const serverCapabilities = client.getServerCapabilities();

      emit(eventChannel, 'connected', {
        connectionStatus: 'connected',
        serverCapabilities,
      });

      pm.logger.info(`MCPClient~connect: Connected to MCP server with transport: ${transport}`);

      this.requestIdToClientMap.set(requestId, { client, eventChannel, request });

      eventChannel?.addCleanup(async () => await this.disconnect(requestId));
      return requestId;
    } catch (error) {
      pm.logger.error(`MCPClient~connect: Error connecting to MCP server: ${error.message}`);

      // Remove the client from the requestIdToClientMap
      this.requestIdToClientMap.delete(requestId);

      setImmediate(() => {
        emit(eventChannel, 'error', {
          message: `Error connecting to MCP server: ${error.message}`,
          source: 'connect',
          statusCode: error?.code
        });
        eventChannel?.destroy();
      });

      throw error;
    }
  }

  // TODO: Update this to reflect the two types of requests
  /**
   * Helper function to create a client
   * @param {object} request - Information about the request to connect to the MCP server
   * @param {string} request.url - The URL of the MCP server
   * @param {string} request.requestId - The request ID of the request to connect to the MCP server
   * @param {object} request.auth - The authentication information for the request
   * @param {object} [request.certs] - The certificates for the request
   * @param {object} [request.settings] - Options for the connection
   * @param {boolean} [request.settings.verifySSLCertificates] - Whether to verify the SSL certificates of the MCP server
   * @param {number} [request.settings.requestTimeout] - The timeout for the request
   * @param {number} [request.settings.sessionTimeout] - The timeout for the session
   * @param {object} [request.proxy] - Proxy configuration for the request
   * @param {string} [request.proxy.url] - The URL of the proxy server
   * @param {boolean} request.proxy.system - Whether to use the system proxy
   * @param {boolean} request.proxy.env - Whether to use the environment variables for proxy
   * @param {boolean} [fresh] - whether to create a new client or use an existing one
   * @returns {Promise<Client>}
   */
  async createOrGetClient (request, fresh = false) {
    const { requestId } = request;

    if (this.requestIdToClientMap.has(requestId)) {
      // If we want to create a fresh client, we close and remove the old client
      if (fresh) {
        const { client } = this.requestIdToClientMap.get(requestId);

        client.close && await client.close();

        this.requestIdToClientMap.delete(requestId);
      } else {
        return this.requestIdToClientMap.get(requestId);
      }
    }

    return new Client({
      name: `Postman Client - ${requestId}`,
      version: '1.0.0',
    }, {
        capabilities: {
          elicitation: {},
          sampling: {},
        },
    });
  }

  /**
   * Disconnect from the MCP server
   * @param {string} requestId - The request ID of the request to disconnect from the MCP server
   */
  async disconnect (requestId) {
    const { client, eventChannel } = this.requestIdToClientMap.get(requestId) ?? {};

    // If the client or event channel is not found or destroyed, do nothing
    if (client) {
      await client.close();
    }

    this.requestIdToClientMap.delete(requestId);

    emit(eventChannel, 'disconnected', {
      message: 'Disconnected from MCP server',
    });

    // This is so that any remaining events are emitted before the server disconnects and the eventChannel is closed.
    setTimeout(() => eventChannel?.destroy());
  }

    /**
     * Generate either a streamable HTTP or SSE transport for the MCP Client
     * @param {object} request - Information about the request to connect to the MCP server
     * @param {string} request.url - The URL of the MCP server
     * @param {string} request.requestId - The request ID of the request to connect to the MCP server
     * @param {object} request.auth - The authentication information for the request
     * @param {object} [request.certs] - The certificates for the request
     * @param {object} [request.settings] - Options for the connection
     * @param {boolean} [request.settings.verifySSLCertificates] - Whether to verify the SSL certificates of the MCP server
     * @param {number} [request.settings.requestTimeout] - The timeout for the request
     * @param {number} [request.settings.sessionTimeout] - The timeout for the session
     * @param {object} [request.headers] - The headers for the request
     * @param {object} [request.proxy] - Proxy configuration for the request
     * @param {string} [request.proxy.url] - The URL of the proxy server
     * @param {boolean} [request.proxy.system] - Whether to use the system proxy
     * @param {boolean} [request.proxy.env] - Whether to use the environment variables for proxy
     * @param {EventChannel} eventChannel - The event channel to emit events to
     * @param {string} [transport] - The transport to use, either 'sse' or 'streamableHTTP'
     * @returns {Promise<[Error | null, CustomSSEClientTransport | CustomStreamableHTTPClientTransport | null]>}
   */
   async generateHTTPTransport (request, eventChannel, transport = 'streamableHTTP') {
    const { url, auth, certs, settings = {}, requestId, headers: headersFromRequest = [], proxy: proxyConfig = { url: undefined, system: false, env: false } } = request;

    const validatedURL = validateURL(url, 'http');
    const authHeaders = await getAuthHeaders(url, auth, {});
    const enabledHeaders = headersFromRequest.reduce((acc, header) => {
      if (!header.disabled) {
        acc[header.key] = header.value;
      }

      return acc;
    }, {});
    const headers = { ...authHeaders, ...enabledHeaders };

    let certificates, envProxy, systemProxy, proxy;

    try {
      certificates = certs ? await this.runtimeUtilities.loadSecureContext(certs) : {};
    } catch (error) {
      pm.logger.error(`MCPClient~connectSSE: Unable to load certificates: ${error.message}`);

      return [error, null];
    }


    try {
      envProxy = proxyConfig.env ? this.runtimeUtilities.loadEnvProxy(validatedURL) : undefined;
      systemProxy = proxyConfig.system ? await this.runtimeUtilities.loadSystemProxy(url) : undefined;
      proxy = proxyConfig.url ?? systemProxy ?? envProxy;
    } catch (error) {
      pm.logger.error(`MCPClient~connectSSE: Unable to load proxy configuration: ${error.message}`);

      return [error, null];
    }

    const secureContext = tls.createSecureContext({
      key: certificates.key ?? undefined,
      cert: certificates.cert ?? undefined,
      pfx: certificates.pfx ?? undefined,
      passphrase: certificates.passphrase ?? undefined,
    });

    certificates.ca && secureContext.context.addCACert(certificates.ca);

    const connectOptions = {
      secureContext,
      rejectUnauthorized: Boolean(settings.verifySSLCertificates),
    };

    let streamingAgent, agent;

    if (proxy) {
      streamingAgent = transport === 'sse' ? new ProxyAgent({
        uri: proxy,
        requestTls: connectOptions
      }) : undefined;

      agent = new ProxyAgent({
        uri: proxy,
        requestTls: connectOptions
      });
    } else {
      // If no proxy just use the normal TLS agent
      streamingAgent = transport === 'sse' ? new Agent({
        connect: connectOptions
      }) : undefined;

      agent = new Agent({
        connect: connectOptions
      });
    }

    streamingAgent?.on('disconnect', async () => {
      await this.disconnect(requestId);
    });

    const clientTransport = transport === 'streamableHTTP' ? new CustomStreamableHTTPClientTransport(validatedURL, {
      requestInit: {
        // @ts-ignore
        dispatcher: agent,
        ...(headers && { headers }),
      },
      fetch: applyMiddlewares(loggingMiddleware(eventChannel))(async (url, init) => {
        let response = await fetch(url, init);

        // Only updating transport here. The rest of the redirect logic lives in the logger.
        if (response.status >= 300 && response.status < 400) {
          let location = response.headers.get('Location');

          if (location) {
            if (location.startsWith('/')) {
              location = (url.host ?? url) + location;
            }

            // @ts-expect-error this is a private property but need to do this to update the url if there was a redirect
            clientTransport._url = location;
          }

        }

        return response;
      })
    }, eventChannel) : new CustomSSEClientTransport(validatedURL, {
      eventSourceInit: {
        fetch: applyMiddlewares(streamLoggingMiddleware(eventChannel))((url, init) => fetch(url, {
          ...init,
          headers: {
            ...init.headers,
            ...headers,
            'Accept': 'text/event-stream',
          },

          // @ts-ignore
          dispatcher: streamingAgent,
        }))
      },
      requestInit: {
        // @ts-ignore
        dispatcher: agent,
        ...(headers && { headers }),
      },
      fetch: applyMiddlewares(loggingMiddleware(eventChannel))(fetch),
    }, eventChannel);

    return [undefined, clientTransport];
  }

  /**
   * Generate a Stdio transport for the MCP Client
   * @param {object} request - Information about the request to connect to the MCP server
   * @param {string} request.command - The command to run the MCP server
   * @param {string} request.requestId - The request ID of the request to connect to the MCP server
   * @param {Array<string>} [request.args] - The arguments to pass to the command
   * @param {Array<object>} [request.env] - The environment variables to pass to the command
   * @param {EventChannel} eventChannel - The event channel to emit events to
   * @returns {Promise<[Error, CustomStdioClientTransport]>}
   */
  async generateStdioTransport (request, eventChannel) {
    const { command, args, env: envArray = [] } = request;

    const userEnv = envArray.reduce((acc, { key, value, disabled }) => {
      if (!disabled && (value === null || value !== undefined) && key) {
        acc[key] = value;
      }

      return acc;
    }, {});

    try {
      // This is a hack to fix the PATH
      // Possible reason: https://github.com/postman-eng/postman-app/blob/develop/.circleci/config/orbs/beta-app-cd.yml#L162
      // If we don't have a path or the user hasn't set a path we attempt to read the path from the shell
      // TODO: try to remove this once we have a better solution
    if (!this._PATH && !userEnv.PATH) {
      const shellInfo = await shellEnv();

      this._PATH = process.env.PATH = shellInfo.PATH;
    }

    // TODO: check if the env is set
    const defaultEnv = getDefaultEnvironment();

    const env = { ...defaultEnv, ...userEnv };

    const transport = new CustomStdioClientTransport({ command, args, env }, eventChannel);

      return [undefined, transport];
    } catch (err) {
      pm.logger.error(`MCPClient~generateStdioTransport: Error generating Stdio transport: ${err.message}`);

      return [err, null];
    }
  }

  // #endregion

  /**
   * Helper function to get the client and event channel from the requestId
   * @param {string} requestId
   * @param {string} methodName - Name of caller for logging purposes
   * @returns {Object} - The MCP client
   */
  getClientFromRequestId (requestId, methodName) {
    const { client } = this.requestIdToClientMap.get(requestId) ?? {};

    if (!client) {
      const errorMessage = `No client found for requestId: ${requestId}`;
      pm.logger.error(`MCPClient~${methodName}: ${errorMessage}`);
      throw new Error(errorMessage);
    }

    return client;
  }

  /**
   * Helper function to get request settings from the requestId
   * @param {string} requestId
   * @param {string} methodName - Name of caller for logging purposes
   * @returns {Object} - The request settings
   */
  getRequestSettingsFromRequestId (requestId, methodName) {
    const { request } = this.requestIdToClientMap.get(requestId) ?? {};

    if (!request) {
      const errorMessage = `No request found for requestId: ${requestId}`;
      pm.logger.error(`MCPClient~${methodName}: ${errorMessage}`);
      throw new Error(errorMessage);
    }

    return request.settings || {};
  }

  // #region Tools

  /**
   * Get tools from the MCP server
   * @param {string} requestId
   * @param {object} [params]
   * @param {string} params.cursor
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async getTools (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'getTools');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'getTools');
      const tools = await client.listTools(params, options);

      return [undefined, tools];
    } catch (error) {
      pm.logger.error(`MCPClient~getTools: Unable to get tools: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Call a tool from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {string} params.name
   * @param {object} [params.arguments]
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async callTool (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'callTool');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'callTool');
      const response = await client.callTool(params, undefined, options);

      return [undefined, response];
    } catch (error) {
      pm.logger.error(`MCPClient~callTool: Unable to call tool: ${error.message}`);

      return [error, undefined];
    }
  }

  // #endregion

  // #region Resources

  /**
   * Get resources from the MCP server
   * @param {string} requestId
   * @param {object} [params]
   * @param {string} params.cursor
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async getResources (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'getResources');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
      };
      const client = this.getClientFromRequestId(requestId, 'getResources');
      const resources = await client.listResources(params, options);

      return [undefined, resources];
    } catch (error) {
      pm.logger.error(`MCPClient~getResources: Unable to get resources: ${error.message}`);

      return [error, []];
    }
  }

  /**
   * Get resource templates from the MCP server
   * @param {string} requestId
   * @param {object} [params]
   * @param {string} params.cursor
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async getResourceTemplates (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'getResourceTemplates');
      const options = this.runtimeUtilities.createTimeoutOptions(requestTimeout);
      const client = this.getClientFromRequestId(requestId, 'getResourceTemplates');
      const resourceTemplates = await client.listResourceTemplates(params, options);

      return [undefined, resourceTemplates];
    } catch (error) {
      pm.logger.error(`MCPClient~getResourceTemplates: Unable to get resource templates: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Read a specific resource from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {string} params.uri
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async readResource (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'readResource');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'readResource');
      const resource = await client.readResource(params, options);

      return [undefined, resource];
    } catch (error) {
      pm.logger.error(`MCPClient~readResource: Unable to read resource: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Subscribe to a resource from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {string} params.uri
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async subscribeToResource (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'subscribeToResource');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'subscribeToResource');
      const subscription = await client.subscribeResource(params, options);

      return [undefined, subscription];
    } catch (error) {
      pm.logger.error(`MCPClient~subscribeToResource: Unable to subscribe to resource: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Unsubscribe from a resource from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {string} params.uri
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async unsubscribeFromResource (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'unsubscribeFromResource');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'unsubscribeFromResource');
      const subscription = await client.unsubscribeResource(params, options);

      return [undefined, subscription];
    } catch (error) {
      pm.logger.error(`MCPClient~unsubscribeFromResource: Unable to unsubscribe from resource: ${error.message}`);

      return [error, undefined];
    }
  }

  // #endregion

  // #region Prompts

  /**
   * Get prompts from the MCP server
   * @param {string} requestId
   * @param {object} [params]
   * @param {string} params.cursor
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async getPrompts (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'getPrompts');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'getPrompts');
      const prompts = await client.listPrompts(params, options);

      return [undefined, prompts];
    } catch (error) {
      pm.logger.error(`MCPClient~getPrompts: Unable to get prompts: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Get a specific prompt from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {string} params.name
   * @param {object} [params.arguments]
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async getPrompt (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'getPrompt');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'getPrompt');
      const prompt = await client.getPrompt(params, options);

      return [undefined, prompt];
    } catch (error) {
      pm.logger.error(`MCPClient~getPrompt: Unable to get prompt: ${error.message}`);

      return [error, undefined];
    }
  }

  // #endregion

  // #region Completions & Logging & Ping

  /**
   * Request completion options from the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {object} params.ref
   * @param {object} params.argument
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async requestCompletionOptions (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'requestCompletionOptions');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'requestCompletionOptions');
      const completionOptions = await client.complete(params, options);

      return [undefined, completionOptions];
    } catch (error) {
      pm.logger.error(`MCPClient~requestCompletionOptions: Unable to request completion options: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Enable or adjust logging for the MCP server
   * @param {string} requestId
   * @param {object} params
   * @param {"debug" | "info" | "notice" | "warning" | "error" | "critical" | "alert" | "emergency"} params.level
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async setLoggingLevel (requestId, params, signal) {
    try {
      const { requestTimeout } = this.getRequestSettingsFromRequestId(requestId, 'setLoggingLevel');
      const options = {
        ...this.runtimeUtilities.createTimeoutOptions(requestTimeout),
        signal,
      };
      const client = this.getClientFromRequestId(requestId, 'setLoggingLevel');
      const { level } = params;
      const response = await client.setLoggingLevel(level, options);

      return [undefined, response];
    } catch (error) {
      pm.logger.error(`MCPClient~setLoggingLevel: Unable to set log level: ${error.message}`);

      return [error, undefined];
    }
  }

  /**
   * Ping the MCP server
   * @param {string} requestId
   * @param {AbortSignal} [signal]
   * @returns {Promise<[Error, object]>}
   */
  async ping (requestId, signal) {
    try {
      const client = this.getClientFromRequestId(requestId, 'ping');
      const response = await client.ping({ signal });
      return [undefined, response];
    } catch (error) {
      pm.logger.error(`MCPClient~ping: Unable to ping: ${error.message}`);

      return [error, undefined];
    }
  }

  // #endregion

  /**
   * Get the capabilities of the MCP server
   * @param {string} requestId
   * @returns {Promise<object>}
   */
  async getCapabilities (requestId) {
    const { client, eventChannel } = this.requestIdToClientMap.get(requestId) ?? {};

    if (!client) {
      const errorMessage = `No client found for requestId: ${requestId}`;
      pm.logger.error(`MCPClient~ping: ${errorMessage}`);
      return emit(eventChannel, 'error', {
          message: errorMessage,
        });
    }

    const [[toolsError, tools],
      [resourcesError, resources],
      [resourceTemplatesError, resourceTemplates],
      [promptsError, prompts]
    ] = await Promise.all([
      this.getTools(requestId),
      this.getResources(requestId),
      this.getResourceTemplates(requestId),
      this.getPrompts(requestId),
    ]);

    return {
      tools,
      resources,
      resourceTemplates,
      prompts,
      errors: {
        ...(toolsError ? { tools: toolsError } : {}),
        ...(resourcesError ? { resources: resourcesError } : {}),
        ...(resourceTemplatesError ? { resourceTemplates: resourceTemplatesError } : {}),
        ...(promptsError ? { prompts: promptsError } : {}),
      },
    };
  }

  // TODO: Update jsdoc types
  /**
   * Handle a message from the client to send to the MCP server
   * @param {object} payload
   * @param {string} payload.requestId
   * @param {string | object} payload.message
   * @returns {Promise<void | object>}
   */
  async sendMessage ({ requestId, message }) {
    let { eventChannel } = this.requestIdToClientMap.get(requestId);
    let signal = this.requestIdToAbortControllerMap.get(requestId)?.signal;


    if (!eventChannel || eventChannel?.isDestroyed()) {
      const message = `No client or channel found for requestId: ${requestId}`;
      pm.logger.error(message);

      // Error handled in the connect method
      return eventChannel && !eventChannel?.isDestroyed() ? emit(eventChannel, 'error', {
        payload: {
          message,
          source: 'message'
        },
      }) : {
        type: 'error',
        timestamp: new Date().toISOString(),
        payload: {
          message,
          source: 'message'
        },
      };
    }

    if (signal?.aborted) {
      const abortController = new AbortController();
      this.requestIdToAbortControllerMap.set(requestId, abortController);
      signal = abortController.signal;
    }

    let parsedMessage;

    try {
      if (typeof message === 'string' && message.length > 0) {
        parsedMessage = JSON.parse(stripJSONComments(message));
      } else {
        parsedMessage = JSON.parse(stripJSONComments(JSON.stringify(message))) ?? {};
      }
    } catch (error) {
      return emit(eventChannel, 'error', {
        message: `Error parsing message: ${error.message}`,
        source: 'message'
      });
    }

    const { method, params } = parsedMessage ?? {};

    if (!method) {
      return emit(eventChannel, 'error', {
        message: `Invalid message: ${message}`,
        source: 'message'
      });
    }

    let error, response, toolName;
    const startTime = performance.now();

    switch (method) {
      // This is a custom method for refreshing all capabilities
      case 'capabilities/refresh':
        response = await this.getCapabilities(requestId);

        break;

      // Tools related methods
      case 'tools/list':
        [error, response] = await this.getTools(requestId, params, signal);

        break;

      case 'tools/call':
        [error, response] = await this.callTool(requestId, params, signal);

        if (response) {
          toolName = params.name;
        }

        break;

      // Resource related methods
      case 'resources/list':
        [error, response] = await this.getResources(requestId, params, signal);

        break;

      case 'resources/templates/list':
        [error, response] = await this.getResourceTemplates(requestId, params, signal);

        break;

      case 'resources/read':
        [error, response] = await this.readResource(requestId, params, signal);

        break;

      case 'resources/subscribe':
        [error, response] = await this.subscribeToResource(requestId, params, signal);

        break;

      case 'resources/unsubscribe':
        [error, response] = await this.unsubscribeFromResource(requestId, params, signal);

        break;

      // Prompt related methods
      case 'prompts/list':
        [error, response] = await this.getPrompts(requestId, params, signal);

        break;

      case 'prompts/get':
        [error, response] = await this.getPrompt(requestId, params, signal);

        break;

      // Completion, logging, and ping related methods
      case 'completions/complete':
        [error, response] = await this.requestCompletionOptions(requestId, params, signal);

        break;

      case 'logging/setLevel':
        [error, response] = await this.setLoggingLevel(requestId, params, signal);

        break;

      case 'ping':
        [error, response] = await this.ping(requestId, signal);

        break;

      default:
        emit(eventChannel, 'error', {
          source: 'message',
          message: `Invalid method: ${method}`,
        });

        return;
    }

    const endTime = performance.now();
    const responseTime = endTime - startTime;

    error ? emit(eventChannel, 'error', {
      message: `Error calling method: ${method}. Error: ${error.message}`,
      source: 'message'
    }) : emit(eventChannel, 'received-data', {
      method,
      data: response,
      responseTime,
      ...(toolName && { toolName }),
    });
  }
}

// @ts-ignore
class CustomStdioClientTransport extends StdioClientTransport {
  constructor (server, eventChannel) {
    const serverParams = { ...server, stderr: 'pipe' };
    super(serverParams);
    this.eventChannel = eventChannel;
    this._readBuffer = new ReadBuffer(eventChannel);
    this._errorReadBuffer = new ErrorReadBuffer(eventChannel);
  }

  async close () {
    pm.logger.info('CustomStdioClientTransport~close: closing stdio process');

    // @ts-ignore process is a private property
    this._process.kill('SIGKILL');
    await super.close();
  }

  send (message) {
    emit(this.eventChannel, 'sent-data', {
      method: message.method ?? 'unknown',
      data: message,
    });

    return super.send(message);
  }

  async start () {
    await super.start();

    // @ts-expect-error process is a private property
    this._process.stderr?.on('data', (chunk) => {
      this._errorReadBuffer.readMessage(chunk);
    });
  }
}

class CustomStreamableHTTPClientTransport extends StreamableHTTPClientTransport {
  constructor (url, opts, eventChannel) {
    super(url, opts);
    this.eventChannel = eventChannel;
  }

  send (message, options) {
    emit(this.eventChannel, 'sent-data', {
      method: message.method ?? 'unknown',
      data: message,
    });

    return super.send(message, options);
  }
}

class CustomSSEClientTransport extends SSEClientTransport {
  constructor (url, opts, eventChannel) {
    super(url, opts);
    this.eventChannel = eventChannel;
  }

  send (message) {
    emit(this.eventChannel, 'sent-data', {
      method: message.method ?? 'unknown',
      data: message,
    });

    return super.send(message);
  }
}

/**
 * Validate a URL for an MCP server and add the protocol if it is not present
 * @param {string} url - The URL to validate
 * @param {string} transport - The transport to use HTTP or WS (one day)
 */
function validateURL (url, transport) {
  const protocol = transport === 'http' ? 'http:' : 'ws:';

  if (!(/^[a-z0-9+.-]+:\/\//i).test(url)) {
    url = protocol + '//' + url;
  }

  let parsedURL;
  try {
    parsedURL = new URL(url);
  } catch (_) {
    const error = new Error(`Invalid URL: ${url}`);

    // Use property assignment that works with TypeScript
    Object.defineProperty(error, 'code', {
      value: 'ERR_INVALID_URL',
      enumerable: true
    });

    throw error;
  }

  return parsedURL;
}

/**
 * This returns an event to the given channel, using the format expected by Scribe.
 */
function emit (channel, eventName, payload) {
  if (!channel || channel.isDestroyed()) return;

  channel.emit(eventName, {
    type: eventName,
    timestamp: new Date().toISOString(),
    payload,
  });
}

const supportedAuthTypes = new Set([
  'noauth',
  'basic',
  'bearer',
  'oauth2',
]);

/**
 * Return auth headers based on the auth extension provided by the user.
 *
 * @param {string} url - The URL for the request
 * @param {Object} auth - JSON representation of collectionSDK.RequestAuth
 * @param {Object} params - Request parameters
 * @returns {Promise<Object>}
 */
async function getAuthHeaders (url, auth, params) {
  if (!auth) {
    return null;
  }

  if (!auth.type || (!auth[auth.type] && auth.type !== 'noauth')) {
    throw new Error('Invalid auth format');
  }

  if (!supportedAuthTypes.has(auth.type)) {
    throw new Error(`Unsupported authorization type: ${auth.type}`);
  }

  return new Promise((resolve, reject) => {
    const request = new collectionSDK.Request({
      url: url,
      auth,
      method: 'POST',
      body: {
        mode: 'raw',
        raw: JSON.stringify(params)
      }
    });

    authorizeRequest(request, (err, result) => {
      if (err) {
        reject(err);
      } else {
        resolve(
          _.fromPairs(result.headers.toJSON().map((x) => [x.key, x.value]))
        );
      }
    });
  });
}

/**
 * For an array of notification schemas update the handlers for a given client with a given callback
 * @param {Array} schemas - The schemas to update
 * @param {Object} client - The client to update
 * @param {Function} callback - The callback to use for the handlers
 * @returns {void}
 */
function updateNotificationHandlers (schemas, client, callback) {
  schemas.forEach((schema) => {
    client.setNotificationHandler(schema, callback);
  });
}

class BaseReadBuffer {
  constructor (eventChannel) {
    this.eventChannel = eventChannel;
  }

  append (chunk) {
    this._buffer = this._buffer ? Buffer.concat([this._buffer, chunk]) : chunk;
  }

  clear () {
    this._buffer = undefined;
  }

  readMessage (chunk) {
    /**
     * Implemented by subclasses
     */
  }
}

class ReadBuffer extends BaseReadBuffer {
  _buffer;

  readMessage () {
    if (!this._buffer) {
      return null;
    }

    const index = this._buffer.indexOf('\n');
    if (index === -1) {
      return null;
    }

    let line, jsonRPCMessage;
    try {
      line = this._buffer.toString('utf8', 0, index).replace(/\r$/, '');
      this._buffer = this._buffer.subarray(index + 1);

      jsonRPCMessage = deserializeMessage(line);

      return jsonRPCMessage;
    } catch {
      emit(this.eventChannel, 'logs', {
        data: line,
        level: 'info'
      });
    }
  }
}

class ErrorReadBuffer extends BaseReadBuffer {

  readMessage (chunk) {
    if (!chunk) {
      return null;
    }

    const line = chunk.toString('utf8',).replace(/\r$/, '');

    emit(this.eventChannel, 'logs', {
      data: line.trim(),
      level: 'error'
    });
    return line;
  }
}

/**
 * Deserialize a message from a string
 * @param {string} line - The line to deserialize
 * @returns {Object}
 */
function deserializeMessage (line) {
  return JSONRPCMessageSchema.parse(JSON.parse(line));
}

const loggingMiddleware = (eventChannel) => createMiddleware(async (next, input, init) => {
  const id = uuidv4();
  const history = createHistory(id);
  let request = buildRequest(init, input.href ?? input);
  let start = performance.now();
  let originalResponse = await next(input, { ...init, redirect: 'manual' });
  let end = performance.now();
  let redirectCount = 0;

  // Handle redirects
  while (originalResponse.status >= 300 && originalResponse.status < 400 && redirectCount < MAX_REDIRECTS) {
    const location = getLocationHeader(originalResponse.headers);
    if (!location) break;

    // Log the redirect response
    const response = originalResponse.clone();
    addToHistory(history, request, buildResponse(response, undefined), id);

    // Prepare for next request
    const resolvedLocation = resolveLocation(location, input);
    request = buildRequest(init, resolvedLocation);
    start = performance.now();
    originalResponse = await next(new URL(location), { ...init, redirect: 'manual' });
    end = performance.now();
    redirectCount++;
  }

  // Handle final response
  const response = originalResponse.clone();
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();

  reader.read().then(({ value }) => {
    const finalResponse = buildResponse(response, end - start, value);
    addToHistory(history, request, finalResponse, id);
    emit(eventChannel, 'http:request', { request, response: finalResponse, history });
  }).catch((err) => {
    // Ignore AbortError. This is expected because the sdk closes the client using an AbortSignal instead of closing the connection.
    if (err?.name !== 'AbortError') {
      pm.logger.error(`MCPClient~loggingMiddleware: had an error while reading the response: ${err}`);
    }
  });

  return originalResponse;
});


const streamLoggingMiddleware = (eventChannel) => createMiddleware(async (next, input, init) => {
  const start = performance.now();
  const originalResponse = await next(input, init);
  const { signal } = init;

  // Assuming method is POST if it is undefined. This is only the case when using the SSE transport.
  const request = buildRequest({ ...init, method: 'POST' }, input.href);
  const response = originalResponse.clone();
  const reader = response.body.pipeThrough(new TextDecoderStream(), { signal }).getReader();

  let body = '';
  const readStream = async () => {
    if (!reader) return;

    try {
      while (!signal?.aborted) {
        const { value, done } = await reader.read();

        if (value) {
          body += value;
        }

        if (done) {
          break;
        }
      }
    } catch (error) {
      // An abort error is thrown when the client is closed.
      // We emit the event here assuming the connection is closed.
      if (error.name === 'AbortError') {
        const end = performance.now();
        const finalResponse = buildResponse(response, end - start, body);

        const id = uuidv4();
        const history = createHistory(id);
        addToHistory(history, request, finalResponse, id);

        emit(eventChannel, 'http:request', { request, response: finalResponse, history });
      }
    } finally {
      reader.releaseLock();
    }
  };

  readStream().catch(() => {
    // no-op
  });

  return originalResponse;
});

module.exports = MCPClient;
