<template>
  <el-tag :type="type" size="medium">
    {{ displayName }}
  </el-tag>
</template>

<script>

/* eslint-disable quote-props */
const judgeStateMap = {
  'WAIT': { displayName: '正在等待', type: 'info' },
  'PEND': { displayName: '正在排队', type: undefined },

  'CMPL': { displayName: '正在编译', type: undefined },
  'CE': { displayName: '编译错误', type: 'danger' },
  'CTLE': { displayName: '编译超时', type: 'danger' },

  'RUN': { displayName: '正在运行', type: undefined },
  'RE': { displayName: '运行错误', type: 'danger' },
  'TLE': { displayName: '运行超时', type: 'danger' },
  'MLE': { displayName: '内存超限', type: 'danger' },
  'OLE': { displayName: '输出超限', type: 'danger' },

  'CMPR': { displayName: '正在比较', type: undefined },

  'AC': { displayName: '顺利通过', type: 'success' },
  'WA': { displayName: '答案错误', type: 'danger' },
  'PE': { displayName: '格式错误', type: 'warning' },

  'SYSE': { displayName: '系统错误', type: 'danger' },
};

export default {
  name: 'JudgeRequestState',
  props: {
    value: String,
  },
  computed: {
    displayName() {
      return judgeStateMap[this.value].displayName;
    },
    type() {
      return judgeStateMap[this.value].type;
    },
  },
};

</script>

<style scoped>
</style>
