<template>
  <div class="field">
    <label v-if="label" :for="inputId" class="field__label">{{ label }}</label>
    <div class="field__wrapper" :class="{ 'field__wrapper--error': error, 'field__wrapper--focus': focused }">
      <input
        :id="inputId"
        class="field__input"
        :type="type"
        :value="modelValue"
        :min="min"
        :max="max"
        :step="step"
        :placeholder="placeholder"
        @input="$emit('update:modelValue', $event.target.valueAsNumber || $event.target.value)"
        @focus="focused = true"
        @blur="focused = false"
      />
      <span v-if="suffix" class="field__suffix">{{ suffix }}</span>
    </div>
    <p v-if="error" class="field__error">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  label: String,
  modelValue: [String, Number],
  type: { type: String, default: 'number' },
  min: { type: Number, default: 0 },
  max: Number,
  step: { type: Number, default: 0.01 },
  placeholder: String,
  suffix: String,
  error: String,
})

defineEmits(['update:modelValue'])

const focused = ref(false)
const inputId = computed(() => `input-${props.label?.toLowerCase().replace(/\s+/g, '-') ?? Math.random().toString(36).slice(2)}`)
</script>

<style scoped>
.field { display: flex; flex-direction: column; gap: 5px; }

.field__label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gray-700);
  letter-spacing: 0.02em;
}

.field__wrapper {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--gray-300);
  border-radius: var(--radius-md);
  background: #fff;
  transition: border-color 0.15s, box-shadow 0.15s;
  overflow: hidden;
}
.field__wrapper--focus {
  border-color: var(--green-500);
  box-shadow: 0 0 0 3px rgba(58,153,80,0.12);
}
.field__wrapper--error {
  border-color: var(--red-500);
  box-shadow: 0 0 0 3px rgba(220,38,38,0.1);
}

.field__input {
  flex: 1;
  padding: 0.55rem 0.8rem;
  border: none;
  background: transparent;
  font-size: 0.9rem;
  color: var(--gray-900);
  outline: none;
  min-width: 0;
}
.field__input::placeholder { color: var(--gray-400); }

.field__suffix {
  padding: 0 0.75rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--gray-500);
  background: var(--gray-50);
  border-left: 1px solid var(--gray-200);
  height: 100%;
  display: flex;
  align-items: center;
  white-space: nowrap;
  align-self: stretch;
}

.field__error { font-size: 0.78rem; color: var(--red-500); }
</style>
