import Vue from 'vue'
import Router from 'vue-router'

import PhotoWall from '../components/PhotoWall/PhotoWall'

import UserLogin from '../components/Identity/UserLogin'
import UserRegister from '../components/Identity/UserRegister'

import ProblemList from '../components/Problem/ProblemList'
// import ProblemDetail from '../components/Problem/ProblemDetail'

import ContestList from '../components/Contest/ContestList'
// import ContestDetail from '../components/Contest/ContestDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/register',
      name: 'UserRegister',
      component: UserRegister
    },
    {
      path: '/login',
      name: 'UserLogin',
      component: UserLogin
    },
    {
      path: '/photo',
      name: 'PhotoWall',
      component: PhotoWall
    },
    {
      path: '/problem',
      name: 'ProblemList',
      component: ProblemList
    },
    {
      path: '/contest',
      name: 'ContestList',
      component: ContestList
    }
  ]
})
