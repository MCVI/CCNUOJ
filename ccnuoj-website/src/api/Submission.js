import request from './request';

export const createSubmission = (problemID, language, code) => new Promise(
  (resolve, reject) => {
    request.post('/submission', {
      problemID,
      language,
      text: code,
    })
      .then((response) => {
        const { data } = response;
        resolve({
          submissionID: data.submissionID,
          judgeRequestID: data.judgeRequestID,
        });
      })
      .catch((error) => {
        if ('response' in error) {
          const { data } = error.response;
          if ('reason' in data) {
            reject(error);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);

export const getSubmissionList = (pageNum) => new Promise(
  (resolve, reject) => {
    request.get(`/submission/page/${pageNum}`)
      .then((response) => {
        const problemList = response.data.result;
        resolve(problemList);
      })
      .catch((error) => {
        if ('response' in error) {
          const { data } = error.response;
          if ('reason' in data) {
            reject(error);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);

export const getSubmission = (submissionID) => new Promise(
  (resolve, reject) => {
    request.get(`/submission/id/${submissionID}`)
      .then((response) => {
        const problemList = response.data.result;
        resolve(problemList);
      })
      .catch((error) => {
        if ('response' in error) {
          const { data } = error.response;
          if ('reason' in data) {
            reject(error);
          } else {
            reject('UnknownError');
          }
        } else {
          reject('NetworkError');
        }
      });
  },
);
