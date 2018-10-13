import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import homeheader from '../components/homeheader'
import home from '../pages/home'
import photowalls from '../components/photowalls'
import queslist from '../components/queslist'
import quesdetail from '../components/quesdetail'
import questable from '../components/questable'
import login from '../components/login'
import register from '../components/register'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      children: [
        {
          path: '',
          redirect: login
        },
        {
          path: 'register',
          name: 'register',
          component: register
        },
        {
          path: 'login',
          name: 'login',
          component: login
        }
      ]
    },
    {
      path: '/home',
      name: 'home',
      component: home
    },
    {
      path: '/homeheader',
      name: 'homeheader',
      component: homeheader
    },
    {
      path: '/photowalls',
      name: 'photowalls',
      component: photowalls
    },
    {
      path: '/queslist',
      name: 'queslist',
      component: queslist,
      children: [
        {
          path: '',
          component: questable
        },
        {
          path: 'quesdetail',
          name: 'quesdetail',
          component: quesdetail
        }
      ]
    }
  ]
})
