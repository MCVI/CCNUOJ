<template>
<div>
   <div class="left">
       <router-view/>
  </div>
  <div class="right">
    <img src="../assets/acmlogo.jpg">
    <p>{{ msg }}</p>
      <router-link to="login" style="height:50px">
        <el-tag class="centerButton">login</el-tag>
      </router-link>
      <router-link to="register">
         <el-tag class="centerButton">register</el-tag>
       </router-link>
      
  </div>
</div>
</template>

<script>
import login from '../components/login'
import register from '../components/register'
export default {
  name: 'HelloWorld',
 data() {
      return {

        msg: "Welcome to CCNU OJ and Analysis System",
      }
  },

  components: {
    login,
    register
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped> /* 只对当前页面有效 */

   *{
       margin:0;
       padding: 0;
   }

   .right{
       margin-left: 700px;
       width: 600px;
       height: 500px;
       background-color: rgb(195, 207, 224);
   }

   .centerButton{
        width:100px ; height:50px ;  text-align:center; line-height:50px; color:rgb(52, 119, 196); background-color: white; border: null;
   }
   .right p{
      font-size: 70%;
   }
   .right img{
      width: 100px;
   }

   .left{
     float: left;
     height: 350px;
     width: 600px;
   }

</style>
