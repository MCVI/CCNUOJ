<template>
  <!-- 是 contestlisT  的儿子组件
     另一个儿子组件是 contable ,该组件是从后端获取所有的比赛,按照开始时间由近到远排序
     contdetail该组件是,当我们在conttable点击某一个比赛的时候,进入到该比赛的详情界面
    -->
 <div>
   <p>  {{ obj['contest']['title']}}  </p>
   <div>
     <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="题  目" name="conquestable"><conquestable :objj="obj"></conquestable></el-tab-pane>
    <el-tab-pane label="提交记录" name="conquesupdate"><conquesupdate :objj="obj"></conquesupdate></el-tab-pane>
    <el-tab-pane label="榜  单" name="conquesrank"><conquesrank :objj="obj"></conquesrank></el-tab-pane>
    </el-tabs>
 </div>
 </div>
</template>

<script>
import conquesrank from '../Contest/ConDetailPage/conquesrank'
import conquestable from '../Contest/ConDetailPage/conquestable'
import conquesupdate from '../Contest/ConDetailPage/conquesupdate'
import conquesdetail from '../Contest/ConDetailPage/conquesdetail'
export default {
  name: 'ContestDetail',
  data () {
    return {
      activeName: 'conquestable',
      obj: this.$route.query
    }
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event)
    }
  },
  components: {
    conquesrank,
    conquestable,
    conquesupdate,
    conquesdetail
  }
}
</script>

<style>

</style>
