"use strict";

function index(request, response) {
  response.json({ message: "this is home route" });
}

module.exports = {
  index: index,
};