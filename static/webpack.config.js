const webpack = require('webpack');
const path = require('path');

const config = {
    entry: path.join(__dirname, '/js/index.jsx'),
    output: {
        path: path.join(__dirname, '/public'),
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css', '.scss']
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.(png|jpg)$/,
                loader: 'url-loader?limit-8192'
            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            }
        ]
    }
};

module.exports = config;