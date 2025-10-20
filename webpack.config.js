const path = require('path');

module.exports = {
  entry: './leadgen/static/js/main.jsx',
  output: {
    path: path.resolve(__dirname, 'leadgen/static/js'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  mode: 'development',
  devtool: 'source-map',
};
