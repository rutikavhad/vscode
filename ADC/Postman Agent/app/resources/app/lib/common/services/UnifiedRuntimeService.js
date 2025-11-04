const { ServerMethods: existing, rpc, Channel } = require('@postman/runtime/server-methods');
const { platform } = require('@postman/runtime/platform');
const { homedir } = require('os');
const { join } = require('path');
const PostmanFs = require('../utils/postmanFs');
const { promisify } = require('util');

module.exports = {
  ServerMethods: {
    ...existing,
    'platform.execute': rpc({
      ...platform,

      fs: {
        async readFile (path) {
          return new Channel(async ({ incoming }) => {
            const cwd = join(homedir(), 'Postman', 'files');
            const fs = new PostmanFs(cwd);
            const readFile = promisify(fs.readFile.bind(fs));

            const data = await readFile(path);

            incoming.enqueue(data);
            incoming.close();
          });
        }
      },

      proxy: {
        async resolveProxy () {
          return new Channel(async ({ incoming }) => {
            // (no system proxy support in Desktop agent)

            incoming.enqueue(null);
            incoming.close();
          });
        }
      }
    })
  }
};
