<template>
  <header class="header">
    <div class="header__inner">
      <RouterLink to="/" class="header__brand">
        <div class="header__logo">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4C16 4 8 10 8 18C8 22.4 11.6 26 16 26C20.4 26 24 22.4 24 18C24 10 16 4 16 4Z" fill="#52b86a"/>
            <path d="M16 8C16 8 20 13 20 18C20 20.2 18.2 22 16 22C13.8 22 12 20.2 12 18C12 13 16 8 16 8Z" fill="#d4f0db"/>
            <path d="M16 26L16 30" stroke="#3a9950" stroke-width="2" stroke-linecap="round"/>
            <path d="M12 28L20 28" stroke="#3a9950" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="header__brand-text">
          <span class="header__brand-name">SafraCerta</span>
          <span class="header__brand-tagline">Simulador de Viabilidade</span>
        </div>
      </RouterLink>

      <nav class="header__nav" :class="{ 'header__nav--open': menuOpen }">
        <RouterLink to="/" class="header__link" @click="menuOpen = false">
          <svg viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>
          <span>Início</span>
        </RouterLink>
        <RouterLink to="/custos" class="header__link" @click="menuOpen = false">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/></svg>
          <span>Custos</span>
        </RouterLink>
        <RouterLink to="/simulacao" class="header__link" @click="menuOpen = false">
          <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>
          <span>Comparar</span>
        </RouterLink>
      </nav>

      <button class="header__menu-btn" @click="menuOpen = !menuOpen" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
const menuOpen = ref(false)
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--green-900);
  border-bottom: 1px solid var(--green-800);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.25rem;
  height: 62px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.header__brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  flex-shrink: 0;
}

.header__logo {
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.08);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
}
.header__logo svg { width: 100%; height: 100%; }

.header__brand-text { display: flex; flex-direction: column; }
.header__brand-name {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.1;
}
.header__brand-tagline {
  font-size: 0.65rem;
  color: var(--green-300);
  font-weight: 500;
  letter-spacing: 0.4px;
}

.header__nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.header__link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-sm);
  color: var(--green-300);
  font-size: 0.875rem;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
  text-decoration: none;
}
.header__link svg { width: 16px; height: 16px; flex-shrink: 0; }
.header__link:hover { background: rgba(255,255,255,0.08); color: #fff; }
.header__link.router-link-exact-active {
  background: rgba(255,255,255,0.12);
  color: #fff;
  font-weight: 600;
}

.header__menu-btn {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.header__menu-btn span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--green-300);
  border-radius: 2px;
  transition: background 0.15s;
}
.header__menu-btn:hover span { background: #fff; }

@media (max-width: 600px) {
  .header__menu-btn { display: flex; }
  .header__nav {
    display: none;
    position: absolute;
    top: 62px;
    left: 0;
    right: 0;
    background: var(--green-900);
    flex-direction: column;
    align-items: stretch;
    padding: 0.5rem 1rem 1rem;
    border-bottom: 1px solid var(--green-800);
    gap: 0.2rem;
  }
  .header__nav--open { display: flex; }
  .header__link { padding: 0.65rem 0.75rem; }
  .header__brand-tagline { display: none; }
}
</style>
