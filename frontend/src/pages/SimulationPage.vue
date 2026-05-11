<template>
  <div class="sim-page">
    <div class="sim-page__inner">

      <div class="sim-page__heading">
        <div>
          <h1 class="sim-page__title">Comparar Culturas</h1>
          <p class="sim-page__subtitle">Simule soja, milho e feijão lado a lado com a mesma produtividade e descubra qual é mais rentável.</p>
        </div>
        <div class="sim-page__step-hint">
          <span class="step-badge step-badge--done">1. Custos</span>
          <span class="step-badge step-badge--done">2. Simular</span>
          <span class="step-badge step-badge--active">3. Comparar</span>
        </div>
      </div>

      <!-- Controls -->
      <div class="sim-page__card">
        <p class="sim-page__card-label">Parâmetros da comparação</p>
        <div class="sim-page__controls">
          <div class="sim-page__ctrl">
            <BaseInput
              label="Produtividade estimada"
              v-model="productivity"
              :min="1"
              :max="500"
              suffix="sc/ha"
              placeholder="Ex: 60"
            />
          </div>

          <div class="sim-page__ctrl">
            <p class="sim-page__ctrl-label">Custo cadastrado</p>
            <div class="sim-page__select-wrap">
              <select class="sim-page__select" v-model="selectedCostId">
                <option value="">— Sem custo registrado —</option>
                <option v-for="c in costStore.costs" :key="c.id" :value="c.id">
                  {{ cropLabel(c.crop_type) }} · {{ formatBRL(c.total_cost) }}/ha
                </option>
              </select>
              <svg class="sim-page__select-arrow" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
            </div>
          </div>

          <div class="sim-page__ctrl sim-page__ctrl--action">
            <BaseButton @click="simulateAll" :loading="loading" :full="true" variant="primary" style="padding: 0.7rem 1.5rem; font-size: 0.95rem;">
              <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>
              Comparar tudo
            </BaseButton>
          </div>
        </div>

        <p v-if="error" class="sim-page__error">{{ error }}</p>
      </div>

      <!-- Results grid -->
      <transition name="results-fade">
        <div v-if="results.length > 0" class="sim-page__results">
          <div
            v-for="result in results"
            :key="result.crop_type"
            :class="['sim-page__result-block', result.is_viable ? 'sim-page__result-block--viable' : 'sim-page__result-block--inviable']"
          >
            <div class="sim-page__crop-header">
              <CropIcon :type="result.crop_type" class="sim-page__crop-icon" />
              <h3 class="sim-page__crop-name">{{ cropLabel(result.crop_type) }}</h3>
              <span :class="['sim-page__viability-badge', result.is_viable ? 'sim-page__viability-badge--viable' : 'sim-page__viability-badge--inviable']">
                {{ result.is_viable ? 'Viável' : 'Inviável' }}
              </span>
            </div>

            <BreakevenGauge
              :breakevenSacks="result.breakeven_sacks_per_hectare"
              :estimatedProductivity="result.estimated_productivity"
              :isViable="result.is_viable"
            />

            <div class="sim-page__summary">
              <div class="sim-page__summary-row">
                <span class="sim-page__summary-label">Custo total</span>
                <span class="sim-page__summary-value">{{ formatBRL(result.total_cost_per_hectare) }}<small>/ha</small></span>
              </div>
              <div class="sim-page__summary-row">
                <span class="sim-page__summary-label">Preço de mercado</span>
                <span class="sim-page__summary-value">{{ formatBRL(result.market_price_per_sack) }}<small>/sc</small></span>
              </div>
              <div class="sim-page__summary-row sim-page__summary-row--highlight">
                <span class="sim-page__summary-label">Margem estimada</span>
                <span :class="['sim-page__summary-value', 'sim-page__summary-margin', result.is_viable ? 'sim-page__summary-margin--pos' : 'sim-page__summary-margin--neg']">
                  {{ formatBRL(result.profit_loss_per_hectare) }}<small>/ha</small>
                </span>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Empty state -->
      <div v-if="results.length === 0 && !loading" class="sim-page__empty">
        <div class="sim-page__empty-icon">
          <ChartBarSquareIcon />
        </div>
        <h3 class="sim-page__empty-title">Compare as três culturas</h3>
        <p class="sim-page__empty-text">Informe a produtividade esperada e clique em <strong>Comparar tudo</strong> para ver qual cultura oferece a melhor margem com os preços de hoje.</p>
        <RouterLink v-if="costStore.costs.length === 0" to="/custos" class="sim-page__empty-link">
          Cadastrar custos operacionais
          <ArrowRightIcon class="sim-page__arrow-icon" />
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { simulationService } from '@/services/simulationService.js'
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import BreakevenGauge from '@/components/simulation/BreakevenGauge.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { ChartBarSquareIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'
import CropIcon from '@/components/ui/CropIcon.vue'

