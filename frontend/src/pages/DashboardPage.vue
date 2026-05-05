<template>
  <div class="dash">
    <CommodityTicker />

    <div class="dash__page">

      <!-- Page heading -->
      <div class="dash__heading">
        <div>
          <h1 class="dash__title">Simulação de Viabilidade</h1>
          <p class="dash__subtitle">Calcule o ponto de equilíbrio para uma cultura específica e descubra se sua safra é rentável.</p>
        </div>
        <div class="dash__step-hint">
          <span class="step-badge step-badge--done">1. Custos</span>
          <span class="step-badge step-badge--active">2. Simular</span>
          <span class="step-badge">3. Comparar</span>
        </div>
      </div>

      <!-- Controls card -->
      <div class="dash__card">
        <p class="dash__card-label">Configure a simulação</p>

        <div class="dash__controls">
          <div class="dash__ctrl">
            <p class="dash__ctrl-label">Cultura</p>
            <CropSelector v-model="store.selectedCrop" @update:modelValue="store.reset()" />
          </div>

          <div class="dash__ctrl">
            <BaseInput
              label="Produtividade estimada"
              v-model="store.estimatedProductivity"
              suffix="sc/ha"
              :min="1"
              :max="500"
              placeholder="Ex: 60"
            />
          </div>

          <div class="dash__ctrl">
            <p class="dash__ctrl-label">Custo cadastrado</p>
            <div class="dash__select-wrap">
              <select class="dash__select" v-model="selectedCostId" @change="store.reset()">
                <option value="">— Sem custo registrado —</option>
                <option v-for="c in costStore.costs" :key="c.id" :value="c.id">
                  {{ cropLabel(c.crop_type) }} · {{ formatBRL(c.total_cost) }}/ha
                </option>
              </select>
              <svg class="dash__select-arrow" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </div>
            <p v-if="costStore.costs.length === 0" class="dash__hint">
              <RouterLink to="/custos">Cadastre seus custos primeiro →</RouterLink>
            </p>
          </div>

          <div class="dash__ctrl dash__ctrl--action">
            <BaseButton @click="handleSimulate" :loading="store.loading" :full="true" variant="primary" style="padding: 0.7rem 1.5rem; font-size: 0.95rem;">
              <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/></svg>
              Simular
            </BaseButton>
          </div>
        </div>

        <p v-if="store.error" class="dash__error">{{ store.error }}</p>
      </div>

      <!-- Results -->
      <transition name="results-fade">
        <div v-if="store.result" class="dash__results">
          <BreakevenGauge
            :breakevenSacks="store.result.breakeven_sacks_per_hectare"
            :estimatedProductivity="store.result.estimated_productivity"
            :isViable="store.result.is_viable"
          />
          <div class="dash__cards">
            <ResultCard
              title="Custo Total"
              :value="formattedTotalCost"
              unit="por hectare"
              variant="neutral"
            />
            <ResultCard
              title="Preço de Mercado"
              :value="formattedMarketPrice"
              unit="por saca 60 kg"
              variant="neutral"
            />
            <ResultCard
              title="Ponto de Equilíbrio"
              :value="formattedBreakeven"
              unit="sacas/ha"
              :highlight="true"
              variant="neutral"
            />
            <ResultCard
              title="Margem Estimada"
              :value="formattedProfitLoss"
              unit="por hectare"
              :variant="store.statusColor"
            />
          </div>

          <div class="dash__next">
            <p class="dash__next-label">Próximo passo</p>
            <RouterLink to="/simulacao" class="dash__next-link">
              <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>
              Comparar todas as culturas →
            </RouterLink>
          </div>
        </div>
      </transition>

      <!-- Empty state -->
      <div v-if="!store.result && !store.loading" class="dash__empty">
        <div class="dash__empty-icon">🌾</div>
        <h3 class="dash__empty-title">Pronto para simular?</h3>
        <p class="dash__empty-text">Selecione a cultura, informe a produtividade esperada e clique em <strong>Simular</strong> para calcular o ponto de equilíbrio.</p>
        <RouterLink v-if="costStore.costs.length === 0" to="/custos" class="dash__empty-link">
          Cadastrar custos operacionais →
        </RouterLink>
      </div>

    </div>
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
const cropLabel = (t) => CROP_LABELS[t] ?? t

