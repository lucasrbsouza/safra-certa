<template>
  <form class="cost-form" @submit.prevent="handleSubmit">

    <div class="cost-form__section">
      <p class="cost-form__section-label">Cultura</p>
      <div class="cost-form__crop-row">
        <button
          v-for="opt in cropOptions" :key="opt.value"
          type="button"
          :class="['crop-pill', { 'crop-pill--active': form.crop_type === opt.value }]"
          @click="form.crop_type = opt.value"
        >
          <CropIcon :type="opt.value" class="crop-pill__icon" />
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="cost-form__section">
      <p class="cost-form__section-label">
        <svg viewBox="0 0 20 20" fill="currentColor"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z"/></svg>
        Insumos
      </p>
      <div class="cost-form__grid">
        <BaseInput label="Sementes"      v-model="form.seeds"        suffix="R$/ha" :min="0" />
        <BaseInput label="Fertilizantes" v-model="form.fertilizers"  suffix="R$/ha" :min="0" />
        <BaseInput label="Defensivos"    v-model="form.defensivos"   suffix="R$/ha" :min="0" />
      </div>
    </div>

    <div class="cost-form__section">
      <p class="cost-form__section-label">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
        Operacionais
      </p>
      <div class="cost-form__grid">
        <BaseInput label="Mão de Obra" v-model="form.labor"       suffix="R$/ha" :min="0" />
        <BaseInput label="Combustível" v-model="form.fuel"        suffix="R$/ha" :min="0" />
        <BaseInput label="Manutenção"  v-model="form.maintenance" suffix="R$/ha" :min="0" />
      </div>
    </div>

    <div v-if="totalPreview > 0" class="cost-form__preview">
      <span class="cost-form__preview-label">Total estimado</span>
      <span class="cost-form__preview-value">{{ formatBRL(totalPreview) }} / ha</span>
    </div>

    <p v-if="error" class="cost-form__error">{{ error }}</p>

    <BaseButton type="submit" :loading="loading" :full="true" variant="primary">
      <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
      {{ loading ? 'Salvando...' : 'Salvar custos' }}
    </BaseButton>

  </form>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useCostStore } from '@/stores/costStore.js'
import { useNotification } from '@/composables/useNotification.js'
import { useCurrency } from '@/composables/useCurrency.js'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import CropIcon from '@/components/ui/CropIcon.vue'

const emit = defineEmits(['saved'])

const store = useCostStore()
const { showSuccess, showError } = useNotification()
const { formatBRL } = useCurrency()

const loading = computed(() => store.loading)
const error   = computed(() => store.error)

const form = reactive({
  crop_type:   'soja',
  seeds:        0,
  fertilizers:  0,
  defensivos:   0,
  labor:        0,
  fuel:         0,
  maintenance:  0,
})

const totalPreview = computed(() =>
  (Number(form.seeds) || 0) +
  (Number(form.fertilizers) || 0) +
  (Number(form.defensivos) || 0) +
  (Number(form.labor) || 0) +
  (Number(form.fuel) || 0) +
  (Number(form.maintenance) || 0)
)

const cropOptions = [
  { value: 'soja',   label: 'Soja'   },
  { value: 'milho',  label: 'Milho'  },
  { value: 'feijao', label: 'Feijão' },
]

async function handleSubmit() {
  try {
    const created = await store.create({ ...form })
    showSuccess('Custos salvos com sucesso!')
    emit('saved', created)
  } catch {
    showError('Erro ao salvar custos.')
  }
}
</script>

<style scoped>
.cost-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cost-form__section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cost-form__section-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--green-700);
  margin: 0;
}
.cost-form__section-label svg { width: 14px; height: 14px; }

.cost-form__crop-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.crop-pill__icon { font-size: 1rem; }

.crop-pill {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 999px;
  background: #fff;
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--gray-600);
  cursor: pointer;
  transition: all 0.15s;
}
.crop-pill:hover:not(.crop-pill--active) {
  border-color: var(--green-300);
  color: var(--green-700);
  background: var(--green-50);
}
.crop-pill--active {
  border-color: var(--green-500);
  background: var(--green-600);
  color: #fff;
}

.cost-form__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.cost-form__preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--green-50);
  border: 1px solid var(--green-200);
  border-radius: var(--radius-md);
  padding: 0.65rem 1rem;
}

.cost-form__preview-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--green-700);
}

.cost-form__preview-value {
  font-size: 1rem;
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--green-800);
}

.cost-form__error {
  font-size: 0.82rem;
  color: var(--red-500);
  background: var(--red-100);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
}
</style>
