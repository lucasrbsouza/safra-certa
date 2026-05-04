<template>
  <header class="header">
    <div class="header__brand">
      <span class="header__icon">🌾</span>
      <span class="header__title">SafraCerta</span>
    </div>
    <nav class="header__nav">
      <RouterLink to="/" class="header__link">Dashboard</RouterLink>
      <RouterLink to="/custos" class="header__link">Custos</RouterLink>
      <RouterLink to="/simulacao" class="header__link">Simulação</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background-color: #2e7d32;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.header__brand { display: flex; align-items: center; gap: 0.5rem; }
.header__icon { font-size: 1.4rem; }
.header__title { font-size: 1.2rem; font-weight: 700; letter-spacing: 0.5px; }
.header__nav { display: flex; gap: 1.5rem; }
.header__link {
  color: #c8e6c9;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s;
}
.header__link:hover,
.header__link.router-link-active { color: #fff; }
</style>
