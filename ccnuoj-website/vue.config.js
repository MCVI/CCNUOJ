module.exports = {
  configureWebpack: (config) => {
    // eslint-disable-next-line no-param-reassign
    config.externals = {
      'core-js': 'core',

      vue: 'Vue',
      'vue-router': 'VueRouter',
      vuex: 'Vuex',
      'element-ui': 'ELEMENT',

      axios: 'axios',
      'crypto-js': 'CryptoJS',
      validator: 'validator',

      marked: 'marked',
      'highlight.js': 'hljs',

    };
  },
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
