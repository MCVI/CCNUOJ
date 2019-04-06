import request from './request';

export const getContestRegister = (contestID, userID) => new Promise((resolve, reject) => {
  request.get(`/contest/id/${contestID}/register/user/id/${userID}`)
    .then((response) => {
      resolve(response.data.result);
    })
    .catch((error) => {
      if ('response' in error) {
        const data = error.response.data;
        if ('reason' in data) {
          reject(data.reason);
        } else {
          reject('UnknownError');
        }
      } else {
        reject('NetworkError');
      }
    });
});

export const createContestRegister = (contestID, userID, registerInfo) => new Promise((resolve, reject) => {
  request.post(`/contest/id/${contestID}/register/user/id/${userID}`, registerInfo)
    .then((response) => {
      resolve({
        registerTime: response.data.registerTime,
      });
    })
    .catch((error) => {
      if ('response' in error) {
        const data = error.response.data;
        if ('reason' in data) {
          reject(data.reason);
        } else {
          reject('UnknownError');
        }
      } else {
        reject('NetworkError');
      }
    });
});

export const updateContestRegister = (contestID, userID, registerInfo) => new Promise((resolve, reject) => {
  request.put(`/contest/id/${contestID}/register/user/id/${userID}`, registerInfo)
    .then((response) => {
      resolve({
        registerTime: response.data.registerTime,
      });
    })
    .catch((error) => {
      if ('response' in error) {
        const data = error.response.data;
        if ('reason' in data) {
          reject(data.reason);
        } else {
          reject('UnknownError');
        }
      } else {
        reject('NetworkError');
      }
    });
});

export const deleteContestRegister = (contestID, userID) => new Promise((resolve, reject) => {
  request.delete(`/contest/id/${contestID}/register/user/id/${userID}`)
    .then((response) => {
      resolve();
    })
    .catch((error) => {
      if ('response' in error) {
        const data = error.response.data;
        if ('reason' in data) {
          reject(data.reason);
        } else {
          reject('UnknownError');
        }
      } else {
        reject('NetworkError');
      }
    });
});

export const updateContestRegisterPassState = (contestID, userID, passed) => new Promise(
  (resolve, reject) => {
    request.put(`/contest/id/${contestID}/register/user/id/${userID}/passed`, {
      passed,
    })
      .then((response) => {
        resolve();
      })
      .catch((error) => {
        if ('response' in error) {
          const data = error.response.data;
          if ('reason' in data) {
            reject(data.reason);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);

export const getContestRegisterAllList = (contestID, pageNum) => new Promise(
  (resolve, reject) => {
    request.get(`/contest/id/${contestID}/register/filter/all/page/${pageNum}`)
      .then((response) => {
        resolve(response.data.result);
      })
      .catch((error) => {
        if ('response' in error) {
          const data = error.response.data;
          if ('reason' in data) {
            reject(data.reason);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);

export const getContestRegisterPassedList = (contestID, pageNum) => new Promise(
  (resolve, reject) => {
    request.get(`/contest/id/${contestID}/register/filter/passed/page/${pageNum}`)
      .then((response) => {
        resolve(response.data.result);
      })
      .catch((error) => {
        if ('response' in error) {
          const data = error.response.data;
          if ('reason' in data) {
            reject(data.reason);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);
