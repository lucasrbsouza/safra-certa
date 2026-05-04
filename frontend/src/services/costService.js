import http from './http.js'

export const costService = {
  getAll: () => http.get('/costs').then((r) => r.data),
  getById: (id) => http.get(`/costs/${id}`).then((r) => r.data),
  create: (data) => http.post('/costs', data).then((r) => r.data),
  update: (id, data) => http.put(`/costs/${id}`, data).then((r) => r.data),
  remove: (id) => http.delete(`/costs/${id}`),
}
