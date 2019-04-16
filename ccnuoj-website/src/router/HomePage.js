const HomePage = () => import('../views/HomePage');

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
