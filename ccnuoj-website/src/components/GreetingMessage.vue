<template>

<div>

  <img src="../assets/acmlogo.jpg" alt="CCNU ACM">

  <p>Welcome to CCNU OJ and Analysis System</p>

  <router-link style="height:50px" to="login">
    <el-tag class="switch-button">登录</el-tag>
  </router-link>

  <router-link to="register">
    <el-tag class="switch-button">注册</el-tag>
  </router-link>

</div>

</template>

<script>

export default {
  name: 'GreetingMessage'
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

* {
  margin: 0;
  padding: 0;
}

.switch-button {
  width: 100px;
  height: 50px;
  text-align: center;
  line-height: 50px;
  color: rgb(52, 119, 196);
  background-color: white;
}

p {
  font-size: 40%;
}

img {
  width: 100px;
}

</style>
