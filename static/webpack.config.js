const webpack = require('webpack');
const path = require('path');

module.exports = (env) => {
    return {
        entry: path.join(__dirname, '/src/index.jsx'),
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
        },
        plugins: [
            new webpack.DefinePlugin({ "process.env.API_URL": JSON.stringify(`${env.API_URL}`) })
        ]
    };
};
