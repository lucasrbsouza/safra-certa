<template>
  <div :class="['card', `card--${colorVariant}`, { 'card--highlight': highlight }]">
    <p class="card__title">{{ title }}</p>
    <p class="card__value">{{ value }}</p>
    <p v-if="unit" class="card__unit">{{ unit }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], required: true },
  unit: String,
  highlight: { type: Boolean, default: false },
  colorVariant: { type: String, default: 'neutral' },
})
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-left: 4px solid #ccc;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.card--neutral { border-left-color: #607d8b; }
.card--positive { border-left-color: #2e7d32; }
.card--negative { border-left-color: #c62828; }
.card--highlight { box-shadow: 0 4px 16px rgba(46,125,50,0.2); }
.card__title { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; color: #666; margin: 0; }
.card__value { font-size: 1.5rem; font-weight: 700; color: #1a1a1a; margin: 0; }
.card--positive .card__value { color: #2e7d32; }
.card--negative .card__value { color: #c62828; }
.card__unit { font-size: 0.78rem; color: #888; margin: 0; }
</style>
