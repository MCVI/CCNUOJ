import Vue from 'vue';
import Router from 'vue-router';

import NotFoundPage from '../views/NotFoundPage';

import PhotoPage from '../views/PhotoPage';

import IdentityPage from '../views/IdentityPage';
import UserLogin from '../components/User/UserLogin';
import UserRegister from '../components/User/UserRegister';

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
      alias: ['/login', '/register'],
      component: IdentityPage,
      children: [
        {
          path: '',
          redirect: 'login',
        },
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
      ],
    },
    {
      path: '/photo',
      name: 'PhotoPage',
      component: PhotoPage,
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
