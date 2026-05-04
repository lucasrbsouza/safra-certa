<template>
  <div class="ticker">
    <div class="ticker__label">Cotações de Hoje</div>
    <div class="ticker__items">
      <div
        v-for="item in priceList"
        :key="item.crop_type"
        class="ticker__item"
      >
        <span class="ticker__crop">{{ cropLabel(item.crop_type) }}</span>
        <span class="ticker__price">{{ formatBRL(item.price_per_sack) }}</span>
        <span class="ticker__unit">/sc 60kg</span>
      </div>
      <div v-if="loading && priceList.length === 0" class="ticker__loading">
        Carregando cotações...
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useCommodityStore } from '@/stores/commodityStore.js'
import { useCurrency } from '@/composables/useCurrency.js'

const store = useCommodityStore()
const { formatBRL } = useCurrency()

const priceList = computed(() => store.priceList)
const loading = computed(() => store.loading)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (type) => CROP_LABELS[type] ?? type

let interval = null

onMounted(() => {
  store.fetchAll()
  interval = setInterval(() => store.fetchAll(), 5 * 60 * 1000)
})

onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.ticker {
  background: #1b5e20;
  color: #fff;
  padding: 0.5rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.ticker__label { font-size: 0.75rem; font-weight: 700; opacity: 0.8; white-space: nowrap; }
.ticker__items { display: flex; gap: 2rem; flex-wrap: wrap; }
.ticker__item { display: flex; align-items: center; gap: 0.3rem; }
.ticker__crop { font-weight: 700; font-size: 0.9rem; }
.ticker__price { font-size: 0.9rem; color: #a5d6a7; }
.ticker__unit { font-size: 0.75rem; opacity: 0.7; }
.ticker__loading { font-size: 0.85rem; opacity: 0.7; }
</style>
