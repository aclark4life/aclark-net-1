module.exports = {
    entry: './aclark/root/static/index.js',
    output: {
        path: __dirname + '/aclark/root/static/webpack_bundles',
        filename: "[name]-[hash].js"
    },
}