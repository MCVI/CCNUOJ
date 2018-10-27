<template>
<!-- 本组件是从后端调用所有比赛的简况,并按照时间顺序排序-->
<div>

  <el-table :data="contest" height="500" border style="width: 100%">

    <el-table-column prop="id" label="编号" sortable style="width: 20%"></el-table-column>

    <el-table-column prop="title" label="比赛" border style="width: 20%">
      <template  slot-scope="scope">
        <router-link :to="{
          name:'ContestDetail',
          params:{
            contest_id: scope.row.id
           }
         }">
          {{scope.row.title}}
        </router-link>
      </template>
    </el-table-column>

    <el-table-column prop="createTime" label="开始时间" sortable border style="width: 20%"></el-table-column>

  </el-table>

</div>
</template>

<script>
import ContestDetail from './ContestDetail'
export default {
  name: 'ContestList',
  data () {
    return {
      contest: []
    }
  },
  components: {
    ContestDetail
  },
  mounted: function () {
    this.$http.get('/api/contest')
      .then((res) => {
        console.log(res)
        this.contest = res.body.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>

<style scoped>

</style>
