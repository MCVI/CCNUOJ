<template>
  <el-menu
    :default-active="activeIndex"
    mode="horizontal"
    :router="true"
    background-color="#409EFF"
    text-color="#fff"
    active-text-color="#ffd04b">

    <el-menu-item index="/home">首 页</el-menu-item>
    <el-menu-item index="/contest/list">比 赛</el-menu-item>
    <el-menu-item index="/problem/list">题 库</el-menu-item>
    <el-menu-item disabled index="">课 堂</el-menu-item>
    <el-menu-item disabled index="">数据中心</el-menu-item>

    <div style="float: right;" class="el-menu--horizontal">
      <template v-if="loginState === null">
        <el-menu-item index="/user/login">登 录</el-menu-item>
        <el-menu-item index="/user/register">注 册</el-menu-item>
      </template>
      <template v-else-if="loginState === undefined">
        <el-menu-item
          index=""
          v-loading="true"
          element-loading-spinner="el-icon-loading"
          element-loading-background="#409EFF"
          class="is-active custom-color"
        />
      </template>
      <template v-else>
        <el-submenu index="/user/info">
          <template slot="title">{{ loginState }}</template>
          <el-menu-item index="/user/info">用户信息</el-menu-item>
          <el-menu-item @click="onClickLogout()" index="">退出登录</el-menu-item>
        </el-submenu>
      </template>
    </div>

  </el-menu>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: 'undefined',
    };
  },
  computed: {
    loginState() {
      return this.$store.getters['user/shortName'];
    },
  },

  methods: {
    onClickLogout() {
      this.$store.dispatch('user/logout');
    },
  },

  mounted() {
    this.activeIndex = this.$route.path;
  },
  watch: {
    $route() {
      this.activeIndex = this.$route.path;
    },
  },
};
</script>

<style scoped>
  .custom-color{
    color: black !important;
  }
</style>