onMounted(() => costStore.fetchAll())

async function handleSimulate() {
  const payload = {
    crop_type: store.selectedCrop,
    estimated_productivity: Number(store.estimatedProductivity),
  }
  if (selectedCostId.value) payload.cost_entry_id = selectedCostId.value
  await store.runSimulation(payload)
}
</script>

<style scoped>
.dash { display: flex; flex-direction: column; min-height: calc(100vh - 62px); }

.dash__page {
  flex: 1;
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
  padding: 1.5rem 1.25rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dash__heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.dash__title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--gray-900);
}
.dash__subtitle {
  font-size: 0.875rem;
  color: var(--gray-500);
  margin-top: 0.25rem;
}

.dash__step-hint {
  display: flex;
  gap: 0.35rem;
  align-items: center;
  flex-wrap: wrap;
}

.step-badge {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  background: var(--gray-100);
  color: var(--gray-500);
  white-space: nowrap;
}
.step-badge--done   { background: var(--green-100); color: var(--green-700); }
.step-badge--active { background: var(--green-600);  color: #fff; }

.dash__card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.dash__card-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gray-400);
  margin: 0;
}

.dash__controls {
  display: flex;
  gap: 1.25rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.dash__ctrl { display: flex; flex-direction: column; gap: 5px; min-width: 160px; flex: 1; }
.dash__ctrl--action { min-width: 120px; max-width: 160px; flex: 0; align-self: flex-end; }

.dash__ctrl-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gray-700);
  margin: 0;
  letter-spacing: 0.02em;
}

.dash__select-wrap {
  position: relative;
  border: 1.5px solid var(--gray-300);
  border-radius: var(--radius-md);
  background: #fff;
  transition: border-color 0.15s;
}
.dash__select-wrap:focus-within {
  border-color: var(--green-500);
  box-shadow: 0 0 0 3px rgba(58,153,80,0.12);
}

.dash__select {
  width: 100%;
  padding: 0.55rem 2.25rem 0.55rem 0.8rem;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  color: var(--gray-900);
  cursor: pointer;
  outline: none;
  appearance: none;
  font-family: var(--font-body);
}

.dash__select-arrow {
  pointer-events: none;
  position: absolute;
  right: 0.6rem;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--gray-400);
}

.dash__hint { margin: 0; font-size: 0.75rem; }
.dash__hint a { color: var(--green-600); font-weight: 600; }

.dash__error {
  font-size: 0.82rem;
  color: var(--red-500);
  background: var(--red-100);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
}

.dash__results {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.dash__cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

@media (min-width: 600px) {
  .dash__cards { grid-template-columns: repeat(4, 1fr); }
}

.dash__next {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
}
.dash__next-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--gray-500);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.dash__next-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--green-600);
  text-decoration: none;
  margin-left: auto;
}
.dash__next-link svg { width: 16px; height: 16px; }
.dash__next-link:hover { color: var(--green-700); }

.dash__empty {
  text-align: center;
  padding: 3rem 1.5rem;
  background: #fff;
  border-radius: var(--radius-lg);
  border: 1.5px dashed var(--gray-200);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}
.dash__empty-icon { font-size: 2.5rem; }
.dash__empty-title { font-size: 1.1rem; font-weight: 700; color: var(--gray-700); }
.dash__empty-text { font-size: 0.875rem; color: var(--gray-500); max-width: 360px; }
.dash__empty-link {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--green-600);
}
.dash__empty-link:hover { color: var(--green-700); }

.results-fade-enter-active { animation: slide-up 0.35s ease; }
@keyframes slide-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 540px) {
  .dash__ctrl--action { max-width: 100%; flex: 1; }
  .dash__step-hint { display: none; }
}
</style>
