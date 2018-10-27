<template>
  <greeting-message>

    <el-form :model="UserLoginForm" :rules="UserRulers" label-width="80px" ref="UserForm" style="margin-top: 10%;">

      <el-form-item label="昵称" prop="name">
        <el-input v-model="UserLoginForm.name"></el-input>
      </el-form-item>

      <div style="height:30px"></div>

      <el-form-item label="密码" prop="major">
        <el-input v-model="UserLoginForm.major"></el-input>
      </el-form-item>

      <div style="height:35px"></div>

      <el-form-item size="large">
        <el-button @click="onSubmit('UserLoginForm')" style="width:200px ; height:40px" type="primary">登录</el-button>
      </el-form-item>

    </el-form>

  </greeting-message>
</template>

<script>
import GreetingMessage from './GreetingMessage'
export default {
  name: 'UserLogin',
  data () {
    return {
      UserLoginForm: {
        name: '',
        phone: '',
        school: '',
        major: '',
        sex: ''
      },
      UserRulers: {
        name: [
          {required: true, message: '请输入昵称', trigger: 'blur'},
          {min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur'}
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
  },

  components: {GreetingMessage}
}
</script>

<style>
</style>
