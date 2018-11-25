import Vue from 'vue';
import Router from 'vue-router';

import NotFoundPage from '../views/NotFoundPage';

import HomePage from '../views/HomePage';

import UserPage from '../views/UserPage';
import UserLogin from '../components/User/UserLogin';
import UserRegister from '../components/User/UserRegister';
import UserInfoDisplay from '../components/User/UserInfoDisplay';
import UserInfoEdit from '../components/User/UserInfoEdit';

import ProblemPage from '../views/ProblemPage';
import ProblemList from '../components/Problem/ProblemList';
import ProblemDetail from '../components/Problem/ProblemDetail';

import ContestPage from '../views/ContestPage';
import ContestList from '../components/Contest/ContestList';
import ContestDetail from '../components/Contest/ContestDetail';
import ContestRank from '../components/Contest/ContestRank';

import ContestProblemList from '../components/Contest/Problem/ContestProblemList';
import ContestProblemDetail from '../components/Contest/Problem/ContestProblemDetail';

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
      component: ProblemPage,
      children: [
        {
          path: '',
          redirect: 'list',
        },
        {
          path: 'list',
          name: 'ProblemList',
          component: ProblemList,
        },
        {
          path: ':problem_id',
          name: 'ProblemDetail',
          component: ProblemDetail,
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
          name: 'ContestDetail',
          component: ContestDetail,
          children: [
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
                  name: 'ProblemDetail',
                  component: ProblemDetail,
                },
              ],
            },
            {
              path: 'rank',
              name: 'ContestRank',
              component: ContestRank,
            },
            {
              path: ':problem_id',
              name: 'ContestProblemDetail',
              component: ContestProblemDetail,
            },
          ],
        },
      ],
    },
    {
      path: '*',
      name: 'NotFoundPage',
      component: NotFoundPage,
    },
  ],
});
