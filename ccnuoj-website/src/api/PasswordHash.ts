import {CCNU_PASSWORD_FIXED_SALT} from "./common";
import CryptoJS from "crypto-js/crypto-js";

const saltAvailableChar = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

export interface RandomSalt {
  front: string;
  back: string;
}

const generateRandomSaltString = (): string => {
  const r = saltAvailableChar.length;
  const length = 8;

  return "x".repeat(length).replace(
    /x/g,
    (c: string): string => {
      const index = (Math.random() * r) % r;
      return saltAvailableChar.charAt(index);
    },
  );
};

export const generateRandomSalt = (): RandomSalt => {
  return {
    front: generateRandomSaltString(),
    back: generateRandomSaltString(),
  };
};

export const passwordHash = (randomSalt: RandomSalt, password: string): string => {
  const plain: string = [
    randomSalt.front,
    CCNU_PASSWORD_FIXED_SALT,
    password,
    randomSalt.back,
  ].join("-");
  return CryptoJS.SHA512(plain).toString();
};
