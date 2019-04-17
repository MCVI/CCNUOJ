<template>
  <div class="loading-error-external">
    <div class="loading-error-internal">
      <div>加载错误</div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'AsyncComponentError',
};

</script>

<style scoped>

.loading-error-external {
  height: 100%;
  width: 100%;
  display: table;
}

.loading-error-internal {
  display: table-cell;
  vertical-align: middle;
  text-align: center;
}

</style>
