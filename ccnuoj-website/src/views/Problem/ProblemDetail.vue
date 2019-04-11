<template>
  <page-common :display-common-line="false">

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <!-- 取值如下 -->

      <el-row>
        <p class="title-css">
          {{ problem.title }}
        </p>
        <el-button
          @click="$router.push({name:'UpdateProblem'})"
          id="update-problem"
          type="primary">
          编辑题目
        </el-button>
      </el-row>

      <markdown-viewer :value="problem.text"></markdown-viewer>

      <br/>
    </template>

    <p style='font-size: 20px;font-weight:500;text-align:left;'>提交代码</p>

    <el-select clearable placeholder="请选择" style='float:left' v-model="language">
      <el-option
        :key="item.value"
        :label="item.label"
        :value="item.value"
        v-for="item in options">
      </el-option>
    </el-select>

    <br/>

    <el-input :rows="10" placeholder="请输入内容" type="textarea" v-model="code"></el-input>

    <el-button
      @click="onClickSubmit"
      round type="primary">
      提交
    </el-button>

  </page-common>
</template>

<script>
import { getProblem } from '@/api/Problem';
import { createSubmission } from '@/api/Submission';

import PageCommon from '../PageCommon';
import MarkdownViewer from '../../components/MarkdownViewer';

export default {
  name: 'ProblemDetail',
  components: {
    PageCommon,
    MarkdownViewer,
  },
  data() {
    return {
      loading: true,
      problem: undefined,
      code: '',
      options: [{
        value: 'cpp',
        label: 'c++',
      }, {
        value: 'c',
        label: 'c',
      }, {
        value: 'c#',
        label: 'csharp',
      }, {
        value: 'python',
        label: 'python',
      }, {
        value: 'java',
        label: 'java',
      }],
      language: '',
    };
  },
  computed: {
    problemID() {
      return parseInt(this.$route.params.problem_id, 10);
    },
  },

  mounted() {
    const problemID = this.$route.params.problem_id;
    getProblem(problemID)
      .then((problem) => {
        this.problem = problem;
        this.loading = false;
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
    onClickSubmit() {
      createSubmission(this.problemID, this.language, this.code)
        .then((result) => {
          this.$message.success('提交成功');
          this.$router.push('/submission/list');
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('提交失败：网络错误');
              break;
            default:
              this.$message.error('提交失败：未知错误');
              break;
          }
        });
    },
  },
};

</script>

<style scoped>

.title-css {
  width: 90%;
  height: 100px;
  font-size: 50%;
  font-weight: 600;
  text-align: center;
  font-family: 宋体, 幼圆, sans-serif;
  border-bottom: 1px solid #000
}

.text-css {
  width: 90%;
  font-size: 20px;
  font-family: 幼圆, sans-serif;
  word-wrap: break-word;
  word-break: keep-all;
  text-align: left;
}

/* 强制换行 */
.text-css p {
  text-align: left;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}

.el-icon-arrow-down {
  font-size: 12px;
}

#update-problem {
  float: right;
}
</style>
