<template>
  <!-- 本组件 是 用于推荐题目 -->
  <!-- 本组件是由RecommendPage跳转过来的 -->
  <div>
    <el-form label-width="80px" ref="RecommendForm" style="margin-top: 10%;">

      <el-form-item label="题号" prop="account">
        <el-input v-model="problemId"> </el-input>
      </el-form-item>

      <div style="height:35px"></div>

      <el-form-item size="large">
        <el-button @click="onSubmit()" style="width:200px ; height:40px" type="primary">预测</el-button>
      </el-form-item>

    </el-form>

    <el-table :data="predictList" height="500" border style="width: 100%">

      <el-table-column prop="problemId" label="编号" sortable style="width: 20%"></el-table-column>

      <el-table-column prop="handle" label="用户" border style="width: 20%"></el-table-column>

      <el-table-column prop="result" label="状态" sortable border style="width: 20%"></el-table-column>
      <el-table-column prop="probability" label="预测通过概率" sortable border style="width: 20%"></el-table-column>

    </el-table>
  </div>


</template>


<script>
import { getPredictById } from '../../api/Help';

export default {
  name: 'RecommendProblem',
  data() {
    return {
      problemId: '',
      predictList: [],
    };
  },

  methods: {
    onSubmit() {
      getPredictById(this.problemId)
        .then((result) => {
          this.predictList = result.result;
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
  },
};
</script>

<style scoped>

</style>
