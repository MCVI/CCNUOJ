<template>

  <div v-loading="loading">
    <div v-html="text"></div>
  </div>

</template>

<script>
import marked from 'marked';

import { getContest } from '@/api/Contest';

export default {
  name: 'ContestRegister',

  data() {
    return {
      loading: true,
      contest: {},
      text: '',
    };
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
</style>
