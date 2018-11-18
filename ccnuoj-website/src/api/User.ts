import axios from "axios";
import * as validator from "validator";

import { BASE_URI, AUTH_TOKEN_HEADER_NAME } from "./common";
import * as PasswordHash from "./PasswordHash";
import { RandomSalt } from "./PasswordHash";

export interface UserLoginInfo {
  id: number;
  email: string;
  shortName: string;
  token: string;
}

export const userRegister = (param: {
  email: string;
  shortName: string;
  realPersonInfo: string;
  extraInfo: string;
  password: string;
}): Promise<number> => {
  const salt: RandomSalt = PasswordHash.generateRandomSalt();
  const hashResult: string = PasswordHash.passwordHash(salt, param.password);
  const requestData: object = {
    email: param.email,
    shortName: param.shortName,
    realPersonInfo: param.realPersonInfo,
    extraInfo: param.extraInfo,
    authentication: {
      salt: salt,
      hashResult: hashResult,
    },
  };
  return new Promise<number>((resolve, reject) => {
    axios.post(BASE_URI + "/user", requestData)
      .then((response) => {
        resolve(response.data.userID);
      })
      .catch((error) => {
        console.log(error);
      },
    );
  });
};

export const userLogin = (param: {
  account: string;
  password: string;
}): Promise<UserLoginInfo> => {

  return new Promise<UserLoginInfo>((resolve, reject) => {

    const authById = (response) => {
      const id: number = response.data.result.id;
      const salt: RandomSalt = response.data.result.salt;
      axios.get(BASE_URI + "/user/authentication/id/" + id)
        .then((res) => {
          resolve(res.data.result);
        });
    };

    if (validator.isEmail(param.account)) {
      const email: string = param.account;
      axios.get(BASE_URI + "/user/authentication_info/email/" + email)
        .then((response) => {
          authById(response);
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      const shortName: string = param.account;
      axios.get(BASE_URI + "/user/authentication_info/shortName/" + shortName)
        .then((response) => {
          authById(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  });
};

export const authEcho = (token: string): Promise<UserLoginInfo> => {
  return new Promise<UserLoginInfo>((resolve, reject) => {
    axios.get(BASE_URI+"/user/authentication/echo", {
      headers: {
        AUTH_TOKEN_HEADER_NAME: token,
      },
    })
      .then((response) => {
        resolve(response.data.result);
      })
      .catch((error) => {
        console.log(error);
      });
  });
};
