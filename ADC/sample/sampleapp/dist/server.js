/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./configs sync recursive ^\\.\\/.*$":
/*!********************************!*\
  !*** ./configs/ sync ^\.\/.*$ ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("{var map = {\n\t\"./\": \"./configs/index.js\",\n\t\"./db\": \"./configs/db.js\",\n\t\"./db.js\": \"./configs/db.js\",\n\t\"./development\": \"./configs/development.js\",\n\t\"./development.js\": \"./configs/development.js\",\n\t\"./index\": \"./configs/index.js\",\n\t\"./index.js\": \"./configs/index.js\",\n\t\"./production\": \"./configs/production.js\",\n\t\"./production.js\": \"./configs/production.js\",\n\t\"./settings\": \"./configs/settings.js\",\n\t\"./settings.js\": \"./configs/settings.js\"\n};\n\n\nfunction webpackContext(req) {\n\tvar id = webpackContextResolve(req);\n\treturn __webpack_require__(id);\n}\nfunction webpackContextResolve(req) {\n\tif(!__webpack_require__.o(map, req)) {\n\t\tvar e = new Error(\"Cannot find module '\" + req + \"'\");\n\t\te.code = 'MODULE_NOT_FOUND';\n\t\tthrow e;\n\t}\n\treturn map[req];\n}\nwebpackContext.keys = function webpackContextKeys() {\n\treturn Object.keys(map);\n};\nwebpackContext.resolve = webpackContextResolve;\nmodule.exports = webpackContext;\nwebpackContext.id = \"./configs sync recursive ^\\\\.\\\\/.*$\";\n\n//# sourceURL=webpack://sample-app/./configs/_sync_^\\.\\/.*$?\n}");

/***/ }),

/***/ "./configs/db.js":
/*!***********************!*\
  !*** ./configs/db.js ***!
  \***********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst {\n  database\n} = __webpack_require__(/*! ./settings */ \"./configs/settings.js\");\nmodule.exports = {\n  secret: database.secretKey,\n  database: database.dbURL\n};\n\n//# sourceURL=webpack://sample-app/./configs/db.js?\n}");

/***/ }),

/***/ "./configs/development.js":
/*!********************************!*\
  !*** ./configs/development.js ***!
  \********************************/
/***/ ((module) => {

"use strict";
eval("{\n\nlet devConfig = {\n  hostname: 'localhost',\n  port: 3000,\n  viewDir: './app/views'\n};\nmodule.exports = devConfig;\n\n//# sourceURL=webpack://sample-app/./configs/development.js?\n}");

/***/ }),

/***/ "./configs/index.js":
/*!**************************!*\
  !*** ./configs/index.js ***!
  \**************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst _ = __webpack_require__(/*! lodash */ \"lodash\");\nconst env = \"development\" || 0;\nconst envConfig = __webpack_require__(\"./configs sync recursive ^\\\\.\\\\/.*$\")(\"./\" + env);\nconst defaultConfig = {};\nmodule.exports = _.merge(defaultConfig, envConfig);\n\n//# sourceURL=webpack://sample-app/./configs/index.js?\n}");

/***/ }),

/***/ "./configs/production.js":
/*!*******************************!*\
  !*** ./configs/production.js ***!
  \*******************************/
/***/ ((module) => {

"use strict";
eval("{\n\nlet prodConfig = {\n  hostname: 'reinsureservices.com',\n  port: 8081,\n  viewDir: './app/views'\n};\nmodule.exports = prodConfig;\n\n//# sourceURL=webpack://sample-app/./configs/production.js?\n}");

/***/ }),

/***/ "./configs/settings.js":
/*!*****************************!*\
  !*** ./configs/settings.js ***!
  \*****************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("{const fs = __webpack_require__(/*! fs */ \"fs\");\nconst path = __webpack_require__(/*! path */ \"path\");\nlet rawdata = fs.readFileSync(path.resolve(__dirname, 'settings.json'));\nlet settings = JSON.parse(rawdata);\nmodule.exports = settings;\n\n//# sourceURL=webpack://sample-app/./configs/settings.js?\n}");

/***/ }),

