<template>
  <div>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>

      <markdown-editor v-model="text"></markdown-editor>

      <el-row>
        <el-button @click="onClickSubmit()" type="primary">提交</el-button>
      </el-row>

    </template>

  </div>

</template>

<script>
import { getContest, updateContestText } from '@/api/Contest';
import MarkdownEditor from '../MarkdownEditor';

export default {
  name: 'ContestTextEditor',
  components: {
    MarkdownEditor,
  },
  data() {
    return {
      loading: true,
      text: undefined,
    };
  },
  computed: {
    contestID() {
      return this.$route.params.contest_id;
    },
  },

  methods: {
    onClickSubmit() {
      updateContestText(this.contestID, this.text)
        .then(() => {
          this.$message.success('更新比赛信息成功');
          this.$router.push({
            name: 'ContestText',
            params: {
              contest_id: this.contestID,
            },
          });
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('更新比赛信息失败：网络错误');
              break;
            default:
              this.$message.error('更新比赛信息失败：未知错误');
              break;
          }
        });
    },
  },

  mounted() {
    getContest(this.contestID)
      .then((result) => {
        this.text = result.text;
        this.loading = false;
      })
      .catch((error) => {
        switch (error) {
          case 'NetworkError':
            this.$message.error('获取比赛信息失败：网络错误');
            break;
          default:
            this.$message.error('获取比赛信息失败：未知错误');
            break;
        }
      });
  },
};

</script>

<style scoped>
</style>
