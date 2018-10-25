<template>
  <!-- 本组件是每个页面的菜单栏 包含了 “首页”“比赛”“题库”“课堂”“数据中心”的跳转  -->
  <div>
    <el-tabs @tab-click="handleClick" v-model="activeName">
      <el-tab-pane label="首  页" name="photowalls"></el-tab-pane>
      <el-tab-pane label="比  赛" name="contest"></el-tab-pane>
      <el-tab-pane label="题  库" name="queslist"></el-tab-pane>
      <el-tab-pane label="课  堂" name="class"></el-tab-pane>
      <el-tab-pane label="数据中心" name="analysis"></el-tab-pane>
    </el-tabs>
    <router-view/>
  </div>
</template>

<script>
import queslist from '../components/queslist'
import photowalls from '../components/photowalls'

export default {
  name: 'homeheader',
  data () {
    return {
      activeName: 'qaq'
      // 10.1
      //  初始化tab 路径为 “/” 也就是转到了helloworld组件， 可是我想让他转到photowalls组件，但是必须重新跳转一次路径才对。
      //  所以出了一个歪主意 ， 随便初始化一个activeName（此时是helloworld组件）， 然后再次点击路径正确。
    }
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event)
    }
  },
  created () {
  },
  watch: {
    'activeName': function (val) {
      let url = '/' + val
      this.$router.push(url) //  动态加载 10.1 日
    }
  },
  components: {
    queslist,
    photowalls
  }
}
</script>
<style>
</style>
