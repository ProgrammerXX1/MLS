import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',  // 👈 ОБЯЗАТЕЛЬНО для доступа извне контейнера
    port: 3001        // не обязательно, но можно указать явно
  }
})
