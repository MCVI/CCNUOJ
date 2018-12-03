<template>
<!-- 是 ContestList  的儿子组件
   ContestDetail组件是当我们在ContestList点击某一个比赛的时候,进入到该比赛的详情界面
  -->
<div>

  <p style="font-size: 70px;">{{ contest['title'] }}</p>

  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="介绍" name="ContestText"></el-tab-pane>
    <el-tab-pane label="报名" name="ContestRegisterStateDisplay">
      <el-row>
        <el-button
          @click="$router.push({name:'ContestRegisterStateDisplay'})"
          type="primary"
          style="float: left;">
          我的报名状态
        </el-button>
        <el-button
          @click="$router.push({name:'ContestRegisterPassedList'})"
          type="primary"
          style="float: left;">
          查看已通过审核列表
        </el-button>
        <el-button
          @click="$router.push({name:'ContestRegisterAllList'})"
          type="primary"
          style="float: left;">
          管理报名信息
        </el-button>
      </el-row>
    </el-tab-pane>
    <el-tab-pane label="题目" disabled></el-tab-pane>
    <el-tab-pane label="提交记录" disabled></el-tab-pane>
    <el-tab-pane label="榜单" disabled></el-tab-pane>
  </el-tabs>

  <router-view></router-view>

</div>

</template>

<script>
import { mapGetters } from 'vuex';
import { getContest } from '@/api/Contest';

export default {
  name: 'ContestDetail',

  data() {
    return {
      contest: {},
      activeName: '',
    };
  },
  computed: {
    isManager() {
      if ((this.contest !== undefined) && (this.contest.author.id === this.userID)) {
        return true;
      } else if (this.$store.getters['user/isSuper'] === true) {
        return true;
      }
      return false;
    },
    contestID() {
      return this.$route.params.contest_id;
    },
    ...mapGetters({
      userID: 'user/id',
      isSuper: 'user/isSuper',
    }),
  },

  methods: {
    handleClick() {
      const name = this.activeName;
      if (name) {
        this.$router.push({
          name,
          params: {
            contest_id: this.contestID,
          },
        });
      }
    },
  },

  mounted() {
    this.activeName = this.$route.name;
    getContest(this.contestID)
      .then((result) => {
        this.contest = result;
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
