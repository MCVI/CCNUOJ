import request from './request';

import * as PasswordHash from './PasswordHash';

export const userRegister = ({
  email,
  shortName,
  realPersonInfo,
  extraInfo,
  password,
}) => {
  const salt = PasswordHash.generateRandomSalt();
  const hashResult = PasswordHash.passwordHash(salt, password);
  const requestData = {
    email,
    shortName,
    realPersonInfo,
    extraInfo,
    authentication: {
      salt,
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
          const data = error.response.data;
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

const userLoginInternal = ({
  authInfo,
  password,
}) => {
  const id = authInfo.id;
  const salt = authInfo.salt;
  const hashResult = PasswordHash.passwordHash(salt, password);
  return new Promise((resolve, reject) => {
    request.post(`/user/authentication/id/${id}`, { hashResult })
      .then((res) => {
        resolve(res.data.result);
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

export const authEcho = (token) => new Promise((resolve, reject) => {
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
