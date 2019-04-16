const UserPage = () => import('../views/User/UserPage');
const UserLogin = () => import('../views/User/UserLogin');
const UserRegister = () => import('../views/User/UserRegister');
const UserInfoDisplay = () => import('../views/User/UserInfoDisplay');
const UserInfoEdit = () => import('../views/User/UserInfoEdit');

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
