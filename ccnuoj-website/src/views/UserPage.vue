<template>

<page-common>

  <div>

    <div class="left">
      <router-view/>
    </div>

    <div class="right">
      <greeting-message/>
    </div>

  </div>

</page-common>

</template>

<script>

import PageCommon from './PageCommon';
import GreetingMessage from '../components/GreetingMessage';

export default {
  name: 'UserPage',
  components: { GreetingMessage, PageCommon },
};

</script>

<style scoped>

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

</style>
