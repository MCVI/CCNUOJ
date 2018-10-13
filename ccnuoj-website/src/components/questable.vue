<template>
<!-- 本组件是 从后端调用题目数据 显示题目list  -->
 <div>
    <el-table
    :data="question"
    height="500"
    border
    style="width: 100%">
    <el-table-column
      prop="id"
      label="编号"
      sortable
      style="width: 20%">
    </el-table-column>
    <el-table-column
      prop="title"
      label="题目"
      border
      style="width: 20%">
       <template  slot-scope="scope">
        <router-link :to=" { name:'quesdetail', query:{ques:scope.row}}">
              {{scope.row.title}}
        </router-link> 
       </template>
     </el-table-column>
     <el-table-column
      prop="author"
      label="作者"
      border
      style="width: 20%">
    </el-table-column>
     <el-table-column
      prop="createTime"
      label="创建时间"
      border
      style="width: 20%">
    </el-table-column>
     <el-table-column
      prop="lastModifiedTime"
      label="修改时间"
      border
      style="width: 20%">
    </el-table-column>
  </el-table>
 </div>
</template>

<script>
 import quesdetail from "../components/quesdetail"
 export default {
     name: "queslist",
     data () {
       return {
        question:[],

       }
     },
     created(){
     },

    //  模拟 数据
     mounted: function (){
          var _this = this   //很重要！！
          this.$http.get('/api/question')
              .then(function (res) {
                  console.log(res);
                  _this.question = res.body.data
              })
              .catch(function (error) {
                    console.log(error);
              });
     },
    components: {
      quesdetail
    },
    methods: {
        // routeQuedetail(id){
        //     console.log(hhhhhh)
        //     this.$router.push({name:'quesdetail',params:{quesObj:id}})
        // }

    }
}
</script>

<style>

 
</style>
