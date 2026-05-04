import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { commodityService } from '@/services/commodityService.js'

export const useCommodityStore = defineStore('commodity', () => {
  const prices = ref({})
  const loading = ref(false)
  const error = ref(null)

  const priceList = computed(() => Object.values(prices.value))

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const list = await commodityService.getAll()
      prices.value = Object.fromEntries(list.map((item) => [item.crop_type, item]))
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function refresh() {
    loading.value = true
    try {
      const list = await commodityService.refresh()
      prices.value = Object.fromEntries(list.map((item) => [item.crop_type, item]))
    } finally {
      loading.value = false
    }
  }

  function getPriceByCrop(cropType) {
    return prices.value[cropType] ?? null
  }

  return { prices, loading, error, priceList, fetchAll, refresh, getPriceByCrop }
})
