<template>
  <!-- 本组件是 从后端调用题目数据 显示题目list  -->
  <div>
    <el-table
      :data="question"
      border
      height="500"
      style="width: 100%">
      <el-table-column
        label="编号"
        prop="id"
        sortable
        style="width: 20%">
      </el-table-column>
      <el-table-column
        border
        label="题目"
        prop="title"
        style="width: 20%">
        <template slot-scope="scope">
          <router-link :to=" { name:'quesdetail', query:{ques:scope.row}}">
            {{scope.row.title}}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        border
        label="作者"
        prop="author"
        style="width: 20%">
      </el-table-column>
      <el-table-column
        border
        label="创建时间"
        prop="createTime"
        style="width: 20%">
      </el-table-column>
      <el-table-column
        border
        label="修改时间"
        prop="lastModifiedTime"
        style="width: 20%">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import quesdetail from '../components/quesdetail'

export default {
  name: 'queslist',
  data () {
    return {
      question: []

    }
  },
  created () {
  },

  //  模拟 数据
  mounted: function () {
    var _this = this // 很重要！！
    this.$http.get('/api/question')
      .then(function (res) {
        console.log(res)
        _this.question = res.body.data
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  components: {
    quesdetail
  },
  methods: {
    // routeQuedetail(id){
    //     console.log(hhhhhh)
    //     this.$router.push({name:'quesdetail',params:{quesObj:id}})
    // }

  }
}
</script>

<style>

</style>
