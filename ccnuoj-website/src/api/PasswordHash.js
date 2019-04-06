import CryptoJS from 'crypto-js/crypto-js';

import request from './request';

const saltAvailableChar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

const generateRandomSaltString = () => {
  const r = saltAvailableChar.length;
  const length = 8;

  return 'x'.repeat(length).replace(
    /x/g,
    (c) => {
      const index = (Math.random() * r) % r;
      return saltAvailableChar.charAt(index);
    },
  );
};

export const generateRandomSalt = () => ({
  front: generateRandomSaltString(),
  back: generateRandomSaltString(),
});

export const passwordHash = (randomSalt, fixedSalt, password) => {
  const plain = [
    randomSalt.front,
    fixedSalt.fixed,
    password,
    randomSalt.back,
  ].join('-');
  return CryptoJS.SHA512(plain).toString();
};

let fixedSalt;

export const fetchFixedSalt = () => new Promise(
  (resolve, reject) => {
    if (fixedSalt === undefined) {
      request.get('/user/authentication_info/fixed_salt')
        .then((response) => {
          fixedSalt = response.data.result;
          resolve(fixedSalt);
        })
        .catch((error) => {
          if ('response' in error) {
            const { data } = error.response;
            if ('reason' in data) {
              reject(data.reason);
            } else {
              reject('UnknownError');
            }
          } else {
            reject('NetworkError');
          }
        });
    } else {
      resolve(fixedSalt);
    }
  },
);
