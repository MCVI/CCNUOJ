import Vue from 'vue';
import Vuex from 'vuex';

import UserModule from './user';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user: UserModule,
  },
});
