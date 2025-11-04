// Provider imports
const { createAmazonBedrock } = require('@ai-sdk/amazon-bedrock');
const { createOpenAI } = require('@ai-sdk/openai');
const { createDeepSeek } = require('@ai-sdk/deepseek');
const { createGoogleGenerativeAI } = require('@ai-sdk/google');
const { createAnthropic } = require('@ai-sdk/anthropic');
const { createXai } = require('@ai-sdk/xai');
const { generateText, streamText, APICallError, jsonSchema, tool, stepCountIs } = require('ai');
const tls = require('tls');
const { Agent, ProxyAgent } = require('undici');
const { callTool, getServerById, getToolsByOrigin } = require('./MCPConnectionManager');
const EventChannel = require('../channels/EventChannel');
const RuntimeClientUtilities = require('./RuntimeClientUtilities');

const PROVIDER_TO_CREATE = {
  openai: createOpenAI,
  anthropic: createAnthropic,
  deepseek: createDeepSeek,
  google: createGoogleGenerativeAI,
  xai: createXai,
  bedrock: createAmazonBedrock,
};

const PROVIDER_OPTIONS = {
  openai: {
    compatibility: 'strict',
  }
};

class LLMClient {
  constructor (cwd) {
    this.cwd = cwd;
    this.runtimeUtilities = new RuntimeClientUtilities(cwd);
  }

  /**
   * Creates a provider instance based on the provider name.
   * @param {string} provider - The name of the provider (e.g., 'openai', 'anthropic').
   * @param {Object} options - Options for the client.
   * @param {string|Object} options.apiKey - The API key for the provider, or auth object for Bedrock.
   * @param {function} [options.customFetch] - A custom fetch function to use for the provider.
   *
   * @returns {Object} - The provider instance.
   */
  createProvider (provider, options) {
    if (!PROVIDER_TO_CREATE[provider]) {
      throw new Error(`Unsupported provider: ${provider}`);
    }

    const createFunction = PROVIDER_TO_CREATE[provider];
    const providerSettings = PROVIDER_OPTIONS[provider] || {};

    pm.logger.info(`[LLMClient~createProvider] Creating provider for: ${provider}`);

    // Special handling for Bedrock provider
    if (provider === 'bedrock') {
      const authData = typeof options.apiKey === 'object' ? options.apiKey : {};
      return createFunction({
        region: authData.region || 'us-east-1', // Default to us-east-1 if not provided
        accessKeyId: authData.accessKeyId || undefined,
        secretAccessKey: authData.secretAccessKey || undefined,
        sessionToken: authData.sessionToken || undefined,
        ...providerSettings,
        fetch: options.customFetch,
      });
    }

    // Standard handling for other providers
    return createFunction({
      apiKey: options.apiKey,
      ...providerSettings,
      fetch: options.customFetch,
    });
  }

  /**
   * Type of the network settings for the request.
   * @typedef {Object} LLMNetworkSettings
   * @property {string} url - The URL of the request.
   * @property {string} [protocolVersion] - The protocol version to use.
   * @property {boolean} [strictSSL] - Whether to use strict SSL.
   * @property {number} [requestTimeout] - The request timeout in milliseconds.
   * @property {boolean} [includeImplicitCacheControlHeader] - Whether to include an implicit cache control header.
   * @property {Object} [certificates] - The certificates to use for the request.
   */

  /**
   * Type of the proxy settings for the request.
   * @typedef {Object} LLMProxyConfiguration
   * @property {string} [url] - The URL of the proxy.
   * @property {boolean} system - Whether to use the system proxy.
   * @property {boolean} env - Whether to use the environment proxy.
   */

  /**
   * Type of the payload passed from the front-end to initiate a request.
   * @typedef {Object} LLMRequestEventPayload
   * @property {string} provider - The name of the provider (e.g., 'openai', 'anthropic', 'bedrock').
   * @property {string} model - The model to use (e.g., 'gpt-3.5-turbo', 'claude-3-sonnet').
   * @property {string} prompt - The prompt to send to the model.
   * @property {string} [system] - Optional system prompt to include.
   * @property {string} [origin] - The ID of the origin for tool calls.
   * @property {string|Object} apiKey - The API key for the provider. For Bedrock, this is an object with region, accessKeyId, secretAccessKey, sessionToken.
   * @property {Object} settings - Additional settings for the request.
   * @property {number} [settings.maxSteps] - Maximum number of steps to generate.
   * @property {number} [settings.maxTokens] - Maximum number of tokens to generate.
   * @property {number} [settings.temperature] - Temperature for randomness in generation.
   * @property {number} [settings.topP] - Top P for nucleus sampling.
   * @property {number} [settings.frequencyPenalty] - Frequency penalty for repetition.
   * @property {number} [settings.presencePenalty] - Presence penalty for new topics.
   * @property {LLMNetworkSettings} [networkSettings] - Network settings for the request.
   * @property {LLMProxyConfiguration} [proxyConfig] - Proxy settings for the request.
   */

