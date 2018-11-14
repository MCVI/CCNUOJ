<template>
    <div>
        <el-menu
            :default-active="activeIndex"
            mode="horizontal"
            :router="true"
            background-color="#409EFF"
            text-color="#fff"
            active-text-color="#ffd04b">
        <el-menu-item index="/photo">首 页</el-menu-item>
        <el-menu-item index="/contest/list">比 赛</el-menu-item>
        <el-menu-item index="/problem/list">题 库</el-menu-item>
        <el-menu-item index="/login">课 堂</el-menu-item>
        <el-menu-item index="/register">数据中心</el-menu-item>
        </el-menu>
    </div>
</template>

<script>
export default {
  data () {
    return {
      activeIndex: ''
    }
  },
  mounted: function () {
    this.activeIndex = this.$route.path
  },
  watch: {
    $route: function () {
      this.activeIndex = this.$route.path
    }
  }
}
</script>
