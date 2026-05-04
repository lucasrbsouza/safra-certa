<template>
  <form class="cost-form" @submit.prevent="handleSubmit">
    <div class="cost-form__section">
      <h3 class="cost-form__section-title">Dados Gerais</h3>
      <div class="cost-form__row">
        <BaseSelect
          label="Tipo de Cultura"
          v-model="form.crop_type"
          :options="cropOptions"
        />
      </div>
    </div>

    <div class="cost-form__section">
      <h3 class="cost-form__section-title">Insumos (R$/ha)</h3>
      <div class="cost-form__grid">
        <BaseInput label="Sementes" v-model="form.seeds" suffix="R$/ha" />
        <BaseInput label="Fertilizantes" v-model="form.fertilizers" suffix="R$/ha" />
        <BaseInput label="Defensivos" v-model="form.defensivos" suffix="R$/ha" />
      </div>
    </div>

    <div class="cost-form__section">
      <h3 class="cost-form__section-title">Custos Operacionais (R$/ha)</h3>
      <div class="cost-form__grid">
        <BaseInput label="Mão de Obra" v-model="form.labor" suffix="R$/ha" />
        <BaseInput label="Combustível" v-model="form.fuel" suffix="R$/ha" />
        <BaseInput label="Manutenção" v-model="form.maintenance" suffix="R$/ha" />
      </div>
    </div>

    <p v-if="error" class="cost-form__error">{{ error }}</p>

    <BaseButton type="submit" :loading="loading" class="cost-form__submit">
      SALVAR E CALCULAR VIABILIDADE
    </BaseButton>
  </form>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useCostStore } from '@/stores/costStore.js'
import { useNotification } from '@/composables/useNotification.js'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const emit = defineEmits(['saved'])

const store = useCostStore()
const { showSuccess, showError } = useNotification()

const loading = computed(() => store.loading)
const error = computed(() => store.error)

const form = reactive({
  crop_type: 'soja',
  seeds: 0,
  fertilizers: 0,
  defensivos: 0,
  labor: 0,
  fuel: 0,
  maintenance: 0,
})

const cropOptions = [
  { value: 'soja', label: 'Soja' },
  { value: 'milho', label: 'Milho' },
  { value: 'feijao', label: 'Feijão' },
]

async function handleSubmit() {
  try {
    const created = await store.create({ ...form })
    showSuccess('Custos salvos com sucesso!')
    emit('saved', created)
  } catch {
    showError('Erro ao salvar custos. Verifique os campos.')
  }
}
</script>

<style scoped>
.cost-form { display: flex; flex-direction: column; gap: 1.5rem; }
.cost-form__section { display: flex; flex-direction: column; gap: 1rem; }
.cost-form__section-title { font-size: 0.9rem; font-weight: 700; color: #2e7d32; text-transform: uppercase; margin: 0; }
.cost-form__row { display: grid; grid-template-columns: 1fr; gap: 1rem; }
.cost-form__grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }
.cost-form__error { color: #c62828; font-size: 0.88rem; }
.cost-form__submit { width: 100%; justify-content: center; padding: 0.8rem; }
</style>
