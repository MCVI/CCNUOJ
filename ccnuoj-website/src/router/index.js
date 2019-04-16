import Vue from 'vue';
import Router from 'vue-router';

import NotFoundPage from '../views/NotFoundPage';

import HomePage from '../views/HomePage';

import UserPage from '../views/User/UserPage';
import UserLogin from '../views/User/UserLogin';
import UserRegister from '../views/User/UserRegister';
import UserInfoDisplay from '../views/User/UserInfoDisplay';
import UserInfoEdit from '../views/User/UserInfoEdit';

import ProblemList from '../views/Problem/ProblemList';
import ProblemDetail from '../views/Problem/ProblemDetail';
import ProblemEditor from '../views/Problem/ProblemEditor';

import SubmissionList from '../views/Submission/SubmissionList';

import ContestPage from '../views/Contest/ContestPage';
import ContestList from '../views/Contest/ContestList';
import ContestDetail from '../views/Contest/ContestDetail';
import ContestRank from '../views/Contest/ContestRank';
import ContestProblemList from '../views/Contest/Problem/ContestProblemList';
import ContestProblemDetail from '../views/Contest/Problem/ContestProblemDetail';

import ContestText from '../views/Contest/ContestText';
import ContestTextEditor from '../views/Contest/ContestTextEditor';
import ContestRegisterStateDisplay from '../views/Contest/Register/ContestRgisterStateDisplay';
import ContestRegisterAllList from '../views/Contest/Register/ContestRegisterAllList';
import ContestRegisterPassedList from '../views/Contest/Register/ContestRegisterPassedList';

import HelpPage from '../views/HelpPage';
import RecommendPage from '../views/Recommend/RecommendPage';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/home',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/user',
      component: UserPage,
      children: [
        {
          path: 'login',
          name: 'UserLogin',
          component: UserLogin,
        },
        {
          path: 'register',
          name: 'UserRegister',
          component: UserRegister,
        },
        {
          path: 'info',
          name: 'UserInfoDisplay',
          component: UserInfoDisplay,
        },
        {
          path: 'info/edit',
          name: 'UserInfoEdit',
          component: UserInfoEdit,
        },
      ],
    },
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
    {
      path: '/submission/list',
      name: 'SubmissionList',
      component: SubmissionList,
    },
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
    {
      path: '/help',
      name: 'HelpPage',
      component: HelpPage,
    },
    {
      path: '/recommend',
      name: 'RecommendPage',
      component: RecommendPage,
    },
    {
      path: '*',
      name: 'NotFoundPage',
      component: NotFoundPage,
    },
  ],
});
