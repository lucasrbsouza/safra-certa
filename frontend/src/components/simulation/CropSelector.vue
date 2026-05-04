<template>
  <div class="crop-selector">
    <button
      v-for="crop in crops"
      :key="crop.value"
      :class="['crop-selector__btn', { 'crop-selector__btn--active': modelValue === crop.value }]"
      type="button"
      @click="$emit('update:modelValue', crop.value)"
    >
      {{ crop.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({ modelValue: { type: String, required: true } })
defineEmits(['update:modelValue'])

const crops = [
  { value: 'soja', label: 'Soja' },
  { value: 'milho', label: 'Milho' },
  { value: 'feijao', label: 'Feijão' },
]
</script>

<style scoped>
.crop-selector { display: flex; gap: 0; border-radius: 8px; overflow: hidden; border: 1.5px solid #2e7d32; width: fit-content; }
.crop-selector__btn {
  padding: 0.5rem 1.2rem;
  border: none;
  background: #fff;
  color: #2e7d32;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  font-size: 0.9rem;
}
.crop-selector__btn--active { background: #2e7d32; color: #fff; }
.crop-selector__btn:not(.crop-selector__btn--active):hover { background: #e8f5e9; }
</style>
