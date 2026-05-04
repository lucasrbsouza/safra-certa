<template>
  <div class="dashboard">
    <CommodityTicker />

    <main class="dashboard__main">
      <section class="dashboard__controls">
        <div class="dashboard__control-row">
          <div>
            <label class="dashboard__field-label">Cultura</label>
            <CropSelector v-model="store.selectedCrop" @update:modelValue="resetAndSimulate" />
          </div>
          <div>
            <BaseInput
              label="Produtividade estimada"
              v-model="store.estimatedProductivity"
              suffix="sc/ha"
              :min="1"
              :max="500"
            />
          </div>
          <div>
            <label class="dashboard__field-label">Usar custo salvo</label>
            <select class="dashboard__select" v-model="selectedCostId" @change="resetAndSimulate">
              <option value="">Nenhum (sem custo)</option>
              <option v-for="c in costStore.costs" :key="c.id" :value="c.id">
                {{ cropLabel(c.crop_type) }} – {{ formatBRL(c.total_cost) }}
              </option>
            </select>
          </div>
          <BaseButton @click="handleSimulate" :loading="store.loading">
            Simular
          </BaseButton>
        </div>
      </section>

      <section v-if="store.result" class="dashboard__results">
        <BreakevenGauge
          :breakeven="store.result.breakeven_sacks_per_hectare"
          :productivity="store.result.estimated_productivity"
        />

        <div class="dashboard__cards">
          <ResultCard
            title="Custo Total"
            :value="formattedTotalCost"
            unit="por hectare"
            color-variant="neutral"
          />
          <ResultCard
            title="Preço de Mercado"
            :value="formattedMarketPrice"
            unit="por saca 60kg"
            color-variant="neutral"
          />
          <ResultCard
            title="Ponto de Equilíbrio"
            :value="formattedBreakeven"
            :highlight="true"
            color-variant="neutral"
          />
          <ResultCard
            title="Margem Estimada"
            :value="formattedProfitLoss"
            unit="por hectare"
            :color-variant="store.statusColor"
          />
        </div>
      </section>

      <section v-else class="dashboard__empty">
        <p>Selecione uma cultura e clique em <strong>Simular</strong> para ver o ponto de equilíbrio.</p>
        <RouterLink to="/custos" class="dashboard__link">Cadastrar custos operacionais →</RouterLink>
      </section>

      <p v-if="store.error" class="dashboard__error">{{ store.error }}</p>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSimulationStore } from '@/stores/simulationStore.js'
import { useCostStore } from '@/stores/costStore.js'
import { useBreakeven } from '@/composables/useBreakeven.js'
import { useCurrency } from '@/composables/useCurrency.js'
import CommodityTicker from '@/components/commodity/CommodityTicker.vue'
import CropSelector from '@/components/simulation/CropSelector.vue'
import BreakevenGauge from '@/components/simulation/BreakevenGauge.vue'
import ResultCard from '@/components/simulation/ResultCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const store = useSimulationStore()
const costStore = useCostStore()
const { formattedBreakeven, formattedProfitLoss, formattedTotalCost, formattedMarketPrice } = useBreakeven()
const { formatBRL } = useCurrency()

const selectedCostId = ref('')
const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (type) => CROP_LABELS[type] ?? type

onMounted(() => costStore.fetchAll())

async function handleSimulate() {
  const payload = {
    crop_type: store.selectedCrop,
    estimated_productivity: Number(store.estimatedProductivity),
  }
  if (selectedCostId.value) payload.cost_entry_id = selectedCostId.value
  await store.runSimulation(payload)
}

function resetAndSimulate() {
  store.reset()
}
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; min-height: 100vh; }
.dashboard__main { padding: 1.5rem; display: flex; flex-direction: column; gap: 2rem; max-width: 960px; margin: 0 auto; width: 100%; }
.dashboard__controls { background: #fff; padding: 1.2rem 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.dashboard__control-row { display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-end; }
.dashboard__field-label { display: block; font-size: 0.85rem; font-weight: 600; color: #333; margin-bottom: 4px; }
.dashboard__select { padding: 0.5rem 0.75rem; border: 1.5px solid #ccc; border-radius: 6px; font-size: 0.95rem; cursor: pointer; }
.dashboard__results { display: flex; flex-direction: column; gap: 1.5rem; }
.dashboard__cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
.dashboard__empty { background: #f9fbe7; border-radius: 10px; padding: 2rem; text-align: center; color: #555; }
.dashboard__link { display: inline-block; margin-top: 1rem; color: #2e7d32; font-weight: 600; text-decoration: none; }
.dashboard__error { color: #c62828; font-size: 0.88rem; text-align: center; }
</style>
