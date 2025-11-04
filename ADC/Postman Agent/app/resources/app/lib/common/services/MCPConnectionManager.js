const { v4: uuidv4 } = require('uuid');
const MCPClient = require('./MCPClient');

const HEARTBEAT_INTERVAL = 60000; // 60 seconds;

/**
 * @typedef {object} MCPConnection
 * @property {string} id - The id of the connection.
 * @property {string} origin - Tab ID or other identifier (agent-mode) for the connection.
 * @property {MCPRequest} mcpRequest - The MCPRequest object used for the connection.
 * @property {boolean} connected - Whether the connection is connected to the MCP server.
 * @property {string} authStatus
 * @property {Map<string, ToolEntry>} tools - A map of tool entries available for this connection.
 */

/**
 * @typedef {object} Tool
 * @property {string} name - The name of the tool.
 * @property {string} [description] - The description of the tool.
 * @property {object} inputSchema - The input schema for the tool.
 * @property {'object'} inputSchema.type
 * @property {object} [inputSchema.properties] - The expected parameters for the tool
 * @property {object} [inputSchema.required] - The required parameters for the tool
 */

/**
 * @typedef {object} ToolEntry
 * @property {Tool} tool - The tool object.
 * @property {string} id - UUID of the tool entry
 * @property {string} origin - The origin of the tool, e.g., tab ID or agent mode.
 * @property {string} serverId - The id of the server the tool is registered on
 * @property {boolean} enabled - Whether the tool is enabled or not.
 */

/**
 * @typedef {object} KeyValuePair
 * @property {string} key - The key of the key-value pair.
 * @property {string} value - The value of the key-value pair.
 * @property {boolean} disabled - Whether the key-value pair is disabled or not.
 */

/**
 * @typedef {object} MCPRequestHTTP
 * @property {string} serverName
 * @property {'sse'} transport - The transport type for the MCP request, e.g., 'sse'.
 * @property {string} url - The URL of the MCP server.
 * @property {KeyValuePair[]} headers - An array of key-value pairs representing the headers for the request.
 * @property {object} [settings] - Additional settings for the MCP request, such as timeout.
 * @property {number} [settings.requestTimeout=10000] - The timeout for the request
 * @param {string} [proxy.url] - The URL of the proxy server
 * @param {boolean} proxy.system - Whether to use the system proxy
 * @param {boolean} proxy.env - Whether to use the environment variables for proxy
 */

/**
 * @typedef {object} MCPRequestStdio
 * @property {string} serverName
 * @property {'stdio'} transport - The transport type for the MCP request, e.g., 'stdio'.
 * @property {string} command - The command to execute for the MCP request.
 * @property {string[]} args - An array of arguments to pass to the command.
 * @property {KeyValuePair[]} env - An array of key-value pairs representing the environment variables for the MCP request.
 */

/**
 * @typedef {MCPRequestHTTP | MCPRequestStdio} MCPRequest
 */

class MCPConnectionManager {
  constructor (cwd) {
    /**
     * @type {Map<string, MCPConnection>} ConnectionRegistry
     */
    this.connections = new Map();

    /**
     * A centralized, in-memory cache of all available tools across all connections, mapping
     * a unique `toolId` to its `ToolEntry` object.
     *
     * This registry serves as the single source of truth for all registered tools. It is more
     * performant than dynamically aggregating tools from the `connections` map on-demand, as
     * that would require iterating over all connections and their respective tool sets repeatedly.
     * By maintaining this separate registry, looking up, enabling, or disabling a tool becomes a
     * simple and efficient map operation.
     *
     * @type {Map<string, ToolEntry>}
     */
    this.toolRegistry = new Map();

    this.mcpClient = new MCPClient(cwd);

    /**
     * @type {Map<string, AbortController>} abortControllerMap
     * This map is used to store AbortControllers for each connection.
     * It allows us to cancel ongoing requests or operations for a specific connection.
     */
    this.abortControllerMap = new Map();

    /**
     * @type {Map<string, NodeJS.Timeout>}
     * This map is used to store timeouts for each connection's heartbeats
     */
    this.heartbeatMap = new Map();
  }

