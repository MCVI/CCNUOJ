import asyncLoad from '../components/async-load';

const ProblemList = asyncLoad(import('../views/Problem/ProblemList'));
const ProblemDetail = asyncLoad(import('../views/Problem/ProblemDetail'));
const ProblemEditor = asyncLoad(import('../views/Problem/ProblemEditor'));

export default [
  {
    path: '/problem',
    redirect: 'problem/list',
  },
  {
    path: '/problem/list',
    name: 'ProblemList',
    component: ProblemList,
  },
  {
    path: '/problem/:problem_id(\\d+)',
    name: 'ProblemDetail',
    component: ProblemDetail,
  },
  {
    path: '/problem/:problem_id(\\d+)/editor',
    name: 'UpdateProblem',
    component: ProblemEditor,
    props: true,
  },
  {
    path: '/problem/new/editor',
    name: 'CreateProblem',
    component: ProblemEditor,
    props: {
      problem_id: null,
    },
  },
];
