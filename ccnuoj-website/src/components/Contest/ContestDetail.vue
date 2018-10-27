<template>
<!-- 是 ContestList  的儿子组件
   ContestDetail组件是当我们在ContestList点击某一个比赛的时候,进入到该比赛的详情界面
  -->
<div>

 <p>{{ contest['title']}}</p>

 <el-tabs v-model="activeName" @tab-click="handleClick">

  <el-tab-pane label="题目" name="conquestable">
    <conquestable :objj="obj"></conquestable>
  </el-tab-pane>

  <el-tab-pane label="提交记录" name="conquesupdate">
    <conquesupdate :objj="obj"></conquesupdate>
  </el-tab-pane>

  <el-tab-pane label="榜单" name="conquesrank">
    <conquesrank :objj="obj"></conquesrank>
  </el-tab-pane>

 </el-tabs>

</div>

</template>

<script>

import conquesrank from '../Contest/ConDetailPage/conquesrank'
import conquestable from '../Contest/ConDetailPage/conquestable'
import conquesupdate from '../Contest/ConDetailPage/conquesupdate'
import conquesdetail from '../Contest/ConDetailPage/conquesdetail'

export default {
  name: 'ContestDetail',
  data () {
    return {
      activeName: 'conquestable',
      contest: null
    }
  },
  mounted () {
    this.$http.get('/api/contest')
      .then((res) => {
        const id = this.$route.params['contest_id']
        const list = res.body.data
        for (let contest of list) {
          if (contest.id === id) {
            this.contest = contest
          }
        }
      })
      .catch((error) => {
        console.log(error)
      })
  },
  components: {
    conquesrank,
    conquestable,
    conquesupdate,
    conquesdetail
  }
}

</script>

<style scoped>

</style>
