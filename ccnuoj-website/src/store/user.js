import { userLoginByEmail, userLoginByShortName } from '@/api/User';

const UserModule = {
  namespaced: true,

  state: {
    loginState: undefined,
  },

  getters: {
    token: (state) => {
      if (state.loginState === undefined) {
        return undefined;
      } else if (state.loginState === null) {
        return null;
      } else {
        return state.loginState.token;
      }
    },
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
