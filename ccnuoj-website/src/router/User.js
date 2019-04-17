import asyncLoad from '../components/async-load';

const UserPage = asyncLoad(import('../views/User/UserPage'));
const UserLogin = asyncLoad(import('../views/User/UserLogin'));
const UserRegister = asyncLoad(import('../views/User/UserRegister'));
const UserInfoDisplay = asyncLoad(import('../views/User/UserInfoDisplay'));
const UserInfoEdit = asyncLoad(import('../views/User/UserInfoEdit'));

export default [
  {
    path: '/user',
    component: UserPage,
    children: [
      {
        path: 'login',
        name: 'UserLogin',
        component: UserLogin,
      },
      {
        path: 'register',
        name: 'UserRegister',
        component: UserRegister,
      },
      {
        path: 'info',
        name: 'UserInfoDisplay',
        component: UserInfoDisplay,
      },
      {
        path: 'info/edit',
        name: 'UserInfoEdit',
        component: UserInfoEdit,
      },
    ],
  },
];
