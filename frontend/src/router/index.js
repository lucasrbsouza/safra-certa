import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
  },
  {
    path: '/custos',
    name: 'custos',
    component: () => import('@/pages/CostRegistrationPage.vue'),
  },
  {
    path: '/simulacao',
    name: 'simulacao',
    component: () => import('@/pages/SimulationPage.vue'),
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
