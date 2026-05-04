<template>
  <div class="cost-table-wrapper">
    <p v-if="costs.length === 0" class="cost-table__empty">Nenhum custo cadastrado ainda.</p>
    <div v-else class="cost-table__scroll">
      <table class="cost-table">
        <thead>
          <tr>
            <th>Cultura</th>
            <th>Sementes</th>
            <th>Fertilizantes</th>
            <th>Defensivos</th>
            <th>Mão de Obra</th>
            <th>Combustível</th>
            <th>Manutenção</th>
            <th>Total</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="entry in costs"
            :key="entry.id"
            :class="{ 'cost-table__row--selected': selectedId === entry.id }"
            @click="emit('select', entry)"
          >
            <td><span :class="['crop-badge', `crop-badge--${entry.crop_type}`]">{{ cropLabel(entry.crop_type) }}</span></td>
            <td>{{ formatBRL(entry.seeds) }}</td>
            <td>{{ formatBRL(entry.fertilizers) }}</td>
            <td>{{ formatBRL(entry.defensivos) }}</td>
            <td>{{ formatBRL(entry.labor) }}</td>
            <td>{{ formatBRL(entry.fuel) }}</td>
            <td>{{ formatBRL(entry.maintenance) }}</td>
            <td><strong>{{ formatBRL(entry.total_cost) }}</strong></td>
            <td>
              <BaseButton
                variant="danger"
                @click.stop="handleDelete(entry.id)"
                style="font-size: 0.78rem; padding: 0.3rem 0.6rem"
              >
                Excluir
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useCostStore } from '@/stores/costStore.js'
import { useCurrency } from '@/composables/useCurrency.js'
import { useNotification } from '@/composables/useNotification.js'
import BaseButton from '@/components/ui/BaseButton.vue'
import { computed } from 'vue'

const emit = defineEmits(['select'])

const store = useCostStore()
const { formatBRL } = useCurrency()
const { showSuccess } = useNotification()

const costs = computed(() => store.costs)
const selectedId = computed(() => store.selectedId)

const CROP_LABELS = { soja: 'Soja', milho: 'Milho', feijao: 'Feijão' }
const cropLabel = (type) => CROP_LABELS[type] ?? type

async function handleDelete(id) {
  await store.remove(id)
  showSuccess('Entrada de custo removida.')
}
</script>

<style scoped>
.cost-table-wrapper { overflow: hidden; border-radius: 8px; border: 1px solid #e0e0e0; }
.cost-table__scroll { overflow-x: auto; }
.cost-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.cost-table th, .cost-table td { padding: 0.7rem 0.9rem; text-align: left; border-bottom: 1px solid #f0f0f0; }
.cost-table th { background: #f5f5f5; font-weight: 700; color: #444; white-space: nowrap; }
.cost-table tr { cursor: pointer; transition: background 0.15s; }
.cost-table tr:hover { background: #f1f8e9; }
.cost-table__row--selected { background: #e8f5e9 !important; }
.cost-table__empty { padding: 1.5rem; text-align: center; color: #888; }
.crop-badge { padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
.crop-badge--soja { background: #fff9c4; color: #795548; }
.crop-badge--milho { background: #fffde7; color: #f57f17; }
.crop-badge--feijao { background: #fce4ec; color: #880e4f; }
</style>