  /**
   * Adds a connection to the manager. Returns an id to the consumer for invoking the connection.
   * @param {MCPRequest} mcpRequest - The MCPRequest object to be used for the connection.
   * @param {string} origin - The origin of the connection, e.g., tab ID or agent mode.
   * @param {object} options - The connection options.
   * @param {string} [options.id] - The id of the connection. If not provided, a new id will be generated.
   * @param {boolean} [options.autoConnect=true] - Whether to automatically connect the connection after adding it.
   * @param {boolean} [options.getToolsOnConnect=true] - Whether to fetch the tools list after connecting.
   * @returns {Promise<string>} - The id of the connection.
   */
  async addConnection (mcpRequest, origin, options = { autoConnect: true, getToolsOnConnect: true }) {
    const { autoConnect = true, getToolsOnConnect = true, id: providedId } = options;
    const id = providedId ?? uuidv4();
    const abortController = new AbortController();

    const connection = { id, mcpRequest, connected: false, tools: new Map(), origin, authStatus: undefined };

    this.connections.set(id, connection);
    this.abortControllerMap.set(id, abortController);

    if (autoConnect) {
      try {
        const isConnected = await this.connect(id);

        if (isConnected && getToolsOnConnect) {
          // Fetch tools before marking connection as successful
          await this.fetchToolsForServer(id);
          pm.logger.info(`MCPConnectionManager~addConnection: Connection ${id} established with tools registered`);
        } else if (isConnected) {
          pm.logger.info(`MCPConnectionManager~addConnection: Connection ${id} established without tools`);
        }
      } catch (error) {
        pm.logger.error('MCPConnectionManager~addConnection: Error when connecting and fetching tools', error);
        connection.connected = false;
      }
    }

    return id;
  }

  /**
   * Connects to the MCP server for the given connection.
   * @param {string} id - The id of the connection to connect.
   * @return {Promise<boolean>} - Returns true if the connection was established successfully, false otherwise.
   * @throws {Error} - Throws an error if the connection with the given id is not found or connection fails.
   */
  async connect (id) {
    const connection = this.connections.get(id);

    if (!connection) {
      throw new Error(`Connection with id ${id} not found`);
    }

    pm.logger.info(`MCPConnectionManager~connect: Connecting to server ${id}`);

    const request = { ...connection.mcpRequest, requestId: id };
    const signal = this._getOrCreateAbortSignal(id);
    let connected = false;

    try {
      connected = await this.mcpClient.startConnection(request, false, null, signal);

      // If the connection was successful and the authStatus previously was needs_auth we update it.
      // If there was no authStatus we set the status to no_auth
      if (connection.authStatus === 'needs_auth') {
        connection.authStatus = 'auth_success';
      } else if (!connection.authStatus) {
        connection.authStatus = 'no_auth';
      }
    } catch (error) {
      if (error.code === 401) {
        connection.authStatus = 'needs_auth';
      } else {
        throw error;
      }
    }

    if (connected) {
      connection.connected = true;
      this.connections.set(id, connection);
      this.initializeHeartbeat(id);
      pm.logger.info(`MCPConnectionManager~connect: Successfully connected to server ${id}`);
    } else {
      pm.logger.error(`MCPConnectionManager~connect: Failed to connect to server ${id}`);
    }

    return Boolean(connected);
  }

  /**
   * Add multiple connections to the manager.
   * @param {MCPRequest[]} mcpRequests - An array of MCPRequest objects to be used for the connections.
   * @param {string} origin - The origin of the connections, e.g., tab ID or agent mode.
   * @param {object} options - The connection options.
   * @param {boolean} [options.autoConnect=true] - Whether to automatically connect the connections after adding them.
   * @param {boolean} [options.getToolsOnConnect=true] - Whether to fetch the tools list after connecting.
   * @returns {Promise<Array<string | boolean>>} - An array of ids for the successful connections and error messages or false if the connection failed.
   */
  async addConnections (mcpRequests, origin, options = {}) {
    const results = [];
    const promises = mcpRequests.map((mcpRequest) => {
      try {
        const id = this.addConnection(mcpRequest, origin, options);
        results.push(id);
      } catch (error) {
        results.push(error.message || false);
      }
    });

    await Promise.all(promises);
    return results;
  }

