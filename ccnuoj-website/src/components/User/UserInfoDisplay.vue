<template>
  <div>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>账户信息</span>
      </div>

      <div v-loading="loading">
        <div class="text item">
          <span>电子邮箱：{{ email }}</span>
        </div>
        <div class="text item">
          <span>用户名：{{ shortName }}</span>
        </div>
      </div>
    </el-card>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>真实信息</span>
        <el-button style="float: right; padding: 3px 0" type="text">编辑</el-button>
      </div>

      <div v-loading="loading">
        <div class="text item">
          <span>真实姓名：{{ realPersonInfo.realName }}</span>
        </div>
      </div>
      <div v-loading="loading">
        <div class="text item">
          <span>性别：{{ gender }}</span>
        </div>
      </div>
      <div v-loading="loading">
        <div class="text item">
          <span>电话：{{ realPersonInfo.phone }}</span>
        </div>
      </div>
      <div v-loading="loading">
        <div class="text item">
          <span>学校：{{ realPersonInfo.studentInfo.school }}</span>
        </div>
      </div>
      <div v-loading="loading">
        <div class="text item">
          <span>专业：{{ realPersonInfo.studentInfo.major }}</span>
        </div>
      </div>

    </el-card>

  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import { getUserInfo } from '../../api/User';

export default {
  name: 'UserInfoDisplay',
  data() {
    return {
      loading: true,

      email: '',
      shortName: '',

      realPersonInfo: {},
      gender: '',

      extraInfo: {},
      createTime: '',
    };
  },

  computed: {
    ...mapGetters({ userID: 'user/id' }),
  },

  methods: {
    loadUserInfo() {
      if (typeof this.userID === 'number') {
        getUserInfo(this.userID)
          .then((result) => {
            this.email = result.email;
            this.shortName = result.shortName;
            this.realPersonInfo = result.realPersonInfo;
            this.extraInfo = result.extraInfo;
            this.createTime = result.createTime;

            const gender = this.realPersonInfo.gender;
            if (gender === 'MALE') {
              this.gender = '男';
            } else if (gender === 'FEMALE') {
              this.gender = '女';
            } else {
              this.gender = gender;
            }

            this.loading = false;
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
      }
    },
  },

  watch: {
    userID() {
      this.loadUserInfo(this.userID);
    },
  },
  mounted() {
    this.loadUserInfo(this.userID);
  },
};

</script>

<style scoped>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    font-size: 20px;
  }
</style>
