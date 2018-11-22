<template>
  <div>
    <!-- 取值如下 -->

    <p class="title-css">
      {{ problem['title'] }}
    </p>

    <div class="text-css">
      {{ problem['text'] }}
    </div>

    <br/>

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

    <el-input :rows="10" placeholder="请输入内容" type="textarea" v-model="textarea"></el-input>

    <el-button round type="primary">提交</el-button>

  </div>
</template>

<script>
export default {
  name: 'ProblemDetail',
  data() {
    return {
      textarea: '',
      options: [{
        value: 'c++',
        label: 'c++',
      }, {
        value: 'c',
        label: 'c',
      }, {
        value: 'c#',
        label: 'c#',
      }, {
        value: 'python',
        label: 'python',
      }, {
        value: 'java',
        label: 'java',
      }],
      language: '',
      problem: null,
    };
  },
  components: {},
  mounted() {
    this.$http.get('/api/problem')
      .then((res) => {
        const id = this.$route.params.problem_id;
        const list = res.body.data;
        for (const problem of list) {
          if (problem.id === id) {
            problem.text = this.renderText(problem.text);
            this.problem = problem;
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    renderText(text) {
      return text
        .replace(/\r\n/ig, '<br/><br/>')
        .replace(/描述/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        .replace(/输入格式/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        .replace(/输出格式/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        .replace(/样例/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        .replace(/input/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        .replace(/output/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>');
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

</style>
