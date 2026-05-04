import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    const detail = error.response?.data?.detail ?? error.message
    return Promise.reject(new Error(detail))
  },
)

export default http
