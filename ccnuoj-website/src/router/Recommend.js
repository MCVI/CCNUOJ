import asyncLoad from '../components/async-load';

const RecommendPage = asyncLoad(import('../views/Recommend/RecommendPage'));

export default [
  {
    path: '/recommend',
    name: 'RecommendPage',
    component: RecommendPage,
  },
];
