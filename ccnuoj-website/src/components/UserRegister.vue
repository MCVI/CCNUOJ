<template>
  <div>
    <el-form :model="UserRegisterForm" :rules="UserRegisterRule" label-width="80px" ref="UserForm" style="margin-top: 0;">

      <el-form-item label="昵称" prop="name">
        <el-input v-model="UserForm.name"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="电话" prop="phone">
        <el-input v-model="UserForm.phone"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="学校" prop="school">
        <el-input v-model="UserForm.school"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="密码" prop="password">
        <el-input v-model="UserForm.password"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="专业" prop="major">
        <el-input v-model="UserForm.major"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="性别" prop="sex">
        <el-radio-group size="medium" v-model="UserForm.sex">
          <el-radio border label="MAN"></el-radio>
          <el-radio border label="WOMAN"></el-radio>
        </el-radio-group>
      </el-form-item>

      <div style="height:18px"></div>

      <el-form-item size="large">
        <el-button @click="onSubmit('UserForm')" style="width:200px ; height:40px" type="primary">注册</el-button>
      </el-form-item>

    </el-form>
  </div>
</template>

<script>
export default {
  name: 'UserRegister',
  data () {
    return {
      UserRegisterForm: {
        name: '',
        phone: '',
        school: '',
        major: '',
        sex: '',
        password: ''
      },
      UserRegisterRule: {
        name: [
          {required: true, message: '请输入昵称', trigger: 'blur'},
          {min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur'}
        ],
        phone: [
          {min: 11, max: 11, message: '请输入正确的电话号码', trigger: 'blur'}
        ],
        school: [
          {required: true, message: '请输入学校', trigger: 'blur'}
        ],
        major: [
          {required: true, message: '请输入专业', trigger: 'blur'}
        ],
        sex: [
          {required: true, message: '请选择性别', trigger: 'change'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    onSubmit (UserRegisterForm) {
      this.$refs[UserRegisterForm].validate((valid) => {
        if (valid) {
          alert('submit!')
        } else {
          alert('注册信息有无效部分！')
          return false
        }
      })
    }
  }
}
</script>

<style>
</style>
