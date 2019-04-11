<template>
  <div>
    <el-row>
      <el-col :span="1">
        <br/>
      </el-col>
      <el-col :span="9">
        <el-input
          :value="value"
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
        <markdown-viewer :value="value"></markdown-viewer>
      </el-col>
      <el-col :span="1">
        <br/>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MarkdownViewer from './MarkdownViewer';

export default {
  name: 'MarkdownEditor',
  components: {
    MarkdownViewer,
  },
  props: {
    value: String,
  },
  model: {
    prop: 'value',
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
</style>
