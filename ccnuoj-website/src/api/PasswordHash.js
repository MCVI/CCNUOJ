import CryptoJS from 'crypto-js/crypto-js';
import { CCNU_PASSWORD_FIXED_SALT } from './common';

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

export const passwordHash = (randomSalt, password) => {
  const plain = [
    randomSalt.front,
    CCNU_PASSWORD_FIXED_SALT,
    password,
    randomSalt.back,
  ].join('-');
  return CryptoJS.SHA512(plain).toString();
};
