<template>

<page-common>

  <div>

    <div class="left">
      <router-view/>
    </div>

    <div class="right">
      <ask-for-help/>
    </div>

  </div>

</page-common>

</template>

<script>

import PageCommon from './PageCommon';
import AskForHelp from '../components/Help/AskForHelp';

export default {
  name: 'HelpPage',
  components: { PageCommon, AskForHelp },
};

</script>

<style scoped>
</style>
