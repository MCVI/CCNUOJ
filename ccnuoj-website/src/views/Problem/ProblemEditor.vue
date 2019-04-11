<template>
  <page-common>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <el-form
        :model="problemForm"
        :rules="problemFormRules"
        label-width="80px"
        ref="problemForm"
        style="margin-top: 0;">

        <el-form-item label="标题" prop="title">
          <el-input v-model="problemForm.title"></el-input>
        </el-form-item>

        <el-form-item label="内容" prop="text">
          <markdown-editor v-model="problemForm.text"></markdown-editor>
        </el-form-item>

        <el-form-item label="评测方案" prop="judgeScheme">
          <el-input disabled value="简单对比"></el-input>
        </el-form-item>

        <el-form-item label="时间限制" prop="timeLimit">
          <el-input v-model="problemForm.timeLimit"></el-input>
        </el-form-item>

        <el-form-item label="内存限制" prop="memoryLimit">
          <el-input v-model="problemForm.memoryLimit"></el-input>
        </el-form-item>

        <el-form-item size="large">
          <el-button
            :disabled="!formValid"
            @click="onClickSubmit()"
            style="width:200px ; height:40px"
            type="primary">
            提交
          </el-button>
        </el-form-item>

      </el-form>
    </template>

  </page-common>

</template>

<script>
import {
  getProblem,
  createProblem,
  updateProblem,
} from '../../api/Problem';

import PageCommon from '../PageCommon';
import MarkdownEditor from '../../components/MarkdownEditor';

export default {
  name: 'ProblemEditor',
  components: {
    PageCommon,
    MarkdownEditor,
  },
  props: ['problem_id'],
  data() {
    return {
      loading: true,
      formValid: false,
      problemForm: {
        title: '',
        text: '',
        timeLimit: '1000',
        memoryLimit: '268435456',
      },
      problemFormRules: {
        title: [
          { required: true, message: '标题不能为空', trigger: 'blur' },
        ],
        text: [
          { required: true, message: '内容不能为空', trigger: 'blur' },
        ],
        timeLimit: [
          { required: true, message: '时间限制不能为空', trigger: 'blur' },
        ],
        memoryLimit: [
          { required: true, message: '内存限制不能为空', trigger: 'blur' },
        ],
      },
    };
  },
  computed: {
    isCreatingProblem() {
      return this.problem_id === null;
    },
    isUpdatingProblem() {
      return this.problem_id !== null;
    },
  },
  methods: {
    getData() {
      const form = this.problemForm;
      return {
        title: form.title,
        text: form.text,
        extraInfo: {},
        judgeScheme: 'SimpComp',
        limitInfo: {
          time: parseFloat(form.timeLimit),
          memory: parseInt(form.memoryLimit, 10),
        },
      };
    },
    setFormData(problemData) {
      const data = problemData;
      this.problemForm = {
        title: data.title,
        text: data.text,
        timeLimit: data.limitInfo.time.toString(),
        memoryLimit: data.limitInfo.memory.toString(),
      };
    },
    onClickSubmit() {
      const problemData = this.getData();
      if (this.isCreatingProblem) {
        createProblem(problemData)
          .then((data) => {
            this.$message.success('创建问题成功');
            this.$router.push({
              name: 'ProblemDetail',
              params: {
                problem_id: data.problemID,
              },
            });
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('创建问题失败：网络错误');
                break;
              default:
                this.$message.error('创建问题失败：未知错误');
                break;
            }
          });
      } else if (this.isUpdatingProblem) {
        updateProblem(this.problem_id, problemData)
          .then((data) => {
            this.$message.success('更新问题成功');
            this.$router.push({
              name: 'ProblemDetail',
              params: {
                problem_id: this.problem_id,
              },
            });
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('更新问题失败：网络错误');
                break;
              default:
                this.$message.error('更新问题失败：未知错误');
                break;
            }
          });
      }
    },
  },

  mounted() {
    if (this.isCreatingProblem) {
      this.loading = false;
    } else if (this.isUpdatingProblem) {
      getProblem(this.problem_id)
        .then((problem) => {
          this.setFormData(problem);
          this.loading = false;
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('获取问题失败：网络错误');
              break;
            default:
              this.$message.error('获取问题失败：未知错误');
              break;
          }
        });
    } else {
      this.message.error('未知错误');
    }
  },
  watch: {
    problemForm: {
      deep: true,
      handler() {
        if ('problemForm' in this.$refs) {
          this.$refs.problemForm.validate((valid) => {
            this.formValid = valid;
          });
        } else {
          this.formValid = false;
        }
      },
    },
  },
};

</script>

<style scoped>
.markdown-text {
  text-align: left;
  font-size: 20px;
}
</style>
