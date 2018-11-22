<template>

  <el-form :model="registerForm" :rules="registerRule" label-width="80px" ref="registerForm" style="margin-top: 0;">

    <el-form-item label="电子邮箱" prop="email">
      <el-input v-model="registerForm.email"></el-input>
    </el-form-item>

    <el-form-item label="用户名" prop="shortName">
      <el-input v-model="registerForm.shortName"></el-input>
    </el-form-item>

    <el-form-item label="密码" prop="password">
      <el-input v-model="registerForm.password"></el-input>
    </el-form-item>

    <div style="height:12px"></div>

    <el-form-item label="真实姓名" prop="realName">
      <el-input v-model="registerForm.realName"></el-input>
    </el-form-item>

    <el-form-item label="性别" prop="gender">
      <el-radio-group size="medium" v-model="registerForm.gender">
        <el-radio border label="MALE"></el-radio>
        <el-radio border label="FEMALE"></el-radio>
      </el-radio-group>
    </el-form-item>

    <div style="height:12px"></div>

    <el-form-item label="电话" prop="phone">
      <el-input v-model="registerForm.phone"></el-input>
    </el-form-item>

    <div style="height:12px"></div>

    <el-form-item label="学校" prop="school">
      <el-input v-model="registerForm.school"></el-input>
    </el-form-item>

    <el-form-item label="专业" prop="major">
      <el-input v-model="registerForm.major"></el-input>
    </el-form-item>

    <div style="height:18px"></div>

    <el-form-item size="large">
      <el-button @click="onSubmit()" style="width:200px ; height:40px" type="primary">注册</el-button>
    </el-form-item>

  </el-form>

</template>

<script>
import { userRegister } from '@/api/User';

export default {
  name: 'UserRegister',
  data() {
    return {
      registerForm: {
        name: '',
        phone: '',
        school: '',
        major: '',
        gender: '',
        password: '',
      },
      registerRule: {
        email: [
          { required: true, message: '电子邮箱为必填项', trigger: 'blur' },
          { min: 8, max: 30, message: '电子邮箱长度不符合要求', trigger: 'blur' },
        ],
        shortName: [
          { required: true, message: '用户名为必填项', trigger: 'blur' },
          { min: 3, max: 15, message: '长度在 5 到 20 个字符', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' },
        ],

        realName: [
          { required: true, message: '真实姓名为必填项', trigger: 'blur' },
          { min: 3, max: 15, message: '真实姓名长度限制在 3 到 15 个字符之间', trigger: 'blur' },
        ],
        gender: [
          { required: true, message: '性别为必填项', trigger: 'change' },
        ],
        phone: [
          { min: 11, max: 11, message: '电话号码格式不正确', trigger: 'blur' },
        ],

        school: [
          { required: true, message: '学校为必填项', trigger: 'blur' },
        ],
        major: [
          { required: true, message: '专业为必填项', trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    onSubmit() {
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          userRegister({
            email: this.registerForm.email,
            shortName: this.registerForm.shortName,
            realPersonInfo: {
              realName: this.registerForm.realName,
              gender: this.registerForm.gender,
              phone: this.registerForm.phone,
              studentInfo: {
                school: this.registerForm.school,
                major: this.registerForm.major,
              },
            },
            extraInfo: {},
            password: this.registerForm.password,
          })
            .then((userID) => {
              alert('注册成功！');
            });
        } else {
          alert('注册信息有无效部分！');
        }
      });
    },
  },
};

</script>

<style>
</style>
