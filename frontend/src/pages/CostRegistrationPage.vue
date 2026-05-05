<template>
  <div class="cost-page">
    <div class="cost-page__inner">

      <div class="cost-page__heading">
        <div>
          <h1 class="cost-page__title">Cadastro de Custos</h1>
          <p class="cost-page__subtitle">Registre os custos por hectare de cada cultura para usar nas simulações.</p>
        </div>
        <div class="cost-page__step-hint">
          <span class="step-badge step-badge--active">1. Custos</span>
          <span class="step-badge">2. Simular</span>
          <span class="step-badge">3. Comparar</span>
        </div>
      </div>

      <div class="cost-page__info-banner">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>
        <p>Preencha os custos de produção para sua lavoura. Você pode cadastrar diferentes conjuntos de custos para cada cultura e selecionar qual usar na simulação.</p>
      </div>

      <div class="cost-page__layout">
        <section class="cost-page__form-col">
          <div class="cost-page__card">
            <h2 class="cost-page__card-title">
              <svg viewBox="0 0 20 20" fill="currentColor"><path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/></svg>
              Novo registro de custos
            </h2>
            <CostForm @saved="handleSaved" />
          </div>
        </section>

        <section class="cost-page__table-col">
          <div class="cost-page__card">
            <div class="cost-page__card-header">
              <h2 class="cost-page__card-title">
                <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd"/></svg>
                Custos cadastrados
              </h2>
              <span v-if="store.costs.length > 0" class="cost-page__count">{{ store.costs.length }} registro{{ store.costs.length > 1 ? 's' : '' }}</span>
            </div>

            <CostTable />

            <div v-if="selectedEntry" class="cost-page__selected-action">
              <div class="cost-page__selected-info">
                <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                <span>Selecionado: <strong>{{ cropLabel(selectedEntry.crop_type) }} – {{ formatBRL(selectedEntry.total_cost) }}/ha</strong></span>
              </div>
              <RouterLink to="/" class="cost-page__goto-sim">
                Ir para simulação →
              </RouterLink>
            </div>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import CostForm from '@/components/cost/CostForm.vue'
import CostTable from '@/components/cost/CostTable.vue'

const store = useCostStore()
const { formatBRL } = useCurrency()

const selectedEntry = computed(() =>
  store.costs.find(c => c.id === store.selectedId) ?? null
)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (t) => CROP_LABELS[t] ?? t

onMounted(() => store.fetchAll())

function handleSaved(entry) {
  store.select(entry.id)
}
</script>

<style scoped>
.cost-page {
  min-height: calc(100vh - 62px);
  background: var(--gray-50);
}

.cost-page__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cost-page__heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.cost-page__title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--gray-900);
}
.cost-page__subtitle {
  font-size: 0.875rem;
  color: var(--gray-500);
  margin-top: 0.25rem;
}

.cost-page__step-hint {
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
.step-badge--active { background: var(--green-600); color: #fff; }

.cost-page__info-banner {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  background: var(--amber-100);
  border: 1px solid #fde68a;
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  color: #92400e;
}
.cost-page__info-banner svg { width: 18px; height: 18px; flex-shrink: 0; color: var(--amber-600); margin-top: 1px; }
.cost-page__info-banner p { margin: 0; line-height: 1.5; }

.cost-page__layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 860px) {
  .cost-page__layout { grid-template-columns: 1fr; }
}

.cost-page__card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.cost-page__card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cost-page__card-title {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--gray-800);
}
.cost-page__card-title svg { width: 16px; height: 16px; color: var(--green-600); }

.cost-page__count {
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--green-100);
  color: var(--green-700);
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
}

.cost-page__selected-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: var(--green-50);
  border: 1px solid var(--green-200);
  border-radius: var(--radius-md);
  padding: 0.7rem 1rem;
  flex-wrap: wrap;
}

.cost-page__selected-info {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: var(--green-800);
}
.cost-page__selected-info svg { width: 16px; height: 16px; color: var(--green-500); flex-shrink: 0; }

.cost-page__goto-sim {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--green-600);
  text-decoration: none;
  white-space: nowrap;
}
.cost-page__goto-sim:hover { color: var(--green-800); }
</style>
