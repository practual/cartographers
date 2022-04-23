const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');

const cssScopedNameFormat = '[name]__[local]--[hash:base64:5]';

module.exports = {
    mode: 'development',
    plugins: [new MiniCssExtractPlugin()],
    output: {
        path: path.resolve(__dirname, 'static'),
    },
    module: {
        rules: [{
            test: /\.m?js$/,
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader',
                options: {
                    presets: [
                        '@babel/preset-react',
                    ],
                    plugins: [
                        // See https://github.com/gajus/babel-plugin-react-css-modules/issues/291
                        // for issue leading to use of fork.
                        ['@dr.pogodin/react-css-modules', {
                           generateScopedName: cssScopedNameFormat,
                        }],
                    ],
                },
            },
        }, {
             test: /\.css$/,
             use: [{
                 loader: MiniCssExtractPlugin.loader,
             }, {
                 loader: 'css-loader',
                 options: {
                     modules: {
                         localIdentName: cssScopedNameFormat,
                     },
                 },
             },
             'sass-loader',
             ],
        }],
    },
};

