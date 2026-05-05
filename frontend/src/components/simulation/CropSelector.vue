<template>
  <div class="crop-selector" role="group" aria-label="Selecionar cultura">
    <button
      v-for="crop in crops"
      :key="crop.value"
      :class="['crop-btn', `crop-btn--${crop.value}`, { 'crop-btn--active': modelValue === crop.value }]"
      type="button"
      @click="$emit('update:modelValue', crop.value)"
    >
      <span class="crop-btn__icon">{{ crop.icon }}</span>
      <span class="crop-btn__label">{{ crop.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({ modelValue: { type: String, required: true } })
defineEmits(['update:modelValue'])

const crops = [
  { value: 'soja',   label: 'Soja',   icon: '🌱' },
  { value: 'milho',  label: 'Milho',  icon: '🌽' },
  { value: 'feijao', label: 'Feijão', icon: '🫘' },
]
</script>

<style scoped>
.crop-selector {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.crop-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-lg);
  background: #fff;
  color: var(--gray-600);
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.crop-btn:hover:not(.crop-btn--active) {
  border-color: var(--green-300);
  background: var(--green-50);
  color: var(--green-700);
}

.crop-btn--active {
  border-color: var(--green-500);
  background: var(--green-600);
  color: #fff;
  box-shadow: 0 2px 6px rgba(45,122,62,0.3);
}

.crop-btn__icon { font-size: 1rem; line-height: 1; }
</style>
