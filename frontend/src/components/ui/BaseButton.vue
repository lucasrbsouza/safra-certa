<template>
  <button
    :class="['btn', `btn--${variant}`, { 'btn--loading': loading, 'btn--full': full }]"
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
  full: { type: Boolean, default: false },
})
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s, box-shadow 0.15s;
  white-space: nowrap;
  letter-spacing: 0.01em;
}

.btn:active:not(:disabled) { transform: scale(0.98); }
.btn:disabled { opacity: 0.55; cursor: not-allowed; }
.btn--full { width: 100%; }

.btn--primary {
  background: var(--green-600);
  color: #fff;
  box-shadow: 0 1px 3px rgba(45,122,62,0.3);
}
.btn--primary:hover:not(:disabled) {
  background: var(--green-700);
  box-shadow: 0 3px 8px rgba(45,122,62,0.35);
}

.btn--secondary {
  background: var(--green-50);
  color: var(--green-700);
  border: 1.5px solid var(--green-300);
}
.btn--secondary:hover:not(:disabled) {
  background: var(--green-100);
  border-color: var(--green-500);
}

.btn--danger {
  background: var(--red-100);
  color: var(--red-600);
  border: 1.5px solid #fca5a5;
}
.btn--danger:hover:not(:disabled) {
  background: var(--red-500);
  color: #fff;
  border-color: var(--red-500);
}

.btn--ghost {
  background: transparent;
  color: var(--gray-600);
}
.btn--ghost:hover:not(:disabled) {
  background: var(--gray-100);
  color: var(--gray-900);
}

.btn :deep(svg) {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.btn__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