/***/ "./index.js":
/*!******************!*\
  !*** ./index.js ***!
  \******************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\n__webpack_require__(/*! babel-polyfill */ \"babel-polyfill\");\nconst server = __webpack_require__(/*! ./server */ \"./server/index.js\")();\nconst config = __webpack_require__(/*! ./configs */ \"./configs/index.js\");\nconst db = __webpack_require__(/*! ./configs/db */ \"./configs/db.js\");\nconst terminate = __webpack_require__(/*! ./utils/terminate */ \"./utils/terminate.js\");\ntry {\n  server.create(config, db);\n  server.start();\n  const exitHandler = terminate(server, {\n    coredump: false,\n    timeout: 500\n  });\n  process.on('uncaughtException', exitHandler(1, 'Unexpected Error'));\n  process.on('unhandledRejection', exitHandler(1, 'Unhandled Promise'));\n  process.on('SIGTERM', exitHandler(1, 'SIGTERM'));\n  process.on('SIGINT', exitHandler(1, 'SIGINT'));\n} catch (error) {\n  throw error;\n}\n\n//# sourceURL=webpack://sample-app/./index.js?\n}");

/***/ }),

/***/ "./server/controllers/apis/movies.js":
/*!*******************************************!*\
  !*** ./server/controllers/apis/movies.js ***!
  \*******************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst express = __webpack_require__(/*! express */ \"express\");\nconst {\n  getMovies,\n  deleteMovie,\n  saveMovies,\n  updateMovies\n} = __webpack_require__(/*! ../../services/movies */ \"./server/services/movies/index.js\");\nlet router = express.Router();\nrouter.get('/', getMovies);\nrouter.delete('/:id', deleteMovie);\nrouter.post('/', saveMovies);\nrouter.put('/:id', updateMovies);\nmodule.exports = router;\n\n//# sourceURL=webpack://sample-app/./server/controllers/apis/movies.js?\n}");

/***/ }),

/***/ "./server/controllers/home.js":
/*!************************************!*\
  !*** ./server/controllers/home.js ***!
  \************************************/
/***/ ((module) => {

"use strict";
eval("{\n\nfunction index(request, response) {\n  response.json({\n    message: \"this is home route\"\n  });\n}\nmodule.exports = {\n  index: index\n};\n\n//# sourceURL=webpack://sample-app/./server/controllers/home.js?\n}");

/***/ }),

/***/ "./server/index.js":
/*!*************************!*\
  !*** ./server/index.js ***!
  \*************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst express = __webpack_require__(/*! express */ \"express\");\nconst helmet = __webpack_require__(/*! helmet */ \"helmet\");\nconst bodyParser = __webpack_require__(/*! body-parser */ \"body-parser\");\nconst mongoose = __webpack_require__(/*! mongoose */ \"mongoose\");\nconst cookieParser = __webpack_require__(/*! cookie-parser */ \"cookie-parser\");\nconst cors = __webpack_require__(/*! cors */ \"cors\");\nmodule.exports = function () {\n  let server = express(),\n    create,\n    start,\n    close;\n  create = function (config, db) {\n    try {\n      let routes = __webpack_require__(/*! ./routes */ \"./server/routes/index.js\");\n      const originalSend = server.response.send;\n\n      // Server settings\n      server.set('env', config.env);\n      server.set('port', config.port);\n      server.set('hostname', config.hostname);\n\n      // Returns middleware that parses json\n      server.use(helmet());\n      server.use(cors());\n      server.use(bodyParser.json());\n      server.use(bodyParser.urlencoded({\n        extended: false\n      }));\n      server.use(cookieParser());\n      server.response.send = function sendOverWrite(body) {\n        originalSend.call(this, body);\n        this.__custombody__ = body;\n      };\n      //DB connection\n      mongoose.connect(db.database, {\n        useNewUrlParser: true,\n        useUnifiedTopology: true,\n        autoIndex: true\n      });\n      // Set up routes\n      routes.init(server);\n    } catch (error) {\n      throw error;\n    }\n  };\n  start = function () {\n    try {\n      let hostname = server.get('hostname'),\n        port = server.get('port');\n      server.listen(port, function () {\n        console.log('Express server listening on - http://' + hostname + ':' + port);\n      });\n    } catch (error) {\n      throw error;\n    }\n  };\n  close = function (exit, code) {\n    try {\n      setTimeout(() => {\n        exit(code);\n      }, 100);\n    } catch (error) {\n      throw error;\n    }\n  };\n  return {\n    create: create,\n    start: start,\n    close: close\n  };\n};\n\n//# sourceURL=webpack://sample-app/./server/index.js?\n}");

