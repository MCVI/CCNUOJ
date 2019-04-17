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

import AsyncComponentLoading from './AsyncComponentLoading';
import AsyncComponentError from './AsyncComponentError';

const asyncComponentFactory = (path, delay, timeout) => () => ({
  component: import(`@/${path}`),
  loading: AsyncComponentLoading,
  error: AsyncComponentError,
  delay,
  timeout,
});

export default {
  name: 'AsyncComponent',
  inheritAttrs: false, // do not make unregistered props as HTML properties
  props: {
    path: {
      type: String,
      required: true,
    },
    keepAlive: {
      type: Boolean,
      required: false,
      default: true,
    },
    delay: {
      type: Number,
      required: false,
      default: 200, // delay before display to avoid flickering
    },
    timeout: {
      type: Number,
      required: false,
      default: undefined,
    },
  },
  computed: {
    comp() {
      return asyncComponentFactory(this.path, this.delay, this.timeout);
    },
  },
};

</script>

<style scoped>
</style>
