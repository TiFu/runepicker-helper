const path = require('path')

const commonConfig = {
  node: {
    __dirname: false
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader'
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.ts', '.tsx', '.jsx', '.json']
  }
}

const HtmlWebpackPlugin = require('html-webpack-plugin')
module.exports = [
  Object.assign(
    {
      output: {
        path: path.resolve(__dirname, 'dist/electron'),
        filename: '[name].js'
      },
      target: 'electron-main',
      entry: { main: './src/electron.ts' }
    },
    commonConfig),
  Object.assign(
    {
      output: {
        path: path.resolve(__dirname, 'dist/electron'),
        filename: '[name].js'
      },      target: 'electron-renderer',
      entry: { index: './src/index.tsx' },
      plugins: [new HtmlWebpackPlugin()]
    },
    commonConfig),
  Object.assign(
    {  output: {
      path: path.resolve(__dirname, 'dist/web'),
      filename: '[name].js'
    },
      target: "web",
      entry: { index: "./src/index.tsx"},
      plugins: []
    }, commonConfig
  )
]
