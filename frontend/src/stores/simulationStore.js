import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { simulationService } from '@/services/simulationService.js'

export const useSimulationStore = defineStore('simulation', () => {
  const result = ref(null)
  const selectedCrop = ref('soja')
  const estimatedProductivity = ref(60)
  const loading = ref(false)
  const error = ref(null)

  const isViable = computed(() => result.value?.is_viable ?? null)
  const statusColor = computed(() => {
    if (result.value === null) return 'neutral'
    return result.value.is_viable ? 'positive' : 'negative'
  })
  const statusLabel = computed(() => {
    if (result.value === null) return '–'
    return result.value.is_viable ? 'Viável' : 'Inviável'
  })

  async function runSimulation(payload) {
    loading.value = true
    error.value = null
    try {
      result.value = await simulationService.simulate(payload)
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  function reset() {
    result.value = null
    error.value = null
  }

  return {
    result,
    selectedCrop,
    estimatedProductivity,
    loading,
    error,
    isViable,
    statusColor,
    statusLabel,
    runSimulation,
    reset,
  }
})
