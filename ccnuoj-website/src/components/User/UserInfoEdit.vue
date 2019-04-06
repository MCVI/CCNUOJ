<template>

  <el-form
    :model="userInfoForm"
    :rules="userInfoRule"
    label-width="80px"
    ref="registerForm"
    style="margin-top: 0;">

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>

      <el-form-item label="真实姓名" prop="realName">
        <el-input v-model="userInfoForm.realName"></el-input>
      </el-form-item>

      <el-form-item label="性别" prop="gender">
        <el-radio-group size="medium" v-model="userInfoForm.gender" style="float: left;">
          <el-radio-button label="Male">男</el-radio-button>
          <el-radio-button label="Female">女</el-radio-button>
        </el-radio-group>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="电话" prop="phone">
        <el-input v-model="userInfoForm.phone"></el-input>
      </el-form-item>

      <div style="height:12px"></div>

      <el-form-item label="学校" prop="school">
        <el-input v-model="userInfoForm.school"></el-input>
      </el-form-item>

      <el-form-item label="专业" prop="major">
        <el-input v-model="userInfoForm.major"></el-input>
      </el-form-item>

      <div style="height:18px"></div>

      <el-form-item size="large">
        <el-button
          :disabled="!formValid"
          @click="onSubmit()"
          style="width:200px ; height:40px"
          type="primary">
          提交
        </el-button>
      </el-form-item>

    </template>
  </el-form>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserInfoEdit',
  data() {
    return {
      loading: true,
      formValid: false,

      userInfoForm: {
        realName: '',
        gender: '',

        phone: '',

        school: '',
        major: '',
      },
      userInfoRule: {
        realName: [
          { required: true, message: '真实姓名为必填项', trigger: 'blur' },
          {
            min: 3, max: 15, message: '真实姓名长度限制在 3 到 15 个字符之间', trigger: 'blur',
          },
        ],
        gender: [
          { required: true, message: '性别为必填项', trigger: 'change' },
        ],
        phone: [
          {
            min: 11, max: 11, message: '电话号码格式不正确', trigger: 'blur',
          },
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

  computed: {
    ...mapGetters({
      userID: 'user/id',
    }),
  },

  methods: {
    onSubmit() {
      this.$store.dispatch('user/updateDetailInfo', {
        realPersonInfo: {
          realName: this.userInfoForm.realName,
          gender: this.userInfoForm.gender,
          phone: this.userInfoForm.phone,
          studentInfo: {
            school: this.userInfoForm.school,
            major: this.userInfoForm.major,
          },
        },
        extraInfo: {},
      })
        .then((result) => {
          this.$message.success('更改个人信息成功！');
          this.$router.push('/user/info');
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('更改个人信息失败：网络错误');
              break;
            case 'NotLoggedIn':
              this.$message.error('错误：请先登录！');
              break;
            default:
              this.$message.error('更改个人信息失败：未知错误');
              break;
          }
        });
    },

    loadDetailInfo() {
      this.$store.dispatch('user/getDetailInfo')
        .then((result) => {
          if (result === undefined) {
            this.loading = true;
          } else if (result === null) {
            this.$message.error('错误：请先登录！');
            this.$router.push('/user/login');
          } else {
            this.userInfoForm.realName = result.realPersonInfo.realName;
            this.userInfoForm.gender = result.realPersonInfo.gender;
            this.userInfoForm.phone = result.realPersonInfo.phone;
            this.userInfoForm.school = result.realPersonInfo.studentInfo.school;
            this.userInfoForm.major = result.realPersonInfo.studentInfo.major;

            this.loading = false;
          }
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('获取用户信息失败：网络错误');
              break;
            default:
              this.$message.error('获取用户信息失败：未知错误');
              break;
          }
        });
    },
  },

  watch: {
    userInfoForm: {
      deep: true,
      handler(val) {
        this.$refs.registerForm.validate((valid) => {
          this.formValid = valid;
        });
      },
    },

    userID() {
      this.loadDetailInfo();
    },
  },
  mounted() {
    this.loadDetailInfo();
  },
};

</script>

<style scoped>

</style>
