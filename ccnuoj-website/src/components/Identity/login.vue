<template>
 <div>
<el-form ref="UserForm" :model="UserForm" :rules="UserRulers" label-width="80px" style="margin-top: 10%;">
       <el-form-item label="昵称" prop="name">
         <el-input v-model="UserForm.name"></el-input>
       </el-form-item>
       <div style="height:30px"></div>
       <el-form-item label="密码" prop="major">
          <el-input v-model="UserForm.major"></el-input>
        </el-form-item>
        <div style="height:35px"></div>
         <el-form-item size="large">
               <el-button type="primary" @click="onSubmit('UserForm')" style="width:200px ; height:40px">登录</el-button>
        </el-form-item>
     </el-form>
 </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      UserForm: {
        name: '',
        phone: '',
        school: '',
        major: '',
        sex: ''
      },
      UserRulers: {
        name: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
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

  components: {

  }
}
</script>

<style>

</style>
