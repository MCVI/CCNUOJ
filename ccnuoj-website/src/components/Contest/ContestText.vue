<template>

  <div>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>
      <template v-if="textEditable">
        <el-button @click="onClickEditText()" style="float: right;" type="primary">编辑文本</el-button>
      </template>

      <div v-html="text" class="contest-text"></div>
    </template>

  </div>

</template>

<script>

import { mapGetters } from 'vuex';
import marked from 'marked';

import { getContest } from '@/api/Contest';
import ContestRegisterStateDisplay from './Register/ContestRgisterStateDisplay';

export default {
  name: 'ContestText',
  components: { ContestRegisterStateDisplay },
  data() {
    return {
      loading: true,
      contest: {},
      text: '',
    };
  },
  computed: {
    textEditable() {
      if (this.loading) {
        return undefined;
      } else {
        return (this.userID === this.contest.author.id) || (this.isSuper);
      }
    },

    ...mapGetters({
      userID: 'user/id',
      isSuper: 'user/isSuper',
    }),
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
    text-align: left;
    font-size: 20px;
  }
</style>
