<template>

  <div v-loading="loading">
    <div>
      <el-button @click="onClickEditText()" style="float: right;" type="primary">编辑文本</el-button>
      <div v-html="text" class="contest-text"></div>
    </div>

    <contest-register-state-display></contest-register-state-display>
  </div>

</template>

<script>
import marked from 'marked';

import { getContest } from '@/api/Contest';
import ContestRegisterStateDisplay from './ContestRgisterStateDisplay';

export default {
  name: 'ContestRegister',
  components: { ContestRegisterStateDisplay },
  data() {
    return {
      loading: true,
      contest: {},
      text: '',
    };
  },

  methods: {
    onClickEditText() {
      this.$router.push({
        name: 'ContestTextEditor',
        params: {
          contest_id: this.$route.params.contest_id,
        },
      });
    },
  },

  mounted() {
    getContest(this.$route.params.contest_id)
      .then((result) => {
        this.contest = result;
        this.text = marked(this.contest.text, { sanitize: true });
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
};

</script>

<style scoped>
  .contest-text {
    font-size: 20px;
  }
</style>
