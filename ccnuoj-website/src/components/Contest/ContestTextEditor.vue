<template>
  <div>

    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else>

      <el-row>
        <el-col :span="1">
          <br/>
        </el-col>
        <el-col :span="9">
          <el-input
            v-model="text"
            type="textarea"
            autosize
            placeholder="请输入比赛文本"
          >
          </el-input>
        </el-col>
        <el-col :span="3">
          <br/>
        </el-col>
        <el-col :span="9">
          <el-input
            v-html="renderResult"
            class="contest-text"
            type="textarea"
            readonly="true"
            autosize
            placeholder="比赛文本为空"
          >
          </el-input>
        </el-col>
        <el-col :span="1">
          <br/>
        </el-col>
      </el-row>

      <el-row>
        <el-button @click="onClickSubmit()" type="primary">提交</el-button>
      </el-row>

    </template>

  </div>

</template>

<script>
import marked from 'marked';

import { getContest, updateContestText } from '@/api/Contest';

export default {
  name: 'ContestTextEditor',
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
    renderResult() {
      if (this.text === undefined) {
        return undefined;
      } else {
        return marked(this.text, { sanitize: true });
      }
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
    this.loading = false;
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
  .contest-text {
    text-align: left;
    font-size: 20px;
  }
</style>
