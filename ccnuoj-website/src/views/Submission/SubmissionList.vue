<template>
  <page-common>
    <template v-if="initialLoading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <el-table v-loading="loading" :data="submissionList" border style="width: 100%">

        <el-table-column label="编号" prop="id" sortable style="width: 5%"></el-table-column>

        <el-table-column border label="题目" prop="problem.title" style="width: 30%">
          <template slot-scope="scope">
            <router-link :to="{
              name: 'ProblemDetail',
              params: {
                problem_id: scope.row.problem.id
              }
            }">
              {{scope.row.problem.title}}
            </router-link>
          </template>
        </el-table-column>

        <el-table-column border label="用户" prop="author.shortName" style="width: 15%"></el-table-column>

        <el-table-column border label="语言" prop="language" style="width: 15%"></el-table-column>

        <el-table-column border label="状态" prop="latestJudgeRequest.state" style="width: 15%">
          <template slot-scope="scope">
            <judge-request-state :value="scope.row.latestJudgeRequest.state"></judge-request-state>
          </template>
        </el-table-column>

        <el-table-column border label="创建时间" prop="createTime" style="width: 20%"></el-table-column>

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

import { getSubmissionList } from '@/api/Submission';

import PageCommon from '../PageCommon';
import JudgeRequestState from '../../components/JudgeRequestState';

export default {
  name: 'SubmissionList',
  data() {
    return {
      initialLoading: true,
      loading: true,
      pageNum: 1,
      pageCount: undefined,
      submissionList: undefined,
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
        getSubmissionList(this.pageNum)
          .then((result) => {
            this.setPageCount(result.page_count);
            this.submissionList = result.list;
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
  components: { JudgeRequestState, PageCommon },
};
</script>

<style>
</style>