/***/ }),

/***/ "./server/models/Movies.js":
/*!*********************************!*\
  !*** ./server/models/Movies.js ***!
  \*********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst mongoose = __webpack_require__(/*! mongoose */ \"mongoose\");\nconst MoviesSchema = new mongoose.Schema({\n  Title: {\n    type: String,\n    required: true\n  },\n  Year: {\n    type: Number\n  },\n  Runtime: {\n    type: String\n  },\n  Genre: [String],\n  Director: {\n    type: String\n  },\n  Writer: [String],\n  Actors: [String],\n  Plot: {\n    type: String\n  },\n  Language: [String],\n  Country: {\n    type: String\n  },\n  imdbRating: {\n    type: Number\n  },\n  imdbVotes: {\n    type: Number\n  },\n  imdbID: {\n    type: String\n  },\n  BoxOffice: {\n    type: String\n  },\n  Production: {\n    type: String\n  }\n}, {\n  collection: 'movies',\n  // explicitly link to your existing collection\n  strict: false // allows extra fields just in case\n});\nMoviesSchema.index({\n  Title: 'text',\n  Director: 'text',\n  Actors: 'text',\n  Plot: 'text'\n}, {\n  name: 'moviesIndex'\n});\nconst Movies = mongoose.model('Movies', MoviesSchema);\nmodule.exports = Movies;\n\n//# sourceURL=webpack://sample-app/./server/models/Movies.js?\n}");

/***/ }),

/***/ "./server/models/index.js":
/*!********************************!*\
  !*** ./server/models/index.js ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("{const Movies = __webpack_require__(/*! ./Movies */ \"./server/models/Movies.js\");\nmodule.exports = {\n  Movies: Movies\n};\n\n//# sourceURL=webpack://sample-app/./server/models/index.js?\n}");

/***/ }),

/***/ "./server/routes/apis/index.js":
/*!*************************************!*\
  !*** ./server/routes/apis/index.js ***!
  \*************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst express = __webpack_require__(/*! express */ \"express\");\nconst v1ApiController = __webpack_require__(/*! ./v1 */ \"./server/routes/apis/v1.js\");\nlet router = express.Router();\nrouter.use(\"/v1\", v1ApiController);\nmodule.exports = router;\n\n//# sourceURL=webpack://sample-app/./server/routes/apis/index.js?\n}");

/***/ }),

/***/ "./server/routes/apis/v1.js":
/*!**********************************!*\
  !*** ./server/routes/apis/v1.js ***!
  \**********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst moviesController = __webpack_require__(/*! ../../controllers/apis/movies */ \"./server/controllers/apis/movies.js\");\nconst express = __webpack_require__(/*! express */ \"express\");\nlet router = express.Router();\nrouter.use('/movies', moviesController);\nmodule.exports = router;\n\n//# sourceURL=webpack://sample-app/./server/routes/apis/v1.js?\n}");

/***/ }),

/***/ "./server/routes/home.js":
/*!*******************************!*\
  !*** ./server/routes/home.js ***!
  \*******************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst express = __webpack_require__(/*! express */ \"express\");\nconst homeController = __webpack_require__(/*! ../controllers/home */ \"./server/controllers/home.js\");\nlet router = express.Router();\nrouter.get(\"/\", homeController.index);\nmodule.exports = router;\n\n//# sourceURL=webpack://sample-app/./server/routes/home.js?\n}");

/***/ }),

/***/ "./server/routes/index.js":
/*!********************************!*\
  !*** ./server/routes/index.js ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst homeRoute = __webpack_require__(/*! ./home */ \"./server/routes/home.js\");\nconst apiRoute = __webpack_require__(/*! ./apis */ \"./server/routes/apis/index.js\");\nfunction init(server) {\n  server.get('*', function (req, res, next) {\n    console.log('Request was made to: ' + req.originalUrl);\n    return next();\n  });\n  server.get('/', function (req, res) {\n    res.redirect('/home');\n  });\n  server.use('/home', homeRoute);\n  server.use('/api', apiRoute);\n}\nmodule.exports = {\n  init: init\n};\n\n//# sourceURL=webpack://sample-app/./server/routes/index.js?\n}");

