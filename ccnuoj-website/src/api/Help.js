import request from './request';

export const getPredictById = (id) => new Promise((resolve, reject) => {
  request.get(`/help/predict/${id}`)
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
