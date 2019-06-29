var BundleTracker = require("webpack-bundle-tracker");
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var webpack = require("webpack");

module.exports = {
    context: __dirname + "/aclark/root/static",
    entry: "./index",
    output: {
        path: __dirname + "/aclark/root/static/webpack_bundles",
        filename: "[name]-[hash].js"
    },
    plugins: [
        new BundleTracker({
            filename: './webpack-stats.json'
        }),
        new ExtractTextPlugin("[name]-[hash].css"),
        // http://getbootstrap.com/docs/4.0/getting-started/webpack/#importing-javascript
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Popper: ['popper.js', 'default'],
        }),
        new webpack.SourceMapDevToolPlugin({
            filename: '[name].js.map',
            exclude: ['bootstrap.js']
        })
    ],
    // https://github.com/webpack-contrib/extract-text-webpack-plugin#usage
    module: {
        rules: [{
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "url-loader?limit=10000&mimetype=application/font-woff"
            },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file-loader"
            },
        ],
    },
};
