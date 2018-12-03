<template>

  <div>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <el-table
        :data="registerList"
        style="width: 100%">
        <el-table-column prop="registerInfo.realName" label="真实姓名"></el-table-column>
        <el-table-column prop="registerInfo.studentInfo.school" label="学校"></el-table-column>
      </el-table>
      <div style="font-size: 14px;">
        <p>总计：</p>
        <p>已通过审核：{{ passedNum }}</p>
      </div>

      <el-pagination
        :page-count="pageCount"
        :current-page="pageNum"
        @current-change="onSwitchPage"
        layout="prev, pager, next">
      </el-pagination>
    </template>

  </div>

</template>

<script>

import { getContestRegisterPassedList } from '@/api/ContestRegister';

export default {
  name: 'ContestRegisterPassedList',
  data() {
    return {
      loading: true,

      passedNum: undefined,

      pageCount: undefined,
      registerList: undefined,
      pageNum: 1,
    };
  },
  computed: {
    userID() {
      return this.$store.getters['user/id'];
    },
    contestID() {
      return this.$route.params.contest_id;
    },
  },

  methods: {
    loadData() {
      this.loading = true;
      if (this.userID === undefined) {
        // do nothing
      } else if (this.userID === null) {
        this.$message.error('您还未登录，请先登录！');
      } else {
        getContestRegisterPassedList(this.contestID, this.pageNum)
          .then((result) => {
            this.pageCount = result.pageCount;
            this.registerList = result.list;

            this.passedNum = result.passedNum;

            this.loading = false;
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('获取信息失败：网络错误');
                break;
              default:
                this.$message.error('获取信息失败：未知错误');
                break;
            }
          });
      }
    },

    onSwitchPage(pageNum) {
      this.pageNum = pageNum;
      this.loadData();
    },
  },
  watch: {
    userID() {
      return this.loadData();
    },
  },
};

</script>

<style scoped>
</style>
