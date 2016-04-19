var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'build');
var APP_DIR = path.resolve(__dirname, 'app');

var config = {
  entry: {
    javascript: APP_DIR + '/index.jsx',
    html: APP_DIR + '/index.html',
  },
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  module : {
    loaders : [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        loader: 'babel',
      },
      {
        test: /\.html$/,
        include: APP_DIR,
        loader: 'file?name=[name].[ext]',
      }
    ]
  }
};

module.exports = config;