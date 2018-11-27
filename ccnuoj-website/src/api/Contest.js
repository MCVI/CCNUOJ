import request from './request';

export const getContest = (contestID) => new Promise((resolve, reject) => {
  request.get(`/contest/id/${contestID}`)
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

export const getContestList = () => new Promise((resolve, reject) => {
  request.get('/contest/list')
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

export const updateContestText = (contestID, text) => new Promise((resolve, reject) => {
  request.put(`/contest/id/${contestID}/text`, { text })
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