  /**
   * Removes a connection from the manager and disconnects from the MCP server.
   * @param {string} id - The id of the connection to remove.
   * @return {Promise<boolean>} - Returns true if the connection was removed and disconnected successfully, false otherwise.
   */
  async removeConnection (id) {
    const connection = this.connections.get(id);
    if (connection) {
      await this.mcpClient.disconnect(id);
      connection.tools.forEach((tool) => {
        this.toolRegistry.delete(tool.id);
      });
    }
    this.clearConnection(id);

    return true;
  }

  /**
   * Disconnects an MCP server connection by its id.
   * @param {string} id - The id of the connection to disconnect.
   * @return {Promise<boolean>} - Returns true if the connection was disconnected successfully, false otherwise.
   * @throws {Error} - Throws an error if the connection with the given id
   */
  async disconnect (id) {
    const connection = this.connections.get(id);
    if (!connection) {
      throw new Error(`Connection with id ${id} not found`);
    }
    if (!connection.connected) {
      pm.logger.warn(`MCPConnectionManager~disconnect: Connection with id ${id} is not connected`);
      return true; // Return true if already disconnected
    }

    pm.logger.info(`MCPConnectionManager~disconnect: Disconnecting server ${id}`);

    await this.mcpClient.disconnect(id);

    connection.connected = false;
    this.connections.set(id, connection);

    // Clean up heartbeats and abort controllers even when not removing the connection
    const heartbeatTimeout = this.heartbeatMap.get(id);
    if (heartbeatTimeout) {
      clearTimeout(heartbeatTimeout);
      this.heartbeatMap.delete(id);
      pm.logger.info(`MCPConnectionManager~disconnect: Cleared heartbeat for server ${id}`);
    }

    // Clear abort controller to prevent issues with reconnection
    if (this.abortControllerMap.has(id)) {
      this.abortControllerMap.delete(id);
      pm.logger.info(`MCPConnectionManager~disconnect: Cleared abort controller for server ${id}`);
    }

    pm.logger.info(`MCPConnectionManager~disconnect: Successfully disconnected server ${id}`);
    return true;
  }

  /**
   * Heartbeat to check if the connection is still alive.
   * @param {string} id - The id of the connection to check.
   * @return {Promise<boolean>} - Returns true if the connection is still alive, false otherwise.
   */
  async _heartbeat (id) {
    const connection = this.connections.get(id);
    if (!connection || !connection.connected) {
      pm.logger.warn(`MCPConnectionManager~_heartbeat: No active connection found for id ${id}`);
      return false;
    }

    const [error, result] = await this.mcpClient.ping(id);

    if (error || !result) {
      pm.logger.warn(`MCPConnectionManager~_heartbeat: Error during heartbeat for connection ${id}`, error);
      return false;
    }

    return true;
  }

