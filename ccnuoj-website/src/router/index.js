import Vue from 'vue'
import Router from 'vue-router'
import GreetingMessage from '../components/GreetingMessage'
import HomePage from '../views/HomePage'
import PhotoWall from '../components/PhotoWall'
import ProblemDetail from '../components/ProblemDetail'
import ProblemList from '../components/ProblemList'
import UserLogin from '../components/UserLogin'
import UserRegister from '../components/UserRegister'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: HomePage,
      children: [
        {
          path: 'home',
          name: 'GreetingMessage',
          component: GreetingMessage
        },
        {
          path: '',
          redirect: '/login'
        },
        {
          path: 'register',
          name: 'UserRegister',
          component: UserRegister
        },
        {
          path: 'login',
          name: 'UserLogin',
          component: UserLogin
        }
      ]
    },
    {
      path: '/photo-wall',
      name: 'PhotoWall',
      component: PhotoWall
    },
    {
      path: '/problem',
      name: 'ProblemList',
      component: ProblemList,
      children: [
        {
          path: 'ProblemDetail',
          name: 'ProblemDetail',
          component: ProblemDetail
        }
      ]
    }
  ]
})