  /**
   * Executes a streaming request to the LLM provider for a given model and prompt.
   * @param {LLMRequestEventPayload} payload - The payload containing data sent from the front-end.
   * @returns {Promise<EventChannel>} - An event channel to send stream chunks through.
   */
  async executeStreamRequest ({ provider, model, prompt, system = '', origin, apiKey, settings, networkSettings, proxyConfig = { url: undefined, system: false, env: false } }) {
    const providerInstance = this.createProvider(provider, { apiKey, customFetch: await this.generateCustomFetch({ networkSettings, proxyConfig }) });

    // Handle empty prompts for Bedrock provider
    const processedPrompt = (provider === 'bedrock' && !prompt) ? '-' : prompt;

    const request = {
      model: providerInstance(model),
      prompt: processedPrompt,
      ...(system && { system }), // Only include system if it's not empty
      tools: getToolsFromConnectionManager(origin),
      stopWhen: stepCountIs(settings.maxSteps),
      ...settings
    };

    pm.logger.info('[LLMClient~executeRequest] Tools:', request.tools);

    const startTime = performance.now();
    const eventChannel = new EventChannel();
    const abortController = new AbortController();
    const debugLogs = false;

    // On cancel during stream
    eventChannel.on('cancel', () => {
      const payload = {
        text: 'Request cancelled by user',
        request: {
          responseTime: performance.now() - startTime,
          code: 499,
        }
      };
      pm.logger.error('[LLMClient~executeStreamRequest] User cancelled the request during streamText');
      eventChannel.emit('error', emit('response-error', payload));
      abortController.abort();
      eventChannel.destroy();
    });

    (async () => {
      try {
        const result = streamText(request);
        for await (const streamChunk of result.fullStream) {
          if (debugLogs) {
            pm.logger.info('[LLMClient~executeStreamRequest] Stream chunk:', {
              type: streamChunk.type,
              hasText: 'text' in streamChunk && !!streamChunk.text,
              textLength: 'text' in streamChunk ? streamChunk.text?.length : 0,
              finishReason: 'finishReason' in streamChunk ? streamChunk.finishReason : undefined,
              toolCallId: 'toolCallId' in streamChunk ? streamChunk.toolCallId : undefined,
              toolName: 'toolName' in streamChunk ? streamChunk.toolName : undefined
            });
          }
          switch (streamChunk.type) {
            case 'finish':
              eventChannel.emit('response-stream', emit('response-stream', { ...streamChunk, usage: processUsageTokens(streamChunk.totalUsage) }));
              break;
            case 'finish-step':
              eventChannel.emit('response-stream', emit('response-stream', { ...streamChunk, usage: processUsageTokens(streamChunk.usage) }));
              break;
            case 'start-step':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-input-start':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-input-delta':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-input-end':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-call':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-result':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'tool-error':
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
              break;
            case 'error':
              const payload = {
                text: (
                  streamChunk.error &&
                  typeof streamChunk.error === 'object' &&
                  'message' in streamChunk.error &&
                  typeof streamChunk.error.message === 'string'
                ) ? streamChunk.error.message
                : 'An error occurred during streaming',
                response: {
                  responseTime: performance.now() - startTime,
                  statusCode: (
                    streamChunk.error &&
                    typeof streamChunk.error === 'object' &&
                    'statusCode' in streamChunk.error
                  ) ? streamChunk.error.statusCode
                  : undefined,
                  headers: (
                    streamChunk.error &&
                    typeof streamChunk.error === 'object' &&
                    'responseHeaders' in streamChunk.error

                    // @ts-expect-error Error is of type unknown, set if available
                  ) ? processResponseHeaders(streamChunk.error.responseHeaders)
                  : undefined,
                }
              };
              pm.logger.error(`[LLMClient~executeStreamRequest] Error packet found during streamText: ${payload.text}`);
              eventChannel.emit('response-error', emit('response-error', payload));
              eventChannel.destroy();
              break;
            default:
              eventChannel.emit('response-stream', emit('response-stream', streamChunk));
          }
        }

        const payloadSteps = (await result.steps).map((step) => {
          return {
            finishReason: step.finishReason,
            text: step.text,
            usage: processUsageTokens(step.usage),
            toolCalls: step.toolCalls && step.toolCalls.length > 0 ? step.toolCalls.map((toolCall) => {
              return {
                toolCallId: toolCall.toolCallId,
                toolName: toolCall.toolName,
                args: JSON.stringify(toolCall.input, null, 2),
              };
            }) : undefined,
            toolResults: step.toolResults && step.toolResults.length > 0 ? step.toolResults.map((toolResult) => {
              return {
                toolCallId: toolResult.toolCallId,
                toolName: toolResult.toolName,
                result: JSON.stringify(toolResult.output, null, 2),
              };
            }) : undefined,
            response: {
              responseTime: performance.now() - startTime, // [TODO] Calculate step response time
              statusCode: 200, // Successful responses do not have a code attached
              headers: processResponseHeaders(step.response.headers),
            }
          };
        });

        // Emit final response after the stream ends
        pm.logger.info('[LLMClient~executeStreamRequest] Response completed generation from streamText');
        eventChannel.emit('response-received', emit('response-received', payloadSteps));
        eventChannel.destroy();
      } catch (err) {
        let message = err.message;
        let statusCode;
        let headers;
        if (APICallError.isInstance(err)) {
          statusCode = err.statusCode;
          headers = processResponseHeaders(err.responseHeaders);
        }
        const payload = {
          finishReason: 'error',
          text: message || 'Request was unable to stream text',
          response: {
            responseTime: performance.now() - startTime,
            statusCode,
            headers,
          }
        };
        pm.logger.error(`[LLMClient~executeStreamRequest] Error executing streamText: ${message}`);
        eventChannel.emit('error', emit('response-error', payload));
        eventChannel.destroy();
      }
    })();

    pm.logger.info('[LLMClient~executeStreamRequest] Event channel created for streaming response');
    return eventChannel;
  }

