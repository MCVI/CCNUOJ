<template>
<!-- 本组件是 从后端调用题目数据 显示题目list  -->
<div>

  <el-button
    @click="$router.push({name:'CreateProblem'})"
    id="create-problem"
    type="primary">
    添加题目
  </el-button>

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

    <el-table-column border label="作者" prop="author.shortName" style="width: 20%"></el-table-column>

    <el-table-column border label="创建时间" prop="createTime" style="width: 20%"></el-table-column>

    <el-table-column border label="修改时间" prop="lastModifiedTime" style="width: 20%"></el-table-column>

  </el-table>

</div>
</template>

<script>
import { getProblemList } from '@/api/Problem';

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
    getProblemList(1)
      .then((problemList) => {
        this.problem = problemList;
      })
      .catch((error) => {
        this.$message.error('获取数据错误');
      });
  },
  components: {},
};
</script>

<style scoped>
#create-problem {
  float: right;
}
</style>
