<template>
  <div class="cost-page">
    <div class="cost-page__header">
      <h1 class="cost-page__title">Cadastro de Custos Operacionais</h1>
      <p class="cost-page__subtitle">Registre os custos por hectare para calcular o ponto de equilíbrio.</p>
    </div>

    <div class="cost-page__body">
      <section class="cost-page__form-panel">
        <CostForm @saved="handleSaved" />
      </section>

      <section class="cost-page__table-panel">
        <h2 class="cost-page__section-title">Custos Cadastrados</h2>
        <CostTable @select="handleSelect" />
        <p v-if="selectedEntry" class="cost-page__selected">
          ✓ Custo selecionado para simulação: {{ cropLabel(selectedEntry.crop_type) }} – {{ formatBRL(selectedEntry.total_cost) }}
          <RouterLink to="/" class="cost-page__simulate-link">Ir para Dashboard →</RouterLink>
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import CostForm from '@/components/cost/CostForm.vue'
import CostTable from '@/components/cost/CostTable.vue'

const store = useCostStore()
const { formatBRL } = useCurrency()
const selectedEntry = ref(null)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (type) => CROP_LABELS[type] ?? type

onMounted(() => store.fetchAll())

function handleSaved(entry) {
  store.select(entry.id)
  selectedEntry.value = entry
}

function handleSelect(entry) {
  store.select(entry.id)
  selectedEntry.value = entry
}
</script>

<style scoped>
.cost-page { padding: 1.5rem; max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem; }
.cost-page__header { }
.cost-page__title { font-size: 1.4rem; font-weight: 700; color: #1a1a1a; margin: 0; }
.cost-page__subtitle { color: #666; margin: 0.3rem 0 0; font-size: 0.95rem; }
.cost-page__body { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; }
@media (max-width: 768px) { .cost-page__body { grid-template-columns: 1fr; } }
.cost-page__form-panel { background: #fff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); align-self: start; }
.cost-page__table-panel { display: flex; flex-direction: column; gap: 1rem; }
.cost-page__section-title { font-size: 1rem; font-weight: 700; color: #333; margin: 0; }
.cost-page__selected { background: #e8f5e9; padding: 0.7rem 1rem; border-radius: 6px; font-size: 0.9rem; color: #2e7d32; display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
.cost-page__simulate-link { color: #2e7d32; font-weight: 700; text-decoration: none; }
</style>