/***/ }),

/***/ "./server/services/filters/index.js":
/*!******************************************!*\
  !*** ./server/services/filters/index.js ***!
  \******************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst _ = __webpack_require__(/*! lodash */ \"lodash\");\nconst {\n  logger,\n  updateData\n} = __webpack_require__(/*! ../../../utils */ \"./utils/index.js\");\nconst {\n  Movies\n} = __webpack_require__(/*! ../../models */ \"./server/models/index.js\");\nfunction getFilterData(request, response) {\n  try {\n    let filter = request.query ? updateData(request.query) : {};\n    if (filter && filter.type) {\n      let type = filter.type;\n      switch (type) {\n        case \"movies\":\n          getModelData(Movies, filter, response, type, request);\n          break;\n        default:\n          break;\n      }\n    } else {\n      logger.debug(\"request params: \" + JSON.stringify(filter));\n      return response.send({\n        success: false,\n        message: \"Error: Bad Request, fiter type missing\"\n      });\n    }\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\nasync function getModelData(model, filter, response, type, request) {\n  try {\n    let order = 1;\n    let offset = 0;\n    let limit = 100;\n    let page_no = 0;\n    let qfilter = {};\n    if (filter && filter.order) {\n      order = filter.order == \"asc\" ? 1 : -1;\n    }\n    if (filter && filter.query) {\n      qfilter = {\n        $text: {\n          $search: filter.query,\n          $caseSensitive: false\n        }\n      };\n    } else if (filter && filter.qfilter) {\n      qfilter = filter.qfilter;\n    }\n    if (filter && filter.limit) {\n      limit = parseInt(filter.limit);\n    }\n    if (filter && filter.page) {\n      page_no = parseInt(filter.page);\n    }\n    offset = page_no > 1 ? page_no * limit : 0;\n    if (model) {\n      let result = await model.aggregate([{\n        $match: qfilter\n      }, {\n        $skip: offset\n      }, {\n        $sort: {\n          createdAt: order\n        }\n      }, {\n        $limit: limit\n      }]).then(docs => {\n        return docs;\n      });\n      let resp = {\n        list: result,\n        page: page_no,\n        next_page: 0\n      };\n      if (result) {\n        if (result.length == limit) {\n          resp.next_page = page_no + 1;\n        }\n        logger.debug(`${resp}`);\n        return response.send({\n          success: true,\n          data: resp,\n          message: `${type} list get suucessfully!`\n        });\n      } else {\n        return response.send({\n          success: true,\n          data: resp,\n          message: \"No Data Found!\"\n        });\n      }\n    } else {\n      logger.debug(\"request params: \" + JSON.stringify(filter));\n      return response.send({\n        success: false,\n        message: \"Error: Bad Request, data model missing\"\n      });\n    }\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\nmodule.exports = {\n  getFilterData: getFilterData,\n  getModelData: getModelData\n};\n\n//# sourceURL=webpack://sample-app/./server/services/filters/index.js?\n}");

/***/ }),

