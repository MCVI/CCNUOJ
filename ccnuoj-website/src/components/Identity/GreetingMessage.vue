<template>

<div>

  <div class="left">
    <slot></slot>
  </div>

  <div class="right">

    <img src="../../assets/acmlogo.jpg">

    <p>Welcome to CCNU OJ and Analysis System</p>

    <router-link style="height:50px" to="login">
      <el-tag class="switch-button">登录</el-tag>
    </router-link>

    <router-link to="register">
      <el-tag class="switch-button">注册</el-tag>
    </router-link>

  </div>

</div>

</template>

<script>

export default {
  name: 'GreetingMessage',
  data () {
    return {}
  },
  components: {}
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped> /* 只对当前页面有效 */

* {
  margin: 0;
  padding: 0;
}

.left {
  float: left;
  margin-left: 5%;
  margin-right: 5%;
  height: 100%;
  width: 52%;
}

.right {
  margin-left: 62%;
  width: 38%;
  height: 100%;
  background-color: rgb(195, 207, 224);
}

.switch-button {
  width: 100px;
  height: 50px;
  text-align: center;
  line-height: 50px;
  color: rgb(52, 119, 196);
  background-color: white;
}

.right p {
  font-size: 70%;
}

.right img {
  width: 100px;
}

</style>
