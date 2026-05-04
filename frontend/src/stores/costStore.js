import { ref } from 'vue'
import { defineStore } from 'pinia'
import { costService } from '@/services/costService.js'

export const useCostStore = defineStore('cost', () => {
  const costs = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedId = ref(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      costs.value = await costService.getAll()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    loading.value = true
    error.value = null
    try {
      const created = await costService.create(data)
      costs.value.unshift(created)
      return created
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function update(id, data) {
    const updated = await costService.update(id, data)
    const idx = costs.value.findIndex((c) => c.id === id)
    if (idx !== -1) costs.value[idx] = updated
    return updated
  }

  async function remove(id) {
    await costService.remove(id)
    costs.value = costs.value.filter((c) => c.id !== id)
    if (selectedId.value === id) selectedId.value = null
  }

  function select(id) {
    selectedId.value = id
  }

  return { costs, loading, error, selectedId, fetchAll, create, update, remove, select }
})
