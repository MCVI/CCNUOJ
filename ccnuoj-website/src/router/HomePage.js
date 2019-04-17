import asyncLoad from '../components/async-load';

const HomePage = asyncLoad(import('../views/HomePage'));

export default [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage,
  },
];
