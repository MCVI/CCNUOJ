<template>
<!-- 本组件是 从后端调用题目数据 显示题目list  -->
<div>

  <el-table :data="problem" border height="500" style="width: 100%">

    <el-table-column label="编号" prop="id" sortable style="width: 20%"></el-table-column>

    <el-table-column border label="题目" prop="title" style="width: 20%">
      <template slot-scope="scope">
        <router-link :to="{
          name: 'ProblemDetail',
          params: {
            problem_id: scope.row.id
          }
        }">
          {{scope.row.title}}
        </router-link>
      </template>
    </el-table-column>

    <el-table-column border label="作者" prop="author" style="width: 20%"></el-table-column>

    <el-table-column border label="创建时间" prop="createTime" style="width: 20%"></el-table-column>

    <el-table-column border label="修改时间" prop="lastModifiedTime" style="width: 20%"></el-table-column>

  </el-table>

</div>
</template>

<script>

export default {
  name: 'ProblemList',
  data() {
    return {
      problem: [],
    };
  },
  created() {
  },

  //  模拟 数据
  mounted() {
    this.$http.get('/api/problem')
      .then((res) => {
        console.log(res);
        this.problem = res.body.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  components: {},
};
</script>

<style scoped>

</style>
