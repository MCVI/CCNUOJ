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
import ContestRank from './ContestRank'
import ContestProblemList from './Problem/ContestProblemList'
import ContestDetail from './Problem/ContestProblemDetail'

export default {
  name: 'ContestDetail',
  data () {
    return {
      contest: null,
      contestid: null,
      activeName: ''
    }
  },
  created: function () {
    this.activeName = 'ConquesList'
  },
  methods: {
  },
  mounted: function () {
    this.$http.get('/api/contest')
      .then((res) => {
        this.contestid = this.$route.params['contest_id']
        const list = res.body.data
        for (let contest of list) {
          if (contest.id === this.contestid) {
            this.contest = contest
          }
        }
      })
      .catch((error) => {
        console.log(error)
      })
  },
  components: {
    ContestRank,
    ContestProblemList,
    ContestDetail
  }
}

</script>

<style scoped>

</style>
