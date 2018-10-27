<template>
   <!-- queslist 下面有两种组件
         一个是 questable ，是默认组件，里面显示了全部的题目的信息
         另一个是 quesdetail ， 当我们在questable里点击了某个题目，那么组件将转至到 显示 该题目的详细信息的 quesdetail
               需要用到动态router的方法（含参数 question 的 id（主键） ）
    -->
 <div>
    <router-link to=""></router-link>
    <router-view/>
 </div>
</template>

<script>
export default {
  data () {
    return {

    }
  },
  components: {

  }
}
</script>

<style>

</style>
