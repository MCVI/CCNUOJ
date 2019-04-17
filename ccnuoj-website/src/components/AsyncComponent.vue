<template>
  <keep-alive v-if="keepAlive">
    <component
      :is="comp"
      v-bind="$attrs"
      v-on="$listeners"/>
  </keep-alive>
  <component
    v-else
    :is="comp"
    v-bind="$attrs"
    v-on="$listeners"/>
</template>

<script>
/*
  Asynchronous Dynamic Component Loader
*/

import asyncLoad from './async-load';

export default {
  name: 'AsyncComponent',
  inheritAttrs: false, // do not make unregistered props as HTML properties
  props: {
    path: {
      type: String,
      required: true,
    },
    delay: {
      type: Number,
      required: false,
      default: undefined,
    },
    timeout: {
      type: Number,
      required: false,
      default: undefined,
    },
    keepAlive: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  computed: {
    comp() {
      return asyncLoad(import(this.path), this.delay, this.timeout);
    },
  },
};

</script>

<style scoped>
</style>