  /**
   * Executes a request to the LLM provider for a given model and prompt.
   * @param {LLMRequestEventPayload} payload - The payload containing data sent from the front-end.
   * @returns {Promise<Object>} - The response from the LLM provider.
   */
  async executeRequest ({ provider, model, prompt, system = '', origin, apiKey, settings, networkSettings, proxyConfig = { url: undefined, system: false, env: false } }) {
    pm.logger.info('[LLMClient~executeRequest] Starting request for provider:', provider, 'model:', model);
    const providerInstance = this.createProvider(provider, {
      apiKey,
      customFetch: await this.generateCustomFetch({
        networkSettings, proxyConfig
      })
    });

    // Handle empty prompts for Bedrock provider
    const processedPrompt = (provider === 'bedrock' && !prompt) ? '-' : prompt;

    const request = {
      model: providerInstance(model),
      prompt: processedPrompt,
      tools: getToolsFromConnectionManager(origin),
      ...(system && { system }), // Only include system if it's not empty
      stopWhen: stepCountIs(settings.maxSteps),
      ...settings
    };

    pm.logger.info('[LLMClient~executeRequest] Tools:', request.tools);

    let startTime = performance.now();
    try {
      const result = await generateText(request);

      pm.logger.info('[LLMClient~executeRequest] Result from generateText:', result);
      const payloadSteps = result.steps.map((step) => {
        return {
          finishReason: step.finishReason,
          text: step.text,
          usage: processUsageTokens(step.usage),
          toolCalls: step.toolCalls && step.toolCalls.length > 0 ? step.toolCalls.map((toolCall) => {
            return {
              toolCallId: toolCall.toolCallId,
              toolName: toolCall.toolName,
              args: JSON.stringify(toolCall.input, null, 2),
            };
          }) : undefined,
          toolResults: step.toolResults && step.toolResults.length > 0 ? step.toolResults.map((toolResult) => {
              return {
                toolCallId: toolResult.toolCallId,
                toolName: toolResult.toolName,
                result: JSON.stringify(toolResult.output, null, 2),
              };
            }) : undefined,
          reasoning: step.reasoningText,
          response: {
            responseTime: performance.now() - startTime, // [TODO] Calculate step response time
            statusCode: 200, // Successful responses do not have a code attached
            headers: processResponseHeaders(step.response.headers),
            body: JSON.stringify(step.response.body),
            size: calculateResponseSize(step.response.headers, JSON.stringify(step.response.body)),
          }
        };
      });

      pm.logger.info('[LLMClient~executeRequest] Response generated from generateText');
      return emit('response-received', payloadSteps);
    } catch (err) {
      let message = err.message;
      let statusCode;
      let headers;

      if (APICallError.isInstance(err)) {
        statusCode = err.statusCode;
        headers = processResponseHeaders(err.responseHeaders);
      }
      const payload = {
        text: message || 'Request was unable to generate text',
        response: {
          responseTime: performance.now() - startTime,
          statusCode,
          headers,
        }
      };
      pm.logger.error(`[LLMClient~executeRequest] Error executing generateText: ${message}`);
      return emit('response-error', payload);
    }
  }

