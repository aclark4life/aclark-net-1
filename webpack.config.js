var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './aclark/root/static/index',
    output: {
        path: path.resolve('./aclark/root/static/webpack_bundles/'),
        filename: "[name]-[hash].js"
    },

    plugins: [
        new BundleTracker({
            filename: './webpack-stats.json'
        })
    ]
}

new webpack.ProvidePlugin({
    $: 'jquery',
    jQuery: 'jquery'
});