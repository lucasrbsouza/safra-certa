<template>
  <button
    :class="['btn', `btn--${variant}`, { 'btn--loading': loading }]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <span v-if="loading" class="btn__spinner" aria-hidden="true"></span>
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: { type: String, default: 'primary' },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
})
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, background-color 0.2s;
}
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn--primary { background-color: #2e7d32; color: #fff; }
.btn--primary:hover:not(:disabled) { background-color: #1b5e20; }
.btn--secondary { background-color: #e8f5e9; color: #2e7d32; }
.btn--secondary:hover:not(:disabled) { background-color: #c8e6c9; }
.btn--danger { background-color: #c62828; color: #fff; }
.btn--danger:hover:not(:disabled) { background-color: #b71c1c; }
.btn__spinner {
  width: 14px; height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