  /**
   * Initializes the heartbeat for the connection and schedules the next heartbeat.
   * @param {string} id - The id of the connection to initialize the heartbeat for
   * @returns {NodeJS.Timeout} - Returns the timeout object for the heartbeat.
   */
  initializeHeartbeat (id) {
    const connection = this.connections.get(id);
    if (!connection) {
      pm.logger.error(`MCPConnectionManager~initializeHeartbeat: No connection found for id ${id}`);
      return null;
    }

    // Clear any existing heartbeat timeout
    if (this.heartbeatMap.has(id)) {
      clearTimeout(this.heartbeatMap.get(id));
    }

    // Schedule the next heartbeat
    const heartbeatTimeout = setTimeout(() => {
      this._heartbeat(id)
        .then((isAlive) => {
          if (!isAlive) {
            pm.logger.warn(`MCPConnectionManager~initializeHeartbeat: Heartbeat failed for connection ${id}, attempting to reconnect`);

            connection.connected = false;
            this.connections.set(id, connection);

            // Attempt to reconnect if the heartbeat failed
            // This will also clear the heartbeat timeout for this connection
            // and schedule a new one if the reconnection is successful
            clearTimeout(heartbeatTimeout);
            this.reconnect(id);
          } else {
            this.initializeHeartbeat(id); // Schedule the next heartbeat
          }
        })
        .catch((error) => {
          pm.logger.error(`MCPConnectionManager~initializeHeartbeat: Error during heartbeat for connection ${id}`, error);
        });
    }, HEARTBEAT_INTERVAL);

    this.heartbeatMap.set(id, heartbeatTimeout);
    return heartbeatTimeout;
  }

  /**
   * Reconnects to the MCP server for the given connection.
   * @param {string} id - The id of the connection to reconnect.
   * @param {object} [options] - The options for the reconnection.
   * @param {number} [options.retryCount=3] - The number of times to retry the reconnection.
   * @return {Promise<boolean>} - Returns true if the connection was reconnected successfully,
   */
  async reconnect (id, options = {}) {
    const connection = this.connections.get(id);
    if (!connection) {
      pm.logger.warn(`MCPConnectionManager~reconnect: No connection found for id ${id}`);
    }

    const { retryCount = 3 } = options;

    // Attempt to reconnect
    for (let attempt = 0; attempt < retryCount; attempt++) {
      try {
        pm.logger.info(`MCPConnectionManager~reconnect: Attempt ${attempt + 1} to reconnect to connection ${id}`);
        const connected = await this.connect(id);
        if (connected) {
          pm.logger.info(`MCPConnectionManager~reconnect: Successfully reconnected to connection ${id}`);
          connection.connected = true;
          this.connections.set(id, connection);
          this.initializeHeartbeat(id); // Reinitialize heartbeat after successful reconnection
          return true;
        }
      } catch (error) {
        pm.logger.error(`MCPConnectionManager~reconnect: Error reconnecting to connection ${id}`, error);
      }
    }

    // If we reach here, it means all attempts failed
    return false;
  }

  getConnection (id) {
    return this.connections.get(id);
  }

  hasConnection (id) {
    return this.connections.has(id);
  }

  clearConnection (id) {
    const connection = this.connections.get(id);
    if (connection) {
      connection.tools.forEach((toolEntry) => this.toolRegistry.delete(toolEntry.id));
    }

    this.connections.delete(id);
    this.abortControllerMap.delete(id);
    const heartbeatTimeout = this.heartbeatMap.get(id);
    if (heartbeatTimeout) {
      clearTimeout(heartbeatTimeout);
      this.heartbeatMap.delete(id);
    }
  }

  clearAllConnections () {
    this.connections.clear();
    this.toolRegistry.clear();
    this.abortControllerMap.clear();
    this.heartbeatMap.forEach((timeout) => clearTimeout(timeout));
    this.heartbeatMap.clear();
    pm.logger.info('MCPConnectionManager~clearAllConnections: Cleared all connections and abort');
  }

  /**
   * Calls a tool with the given arguments.
   * @param {string} toolId - The id of the tool to call.
   * @param {object} args - The arguments to pass to the tool.
   * @return {Promise} - A promise that resolves with the tool result.
   */
  async callTool (toolId, args) {
    const toolEntry = this.toolRegistry.get(toolId);
    if (!toolEntry || !toolEntry.enabled) {
      pm.logger.error(`MCPConnectionManager~callTool: Tool with id ${toolId} is not enabled`);
      throw new Error(`Tool with id ${toolId} is not enabled`);
    }

    const params = {
      name: toolEntry.tool.name,
      arguments: args,
    };

    const signal = this._getOrCreateAbortSignal(toolEntry.serverId);

    const [error, result] = await this.mcpClient.callTool(toolEntry.serverId, params, signal);

    if (error) {
      pm.logger.error(`MCPConnectionManager~callTool: Error calling tool with id ${toolId}`, error);
      throw new Error(`Error calling tool with id ${toolId}: ${error.message}`);
    }

    return result;
  }

