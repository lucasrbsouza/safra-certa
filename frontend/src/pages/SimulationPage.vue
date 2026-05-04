<template>
  <div class="sim-page">
    <div class="sim-page__header">
      <h1 class="sim-page__title">Simulação de Viabilidade</h1>
      <p class="sim-page__subtitle">Compare as culturas e veja qual oferece melhor margem.</p>
    </div>

    <div class="sim-page__controls">
      <BaseInput
        label="Produtividade estimada (sc/ha)"
        v-model="productivity"
        :min="1"
        :max="500"
        suffix="sc/ha"
      />
      <div>
        <label class="sim-page__label">Usar custo salvo</label>
        <select class="sim-page__select" v-model="selectedCostId">
          <option value="">Sem custo registrado</option>
          <option v-for="c in costStore.costs" :key="c.id" :value="c.id">
            {{ cropLabel(c.crop_type) }} – {{ formatBRL(c.total_cost) }}
          </option>
        </select>
      </div>
      <BaseButton @click="simulateAll" :loading="loading">
        Comparar Todas as Culturas
      </BaseButton>
    </div>

    <div v-if="results.length > 0" class="sim-page__results">
      <div v-for="result in results" :key="result.crop_type" class="sim-page__result-block">
        <h3 class="sim-page__crop-title">{{ cropLabel(result.crop_type) }}</h3>
        <BreakevenGauge
          :breakeven="result.breakeven_sacks_per_hectare"
          :productivity="result.estimated_productivity"
        />
        <div class="sim-page__cards">
          <ResultCard title="Custo Total" :value="formatBRL(result.total_cost_per_hectare)" color-variant="neutral" />
          <ResultCard title="Preço Mercado" :value="formatBRL(result.market_price_per_sack)" unit="por saca" color-variant="neutral" />
          <ResultCard
            title="Margem"
            :value="formatBRL(result.profit_loss_per_hectare)"
            :color-variant="result.is_viable ? 'positive' : 'negative'"
          />
        </div>
      </div>
    </div>

    <p v-if="error" class="sim-page__error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { simulationService } from '@/services/simulationService.js'
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import BreakevenGauge from '@/components/simulation/BreakevenGauge.vue'
import ResultCard from '@/components/simulation/ResultCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const costStore = useCostStore()
const { formatBRL } = useCurrency()

const productivity = ref(60)
const selectedCostId = ref('')
const results = ref([])
const loading = ref(false)
const error = ref(null)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (type) => CROP_LABELS[type] ?? type

onMounted(() => costStore.fetchAll())

async function simulateAll() {
  loading.value = true
  error.value = null
  results.value = []
  try {
    const crops = ['soja', 'milho', 'feijao']
    const payload = (crop) => ({
      crop_type: crop,
      estimated_productivity: Number(productivity.value),
      ...(selectedCostId.value ? { cost_entry_id: selectedCostId.value } : {}),
    })
    results.value = await Promise.all(crops.map((crop) => simulationService.simulate(payload(crop))))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.sim-page { padding: 1.5rem; max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem; }
.sim-page__header { }
.sim-page__title { font-size: 1.4rem; font-weight: 700; margin: 0; }
.sim-page__subtitle { color: #666; margin: 0.3rem 0 0; }
.sim-page__controls { background: #fff; padding: 1.2rem 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: flex-end; }
.sim-page__label { display: block; font-size: 0.85rem; font-weight: 600; color: #333; margin-bottom: 4px; }
.sim-page__select { padding: 0.5rem 0.75rem; border: 1.5px solid #ccc; border-radius: 6px; font-size: 0.95rem; }
.sim-page__results { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.sim-page__result-block { background: #fff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; flex-direction: column; gap: 1rem; }
.sim-page__crop-title { font-size: 1.1rem; font-weight: 700; color: #2e7d32; margin: 0; }
.sim-page__cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }
.sim-page__error { color: #c62828; text-align: center; }
</style>
