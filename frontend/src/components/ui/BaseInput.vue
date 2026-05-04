<template>
  <div class="field">
    <label v-if="label" :for="inputId" class="field__label">{{ label }}</label>
    <div class="field__wrapper">
      <input
        :id="inputId"
        class="field__input"
        :class="{ 'field__input--error': error }"
        :type="type"
        :value="modelValue"
        :min="min"
        :max="max"
        :step="step"
        :placeholder="placeholder"
        @input="$emit('update:modelValue', $event.target.valueAsNumber || $event.target.value)"
      />
      <span v-if="suffix" class="field__suffix">{{ suffix }}</span>
    </div>
    <p v-if="error" class="field__error">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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

const inputId = computed(() => `input-${props.label?.toLowerCase().replace(/\s/g, '-') ?? Math.random()}`)
</script>

<style scoped>
.field { display: flex; flex-direction: column; gap: 4px; }
.field__label { font-size: 0.85rem; font-weight: 600; color: #333; }
.field__wrapper { display: flex; align-items: center; }
.field__input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1.5px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}
.field__input:focus { border-color: #2e7d32; }
.field__input--error { border-color: #c62828; }
.field__suffix { margin-left: 8px; font-size: 0.85rem; color: #666; white-space: nowrap; }
.field__error { font-size: 0.8rem; color: #c62828; }
</style>
