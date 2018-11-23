import axios from 'axios';
import router from 'vue-router';
import { Message } from 'element-ui';
import store from '@/store/index';

const service = axios.create({
  baseURL: '/api',
  timeout: 5000,
});

service.interceptors.request.use(
  (req) => {
    const request = req;
    const state = store.state.user.loginState;
    if (typeof state === 'object') {
      request.headers['X-CCNU-AUTH-TOKEN'] = state.token;
    }
    return request;
  },
);

service.interceptors.response.use(
  (response) => {
    if (status === 401) {
      Message.error('该操作需要登录，请先登录。');
      router.replace({ name: 'UserLogin' });
    }
    return response;
  },
);

export default service;
