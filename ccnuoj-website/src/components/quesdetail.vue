<template>
  <div>
    <!-- 取值如下 -->
    <p class="title-css">
      {{ obj['ques']['title'] }}
    </p>
    <div class="text-css" id="hungrywww" v-pyl>
      {{ obj['ques']['text']}}
    </div>
    <br/>
    <p style='font-size: 20px;font-weight:500;text-align:left;'> 提交代码 </p>
    <el-select clearable placeholder="请选择" style='float:left' v-model="language">
      <el-option
        :key="item.value"
        :label="item.label"
        :value="item.value"
        v-for="item in options">
      </el-option>
    </el-select>
    <br/>
    <el-input
      :rows="10"
      placeholder="请输入内容"
      type="textarea"
      v-model="textarea">
    </el-input>
    <el-button round type="primary">submit</el-button>
  </div>
</template>

<script>
export default {
  name: 'quesdetail',
  data () {
    return {
      textarea: '',
      options: [{
        value: 'c++',
        label: 'c++'
      }, {
        value: 'c',
        label: 'c'
      }, {
        value: 'c#',
        label: 'c#'
      }, {
        value: 'python',
        label: 'python'
      }, {
        value: 'java',
        label: 'java'
      }],
      language: '',
      obj: this.$route.query
      // query来的就是对象。 JSON 对象
    }
  },
  components: {},
  watch: {
    'language': function (language) {
      console.log(language)
    },
    'textarea': function (textarea) {
      console.log(textarea)
    }
  },
  methods: {},
  directives: {
    pyl: {
      inserted: function (el) {
        console.log('please')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/\r\n/ig, '<br/><br/>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/描述/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/输入格式/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/输出格式/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/样例/g, '<br/><br/><p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/input/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
        document.getElementById('hungrywww').innerHTML = document.getElementById('hungrywww').innerHTML.replace(/output/g, '<p style=\'font-size: 20px;font-weight:500;text-align:left\'> $&</p>')
      }
    }
  }
}

</script>

<style>
  .title-css {
    width: 90%;
    height: 100px;
    font-size: 50%;
    font-weight: 600;
    text-align: center;
    font-family: 宋体, 幼圆, sans-serif;
    border-bottom: 1px solid #000
  }

  .text-css {
    width: 90%;
    font-size: 20px;
    font-family: 幼圆, sans-serif;
    word-wrap: break-word;
    word-break: keep-all;
    text-align: left;
  }

  /* 强制换行 */
  .text-css p {
    text-align: left;
  }

  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }

  .el-icon-arrow-down {
    font-size: 12px;
  }

</style>
