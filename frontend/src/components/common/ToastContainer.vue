<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="['toast show bg-glass text-light border', toast.type === 'error' ? 'border-danger' : 'border-success']"
      role="alert"
    >
      <div class="toast-header bg-dark text-light border-bottom border-secondary justify-content-between">
        <strong class="me-auto text-uppercase">{{ toast.type === 'error' ? 'Error' : 'Success' }}</strong>
        <button type="button" class="btn-close btn-close-white" @click="$emit('remove', toast.id)"></button>
      </div>
      <div class="toast-body fs-7">{{ toast.message }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ToastContainer',
  props: { toasts: { type: Array, default: () => [] } },
  emits: ['remove']
};
</script>

<style scoped>
.bg-glass { background: rgba(26, 29, 46, 0.90); backdrop-filter: blur(10px); }
.fs-7 { font-size: 0.85rem; }
</style>
