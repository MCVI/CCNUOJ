<template>
<!-- 本组件是从后端调用所有比赛的简况,并按照时间顺序排序-->
 <div>
    <el-table
    :data="contest"
    height="500"
    border
    style="width: 100%">
    <el-table-column
      prop="id"
      label="编号"
      sortable
      style="width: 20%">
    </el-table-column>
    <el-table-column
      prop="title"
      label="比赛"
      border
      style="width: 20%">
       <template  slot-scope="scope">
        <router-link :to=" { name:'contdetail', query:{contest:scope.row}}">
              {{scope.row.title}}
        </router-link>
       </template>
     </el-table-column>
     <el-table-column
      prop="createTime"
      label="开始时间"
      sortable
      border
      style="width: 20%">
     </el-table-column>
  </el-table>
 </div>
</template>

<script>
import contdetail from '../Contest/contdetail'
export default {
  name: 'contable',
  data () {
    return {
      contest: []
    }
  },
  components: {
    contdetail
  },
  mounted: function () {
    var _this = this
    this.$http.get('/api/contest')
      .then(function (res) {
        console.log(res)
        _this.contest = res.body.data
      })
      .catch(function (erro) {
        console.log(erro)
      })
  }
}
</script>

<style>

</style>