/***/ "./server/services/movies/createmovies.js":
/*!************************************************!*\
  !*** ./server/services/movies/createmovies.js ***!
  \************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst {\n  Movies\n} = __webpack_require__(/*! ../../models */ \"./server/models/index.js\");\nconst {\n  logger,\n  sendPolicyMail\n} = __webpack_require__(/*! ../../../utils */ \"./utils/index.js\");\nconst customId = __webpack_require__(/*! custom-id */ \"custom-id\");\nasync function saveMovies(request, response) {\n  try {\n    const params = request.body;\n    if (params) {\n      let keys = Object.keys(params);\n      let mandetoryKeys = [\"name\"];\n      let plst = keys.map(key => {\n        let val = params[key];\n        if (mandetoryKeys.indexOf(key) > -1 && val === \"\" || val === null) {\n          return key;\n        }\n      }).filter(item => {\n        return item && item != \"\";\n      });\n      if (plst.length) {\n        let msg = `Bad Request: ${plst.join(\",\")} should not be empty fields!`;\n        return response.send({\n          success: false,\n          message: msg\n        });\n      }\n    }\n    const cuId = customId({\n      name: params.name,\n      date: Date.now(),\n      randomLength: 2\n    });\n    params.id = `PY${cuId}`;\n    Movies.findOneAndUpdate(params, {\n      $set: params\n    }, {\n      upsert: true\n    }).then(doc => {\n      if (doc) {\n        logger.error(`${doc}`);\n        return response.send({\n          success: false,\n          message: \"Something wrong, Please try again!\"\n        });\n      } else {\n        return response.send({\n          success: true,\n          message: \"Movie details saved successfully!\"\n        });\n      }\n    }).catch(error => {\n      logger.error(`${error}`);\n      return response.send({\n        success: false,\n        message: `${error}`\n      });\n    });\n    // }\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\nmodule.exports = {\n  saveMovies: saveMovies\n};\n\n//# sourceURL=webpack://sample-app/./server/services/movies/createmovies.js?\n}");

/***/ }),

/***/ "./server/services/movies/deletemovies.js":
/*!************************************************!*\
  !*** ./server/services/movies/deletemovies.js ***!
  \************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst {\n  Movies\n} = __webpack_require__(/*! ../../models */ \"./server/models/index.js\");\nconst {\n  logger\n} = __webpack_require__(/*! ../../../utils */ \"./utils/index.js\");\nasync function deleteMovie(request, response) {\n  try {\n    let params = request.params;\n    if (params && !params.id) {\n      return response.send({\n        success: false,\n        message: \"Bad request: Movie id missing in request url!\"\n      });\n    }\n    let filter = {\n      id: params.id\n    };\n    await Movies.findOneAndDelete(filter).then(doc => {\n      if (!doc) {\n        return response.send({\n          success: false,\n          message: `No movie details found for id ${params.id}`\n        });\n      } else {\n        return response.send({\n          success: true,\n          message: \"Movie details deleted successfully!\"\n        });\n      }\n    }).catch(error => {\n      logger.error(`${error}`);\n      return response.send({\n        success: false,\n        message: `${error}`\n      });\n    });\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\n;\nmodule.exports = {\n  deleteMovie: deleteMovie\n};\n\n//# sourceURL=webpack://sample-app/./server/services/movies/deletemovies.js?\n}");

/***/ }),

/***/ "./server/services/movies/getmovies.js":
/*!*********************************************!*\
  !*** ./server/services/movies/getmovies.js ***!
  \*********************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst {\n  Movies\n} = __webpack_require__(/*! ../../models */ \"./server/models/index.js\");\nconst {\n  getModelData\n} = __webpack_require__(/*! ../filters */ \"./server/services/filters/index.js\");\nconst {\n  logger,\n  updateData,\n  getQueryFilter\n} = __webpack_require__(/*! ../../../utils */ \"./utils/index.js\");\nfunction getMovies(request, response) {\n  try {\n    let fdata = request.query ? updateData(request.query) : {};\n    fdata.qfilter = getQueryFilter(fdata);\n    getModelData(Movies, fdata, response, 'movies', request);\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\nmodule.exports = {\n  getMovies: getMovies\n};\n\n//# sourceURL=webpack://sample-app/./server/services/movies/getmovies.js?\n}");

/***/ }),

/***/ "./server/services/movies/index.js":
/*!*****************************************!*\
  !*** ./server/services/movies/index.js ***!
  \*****************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("{const {\n  getMovies\n} = __webpack_require__(/*! ./getmovies */ \"./server/services/movies/getmovies.js\");\nconst {\n  deleteMovie\n} = __webpack_require__(/*! ./deletemovies */ \"./server/services/movies/deletemovies.js\");\nconst {\n  saveMovies\n} = __webpack_require__(/*! ./createmovies */ \"./server/services/movies/createmovies.js\");\nconst {\n  updateMovies\n} = __webpack_require__(/*! ./updatemovies */ \"./server/services/movies/updatemovies.js\");\nmodule.exports = {\n  getMovies: getMovies,\n  deleteMovie: deleteMovie,\n  saveMovies: saveMovies,\n  updateMovies: updateMovies\n};\n\n//# sourceURL=webpack://sample-app/./server/services/movies/index.js?\n}");

