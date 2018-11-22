<template>
  <!-- 本组件 是 展示 当前比赛下的某个题目的细节（题目内容、时间限制、内存限制、提交代码） -->
  <!-- 本组件是由conquestable跳转过来的 -->
 <div>
    {{id}}
 </div>
</template>

<script>
export default {
  data() {
    return {
      id: this.$route.params.problem_id,
    };
  },
  components: {

  },
};
</script>

<style>

</style>
