<template>
  <div class="app">
    <AppHeader />
    <main class="app__content">
      <RouterView />
    </main>
    <teleport to="body">
      <div class="toast-stack">
        <transition-group name="toast">
          <div
            v-for="n in notifications"
            :key="n.id"
            :class="['toast', `toast--${n.type}`]"
          >
            <span class="toast__icon">
              <svg v-if="n.type === 'success'" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              <svg v-else-if="n.type === 'error'" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
              <svg v-else viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>
            </span>
            <span class="toast__message">{{ n.message }}</span>
          </div>
        </transition-group>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import { useNotification } from '@/composables/useNotification.js'
const { notifications } = useNotification()
</script>

<style scoped>
.app { min-height: 100vh; display: flex; flex-direction: column; background: var(--gray-50); }
.app__content { flex: 1; }

.toast-stack {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 9999;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1.1rem;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  pointer-events: auto;
  max-width: 340px;
}

.toast--success { background: var(--green-800); color: #fff; }
.toast--error   { background: var(--red-600);   color: #fff; }
.toast--info    { background: var(--gray-800);   color: #fff; }

.toast__icon { width: 18px; height: 18px; flex-shrink: 0; }
.toast__icon svg { width: 100%; height: 100%; display: block; }

.toast-enter-active { animation: toast-in 0.3s ease; }
.toast-leave-active { animation: toast-in 0.2s ease reverse; }

@keyframes toast-in {
  from { opacity: 0; transform: translateX(16px) scale(0.96); }
  to   { opacity: 1; transform: translateX(0)   scale(1); }
}
</style>
