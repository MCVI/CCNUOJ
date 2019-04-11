import request from './request';

export const getProblemList = (pageNum) => new Promise(
  (resolve, reject) => {
    request.get(`/problem/page/${pageNum}`)
      .then((response) => {
        const problemList = response.data.result;
        resolve(problemList);
      })
      .catch((error) => {
        reject(error);
      });
  },
);

export const getProblem = (problemID) => new Promise(
  (resolve, reject) => {
    request.get(`/problem/id/${problemID}`)
      .then((response) => {
        const problemList = response.data.result;
        resolve(problemList);
      })
      .catch((error) => {
        reject(error);
      });
  },
);

export const createProblem = (problemData) => new Promise(
  (resolve, reject) => {
    request.post('/problem', problemData)
      .then((response) => {
        resolve(response.data);
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
  },
);

export const updateProblem = (problemID, problemData) => new Promise(
  (resolve, reject) => {
    request.put(`/problem/id/${problemID}`, problemData)
      .then((response) => {
        resolve(response.data);
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
  },
);
