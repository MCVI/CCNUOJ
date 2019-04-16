<template>

  <!-- 本组件是 从后端调用题目数据 显示题目list  -->

  <page-common>
    <template v-if="initialLoading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <el-button
        @click="$router.push({name:'CreateProblem'})"
        id="create-problem"
        type="primary">
        添加题目
      </el-button>

      <el-table v-loading="loading" :data="problemList" border style="width: 100%">

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

      <el-pagination
        background
        layout="prev, pager, next"
        :page-count="pageCount"
        @current-change="changePageCount">
      </el-pagination>

    </template>

  </page-common>

</template>

<script>

import { getProblemList } from '@/api/Problem';

import PageCommon from '../PageCommon';

export default {
  name: 'ProblemList',
  components: { PageCommon },
  data() {
    return {
      initialLoading: true,
      loading: true,
      pageNum: 1,
      pageCount: undefined,
      problemList: undefined,
    };
  },
  methods: {
    changePageCount(pageNum) {
      this.setPageNum(pageNum);
      this.loadList();
    },
    setPageNum(pageNum) {
      this.pageNum = pageNum;
      if (this.pageNum > this.pageCount) {
        this.pageNum = this.pageCount;
      }
      if (this.pageNum < 1) {
        this.pageNum = 1;
      }
    },
    setPageCount(pageCount) {
      this.pageCount = pageCount;
      this.setPageNum(this.pageNum);
    },
    loadList() {
      this.loading = true;
      return new Promise((resolve, reject) => {
        getProblemList(this.pageNum)
          .then((result) => {
            this.setPageCount(result.pageCount);
            this.problemList = result.list;
            this.loading = false;
            resolve();
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
            reject(error);
          });
      });
    },
  },

  mounted() {
    this.loadList()
      .then((result) => {
        this.initialLoading = false;
      });
  },

};
</script>

<style scoped>
#create-problem {
  float: right;
}
</style>