  /**
   * Fetches the tools available for the given connection.
   * @param {string} id;
   * @return {Promise<object>} - A promise that resolves with the tools available for the connection. Or an MCP error
   */
  async fetchToolsForServer (id) {
    if (!this.hasConnection(id)) {
      pm.logger.error(`MCPConnectionManager~fetchToolsForServer: No connection found for id ${id}`);
      return Promise.reject(new Error(`No connection found for id ${id}`));
    }

    const connection = this.getConnection(id);
    if (!connection.connected) {
      // Attempt to reconnect if not connected
      try {
        await this.connect(id);
      } catch (error) {
        pm.logger.error(`MCPConnectionManager~fetchToolsForServer: Error connecting to server with id ${id}`, error);
        return Promise.reject(new Error(`Error connecting to server with id ${id}: ${error.message}`));
      }
    }

    const [error, { tools }] = await this.mcpClient.getTools(id);

    if (error) {
      pm.logger.error(`MCPConnectionManager~fetchToolsForServer: Error fetching tools for server with id ${id}`, error);
      return Promise.reject(new Error(`Error fetching tools for server with id ${id}: ${error.message}`));
    }

    // Add tools to the tool registry
    this.registerTools(id, tools);

    return Promise.resolve(tools || []);
  }

  /**
   * Clears the tool registry for a given server and refetches them.
   * @param {string} id - server id
   * @returns {Promise<Array<Tool>>} - A promise that resolves with the refetched tools.
   */
  async refetchToolsForServer (id) {
    const connection = this.connections.get(id);
    if (!connection) {
      throw new Error(`Connection with id ${id} not found`);
    }

    // 1. Fetch tools
    const [error, { tools }] = await this.mcpClient.getTools(id);

    if (error) {
      pm.logger.error(`MCPConnectionManager~refetchToolsForServer: Error refetching tools for server with id ${id}`, error);
      throw new Error(`Error refetching tools for server with id ${id}: ${error.message}`);
    }

    // 2a. On success, clear existing tools.
    connection.tools.forEach((tool) => this.toolRegistry.delete(tool.id));
    connection.tools.clear();
    pm.logger.info(`[MCPConnectionManager] Cleared existing tools for server ${id} after successful refetch.`);

    // 2b. Register new tools.
    this.registerTools(id, tools);

    return tools || [];
  }


  /**
   * Add tools to registry. Tools are enabled by default.
   * @param {string} id - server id for tools
   * @param {Array<Tool>} tools - tools to add to registry
   */
  registerTools (id, tools) {
    const connection = this.connections.get(id);
    if (!connection) {
      throw new Error(`Connection with id ${id} not found`);
    }

    pm.logger.info(`[MCPConnectionManager] Registering ${tools.length} tools for server ${id} with origin ${connection.origin}`);

    // Register each tool with the origin
    for (const tool of tools) {
      const toolId = `${id}-${tool.name}`;

      // Store the tool entry with id, server id, and enabled status
      const toolEntry = {
        id: toolId,
        serverId: id,
        origin: connection.origin,
        tool: tool,
        enabled: true, // Default to enabled
      };

      this.toolRegistry.set(toolId, toolEntry);
      connection.tools.set(toolId, toolEntry);

      // pm.logger.info(`[MCPConnectionManager] Registered tool ${tool.name} with id ${toolId}`);
    }

    pm.logger.info(`[MCPConnectionManager] Successfully registered ${tools.length} tools for server ${id}`);
  }

