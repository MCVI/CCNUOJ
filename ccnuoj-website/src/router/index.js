import Vue from 'vue';
import Router from 'vue-router';

import NotFoundPage from '../views/NotFoundPage';

import HomePage from '../views/HomePage';

import UserPage from '../views/UserPage';
import UserLogin from '../components/User/UserLogin';
import UserRegister from '../components/User/UserRegister';
import UserInfoDisplay from '../components/User/UserInfoDisplay';
import UserInfoEdit from '../components/User/UserInfoEdit';

import ProblemList from '../views/Problem/ProblemList';
import ProblemDetail from '../views/Problem/ProblemDetail';
import ProblemEditor from '../views/Problem/ProblemEditor';

import SubmissionPage from '../views/SubmissionPage';
import SubmissionList from '../views/Submission/SubmissionList';

import ContestPage from '../views/ContestPage';
import ContestList from '../components/Contest/ContestList';
import ContestDetail from '../components/Contest/ContestDetail';
import ContestRank from '../components/Contest/ContestRank';
import ContestProblemList from '../components/Contest/Problem/ContestProblemList';
import ContestProblemDetail from '../components/Contest/Problem/ContestProblemDetail';

import ContestText from '../components/Contest/ContestText';
import ContestTextEditor from '../components/Contest/ContestTextEditor';
import ContestRegisterStateDisplay from '../components/Contest/Register/ContestRgisterStateDisplay';
import ContestRegisterAllList from '../components/Contest/Register/ContestRegisterAllList';
import ContestRegisterPassedList from '../components/Contest/Register/ContestRegisterPassedList';

import HelpPage from '../views/HelpPage';
import RecommendPage from '../views/RecommendPage';

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
      path: '/submission',
      component: SubmissionPage,
      children: [
        {
          path: '',
          redirect: 'list',
        },
        {
          path: 'list',
          name: 'SubmissionList',
          component: SubmissionList,
        },
      ],
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
