const ContestPage = () => import('../views/Contest/ContestPage');
const ContestList = () => import('../views/Contest/ContestList');
const ContestDetail = () => import('../views/Contest/ContestDetail');
const ContestRank = () => import('../views/Contest/ContestRank');
const ContestProblemList = () => import('../views/Contest/Problem/ContestProblemList');
const ContestProblemDetail = () => import('../views/Contest/Problem/ContestProblemDetail');

const ContestText = () => import('../views/Contest/ContestText');
const ContestTextEditor = () => import('../views/Contest/ContestTextEditor');
const ContestRegisterStateDisplay = () => import('../views/Contest/Register/ContestRgisterStateDisplay');
const ContestRegisterAllList = () => import('../views/Contest/Register/ContestRegisterAllList');
const ContestRegisterPassedList = () => import('../views/Contest/Register/ContestRegisterPassedList');

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