  /**
   * Executes a dry run request to the LLM provider for a given model and prompt.
   * @param {LLMRequestEventPayload & { streamResponse: boolean }} payload - The payload containing data sent from the front-end.
   * @returns {Promise<Object>} - The response from the LLM provider.
   */
  async executeDryRun ({ provider, model, prompt, system = '', origin, apiKey, settings = {}, streamResponse }) {
    // This dry run fetch function errors out to prevent the request from going
    // through the AI-SDK's response transformers.
    const dryRunFetch = async (url, options) => {
      return new Response(JSON.stringify({
        url,
        method: options.method,
        headers: options.headers,
        body: options.body,
        timeout: options.timeout,
      }), {
        status: 400, // Dry run throws an error to exit early
        headers: {
          'Content-Type': 'application/json',
        },
      });
    };

    const providerInstance = this.createProvider(provider, { apiKey, customFetch: dryRunFetch });

    // Handle empty prompts for Bedrock provider
    const processedPrompt = (provider === 'bedrock' && !prompt) ? ' ' : prompt;

    const request = {
      model: providerInstance(model),
      prompt: processedPrompt,
      ...(system && { system }), // Only include system if it's not empty
      tools: getToolsFromConnectionManager(origin),
      ...settings
    };
    try {
      if (streamResponse) {
        const payload = streamText(request);
        for await (const chunk of payload.fullStream) {
          switch (chunk.type) {
            case 'error':
              const error = new Error('Dry run request failed successfully.');

              // @ts-expect-error Response body is created by custom fetch
              error['responseBody'] = chunk.error.responseBody;
              throw error;
            default:
              // Should never get here, dry run throws an error
              break;
          }
        }

        // Should never get here, dry run throws an error
        return emit('request-config-error', {});
      }
      await generateText(request);
      return emit('request-config-error', {});
    } catch (err) {
      return emit('request-config-success', err.responseBody);
    }
  }

  // #region Custom fetch helpers

