<template>
  <div class="select-field">
    <label v-if="label" :for="selectId" class="select-field__label">{{ label }}</label>
    <div class="select-field__wrapper" :class="{ 'select-field__wrapper--focus': focused }">
      <select
        :id="selectId"
        class="select-field__select"
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
        @focus="focused = true"
        @blur="focused = false"
      >
        <option v-for="opt in options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <span class="select-field__chevron" aria-hidden="true">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
      </span>
    </div>
    <p v-if="error" class="select-field__error">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  label: String,
  modelValue: String,
  options: { type: Array, required: true },
  error: String,
})

defineEmits(['update:modelValue'])

const focused = ref(false)
const selectId = computed(() => `select-${props.label?.toLowerCase().replace(/\s+/g, '-') ?? Math.random().toString(36).slice(2)}`)
</script>

<style scoped>
.select-field { display: flex; flex-direction: column; gap: 5px; }

.select-field__label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gray-700);
  letter-spacing: 0.02em;
}

.select-field__wrapper {
  position: relative;
  border: 1.5px solid var(--gray-300);
  border-radius: var(--radius-md);
  background: #fff;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.select-field__wrapper--focus {
  border-color: var(--green-500);
  box-shadow: 0 0 0 3px rgba(58,153,80,0.12);
}

.select-field__select {
  width: 100%;
  padding: 0.55rem 2.25rem 0.55rem 0.8rem;
  border: none;
  background: transparent;
  font-size: 0.9rem;
  color: var(--gray-900);
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.select-field__chevron {
  pointer-events: none;
  position: absolute;
  right: 0.6rem;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--gray-400);
}
.select-field__chevron svg { width: 100%; height: 100%; }

.select-field__error { font-size: 0.78rem; color: var(--red-500); }
</style>
