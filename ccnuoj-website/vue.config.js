module.exports = {
  devServer: {
    open: true,
    host: 'localhost',
    port: 8080,
    https: false,
    proxy: {
      '/api': {
        target: 'http://localhost:5000/',
        secure: false,
        changOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
};
