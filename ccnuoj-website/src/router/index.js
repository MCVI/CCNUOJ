import Vue from 'vue';
import Router from 'vue-router';

import asyncLoad from '../components/async-load';

import homePageRoute from './HomePage';
import userRoute from './User';
import problemRoute from './Problem';
import submissionRoute from './Submission';
import contestRoute from './Contest';
import helpRoute from './Help';
import recommendRoute from './Recommend';

const NotFoundPage = asyncLoad(import('../views/NotFoundPage'));

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    ...homePageRoute,
    ...userRoute,
    ...problemRoute,
    ...submissionRoute,
    ...contestRoute,
    ...helpRoute,
    ...recommendRoute,
    {
      path: '*',
      name: 'NotFoundPage',
      component: NotFoundPage,
    },
  ],
});
