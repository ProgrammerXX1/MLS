// plugins/api.client.ts
import axios from 'axios'
import { defineNuxtPlugin, useRuntimeConfig } from '#app'
export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
  })

  api.interceptors.request.use((cfg) => {
    const token = localStorage.getItem('token')
    if (token) {
      cfg.headers.Authorization = `Bearer ${token}`
    }
    return cfg
  })

  nuxtApp.provide('api', api)
})
