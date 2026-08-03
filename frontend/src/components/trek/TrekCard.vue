<template>
  <div class="card bg-glass text-light border border-secondary shadow-lg rounded-4 overflow-hidden h-100">
    <div class="card-body p-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span :class="['badge', difficultyClass]">{{ trek.difficulty }}</span>
        <span class="fs-8 text-white-50 font-monospace">
          Available Slots: {{ trek.available_slots }} / {{ trek.total_slots }}
        </span>
      </div>

      <h5 class="fw-bold text-light mb-2">{{ trek.trek_name }}</h5>
      <p class="text-white-50 fs-7 mb-3 text-truncate-2">{{ trek.description || 'No description provided.' }}</p>

      <div class="fs-7 border-top border-dark pt-2 mb-3">
        <div class="mb-1"><strong>Location:</strong> <span class="text-light">{{ trek.location }}</span></div>
        <div class="mb-1"><strong>Duration:</strong> <span class="text-light">{{ trek.duration_days }} Days</span></div>
        <div><strong>Dates:</strong> <span class="text-warning">{{ trek.start_date }} to {{ trek.end_date }}</span></div>
      </div>

      <button
        @click="$emit('book', trek)"
        :disabled="trek.available_slots === 0"
        class="btn btn-primary w-100 rounded-pill mt-auto"
        data-bs-toggle="modal"
        data-bs-target="#bookingModal"
      >
        {{ trek.available_slots > 0 ? 'Book Trail' : 'Sold Out' }}
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'TrekCard',
  props: {
    trek: { type: Object, required: true }
  },
  emits: ['book'],
  setup(props) {
    const difficultyClass = computed(() => {
      const map = { Easy: 'bg-success', Moderate: 'bg-warning', Hard: 'bg-danger' };
      return map[props.trek.difficulty] || 'bg-secondary';
    });
    return { difficultyClass };
  }
};
</script>

<style scoped>
.bg-glass {
  background: rgba(26, 29, 46, 0.85);
  backdrop-filter: blur(10px);
}
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.fs-7 { font-size: 0.85rem; }
.fs-8 { font-size: 0.75rem; }
</style>
