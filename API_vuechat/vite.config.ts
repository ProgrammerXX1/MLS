import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // обязательно для доступа извне
    port: 5173       // это порт Vite внутри контейнера
  }
})
