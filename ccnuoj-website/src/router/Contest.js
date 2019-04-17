import asyncLoad from '../components/async-load';

const ContestPage = asyncLoad(import('../views/Contest/ContestPage'));
const ContestList = asyncLoad(import('../views/Contest/ContestList'));
const ContestDetail = asyncLoad(import('../views/Contest/ContestDetail'));
const ContestRank = asyncLoad(import('../views/Contest/ContestRank'));
const ContestProblemList = asyncLoad(import('../views/Contest/Problem/ContestProblemList'));
const ContestProblemDetail = asyncLoad(import('../views/Contest/Problem/ContestProblemDetail'));

const ContestText = asyncLoad(import('../views/Contest/ContestText'));
const ContestTextEditor = asyncLoad(import('../views/Contest/ContestTextEditor'));
const ContestRegisterStateDisplay = asyncLoad(import('../views/Contest/Register/ContestRgisterStateDisplay'));
const ContestRegisterAllList = asyncLoad(import('../views/Contest/Register/ContestRegisterAllList'));
const ContestRegisterPassedList = asyncLoad(import('../views/Contest/Register/ContestRegisterPassedList'));

export default [
  {
    path: '/contest',
    component: ContestPage,
    children: [
      {
        path: '',
        redirect: 'list',
      },
      {
        path: 'list',
        name: 'ContestList',
        component: ContestList,
      },
      {
        path: ':contest_id',
        component: ContestDetail,
        children: [
          {
            path: '',
            redirect: 'introduction',
          },
          {
            path: 'introduction',
            name: 'ContestText',
            component: ContestText,
          },
          {
            path: 'introduction/editor',
            name: 'ContestTextEditor',
            component: ContestTextEditor,
          },
          {
            path: 'register',
            name: 'ContestRegisterStateDisplay',
            component: ContestRegisterStateDisplay,
          },
          {
            path: 'register/all/list',
            name: 'ContestRegisterAllList',
            component: ContestRegisterAllList,
          },
          {
            path: 'register/passed/list',
            name: 'ContestRegisterPassedList',
            component: ContestRegisterPassedList,
          },
          {
            path: 'problem',
            children: [
              {
                path: '',
                redirect: 'list',
              },
              {
                path: 'list',
                name: 'ContestProblemList',
                component: ContestProblemList,
              },
              {
                path: ':problem_id',
                name: 'ContestProblemDetail',
                component: ContestProblemDetail,
              },
            ],
          },
          {
            path: 'rank',
            name: 'ContestRank',
            component: ContestRank,
          },
        ],
      },
    ],
  },
];
