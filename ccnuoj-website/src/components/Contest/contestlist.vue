<template>
<!-- contestlisT  有两个儿子的组件
     一个是 contable ,该组件是从后端获取所有的比赛,按照开始时间由近到远排序
     另一个是contdetail , 该组件是,当我们在conttable点击某一个比赛的时候,进入到该比赛的详情界面
    -->
 <div>
      <router-link to=""></router-link>
      <router-view/>
 </div>
</template>

<script>
export default {
  name: 'contestlist',
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
