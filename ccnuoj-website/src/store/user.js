import {
  userLoginByEmail,
  userLoginByShortName,
  userAuthEcho,
  getUserInfo,
  updateUserInfo,
} from '@/api/User';

const UserModule = {
  namespaced: true,

  state: {
    loginState: undefined,
    detailInfo: undefined,
  },

  getters: {
    id: (state) => {
      if (state.loginState === undefined) {
        return undefined;
      } else if (state.loginState === null) {
        return null;
      } else {
        return state.loginState.id;
      }
    },
    email: (state) => {
      if (state.loginState === undefined) {
        return undefined;
      } else if (state.loginState === null) {
        return null;
      } else {
        return state.loginState.email;
      }
    },
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
    isSuper: (state) => {
      if (state.loginState === undefined) {
        return undefined;
      } else if (state.loginState === null) {
        return null;
      } else {
        return state.loginState.isSuper;
      }
    },
    detailInfo: (state) => {
      if (state.detailInfo === undefined) {
        return undefined;
      } else if (state.detailInfo === null) {
        return null;
      } else {
        return state.detailInfo;
      }
    },
  },

  mutations: {
    changeLoginState(state, newState) {
      state.loginState = newState;
      if ((typeof newState === 'object') && (newState !== null)) {
        const token = newState.token;
        localStorage.setItem('UserLoginToken', token);
        state.detailInfo = undefined;
      } else if (newState === null) {
        localStorage.removeItem('UserLoginToken');
        state.detailInfo = null;
      }
    },
    changeDetailInfo(state, info) {
      state.detailInfo = info;
    },
  },

  actions: {
    loginByEmail({ commit }, { email, password }) {
      return new Promise((resolve, reject) => {
        userLoginByEmail({ email, password })
          .then((loginInfo) => {
            commit('changeLoginState', loginInfo);
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
            commit('changeLoginState', loginInfo);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    logout({ commit }) {
      commit('changeLoginState', null);
    },
    loadLocalToken({ commit }) {
      return new Promise((resolve, reject) => {
        const token = localStorage.getItem('UserLoginToken');
        if (token === null) {
          commit('changeLoginState', null);
          resolve(null);
        } else {
          userAuthEcho(token)
            .then((state) => {
              commit('changeLoginState', state);
              resolve(state);
            })
            .catch((error) => {
              commit('changeLoginState', null);
              reject(null);
            });
        }
      });
    },
    getDetailInfo({ commit, getters }) {
      return new Promise((resolve, reject) => {
        if (getters.detailInfo === undefined) {
          if (getters.id === undefined) {
            commit('changeDetailInfo', undefined);
            resolve(getters.detailInfo);
          } else {
            getUserInfo(getters.id)
              .then((result) => {
                commit('changeDetailInfo', {
                  realPersonInfo: result.realPersonInfo,
                  extraInfo: result.extraInfo,
                  createTime: result.createTime,
                });
                resolve(getters.detailInfo);
              })
              .catch((error) => {
                reject(error);
              });
          }
        } else {
          resolve(getters.detailInfo);
        }
      });
    },
    updateDetailInfo({ commit, getters }, info) {
      return new Promise((resolve, reject) => {
        if ((getters.id === undefined) || (getters.id === null)) {
          reject('NotLoggedIn');
        } else {
          updateUserInfo(getters.id, info)
            .then((result) => {
              commit('changeDetailInfo', info);
              resolve(result);
            })
            .catch((error) => {
              reject(error);
            });
        }
      });
    },
  },
};

export default UserModule;
