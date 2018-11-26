<template>
<!-- 是 ContestList  的儿子组件
   ContestDetail组件是当我们在ContestList点击某一个比赛的时候,进入到该比赛的详情界面
  -->
<div>
 <p>{{ contest['title']}}</p>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="题目" name="ContestProblemList">
      <conques-list :contest_id = this.contestid></conques-list>
    </el-tab-pane>
    <el-tab-pane label="提交记录" name="ContestSubmission">
      <conques-update></conques-update>
    </el-tab-pane>
    <el-tab-pane label="榜单" name="ContestRank">
      <conques-rank></conques-rank>
    </el-tab-pane>
  </el-tabs>
</div>

</template>

<script>
import { getContest } from '@/api/Contest';

export default {
  name: 'ContestDetail',
  data() {
    return {
      contest: {},
    };
  },

  computed: {
    contestID() {
      return this.$route.params.contest_id;
    },
  },
  mounted() {
    getContest(this.contestID)
      .then((result) => {
        this.contest = result;
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
  },
};

</script>

<style scoped>

</style>
