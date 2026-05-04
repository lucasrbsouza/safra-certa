import http from './http.js'

export const simulationService = {
  simulate: (payload) => http.post('/simulation', payload).then((r) => r.data),
}