const costStore = useCostStore()
const { formatBRL } = useCurrency()

const productivity    = ref(60)
const selectedCostId  = ref('')
const results         = ref([])
const loading         = ref(false)
const error           = ref(null)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (t) => CROP_LABELS[t] ?? t

onMounted(() => costStore.fetchAll())

async function simulateAll() {
  loading.value = true
  error.value   = null
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
    error.value = e.message ?? 'Erro ao simular. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.sim-page {
  min-height: calc(100vh - 62px);
  background: var(--gray-50);
}

.sim-page__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sim-page__heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.sim-page__title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--gray-900);
}
.sim-page__subtitle {
  font-size: 0.875rem;
  color: var(--gray-500);
  margin-top: 0.25rem;
}

.sim-page__step-hint {
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

.sim-page__card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.sim-page__card-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gray-400);
  margin: 0;
}

.sim-page__controls {
  display: flex;
  gap: 1.25rem;
  align-items: flex-end;
  flex-wrap: wrap;
}

.sim-page__ctrl { display: flex; flex-direction: column; gap: 5px; min-width: 160px; flex: 1; }
.sim-page__ctrl--action { min-width: 140px; max-width: 180px; flex: 0; align-self: flex-end; }

.sim-page__ctrl-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--gray-700);
  margin: 0;
}

.sim-page__select-wrap {
  position: relative;
  border: 1.5px solid var(--gray-300);
  border-radius: var(--radius-md);
  background: #fff;
  transition: border-color 0.15s;
}
.sim-page__select-wrap:focus-within {
  border-color: var(--green-500);
  box-shadow: 0 0 0 3px rgba(58,153,80,0.12);
}

.sim-page__select {
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

.sim-page__select-arrow {
  pointer-events: none;
  position: absolute;
  right: 0.6rem;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--gray-400);
}

.sim-page__error {
  font-size: 0.82rem;
  color: var(--red-500);
  background: var(--red-100);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
}

.sim-page__results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.25rem;
}

.sim-page__result-block {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.sim-page__result-block--viable {
  border-top: 3px solid var(--green-500);
}
.sim-page__result-block--inviable {
  border-top: 3px solid var(--red-500);
}

.sim-page__crop-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.sim-page__crop-icon { font-size: 1.4rem; }

.sim-page__crop-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--gray-900);
  flex: 1;
}

.sim-page__viability-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  letter-spacing: 0.02em;
}
.sim-page__viability-badge--viable   { background: var(--green-100); color: var(--green-700); }
.sim-page__viability-badge--inviable { background: var(--red-100);   color: var(--red-600); }

.sim-page__summary {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.sim-page__summary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 0.9rem;
  background: #fff;
  border-bottom: 1px solid var(--gray-100);
  gap: 0.5rem;
}
.sim-page__summary-row:last-child { border-bottom: none; }
.sim-page__summary-row--highlight { background: var(--gray-50); }

.sim-page__summary-label {
  font-size: 0.78rem;
  color: var(--gray-500);
  font-weight: 500;
  white-space: nowrap;
}

.sim-page__summary-value {
  font-size: 0.95rem;
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--gray-900);
  white-space: nowrap;
}
.sim-page__summary-value small {
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--gray-400);
  margin-left: 2px;
  font-family: var(--font-body);
}

.sim-page__summary-margin { }
.sim-page__summary-margin--pos { color: var(--green-700); }
.sim-page__summary-margin--neg { color: var(--red-600); }

.sim-page__empty {
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
.sim-page__empty-icon { font-size: 2.5rem; color: var(--gray-400); }
.sim-page__empty-icon svg { width: 1em; height: 1em; }
.sim-page__empty-title { font-size: 1.1rem; font-weight: 700; color: var(--gray-700); }
.sim-page__empty-text { font-size: 0.875rem; color: var(--gray-500); max-width: 380px; }
.sim-page__empty-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--green-600);
}
.sim-page__arrow-icon { width: 0.9em; height: 0.9em; flex-shrink: 0; }

.results-fade-enter-active { animation: slide-up 0.35s ease; }
@keyframes slide-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 540px) {
  .sim-page__ctrl--action { max-width: 100%; flex: 1; }
  .sim-page__step-hint { display: none; }
  .sim-page__cards { grid-template-columns: 1fr 1fr; }
}
</style>
