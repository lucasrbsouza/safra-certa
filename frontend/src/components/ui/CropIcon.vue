<template>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.5"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="crop-icon"
    aria-hidden="true"
  >
    <!-- soja: sprout with two leaves -->
    <template v-if="type === 'soja'">
      <path d="M12 22V13"/>
      <path d="M12 13C11 10 7 7 4 8C4 11 8 13 12 13"/>
      <path d="M12 13C13 10 17 7 20 8C20 11 16 13 12 13"/>
    </template>

    <!-- milho: corn cob with rows -->
    <template v-else-if="type === 'milho'">
      <path d="M12 4C9 4 8 7 8 11C8 15 9 18 12 20C15 18 16 15 16 11C16 7 15 4 12 4Z"/>
      <path d="M10 8.5H14M10 11H14M10 13.5H14M10 16H14"/>
      <path d="M9 4C9 3 10 2 12 2C14 2 15 3 15 4"/>
    </template>

    <!-- feijao: kidney bean shape -->
    <template v-else-if="type === 'feijao'">
      <path d="M7 12C7 8 9 5 12 5C15 5 17 7 17 10C17 15 14 19 11 19C8 19 7 16 7 13Z"/>
      <path d="M11 9C10 9 9 10 10 11"/>
    </template>

    <!-- fallback: wheat stalk -->
    <template v-else>
      <path d="M12 22V8"/>
      <path d="M12 8C12 6 14 4 16 5C16 7 14 9 12 8"/>
      <path d="M12 8C12 6 10 4 8 5C8 7 10 9 12 8"/>
      <path d="M12 12C12 10 14 8 16 9C16 11 14 13 12 12"/>
      <path d="M12 12C12 10 10 8 8 9C8 11 10 13 12 12"/>
    </template>
  </svg>
</template>

<script setup>
defineProps({
  type: { type: String, default: '' },
})
</script>

<style scoped>
.crop-icon {
  width: 1em;
  height: 1em;
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}
</style>
