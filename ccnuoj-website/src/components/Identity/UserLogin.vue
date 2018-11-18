<template>

  <el-form :model="UserLoginForm" :rules="UserRulers" label-width="80px" ref="UserForm" style="margin-top: 10%;">

    <el-form-item label="账号" prop="account">
      <el-input v-model="UserLoginForm.account"></el-input>
    </el-form-item>

    <div style="height:30px"></div>

    <el-form-item label="密码" prop="major">
      <el-input v-model="UserLoginForm.password"></el-input>
    </el-form-item>

    <div style="height:35px"></div>

    <el-form-item size="large">
      <el-button @click="onSubmit('UserLoginForm')" style="width:200px ; height:40px" type="primary">登录</el-button>
    </el-form-item>

  </el-form>

</template>

<script>

export default {
  name: 'UserLogin',
  data () {
    return {
      UserLoginForm: {
        account: '',
        password: ''
      },
      UserRulers: {
        account: [
          {required: true, message: '请输入账号', trigger: 'blur'},
          {min: 3, max: 15, message: '长度在 5 到 30 个字符', trigger: 'blur'}
        ]
      }
    }
  },

  methods: {
    onSubmit (UserForm) {
      this.$refs[UserForm].validate((valid) => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}

</script>

<style>
</style>
