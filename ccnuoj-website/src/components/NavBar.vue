<template>
   <!-- 本组件是每个页面的菜单栏 包含了 “首页”“比赛”“题库”“课堂”“数据中心”的跳转  -->
 <div>
    <el-tabs v-model="activeName">

      <el-tab-pane label="首 页" name="PhotoWall"></el-tab-pane>

      <el-tab-pane label="比  赛" name="ContestList"></el-tab-pane>

      <el-tab-pane label="题  库" name="ProblemList"></el-tab-pane>

      <el-tab-pane label="课  堂"></el-tab-pane>

      <el-tab-pane label="数据中心"></el-tab-pane>

    </el-tabs>
 </div>
</template>

<script>

export default {
  name: 'NavBar',
  data () {
    return {
      activeName: 'UserLogin'
    }
  },
  components: {},
  created () {
  },
  watch: {
    'activeName': function (name) {
      this.$router.push({name: name}) //  动态加载 10.1 日
    }
  }
}
</script>

<style>
</style>
