import { defineNuxtConfig } from 'nuxt/config'
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss', 'nuxt-icon', '@pinia/nuxt'],
  css: ['@/assets/css/tailwind.css'],
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000' // ⚠️ Без https
    },
  },
  
})
