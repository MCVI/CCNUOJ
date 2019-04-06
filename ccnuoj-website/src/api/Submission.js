import request from './request';

export const createSubmission = (problemID, language, code) => new Promise(
  (resolve, reject) => {
    request.post('/submission', {
      problemID,
      language,
      text: code,
    })
      .then((response) => {
        const data = response.data;
        resolve({
          submissionID: data.submissionID,
          judgeRequestID: data.judgeRequestID,
        });
      })
      .catch((error) => {
        if ('response' in error) {
          const data = error.response.data;
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
