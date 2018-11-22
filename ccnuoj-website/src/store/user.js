import { userLoginByEmail, userLoginByShortName } from '@/api/User';

const UserModule = {
  namespaced: true,

  state: {
    loginState: null,
  },

  mutations: {
    changeState(state, newState) {
      state.loginState = newState;
    },
  },

  actions: {
    loginByEmail({ commit }, { email, password }) {
      return new Promise((resolve, reject) => {
        userLoginByEmail({ email, password })
          .then((loginInfo) => {
            commit('changeState', loginInfo);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    loginByShortName({ commit }, { shortName, password }) {
      return new Promise((resolve, reject) => {
        userLoginByShortName({ shortName, password })
          .then((loginInfo) => {
            commit('changeState', loginInfo);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },
};

export default UserModule;
