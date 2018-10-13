// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Vue from 'vue'
import App from './App'
import router from './router/index'
import VueResource from 'vue-resource'

// v-xxx 绑定  （自定义指令）

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  // components: { App },
  router,
  render: h => h(App),
  template: '<App/>'
}).$mount('#app')
