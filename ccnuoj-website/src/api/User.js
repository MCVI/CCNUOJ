import request from './request';

import * as PasswordHash from './PasswordHash';

const userRegisterWithFixedSalt = (fixedSalt, userInfo) => {
  const randomSalt = PasswordHash.generateRandomSalt();
  const hashResult = PasswordHash.passwordHash(
    randomSalt,
    fixedSalt,
    userInfo.password,
  );

  const requestData = {
    email: userInfo.email,
    shortName: userInfo.shortName,
    realPersonInfo: userInfo.realPersonInfo,
    extraInfo: userInfo.extraInfo,
    authentication: {
      salt: randomSalt,
      hashResult,
    },
  };
  return new Promise((resolve, reject) => {
    request.post('/user', requestData)
      .then((response) => {
        resolve(response.data.userID);
      })
      .catch((error) => {
        if ('response' in error) {
          const { data } = error.response;
          if ('reason' in data) {
            console.log(['reason', data.reason]);
            reject(data.reason);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  });
};

export const userRegister = ({
  email,
  shortName,
  realPersonInfo,
  extraInfo,
  password,
}) => {
  const userInfo = {
    email,
    shortName,
    realPersonInfo,
    extraInfo,
    password,
  };

  return new Promise((resolve, reject) => {
    PasswordHash.fetchFixedSalt()
      .then((fixedSalt) => {
        userRegisterWithFixedSalt(fixedSalt, userInfo)
          .then((userID) => {
            resolve(userID);
          })
          .catch((error) => {
            reject(error);
          });
      })
      .catch((error) => {
        reject(error);
      });
  });
};

const userLoginInternal = ({
  authInfo,
  password,
}) => {
  const { id, salt } = authInfo;
  return new Promise((resolve, reject) => {
    PasswordHash.fetchFixedSalt()
      .then((fixedSalt) => {
        const hashResult = PasswordHash.passwordHash(salt, fixedSalt, password);
        request.post(`/user/authentication/id/${id}`, { hashResult })
          .then((res) => {
            resolve(res.data.result);
          })
          .catch((error) => {
            reject(error);
          });
      })
      .catch((error) => {
        reject(error);
      });
  });
};

export const userLoginByEmail = ({
  email,
  password,
}) => new Promise((resolve, reject) => {
  request.get(`/user/authentication_info/email/${email}`)
    .then((response) => {
      userLoginInternal({
        authInfo: response.data.result,
        password,
      })
        .then((newState) => {
          resolve(newState);
        })
        .catch((error) => {
          reject(error);
        });
    })
    .catch((error) => {
      reject(error);
    });
});

export const userLoginByShortName = ({
  shortName,
  password,
}) => new Promise((resolve, reject) => {
  request.get(`/user/authentication_info/shortName/${shortName}`)
    .then((response) => {
      userLoginInternal({
        authInfo: response.data.result,
        password,
      })
        .then((newState) => {
          resolve(newState);
        })
        .catch((error) => {
          reject(error);
        });
    })
    .catch((error) => {
      reject(error);
    });
});

export const userAuthEcho = (token) => new Promise((resolve, reject) => {
  request.get('/user/authentication/echo', {
    headers: {
      'X-CCNU-AUTH-TOKEN': token,
    },
  })
    .then((response) => {
      resolve(response.data.result);
    })
    .catch((error) => {
      reject(error);
    });
});

export const getUserInfo = (userID) => new Promise((resolve, reject) => {
  request.get(`/user/id/${userID}`)
    .then((response) => {
      resolve(response.data.result);
    })
    .catch((error) => {
      if ('response' in error) {
        const { data } = error.response;
        reject(data.reason);
      } else {
        reject('NetworkError');
      }
    });
});

export const updateUserInfo = (userID, userInfo) => new Promise((resolve, reject) => {
  request.put(`/user/id/${userID}/detail_info`, userInfo)
    .then((response) => {
      resolve(response.data.result);
    })
    .catch((error) => {
      if ('response' in error) {
        const { data } = error.response;
        reject(data.reason);
      } else {
        reject('NetworkError');
      }
    });
});