/***/ }),

/***/ "./server/services/movies/updatemovies.js":
/*!************************************************!*\
  !*** ./server/services/movies/updatemovies.js ***!
  \************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst {\n  Movies\n} = __webpack_require__(/*! ../../models */ \"./server/models/index.js\");\nconst {\n  logger,\n  removeEmptyFields,\n  sendPolicyMail\n} = __webpack_require__(/*! ../../../utils */ \"./utils/index.js\");\nasync function updateMovies(request, response) {\n  try {\n    let obj = request.body;\n    let params = request.params;\n    if (params && !params.id) {\n      return response.send({\n        success: false,\n        message: \"Bad request: Movie id missing in request url!\"\n      });\n    }\n    if (params.id.length < 10) {\n      return response.send({\n        success: false,\n        message: `No Policy details found with id ${params.id}`\n      });\n    }\n    let filter = {\n      id: params.id\n    };\n    obj = removeEmptyFields(obj);\n    if (Object.keys(obj).length) {\n      await Movies.findOneAndUpdate(filter, {\n        $set: obj\n      }, {\n        upsert: true\n      }).then(doc => {\n        if (!doc) {\n          return response.send({\n            success: false,\n            message: `No movie details found with id ${params.id}`\n          });\n        } else {\n          sendPolicyMail(params);\n          return response.send({\n            success: true,\n            message: \"Movie details updated successfully!\"\n          });\n        }\n      }).catch(error => {\n        logger.error(`${error}`);\n        return response.send({\n          success: false,\n          message: `${error}`\n        });\n      });\n    } else {\n      return response.send({\n        success: false,\n        message: \"Movie details fields should not be empty!\"\n      });\n    }\n  } catch (error) {\n    logger.error(`${error}`);\n    return response.send({\n      success: false,\n      message: `${error}`\n    });\n  }\n}\nmodule.exports = {\n  updateMovies: updateMovies\n};\n\n//# sourceURL=webpack://sample-app/./server/services/movies/updatemovies.js?\n}");

/***/ }),

/***/ "./utils/index.js":
/*!************************!*\
  !*** ./utils/index.js ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst _ = __webpack_require__(/*! lodash */ \"lodash\");\nconst {\n  logger\n} = __webpack_require__(/*! ./logger */ \"./utils/logger.js\");\nfunction updateData(obj) {\n  try {\n    let keys = _.keys(obj);\n    let fobj = {};\n    _.forEach(keys, function (key) {\n      if (!isNaN(obj[key])) {\n        fobj[key] = parseInt(obj[key]);\n      } else {\n        fobj[key] = obj[key];\n      }\n    });\n    return fobj;\n  } catch (error) {\n    throw error;\n  }\n}\n// return query filter parameter object\nfunction getQueryFilter(filter) {\n  try {\n    let ingoreKeys = ['limit', 'order', 'page', 'query'];\n    let keys = _.keys(filter);\n    let qfilter = {};\n    _.forEach(keys, function (key) {\n      if (ingoreKeys.indexOf(key) == -1) {\n        qfilter[key] = filter[key];\n      }\n    });\n    return qfilter;\n  } catch (error) {\n    throw error;\n  }\n}\n\n// remove empty fields from object\nfunction removeEmptyFields(obj) {\n  for (var k in obj) {\n    if (!obj[k] || typeof obj[k] !== \"object\") {\n      if (obj[k] === null || obj[k] === undefined || obj[k] === \"\") {\n        delete obj[k];\n      }\n      continue;\n    }\n    removeEmptyFields(obj[k]);\n    if (Object.keys(obj[k]).length === 0) {\n      delete obj[k];\n    }\n  }\n  return obj;\n}\nmodule.exports = {\n  updateData: updateData,\n  logger: logger,\n  getQueryFilter: getQueryFilter,\n  removeEmptyFields: removeEmptyFields\n};\n\n//# sourceURL=webpack://sample-app/./utils/index.js?\n}");

/***/ }),

