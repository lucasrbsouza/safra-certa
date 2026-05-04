<template>
  <div class="app">
    <AppHeader />
    <RouterView />
    <div class="notifications">
      <div
        v-for="n in notifications"
        :key="n.id"
        :class="['notification', `notification--${n.type}`]"
      >
        {{ n.message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import { useNotification } from '@/composables/useNotification.js'

const { notifications } = useNotification()
</script>

<style scoped>
.app { min-height: 100vh; background: #f5f5f5; }
.notifications { position: fixed; bottom: 1.5rem; right: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; z-index: 999; }
.notification {
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  animation: slide-in 0.3s ease;
}
.notification--success { background: #2e7d32; color: #fff; }
.notification--error { background: #c62828; color: #fff; }
.notification--info { background: #1565c0; color: #fff; }
@keyframes slide-in { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
</style>
