import { userLoginByEmail, userLoginByShortName, userAuthEcho } from '@/api/User';

const UserModule = {
  namespaced: true,

  state: {
    loginState: undefined,
  },

  getters: {
    shortName: (state) => {
      if (state.loginState === undefined) {
        return undefined;
      } else if (state.loginState === null) {
        return null;
      } else {
        return state.loginState.shortName;
      }
    },
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
      if ((typeof newState === 'object') && (newState !== null)) {
        const token = newState.token;
        localStorage.setItem('UserLoginToken', token);
      } else if (newState === null) {
        localStorage.removeItem('UserLoginToken');
      }
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
    logout({ commit }) {
      commit('changeState', null);
    },
    loadLocalToken({ commit }) {
      return new Promise((resolve, reject) => {
        const token = localStorage.getItem('UserLoginToken');
        if (token === null) {
          commit('changeState', null);
          resolve(null);
        } else {
          userAuthEcho(token)
            .then((state) => {
              commit('changeState', state);
              resolve(state);
            })
            .catch((error) => {
              commit('changeState', null);
              reject(null);
            });
        }
      });
    },
  },
};

export default UserModule;