/***/ "./utils/logger.js":
/*!*************************!*\
  !*** ./utils/logger.js ***!
  \*************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";
eval("{\n\nconst winston = __webpack_require__(/*! winston */ \"winston\");\nconst rfs = __webpack_require__(/*! rotating-file-stream */ \"rotating-file-stream\");\n\n// create a rotating write stream\nlet activityLogStream = rfs.createStream('activity.log', {\n  interval: '1d',\n  // rotate daily\n  path: './log/'\n});\nmodule.exports = {\n  logger: new winston.createLogger({\n    transports: [new winston.transports.Stream({\n      stream: activityLogStream,\n      format: winston.format.combine(winston.format.timestamp(), winston.format.json())\n    })],\n    exitOnError: false\n  })\n};\n\n//# sourceURL=webpack://sample-app/./utils/logger.js?\n}");

/***/ }),

/***/ "./utils/terminate.js":
/*!****************************!*\
  !*** ./utils/terminate.js ***!
  \****************************/
/***/ ((module) => {

"use strict";
eval("{\n\nfunction terminate(server, options = {\n  coredump: false,\n  timeout: 500\n}) {\n  // Exit function\n  const exit = code => {\n    options.coredump ? process.abort() : process.exit(code);\n  };\n  return (code, reason) => (err, promise) => {\n    if (err && err instanceof Error) {\n      // Log error information, use a proper logging library here :)\n      console.error(`${err}`);\n    }\n\n    // Attempt a graceful shutdown\n    server.close(exit, code);\n    setTimeout(exit, options.timeout).unref();\n  };\n}\nmodule.exports = terminate;\n\n//# sourceURL=webpack://sample-app/./utils/terminate.js?\n}");

/***/ }),

/***/ "babel-polyfill":
/*!*********************************!*\
  !*** external "babel-polyfill" ***!
  \*********************************/
/***/ ((module) => {

"use strict";
module.exports = require("babel-polyfill");

/***/ }),

/***/ "body-parser":
/*!******************************!*\
  !*** external "body-parser" ***!
  \******************************/
/***/ ((module) => {

"use strict";
module.exports = require("body-parser");

/***/ }),

/***/ "cookie-parser":
/*!********************************!*\
  !*** external "cookie-parser" ***!
  \********************************/
/***/ ((module) => {

"use strict";
module.exports = require("cookie-parser");

/***/ }),

/***/ "cors":
/*!***********************!*\
  !*** external "cors" ***!
  \***********************/
/***/ ((module) => {

"use strict";
module.exports = require("cors");

/***/ }),

/***/ "custom-id":
/*!****************************!*\
  !*** external "custom-id" ***!
  \****************************/
/***/ ((module) => {

"use strict";
module.exports = require("custom-id");

/***/ }),

/***/ "express":
/*!**************************!*\
  !*** external "express" ***!
  \**************************/
/***/ ((module) => {

"use strict";
module.exports = require("express");

/***/ }),

/***/ "fs":
/*!*********************!*\
  !*** external "fs" ***!
  \*********************/
/***/ ((module) => {

"use strict";
module.exports = require("fs");

/***/ }),

/***/ "helmet":
/*!*************************!*\
  !*** external "helmet" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("helmet");

/***/ }),

/***/ "lodash":
/*!*************************!*\
  !*** external "lodash" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("lodash");

/***/ }),

/***/ "mongoose":
/*!***************************!*\
  !*** external "mongoose" ***!
  \***************************/
/***/ ((module) => {

"use strict";
module.exports = require("mongoose");

/***/ }),

/***/ "path":
/*!***********************!*\
  !*** external "path" ***!
  \***********************/
/***/ ((module) => {

"use strict";
module.exports = require("path");

/***/ }),

/***/ "rotating-file-stream":
/*!***************************************!*\
  !*** external "rotating-file-stream" ***!
  \***************************************/
/***/ ((module) => {

"use strict";
module.exports = require("rotating-file-stream");

/***/ }),

/***/ "winston":
/*!**************************!*\
  !*** external "winston" ***!
  \**************************/
/***/ ((module) => {

"use strict";
module.exports = require("winston");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./index.js");
/******/ 	
/******/ })()
;