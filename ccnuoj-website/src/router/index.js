import Vue from 'vue'
import Router from 'vue-router'
import helloidentity from '../components/Identity/helloidentity'
import homeheader from '../components/homeheader'
import home from '../pages/home'
import photowalls from '../components/NewsAndPhoto/photowalls'
import queslist from '../components/Question/queslist'
import quesdetail from '../components/Question/quesdetail'
import questable from '../components/Question/questable'
import login from '../components/Identity/login'
import register from '../components/Identity/register'
import contestlist from '../components/Contest/contestlist'
import contdetail from '../components/Contest/contdetail'
import contable from '../components/Contest/contable'
import conquesrank from '../components/Contest/ConDetailPage/conquesrank'
import conquestable from '../components/Contest/ConDetailPage/conquestable'
import conquesupdate from '../components/Contest/ConDetailPage/conquesupdate'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'helloidentity',
      component: helloidentity,
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
      path: '/contestlist',
      name: 'contestlist',
      component: contestlist,
      children: [
        {
          path: '',
          component: contable
        },
        {
          path: 'contdetail',
          name: 'contdetail',
          component: contdetail,
          children: [
            {
              path: 'conquesrank',
              name: 'conquesrank',
              component: conquesrank
            },
            {
              path: 'conquestable',
              name: 'conquestable',
              component: conquestable
            },
            {
              path: 'conquesupdate',
              name: 'conquesupdate',
              component: conquesupdate
            }
          ]
        }
      ]
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
