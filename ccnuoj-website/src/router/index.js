import Vue from 'vue'
import Router from 'vue-router'

import PhotoPage from '../views/PhotoPage'

import IdentityPage from '../views/IdentityPage'
import UserLogin from '../components/Identity/UserLogin'
import UserRegister from '../components/Identity/UserRegister'

import ProblemPage from '../views/ProblemPage'
import ProblemList from '../components/Problem/ProblemList'
import ProblemDetail from '../components/Problem/ProblemDetail'

import ContestPage from '../views/ContestPage'
import ContestList from '../components/Contest/ContestList'
import ContestDetail from '../components/Contest/ContestDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      alias: ['/login', '/register'],
      component: IdentityPage,
      children: [
        {
          path: '',
          redirect: 'login'
        },
        {
          path: 'login',
          name: 'UerLogin',
          component: UserLogin
        },
        {
          path: 'register',
          name: 'UserRegister',
          component: UserRegister
        }
      ]
    },
    {
      path: '/photo',
      name: 'PhotoPage',
      component: PhotoPage
    },
    {
      path: '/problem',
      component: ProblemPage,
      children: [
        {
          path: '',
          redirect: 'list'
        },
        {
          path: 'list',
          name: 'ProblemList',
          component: ProblemList
        },
        {
          path: ':problem_id',
          name: 'ProblemDetail',
          component: ProblemDetail
        }
      ]
    },
    {
      path: '/contest',
      component: ContestPage,
      children: [
        {
          path: '',
          redirect: 'list'
        },
        {
          path: 'list',
          name: 'ContestList',
          component: ContestList
        },
        {
          path: ':contest_id',
          name: 'ContestDetail',
          component: ContestDetail
        }
      ]
    }
  ]
})
