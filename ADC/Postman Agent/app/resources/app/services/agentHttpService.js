const contentTypeMap = { json: /\bjson\b/ },
      fetch = require('node-fetch'),
      wrap = (fetch) => {
    return new Promise((resolve, reject) => {
      fetch.then((response) => {
        let parsedResponse,
        contentType = response.headers.get('Content-Type');
        if (contentTypeMap.json.test(contentType)) {
          parsedResponse = response.json();
        }
        else {
          parsedResponse = response.text();
        }

        parsedResponse.then((data) => {
          if (response.ok) {
            resolve({
              body: data,
              status: response.status,
              headers: response.headers
            });
          }
          else {
            reject({
              error: data,
              status: response.status,
              headers: response.headers
            });
          }
        });
      }).catch((error) => {
        // @todo: this is here because the consumers sometimes drop the error and rely on the status
        // status should always be truthy
        reject({ error, status: 1 });
      });
    });
};

class agentHttpService {
  request (path, options) {
    return wrap(fetch(path, options));
  }
}

module.exports = new agentHttpService();
