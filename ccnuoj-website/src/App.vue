<template>
  <div id="app">
    <home-page/>
  </div>
</template>

<script>

import HomePage from './views/HomePage'

export default {
  name: 'App',
  components: {
    HomePage
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
