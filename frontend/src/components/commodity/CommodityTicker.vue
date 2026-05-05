<template>
  <div class="ticker">
    <div class="ticker__left">
      <span class="ticker__dot"></span>
      <span class="ticker__label">Cotações ao vivo</span>
    </div>
    <div class="ticker__items">
      <div v-if="loading && priceList.length === 0" class="ticker__loading">
        <span class="ticker__pulse"></span> Carregando...
      </div>
      <div v-for="item in priceList" :key="item.crop_type" class="ticker__item">
        <span class="ticker__crop-icon">{{ cropIcon(item.crop_type) }}</span>
        <span class="ticker__crop">{{ cropLabel(item.crop_type) }}</span>
        <span class="ticker__price">{{ formatBRL(item.price_per_sack) }}</span>
        <span class="ticker__unit">/ sc</span>
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
const CROP_ICONS  = { soja: '🌱', milho: '🌽', feijao: '🫘' }
const cropLabel = (type) => CROP_LABELS[type] ?? type
const cropIcon  = (type) => CROP_ICONS[type]  ?? '🌾'

let interval = null
onMounted(() => { store.fetchAll(); interval = setInterval(() => store.fetchAll(), 5 * 60 * 1000) })
onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.ticker {
  background: var(--green-950);
  border-bottom: 1px solid var(--green-800);
  padding: 0.45rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  overflow-x: auto;
  scrollbar-width: none;
}
.ticker::-webkit-scrollbar { display: none; }

.ticker__left {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}

.ticker__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green-400);
  animation: pulse-dot 2s ease infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.ticker__label {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--green-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.ticker__items {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.ticker__item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  white-space: nowrap;
}

.ticker__crop-icon { font-size: 0.85rem; }

.ticker__crop {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gray-300);
}

.ticker__price {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--green-300);
}

.ticker__unit {
  font-size: 0.7rem;
  color: var(--gray-500);
}

.ticker__loading {
  font-size: 0.78rem;
  color: var(--gray-500);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.ticker__pulse {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--gray-500);
  animation: pulse-dot 1s ease infinite;
}
</style>
