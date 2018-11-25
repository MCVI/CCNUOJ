import request from './request';

export const getContestList = () => new Promise((resolve, reject) => {
  request.get('/contest/list')
    .then((response) => {
      resolve(response.data.result);
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
