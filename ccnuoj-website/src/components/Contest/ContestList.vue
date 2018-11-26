<template>
<!-- 本组件是从后端调用所有比赛的简况,并按照时间顺序排序-->
<div>

  <el-table :data="contestList" height="500" border style="width: 100%">

    <el-table-column prop="id" label="编号" sortable style="width: 20%"></el-table-column>

    <el-table-column prop="title" label="比赛" border style="width: 20%">
      <template  slot-scope="scope">
        {{scope.row.title}}
        <el-button
          v-if="scope.row.needRegister"
          @click="onRegister(scope.row.id)"
          type="primary">
          我要报名
        </el-button>
        <!--
        <router-link :to="{
          name:'ContestDetail',
          params:{
            contest_id: scope.row.id
           }
         }">
          {{scope.row.title}}
        </router-link>
        -->
      </template>
    </el-table-column>

    <el-table-column prop="startTime" label="开始时间" sortable border style="width: 20%"></el-table-column>

  </el-table>

</div>
</template>

<script>
import { getContestList } from '../../api/Contest';

export default {
  name: 'ContestList',
  data() {
    return {
      contestList: [],
    };
  },
  mounted() {
    getContestList()
      .then((result) => {
        this.contestList = result;
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
  methods: {
    onRegister(contestID) {
      this.$router.push({
        name: 'ContestRegister',
        params: {
          contest_id: contestID,
        },
      });
    },
  },
};
</script>

<style scoped>

</style>