  /**
   * Enables a tool for a given toolId
   * @param {string} toolId - The id of the tool to enable.
   * @return {ToolEntry} - Returns the enabled tool entry if successful, or null if not.
   */
  enableTool (toolId) {
    const toolEntry = this.toolRegistry.get(toolId);

    if (!toolEntry) {
      pm.logger.error(`MCPConnectionManager~enableTool: Tool with id ${toolId} not found`);
      return null;
    }

    toolEntry.enabled = true;

    const connection = this.connections.get(toolEntry.serverId);
    if (connection && connection.tools.has(toolId)) {
      const connToolEntry = connection.tools.get(toolId);
      if (connToolEntry) {
        connToolEntry.enabled = true;
      }
    }

    return toolEntry;
  }

  /**
   * Disables a tool for a given toolId
   * @param {string} toolId - The id of the tool to disable.
   * @return {ToolEntry} - Returns the disabled tool entry if successful, or null if not.
   */
   disableTool (toolId) {
    const toolEntry = this.toolRegistry.get(toolId);
    if (!toolEntry) {
      pm.logger.error(`MCPConnectionManager~disableTool: Tool with id ${toolId} not found`);
      return null;
    }

    toolEntry.enabled = false;

    const connection = this.connections.get(toolEntry.serverId);
    if (connection && connection.tools.has(toolId)) {
      const connToolEntry = connection.tools.get(toolId);
      if (connToolEntry) {
        connToolEntry.enabled = false;
      }
    }

    return toolEntry;
  }

  /**
   * Toggles a tool for a given toolId
   * @param {string} toolId - The id of the tool to toggle.
   * @param {boolean} enabled - Whether to enable or disable the tool. If not provided, the tool will be toggled to the opposite state.
   * @return {ToolEntry} - Returns the toggled tool entry if successful, or null if not.
   */
  toggleTool (toolId, enabled) {
    return enabled ? this.enableTool(toolId) : this.disableTool(toolId);
  }

  /**
   * Gets or creates a fresh AbortController signal for the given ID.
   * If the existing signal is aborted or doesn't exist, creates a new one.
   * @param {string} id - The connection or server ID
   * @returns {AbortSignal} - A valid AbortSignal
   * @private
   */
  _getOrCreateAbortSignal (id) {
    let signal = this.abortControllerMap.get(id)?.signal;
    if (!signal || signal.aborted) {
      const abortController = new AbortController();
      this.abortControllerMap.set(id, abortController);
      signal = abortController.signal;
    }
    return signal;
  }

  // TODO: Add auth handling for MCP connections
}

const connectionManager = new MCPConnectionManager();

/**
 * Connects to the MCP server.
 * @param {MCPRequest} mcpRequest - The MCPRequest object to be used for the connection.
 * @param {string} origin - The origin of the connection, e.g., tab ID or agent mode.
 * @param {object} [options] - The connection options.
 * @param {string} [options.id] - The id of the connection. If not provided, a new id will be generated.
 * @param {boolean} [options.autoConnect=true] - Whether to automatically connect the connection after adding it.
 * @param {boolean} [options.getToolsOnConnect=true] - Whether to fetch the tools list after connecting
 * @returns {Promise<object>} - The connection object
 */
async function connectToMCP (mcpRequest, origin, options = { autoConnect: true, getToolsOnConnect: true }) {
  const id = await connectionManager.addConnection(mcpRequest, origin, options);
  return connectionManager.getConnection(id);
}

/**
 * Connects to multiple MCP servers in at once.
 * @param {MCPRequest[]} mcpRequests - An array of MCPRequest objects to be used for the connections.
 * @param {string} origin - The origin of the connections, e.g., tab ID or agent mode.
 * @param {object} options - The connection options.
 * @param {boolean} [options.autoConnect=true] - Whether to automatically connect the connection after adding it.
 * @param {boolean} [options.getToolsOnConnect=true] - Whether to fetch the tools list after connecting
 * @returns {Promise<Array<MCPConnection | boolean>>} - An array of ToolEntry objects for the successful connections, or error messages or false if the connection failed.
 */
async function bulkConnectToMCP (mcpRequests, origin, options = { autoConnect: true, getToolsOnConnect: true }) {
  const results = await connectionManager.addConnections(mcpRequests, origin, options);
  return results.map((result) => {
    if (typeof result === 'string') {
      return connectionManager.getConnection(result);
    } else {
      return result; // This is an error message or false
    }
  });
}

