<template>
  <div class="cost-table-wrap">

    <div v-if="costs.length === 0" class="cost-table__empty">
      <div class="cost-table__empty-icon">📋</div>
      <p class="cost-table__empty-title">Nenhum custo cadastrado</p>
      <p class="cost-table__empty-sub">Preencha o formulário ao lado para adicionar um registro de custos.</p>
    </div>

    <div v-else class="cost-table__scroll">
      <table class="cost-table">
        <thead>
          <tr>
            <th>Cultura</th>
            <th>Sementes</th>
            <th>Fertiliz.</th>
            <th>Defensivos</th>
            <th>Mão de Obra</th>
            <th>Combust.</th>
            <th>Manuten.</th>
            <th>Total / ha</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="entry in costs"
            :key="entry.id"
            :class="['cost-table__row', { 'cost-table__row--selected': selectedId === entry.id }]"
            @click="store.select(entry.id)"
          >
            <td>
              <span :class="['crop-tag', `crop-tag--${entry.crop_type}`]">
                {{ cropIcon(entry.crop_type) }} {{ cropLabel(entry.crop_type) }}
              </span>
            </td>
            <td>{{ formatBRL(entry.seeds) }}</td>
            <td>{{ formatBRL(entry.fertilizers) }}</td>
            <td>{{ formatBRL(entry.defensivos) }}</td>
            <td>{{ formatBRL(entry.labor) }}</td>
            <td>{{ formatBRL(entry.fuel) }}</td>
            <td>{{ formatBRL(entry.maintenance) }}</td>
            <td class="cost-table__total">{{ formatBRL(entry.total_cost) }}</td>
            <td>
              <button class="cost-table__del-btn" type="button" @click.stop="handleDelete(entry.id)" title="Excluir">
                <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="selectedId && costs.length > 0" class="cost-table__selection-bar">
      <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
      Custo selecionado para simulação: <strong>{{ selectedLabel }}</strong>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import { useNotification } from '@/composables/useNotification.js'

const store = useCostStore()
const { formatBRL } = useCurrency()
const { showSuccess } = useNotification()

const costs     = computed(() => store.costs)
const selectedId = computed(() => store.selectedId)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const CROP_ICONS  = { soja: '🌱', milho: '🌽', feijao: '🫘' }
const cropLabel = (t) => CROP_LABELS[t] ?? t
const cropIcon  = (t) => CROP_ICONS[t]  ?? '🌾'

const selectedLabel = computed(() => {
  const e = costs.value.find(c => c.id === selectedId.value)
  return e ? `${cropLabel(e.crop_type)} – ${formatBRL(e.total_cost)}/ha` : ''
})

async function handleDelete(id) {
  await store.remove(id)
  showSuccess('Registro removido.')
}
</script>

<style scoped>
.cost-table-wrap {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: #fff;
}

.cost-table__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 1.5rem;
  text-align: center;
  gap: 0.5rem;
}
.cost-table__empty-icon { font-size: 2rem; }
.cost-table__empty-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--gray-700);
  margin: 0;
}
.cost-table__empty-sub {
  font-size: 0.85rem;
  color: var(--gray-500);
  max-width: 280px;
}

.cost-table__scroll { overflow-x: auto; }

.cost-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.cost-table th {
  padding: 0.65rem 0.85rem;
  text-align: left;
  background: var(--gray-50);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--gray-500);
  border-bottom: 1px solid var(--gray-200);
  white-space: nowrap;
}

.cost-table td {
  padding: 0.7rem 0.85rem;
  border-bottom: 1px solid var(--gray-100);
  color: var(--gray-700);
  white-space: nowrap;
}

.cost-table__row {
  cursor: pointer;
  transition: background 0.1s;
}
.cost-table__row:hover { background: var(--green-50); }
.cost-table__row--selected { background: #f0fdf4 !important; }
.cost-table__row--selected td { color: var(--gray-900); }

.cost-table__total {
  font-weight: 700;
  color: var(--gray-900) !important;
}

.crop-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.crop-tag--soja   { background: #fef9c3; color: #92400e; }
.crop-tag--milho  { background: #fef3c7; color: #b45309; }
.crop-tag--feijao { background: #fce7f3; color: #9d174d; }

.cost-table__del-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--gray-400);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.cost-table__del-btn:hover {
  background: var(--red-100);
  color: var(--red-500);
}
.cost-table__del-btn svg { width: 15px; height: 15px; }

.cost-table__selection-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1rem;
  background: var(--green-50);
  border-top: 1px solid var(--green-200);
  font-size: 0.82rem;
  color: var(--green-700);
}
.cost-table__selection-bar svg { width: 16px; height: 16px; flex-shrink: 0; color: var(--green-500); }
</style>
