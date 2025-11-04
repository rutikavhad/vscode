/**
 * Set of helpers for converting fetch requests into a format that can be logged in the console
 * */

/**
 * Build a request object from fetch init and URL.
 * @param {RequestInit} init - The fetch initialization object.
 * @param {string} url - The request URL.
 * @returns {Object} The built request object with headers, method, url, and optional body.
 */
function buildRequest (init, url) {
  return {
    headers: (() => {
      if (init.headers && typeof init.headers.entries === 'function') {
        return Array.from(init.headers.entries()).map(([key, value]) => ({ key, value }));
      }
      if (typeof init.headers === 'object' && init.headers !== null) {
        return Object.entries(init.headers).map(([key, value]) => ({ key, value }));
      }
      return [];
    })(),

    method: init.method,
    url,
    ...(init.body ? { body: init.body } : {})
  };
}

/**
 * Build a response object from a Response instance and timing information.
 * @param {Response} response - The fetch Response object.
 * @param {number} [responseTime] - The response time in milliseconds.
 * @param {string} [body] - Optional response body content.
 * @returns {Object} The built response object with headers, status, timing, and other metadata.
 */
function buildResponse (response, responseTime, body) {
  return {
    headers: Array.from(response.headers.entries()).map(([key, value]) => ({ key, value })),

    // Console uses both code and statusCode
    code: response.status,
    statusCode: response.status,
    responseTime,
    status: response.statusText,
    redirected: response.redirected,
    type: response.type,
    ...(body ? { body } : {}),

    // this is added so the console can parse the response body
    contentInfo: {
      charset: 'utf-8',
    }
  };
}

/**
 * Create a history object with execution data structure.
 * @param {string} id - Unique session ID.
 * @returns {Object} History object with execution data and sessions.
 */
function createHistory (id) {
  return {
    execution: {
      data: [],
      sessions: {
        [id]: {},
      },
    },
  };
}

/**
 * Add request/response data to history execution.
 * @param {Object} history - History object to modify.
 * @param {Object} request - Request object.
 * @param {Object} response - Response object.
 * @param {string} sessionId - Session ID.
 */
function addToHistory (history, request, response, sessionId) {
  history.execution.data.push({
    request,
    response,
    session: { id: sessionId, reused: false }
  });
}

/**
 * Get location header with case-insensitive fallback.
 * @param {Headers} headers - Response headers object.
 * @returns {string|null} Location header value or null.
 */
function getLocationHeader (headers) {
  return headers.get('Location') ?? headers.get('location');
}

/**
 * Resolve relative location to absolute URL.
 * @param {string} location - Location header value.
 * @param {string|URL} input - Original input URL.
 * @returns {string} Resolved absolute URL.
 */
function resolveLocation (location, input) {
  if (typeof location === 'string' && location.startsWith('/')) {
    const inputObj = typeof input === 'string' ? new URL(input) : input;
    return inputObj.protocol + '//' + inputObj.host + location;
  }
  return location;
}

module.exports = {
  buildRequest,
  buildResponse,
  createHistory,
  addToHistory,
  getLocationHeader,
  resolveLocation,
};
