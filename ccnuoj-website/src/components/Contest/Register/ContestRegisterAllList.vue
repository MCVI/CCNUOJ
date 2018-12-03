<template>

  <div>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <el-table
        :data="registerList"
        style="width: 100%">
        <el-table-column prop="userID" label="用户ID"></el-table-column>
        <el-table-column prop="registerInfo.realName" label="真实姓名"></el-table-column>
        <el-table-column prop="registerInfo.studentInfo.school" label="学校"></el-table-column>
        <el-table-column prop="registerInfo.studentInfo.major" label="专业"></el-table-column>
        <el-table-column prop="registerInfo.phone" label="电话号码"></el-table-column>
        <el-table-column prop="registerInfo.qq" label="QQ号码"></el-table-column>
        <el-table-column prop="registerInfo.remark" label="备注"></el-table-column>
        <el-table-column label="审核">
          <template  slot-scope="scope">
            <template v-if="scope.row.passed === undefined">
              修改中……
              <el-button v-loading="true"></el-button>
            </template>
            <template v-if="scope.row.passed === true">
              通过审核
              <el-button @click="onMark(scope.$index, false)" type="danger">取消</el-button>
            </template>
            <template v-else-if="scope.row.passed === false">
              未通过审核
              <el-button @click="onMark(scope.$index, true)" type="success">通过</el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
      <div style="font-size: 14px;">
        <p>总计：</p>
        <p>已报名：{{ totalNum }}</p>
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

import { getContestRegisterAllList, updateContestRegisterPassState } from '@/api/ContestRegister';

export default {
  name: 'ContestRegisterAllList',
  data() {
    return {
      loading: true,

      totalNum: undefined,
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
        getContestRegisterAllList(this.contestID, this.pageNum)
          .then((result) => {
            this.pageCount = result.pageCount;
            this.registerList = result.list;

            this.totalNum = result.totalNum;
            this.passedNum = result.passedNum;

            this.loading = false;
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('获取信息失败：网络错误');
                break;
              case 'PermissionDenied':
                this.$message.error('获取信息失败：权限不足');
                break;
              default:
                this.$message.error('获取信息失败：未知错误');
                break;
            }
          });
      }
    },

    onMark(index, passState) {
      const userID = this.registerList[index].userID;

      if (this.registerList[index].passed === true) {
        this.passedNum -= 1;
      }
      this.registerList[index].passed = undefined;

      updateContestRegisterPassState(this.contestID, userID, passState)
        .then(() => {
          if ((this.registerList[index].userID === userID) && (this.registerList[index].passed === undefined)) {
            this.registerList[index].passed = passState;
            if (this.registerList[index].passed === true) {
              this.passedNum += 1;
            }
          }
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('修改信息失败：网络错误');
              break;
            case 'PermissionDenied':
              this.$message.error('修改信息失败：权限不足');
              break;
            default:
              this.$message.error('修改信息失败：未知错误');
              break;
          }
          this.loadData();
        });
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
