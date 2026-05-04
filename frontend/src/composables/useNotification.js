import { ref } from 'vue'

const notifications = ref([])
let nextId = 0

export function useNotification() {
  function show(message, type = 'info', duration = 3500) {
    const id = ++nextId
    notifications.value.push({ id, message, type })
    setTimeout(() => {
      notifications.value = notifications.value.filter((n) => n.id !== id)
    }, duration)
  }

  const showSuccess = (message) => show(message, 'success')
  const showError = (message) => show(message, 'error')
  const showInfo = (message) => show(message, 'info')

  return { notifications, showSuccess, showError, showInfo }
}
