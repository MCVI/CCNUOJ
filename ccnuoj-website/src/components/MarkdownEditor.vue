<template>
  <div>
    <el-row>
      <el-col :span="1">
        <br/>
      </el-col>
      <el-col :span="9">
        <el-input
          :value="text"
          @input="onInput"
          type="textarea"
          autosize
          placeholder="请输入文本"
        >
        </el-input>
      </el-col>
      <el-col :span="3">
        <br/>
      </el-col>
      <el-col :span="9">
        <el-input
          v-html="renderedText"
          class="markdown-text"
          type="textarea"
          :readonly="true"
          autosize
          placeholder="文本为空"
        >
        </el-input>
      </el-col>
      <el-col :span="1">
        <br/>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import marked from 'marked';

export default {
  name: 'MarkdownEditor',
  props: {
    text: String,
  },
  computed: {
    renderedText() {
      return marked(this.text, { sanitize: true });
    },
  },
  model: {
    prop: 'text',
    event: 'change',
  },
  methods: {
    onInput(value) {
      this.$emit('change', value);
    },
  },
};

</script>

<style scoped>
.markdown-text {
  text-align: left;
  font-size: 20px;
}
</style>
