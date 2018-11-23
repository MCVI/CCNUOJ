import request from './request';

export const getProblemList = (pageNum) => new Promise(
  (resolve, reject) => {
    request.get(`/problem/page/${pageNum}`)
      .then((response) => {
        const problemList = response.data.result;
        resolve(problemList);
      })
      .catch((error) => {
        console.log(error);
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
