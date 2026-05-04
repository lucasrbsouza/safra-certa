<template>
  <div class="gauge">
    <p class="gauge__label">Ponto de Equilíbrio (Sacas/ha)</p>
    <div class="gauge__track">
      <div class="gauge__fill" :style="fillStyle"></div>
      <div class="gauge__needle" :style="needleStyle"></div>
    </div>
    <div class="gauge__zones">
      <span class="gauge__zone gauge__zone--danger">Inviável</span>
      <span class="gauge__zone gauge__zone--warning">Limite</span>
      <span class="gauge__zone gauge__zone--safe">Viável</span>
    </div>
    <div class="gauge__numbers">
      <p class="gauge__breakeven">
        Equilíbrio: <strong>{{ formatSacks(breakeven) }}</strong>
      </p>
      <p class="gauge__productivity">
        Estimado: <strong>{{ formatSacks(productivity) }}</strong>
      </p>
    </div>
    <div :class="['gauge__status', `gauge__status--${isViable ? 'viable' : 'inviable'}`]">
      {{ isViable ? 'VIÁVEL' : 'INVIÁVEL' }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCurrency } from '@/composables/useCurrency.js'

const props = defineProps({
  breakeven: { type: Number, default: 0 },
  productivity: { type: Number, default: 0 },
})

const { formatSacks } = useCurrency()

const percentage = computed(() => {
  if (props.breakeven === 0) return 100
  return Math.min((props.productivity / props.breakeven) * 100, 150)
})

const isViable = computed(() => props.productivity >= props.breakeven)

const fillStyle = computed(() => {
  const pct = Math.min(percentage.value, 100)
  const color = pct < 80 ? '#c62828' : pct < 100 ? '#f57f17' : '#2e7d32'
  return { width: `${pct}%`, backgroundColor: color }
})

const needleStyle = computed(() => ({
  left: `${Math.min(percentage.value, 100)}%`,
}))
</script>

<style scoped>
.gauge { background: #fff; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.gauge__label { text-align: center; font-size: 0.85rem; font-weight: 600; color: #555; margin: 0 0 1rem; }
.gauge__track {
  position: relative;
  height: 20px;
  border-radius: 10px;
  background: linear-gradient(to right, #ffcdd2 0%, #fff9c4 60%, #c8e6c9 100%);
  overflow: visible;
}
.gauge__fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease, background-color 0.5s;
  opacity: 0.4;
}
.gauge__needle {
  position: absolute;
  top: -4px;
  width: 3px;
  height: 28px;
  background: #1a1a1a;
  border-radius: 2px;
  transform: translateX(-50%);
  transition: left 0.5s ease;
}
.gauge__zones { display: flex; justify-content: space-between; margin-top: 6px; }
.gauge__zone { font-size: 0.72rem; font-weight: 600; }
.gauge__zone--danger { color: #c62828; }
.gauge__zone--warning { color: #f57f17; }
.gauge__zone--safe { color: #2e7d32; }
.gauge__numbers { display: flex; justify-content: space-between; margin-top: 1rem; }
.gauge__breakeven, .gauge__productivity { font-size: 0.9rem; color: #444; margin: 0; }
.gauge__status {
  text-align: center;
  margin-top: 1rem;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 1px;
  width: fit-content;
  margin-inline: auto;
}
.gauge__status--viable { background: #e8f5e9; color: #2e7d32; }
.gauge__status--inviable { background: #ffebee; color: #c62828; }
</style>