/**
 * Toggles a tool for a given toolId
 * @param {string} toolId - The id of the tool to toggle.
 * @param {boolean} enabled - Whether to enable or disable the tool. If not provided, the tool will be toggled to the opposite state.
 * @return {ToolEntry}
 */
function toggleTool (toolId, enabled) {
  return connectionManager.toggleTool(toolId, enabled);
}

/**
 * Calls a tool with the given arguments.
 * @param {string} toolId - The id of the tool to call.
 * @param {object} args - The arguments to pass to the tool
 */
async function callTool (toolId, args) {
  return await connectionManager.callTool(toolId, args);
}

/**
 * Disconnects from the MCP server.
 * @param {string} id - The id of the connection to disconnect.
 * @param {boolean} [removeConnection=false] - Whether to remove the connection from the manager after disconnecting.
 * @return {Promise<boolean>} - Returns true if the connection was disconnected successfully, false otherwise.
 */
async function disconnectFromMCP (id, removeConnection = false) {
  const disconnected = await connectionManager.disconnect(id);
  if (disconnected && removeConnection) {
    await connectionManager.removeConnection(id);
  }
  return disconnected;
}

/**
 * Refetches tools for a given server.
 * @param {string} id - The id of the server to refetch tools for.
 * @returns {Promise<Array<Tool>>} - A promise that resolves with the refetched tools.
 */
async function refetchToolsForServer (id) {
  return await connectionManager.refetchToolsForServer(id);
}

/**
 * Gets the list of tools for a specific server.
 * @param {string} id - The id of the server to get tools for.
 * @param {boolean} [enabledOnly=false] - Whether to return only enabled tools.
 * @returns {Array<ToolEntry>} - The list of tools for the specified server.
 */
function getToolsForServer (id, enabledOnly = false) {
  const { toolRegistry, connections } = connectionManager;
  return Array.from(toolRegistry.values()).filter((tool) => tool.serverId === id && (!enabledOnly || (tool.enabled && connections.get(tool.serverId)?.connected)));
}

/**
 * Gets tools by origin
 * @param {string} origin - The origin of the tools to get.
 * @param {boolean} [enabledOnly=false] - Whether to return only enabled tools.
 * @returns {Array<ToolEntry>} - The list of tools for the specified origin.
 */
function getToolsByOrigin (origin, enabledOnly = false) {
  const { toolRegistry, connections } = connectionManager;
  return Array.from(toolRegistry.values()).filter((tool) => tool.origin === origin && (!enabledOnly || (tool.enabled && connections.get(tool.serverId)?.connected)));
}

/**
 * Gets a server connection by its id.
 * @param {string} id
 * @returns {MCPConnection | null}
 */
function getServerById (id) {
  const connection = connectionManager.getConnection(id);
  if (!connection) {
    pm.logger.error(`MCPConnectionManager~getServerById: No connection found for id ${id}`);
    return null;
  }
  return connection;
}

/**
 * Gets a list of server connections by their origin.
 * @param {string} origin
 * @returns {Array<MCPConnection>}
 */
function getServersByOrigin (origin) {
  const connections = Array.from(connectionManager.connections.values());
  return connections.filter((connection) => connection.origin === origin);
}

/**
 * Cancel the ongoing request for a specific connection.
 * @param {string} id - The id of the connection to cancel.
 */
function cancelMCPRequest (id) {
  const signal = this._getOrCreateAbortSignal(id);
  signal.abort();
}

// Exporting the connection manager class if the entire class is needed
// Otherwise, we can use the functions to interact with the connection manager
module.exports = {
  connectToMCP,
  toggleTool,
  callTool,
  bulkConnectToMCP,
  getToolsForServer,
  getToolsByOrigin,
  disconnectFromMCP,
  getServerById,
  getServersByOrigin,
  MCPConnectionManager,
  cancelMCPRequest,
  refetchToolsForServer,
};
