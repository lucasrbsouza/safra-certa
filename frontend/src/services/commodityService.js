import http from './http.js'

export const commodityService = {
  getAll: () => http.get('/commodities').then((r) => r.data),
  getByType: (cropType) => http.get(`/commodities/${cropType}`).then((r) => r.data),
  refresh: () => http.post('/commodities/refresh').then((r) => r.data),
}