  /**
   * Validates the URL and returns a URL object.
   * @param {string} url - The URL to validate.
   * @returns {URL} - The validated URL.
   */
  validateUrl (url) {
    if (!(/^[a-z0-9+.-]+:\/\//i).test(url)) {
      url = 'http://' + url;
    }

    try {
      return new URL(url);
    } catch (_) {
      throw new Error(`Invalid URL: ${url}`);
    }
  }

  /**
   * Generates an agent based on the network settings and proxy configuration.
   * @param {LLMNetworkSettings} networkSettings - The network settings for the provider.
   * @param {LLMProxyConfiguration} proxyConfig - The proxy configuration for the provider.
   * @returns {Promise<[Error | null, Agent | ProxyAgent | null]>} - The agent from given parameters, return null if no agent can be generated.
   */
  async generateAgent (networkSettings, proxyConfig) {
    let certificates, envProxy, systemProxy, proxy;

    try {
      certificates = networkSettings.certificates ? await this.runtimeUtilities.loadSecureContext(networkSettings.certificates) : {};
    } catch (error) {
      pm.logger.error(`[LLMClient] Unable to load certificates: ${error.message}`);
      return [error, null];
    }

      try {
        const validatedUrl = this.validateUrl(networkSettings.url);
        envProxy = proxyConfig.env ? this.runtimeUtilities.loadEnvProxy(validatedUrl) : undefined;
        systemProxy = proxyConfig.system ? await this.runtimeUtilities.loadSystemProxy(networkSettings.url) : undefined;
        proxy = proxyConfig.url ?? systemProxy ?? envProxy;
      } catch (error) {
        pm.logger.error(`[LLMClient] Unable to load proxy configuration: ${error.message}`);
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
      rejectUnauthorized: Boolean(networkSettings.strictSSL),
    };

    if (proxy) {
      return [null, new ProxyAgent({
        uri: proxy,
        requestTls: connectOptions,
        bodyTimeout: networkSettings.requestTimeout,
      })];
    }

    return [null, new Agent({
      connect: connectOptions,
      bodyTimeout: networkSettings.requestTimeout,
    })];
  }

  async generateCustomFetch ({ networkSettings, proxyConfig }) {
    const [error, agent] = await this.generateAgent(networkSettings, proxyConfig);

    if (error) {
      pm.logger.error(`[LLMClient] Unable to generate agent: ${error.message}`);
      throw error;
    }

    return async (url, init) => {
      return fetch(url, {
        ...init,
        headers: {
          ...init.headers,
          ...(networkSettings.includeImplicitCacheControlHeader ? { 'Cache-Control': 'no-cache' } : {}),
        },
        dispatcher: agent
      });
    };

  }

  // #endregion
}

/**
 * Gets all the enabled tools from the MCPConnectionManager for a given origin ID.
 * @param {string} origin - Unique ID from the front-end
 * @returns {Object | undefined} - An object to be passed to the
 */
function getToolsFromConnectionManager (origin) {
  pm.logger.info(`[LLMClient] Getting tools for origin: ${origin}`);

  let tools;
  let toolEntries = getToolsByOrigin(origin, true);

  pm.logger.info(`[LLMClient] Found ${toolEntries.length} enabled tool entries for origin ${origin}`);

  if (toolEntries.length > 0) {
    pm.logger.info('[LLMClient] Tool entries details:', toolEntries.map((entry) => ({
      id: entry.id,
      toolName: entry.tool.name,
      enabled: entry.enabled,
      origin: entry.origin,
    })));

    tools = toolEntries.reduce((acc, toolEntry) => {
      const toolKey = `${getServerById(toolEntry.serverId).mcpRequest.serverName}_${toolEntry.tool.name}`;
      acc[toolKey] = tool({
        description: toolEntry.tool.description,
        inputSchema: jsonSchema(toolEntry.tool.inputSchema),
        execute: async (params, options) => {
          return callTool(toolEntry.id, params);
        }
      });
      return acc;
    }, {});

    pm.logger.info(`[LLMClient] Prepared ${Object.keys(tools).length} tools for execution:`, Object.keys(tools));
  } else {
    pm.logger.info(`[LLMClient] No enabled tools found for origin ${origin}`);
  }

  return tools;
}

/**
 * An object containing the sizes of a response headers and body.
 * @typedef {Object} ResponseSize
 * @property {number | undefined} body - The size of the response body in bytes.
 * @property {number | undefined} headers - The size of the response headers in bytes.
 */

/**
 * Calculates the size of the response based on headers and body.
 * @param {Record<string, string> | undefined} headers - The headers of the response.
 * @param {string | undefined} responseBody - JSON string of the response body.
 * @returns {ResponseSize | undefined} - An object containing the sizes of the body, header, and total.
 */
function calculateResponseSize (headers, responseBody) {
  const bodySize = responseBody ? Buffer.byteLength(responseBody, 'utf8') : undefined;
  const headersSize = headers ? Object.entries(headers).reduce((acc, [key, value]) => {
    return acc + Buffer.byteLength(`${key}: ${value}\r\n`, 'utf8');
  }, 0) : undefined;

  return {
    body: bodySize,
    headers: headersSize,
  };
}

/**
 * Returns and cleans the prompt and completion tokens from the usage object. Adding
 * this because the AI-SDK returns NaN for certain models.
 * @param {*} usage - The usage object from the AI-SDK (LanguageModelV2Usage)
 * @returns {{promptTokens: number, completionTokens: number} | undefined} - An object containing the prompt and completion tokens.
 */
function processUsageTokens (usage) {
  if (!usage) return undefined;

  const promptTokens = usage.promptTokens || usage.inputTokens;
  const completionTokens = usage.completionTokens || usage.outputTokens;

  if (!Number.isNaN(promptTokens) && !Number.isNaN(completionTokens)) {
    return {
      promptTokens,
      completionTokens,
    };
  }
  return undefined;
}

/**
 *
 * @param {Record<string, string> | undefined} headers - The headers from the response.
 * @returns {Array<{ key: string; value: string }>} - An object containing the processed headers.
 */
function processResponseHeaders (headers) {
  if (headers) {
    return Object.entries(headers).map(([key, value]) => {
      return { key, value };
    });
  }
  return [];
}

/**
 * This returns an event using the format expected by Scribe.
 * @param {string} eventName - The name of the event (e.g., 'response-received', 'response-error').
 * @param {Object} payload - The payload to include in the event.
 */
function emit (eventName, payload) {
   return {
    type: eventName,
    timestamp: new Date().toISOString(),
    payload,
  };
}

module.exports = LLMClient;
