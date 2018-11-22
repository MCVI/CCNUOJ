<template>
  <!-- 本组件是展示 当前比赛下 的所有题目的列表 -->
  <!-- 当点击本组件上的某个题目，将跳转到 conquesdetail，从而展示该题目的所有信息并提交代码 -->
  <!-- 本组件是由contdetail组件里"题目"菜单栏下的默认展示（跳转）过来的，-->
  <!-- 2018.11。02日 BUG:不能自动显示列表  应该是预加载的问题。。。。。需要动态加载？？-->
 <div>
   <el-table :data="problem" height="500" border style="width: 100%">

     <el-table-column prop="problemid" label="ID" sortable></el-table-column>
     <el-table-column prop="title" label="题目" border>
       <template  slot-scope="scope">
         <router-link :to="{
          name:'ConquesDetail',
          params:{
            problem_id: scope.row.problemid
           }
         }">
           {{scope.row.title}}
         </router-link>
       </template>
     </el-table-column>

   </el-table>
 </div>
</template>

<script>
import ContestProblemDetail from './ContestProblemDetail';

export default {
  name: 'ConquesList',
  data() {
    return {
      contestid: this.$route.params.contest_id, // props 赋值
      contest: null,
      problem: [],
      proid: 0,
    };
  },
  components: {
    ContestProblemDetail,
  },
  mounted() {
    this.$http.get('/api/contest_problem')
      .then((res) => {
        const prolist = res.body.data;
        prolist.forEach((contestProblem) => {
          if (contestProblem.contestid === this.contestid) {
            this.problem[this.proid] = contestProblem;
            this.proid += 1;
          }
        });
      })
      .catch((error) => {
        console.log(error);
      });
    this.$http.get('/api/problem')
      .then((res) => {
        const problemList = res.body.data;
        for (const contestProblem of this.problem) {
          for (const problem of problemList) {
            if (contestProblem.problemid === problem.id) {
              if (!contestProblem.title) {
                this.$set(contestProblem, 'title', problem.title);
                console.log('hhh', 'hhhh');
              }
            }
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
    // 应该是在后台拼装好了传递到前端的。。。。。。 2018.11.01日
  },
};
</script>

<style>

</style>
