import axios from 'axios'
import { useRuntimeConfig } from '#imports'

const config = useRuntimeConfig()
const api = axios.create({
  baseURL: config.public.apiBase,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
