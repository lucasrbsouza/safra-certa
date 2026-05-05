<template>
  <div class="gauge" :class="isViable ? 'gauge--viable' : 'gauge--inviable'">
    <div class="gauge__header">
      <span class="gauge__title">Ponto de Equilíbrio</span>
      <span :class="['gauge__badge', isViable ? 'gauge__badge--viable' : 'gauge__badge--inviable']">
        {{ isViable ? '✓ Viável' : '✗ Inviável' }}
      </span>
    </div>

    <div class="gauge__track-wrap">
      <div class="gauge__track">
        <div class="gauge__fill" :style="fillStyle"></div>
        <div class="gauge__needle" :style="needleStyle">
          <div class="gauge__needle-line"></div>
          <div class="gauge__needle-cap"></div>
        </div>
      </div>
      <div class="gauge__zone-labels">
        <span class="gauge__zone-label gauge__zone-label--danger">Inviável</span>
        <span class="gauge__zone-label gauge__zone-label--warning">Limite</span>
        <span class="gauge__zone-label gauge__zone-label--safe">Viável</span>
      </div>
    </div>

    <div class="gauge__values">
      <div class="gauge__value-item">
        <span class="gauge__value-label">Ponto de equilíbrio</span>
        <span class="gauge__value-number">{{ formatSacks(breakevenSacks) }}</span>
      </div>
      <div class="gauge__value-divider"></div>
      <div class="gauge__value-item gauge__value-item--right">
        <span class="gauge__value-label">Sua produtividade</span>
        <span class="gauge__value-number gauge__value-number--main">{{ formatSacks(estimatedProductivity) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCurrency } from '@/composables/useCurrency.js'

const props = defineProps({
  breakevenSacks:        { type: Number, default: 0 },
  estimatedProductivity: { type: Number, default: 0 },
  isViable:              { type: Boolean, default: false },
})

const { formatSacks } = useCurrency()

const percentage = computed(() => {
  if (!props.breakevenSacks) return 100
  return Math.min((props.estimatedProductivity / props.breakevenSacks) * 100, 150)
})

const fillStyle = computed(() => {
  const pct = Math.min(percentage.value, 100)
  let color
  if (pct < 80)       color = '#ef4444'
  else if (pct < 100) color = '#f59e0b'
  else                color = '#22c55e'
  return { width: `${pct}%`, background: color, transition: 'width 0.6s cubic-bezier(.4,0,.2,1), background 0.4s' }
})

const needleStyle = computed(() => ({
  left: `${Math.min(percentage.value, 100)}%`,
  transition: 'left 0.6s cubic-bezier(.4,0,.2,1)',
}))
</script>

<style scoped>
.gauge {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.gauge__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gauge__title {
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gray-500);
}

.gauge__badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  letter-spacing: 0.02em;
}
.gauge__badge--viable   { background: var(--green-100); color: var(--green-700); }
.gauge__badge--inviable { background: var(--red-100);   color: var(--red-600); }

.gauge__track-wrap { display: flex; flex-direction: column; gap: 5px; }

.gauge__track {
  position: relative;
  height: 16px;
  border-radius: 999px;
  background: linear-gradient(to right,
    #fee2e2 0%,
    #fef3c7 55%,
    #bbf7d0 100%
  );
  overflow: visible;
}

.gauge__fill {
  height: 100%;
  border-radius: 999px;
  opacity: 0.55;
}

.gauge__needle {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
}

.gauge__needle-line {
  width: 3px;
  height: 26px;
  background: var(--gray-800);
  border-radius: 2px;
  margin: 0 auto;
  transform: translateY(-4px);
}

.gauge__needle-cap {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--gray-800);
  border: 2px solid #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  margin: -2px auto 0;
}

.gauge__zone-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 2px;
}
.gauge__zone-label {
  font-size: 0.68rem;
  font-weight: 600;
}
.gauge__zone-label--danger  { color: #ef4444; }
.gauge__zone-label--warning { color: #f59e0b; }
.gauge__zone-label--safe    { color: #22c55e; }

.gauge__values {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  border: 1px solid var(--gray-200);
}

.gauge__value-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.gauge__value-item--right { text-align: right; align-items: flex-end; }

.gauge__value-divider {
  width: 1px;
  height: 36px;
  background: var(--gray-200);
  flex-shrink: 0;
}

.gauge__value-label {
  font-size: 0.7rem;
  color: var(--gray-500);
  font-weight: 500;
}

.gauge__value-number {
  font-size: 1.1rem;
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--gray-700);
}
.gauge__value-number--main {
  color: var(--green-700);
}
</style>
