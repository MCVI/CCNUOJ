<template>

<page-common>

  <div>

    <div class="left">
      <router-view/>
    </div>

    <div class="right">
      <recommend-problem/>
    </div>

  </div>

</page-common>

</template>

<script>

import PageCommon from './PageCommon';
import RecommendProblem from '../components/Recommend/RecommendProblem';
import AskForHelp from '../components/Help/AskForHelp';

export default {
  name: 'RecommendPage',
  components: { PageCommon, RecommendProblem },
};

</script>

<style scoped>
</style>
