<template>
  <div class="d-flex align-items-center justify-content-center py-5">
    <div class="spinner-border text-info" role="status" :style="{ width: size, height: size }">
      <span class="visually-hidden">Loading...</span>
    </div>
    <span v-if="label" class="ms-3 text-white-50 fs-7">{{ label }}</span>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    label: { type: String, default: '' },
    size: { type: String, default: '2rem' }
  }
};
</script>

<style scoped>
.fs-7 { font-size: 0.85rem; }
</style>
