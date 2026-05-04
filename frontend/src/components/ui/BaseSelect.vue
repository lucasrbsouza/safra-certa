<template>
  <div class="select-field">
    <label v-if="label" :for="selectId" class="select-field__label">{{ label }}</label>
    <select
      :id="selectId"
      class="select-field__select"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
    <p v-if="error" class="select-field__error">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  modelValue: String,
  options: { type: Array, required: true },
  error: String,
})

defineEmits(['update:modelValue'])

const selectId = computed(() => `select-${props.label?.toLowerCase().replace(/\s/g, '-') ?? Math.random()}`)
</script>

<style scoped>
.select-field { display: flex; flex-direction: column; gap: 4px; }
.select-field__label { font-size: 0.85rem; font-weight: 600; color: #333; }
.select-field__select {
  padding: 0.5rem 0.75rem;
  border: 1.5px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  background: #fff;
  cursor: pointer;
  outline: none;
}
.select-field__select:focus { border-color: #2e7d32; }
.select-field__error { font-size: 0.8rem; color: #c62828; }
</style>
