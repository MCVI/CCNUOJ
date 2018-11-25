<template>
  <div>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>账户信息</span>
      </div>

      <template v-if="loading">
        <div v-loading="true"></div>
      </template>
      <template v-else>
        <div class="text item">
          <span>电子邮箱：{{ email }}</span>
        </div>
        <div class="text item">
          <span>用户名：{{ shortName }}</span>
        </div>
      </template>
    </el-card>

    <el-card class="box-card">

      <div slot="header" class="clearfix">
        <span>真实信息</span>
        <el-button @click="onEditInfo()" style="float: right; padding: 3px 0" type="text">编辑</el-button>
      </div>

      <template v-if="loading">
        <div v-loading="true"></div>
      </template>

      <template v-else>
        <div class="text item">
          <span>真实姓名：{{ realPersonInfo.realName }}</span>
        </div>
        <div class="text item">
          <span>性别：{{ gender }}</span>
        </div>
        <div class="text item">
          <span>电话：{{ realPersonInfo.phone }}</span>
        </div>
        <div class="text item">
          <span>学校：{{ realPersonInfo.studentInfo.school }}</span>
        </div>
        <div class="text item">
          <span>专业：{{ realPersonInfo.studentInfo.major }}</span>
        </div>
      </template>

    </el-card>

  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserInfoDisplay',
  computed: {
    loading() {
      return (this.detailInfo === undefined);
    },

    realPersonInfo() {
      return this.detailInfo.realPersonInfo;
    },
    extraInfo() {
      return this.detailInfo.extraInfo;
    },
    createTime() {
      return this.detailInfo.createTime;
    },

    gender() {
      const gender = this.realPersonInfo.gender;
      if (gender === 'Male') {
        return '男';
      } else if (gender === 'Female') {
        return '女';
      } else {
        return gender;
      }
    },

    ...mapGetters({
      userID: 'user/id',
      email: 'user/email',
      shortName: 'user/shortName',
      detailInfo: 'user/detailInfo',
    }),
  },

  methods: {
    loadDetailInfo() {
      this.$store.dispatch('user/getDetailInfo')
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

    onEditInfo() {
      this.$router.push('/user/info/edit');
    },
  },

  watch: {
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
