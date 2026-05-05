<template>
  <div :class="['rcard', `rcard--${variant}`, { 'rcard--highlight': highlight }]">
    <p class="rcard__title">{{ title }}</p>
    <p class="rcard__value">{{ value }}</p>
    <p v-if="unit" class="rcard__unit">{{ unit }}</p>
  </div>
</template>

<script setup>
defineProps({
  title:     { type: String, required: true },
  value:     { type: [String, Number], required: true },
  unit:      String,
  highlight: { type: Boolean, default: false },
  variant:   { type: String, default: 'neutral' },
})
</script>

<style scoped>
.rcard {
  background: #fff;
  border-radius: var(--radius-md);
  padding: 0.75rem 0.85rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  gap: 3px;
  position: relative;
  overflow: hidden;
  min-width: 0;
}

.rcard::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}

.rcard--neutral::before  { background: var(--gray-400); }
.rcard--positive::before { background: var(--green-500); }
.rcard--negative::before { background: var(--red-500); }

.rcard--highlight {
  border-color: var(--green-300);
  box-shadow: 0 2px 12px rgba(45,122,62,0.12);
}

.rcard__title {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gray-500);
  margin: 0;
}

.rcard__value {
  font-size: 1.05rem;
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--gray-900);
  margin: 0;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rcard--positive .rcard__value { color: var(--green-700); }
.rcard--negative .rcard__value { color: var(--red-600); }

.rcard__unit {
  font-size: 0.72rem;
  color: var(--gray-400);
  margin: 0;
}
</style>
