<template>
  <div class="loading">
    <div v-loading="true"></div>
  </div>
</template>

<script>

export default {
  name: 'AsyncComponentLoading',
};

</script>

<style scoped>

.loading {
  height: 100%;
  width: 100%;
  display: table;
}

</style>
