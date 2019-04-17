import asyncLoad from '../components/async-load';

const SubmissionList = asyncLoad(import('../views/Submission/SubmissionList'));

export default [
  {
    path: '/submission/list',
    name: 'SubmissionList',
    component: SubmissionList,
  },
];
