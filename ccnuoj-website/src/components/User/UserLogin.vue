<template>

  <el-form :model="loginForm" :rules="loginRulers" label-width="80px" ref="loginForm" style="margin-top: 10%;">

    <el-form-item label="账号" prop="account">
      <el-input v-model="loginForm.account"></el-input>
    </el-form-item>

    <div style="height:30px"></div>

    <el-form-item label="密码" prop="major">
      <el-input v-model="loginForm.password"></el-input>
    </el-form-item>

    <div style="height:35px"></div>

    <el-form-item size="large">
      <el-button @click="onSubmit()" style="width:200px ; height:40px" type="primary">登录</el-button>
    </el-form-item>

  </el-form>

</template>

<script>
import validator from 'validator';

export default {
  name: 'UserLogin',
  data() {
    return {
      loginForm: {
        account: '',
        password: '',
      },
      loginRulers: {
        account: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 3, max: 15, message: '长度在 5 到 30 个字符', trigger: 'blur' },
        ],
      },
    };
  },

  methods: {
    onSubmit() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          const account = this.loginForm.account;
          const password = this.loginForm.password;

          let promise;
          if (validator.isEmail(account)) {
            promise = this.$store.dispatch(
              'user/loginByEmail',
              {
                email: this.loginForm.account,
                password: this.loginForm.password,
              },
            );
          } else {
            promise = this.$store.dispatch(
              'user/loginByShortName',
              {
                email: this.loginForm.account,
                password: this.loginForm.password,
              },
            );
          }
          promise.then(() => {
            console.log(['登录成功', this.$store.state.user.loginState]);
          }).catch((error) => {
            console.error(['登录失败', error]);
          });
        } else {
          console.log('error submit!!');
        }
      });
    },
  },
};

</script>

<style>
</style>
