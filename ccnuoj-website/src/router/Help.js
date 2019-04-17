import asyncLoad from '../components/async-load';

const HelpPage = asyncLoad(import('../views/HelpPage'));

export default [
  {
    path: '/help',
    name: 'HelpPage',
    component: HelpPage,
  },
];
