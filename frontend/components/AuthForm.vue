<template>
  <div class="relative flex min-h-screen items-center justify-center bg-[url('/assets/image.png')] bg-cover bg-center text-white overflow-hidden">
    <!-- NeuralMesh with RTX A6000 background -->
    <NeuralMesh />

    <!-- Card for Login/Register -->
    <div class="relative z-10 w-full max-w-md p-6 group">
      <div
        class="bg-black/5 hover:bg-black/60 border border-amber-500/30 shadow-2xl rounded-2xl backdrop-blur-none group-hover:backdrop-blur-md p-8 transform transition-all duration-500"
      >
        <!-- Заголовки — появляются при наведении -->
        <div class="text-center mb-6 transition-opacity duration-500 opacity-0 group-hover:opacity-100">
          <h1 class="text-3xl font-extrabold bg-gradient-to-r from-amber-400 to-green-500 bg-clip-text text-transparent animate-flicker">
            {{ isLogin ? 'Power up with RTX A6000' : 'Unlock RTX A6000 Compute Power' }}
          </h1>
        </div>

        <!-- Скрытые поля при ненаведении -->
        <div class="grid gap-6 transition-opacity duration-500 opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto">
          <!-- Username Input -->
          <div class="grid gap-2">
            <label for="username" class="text-amber-200 font-medium animate-glow-text">Username</label>
            <input
              id="username"
              v-model="username"
              placeholder="Enter username or email"
              class="bg-green-900/30 text-white border border-amber-800/50 rounded-lg p-3 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/50 transition-all duration-300 shadow-glow placeholder-amber-600/50"
            />
          </div>

          <!-- Password Input -->
          <div class="grid gap-2">
            <label for="password" class="text-amber-200 font-medium animate-glow-text">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="bg-green-900/30 text-white border border-amber-800/50 rounded-lg p-3 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/50 transition-all duration-300 shadow-glow placeholder-amber-600/50"
            />
          </div>

          <!-- Error Message -->
          <p v-if="errorMessage" class="text-red-500 text-sm text-center animate-pulse">
            {{ errorMessage }}
          </p>
        </div>

        <!-- Кнопка — видна всегда -->
        <button
          :disabled="isLoading"
          @click="submit"
          class="relative w-full mt-4 bg-gradient-to-r from-amber-600 to-green-600 hover:from-amber-500 hover:to-green-500 text-white font-bold py-3 px-6 rounded-lg transition-all duration-300 shadow-glow hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="animate-pulse">
            {{ isLogin ? 'Processing...' : 'Creating Account...' }}
          </span>
          <span v-else>
            {{ isLogin ? 'Login' : 'Register' }}
          </span>
        </button>

        <!-- Переключение логин/регистрация — тоже появляется при наведении -->
        <div class="text-center text-sm text-amber-300 mt-4 transition-opacity duration-500 opacity-0 group-hover:opacity-100">
          <span>
            {{ isLogin ? "Need an account?" : 'Already registered?' }}
          </span>
          <NuxtLink
            :to="isLogin ? '/register' : '/login'"
            class="text-amber-400 hover:text-amber-300 ml-1 font-medium transition-colors"
          >
            {{ isLogin ? 'Register' : 'Login' }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, navigateTo } from '#app'
import { apiFetch } from '~/utils/api'
import { useUserStore } from '@/stores/user'

// Define NeuralMesh as a separate Vue component
const NeuralMesh = defineComponent({
  template: `
    <div class="absolute inset-0 opacity-50 z-0">
      <div class="w-full h-full bg-[url('/assets/image.png')] bg-cover bg-center animate-pulse-slow"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-zinc-950/80 to-transparent"></div>
    </div>
  `
})

const route = useRoute()
const isLogin = computed(() => route.path.includes('login'))

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const userStore = useUserStore()

async function submit() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const endpoint = isLogin.value ? '/auth/login' : '/auth/register'

    const body = isLogin.value
      ? new URLSearchParams({
          username: username.value,
          password: password.value
        })
      : JSON.stringify({
          username: username.value,
          password: password.value,
          is_api_user: false
        })

    const headers = isLogin.value
      ? { 'Content-Type': 'application/x-www-form-urlencoded' }
      : { 'Content-Type': 'application/json' }

    const response = await apiFetch(endpoint, {
      method: 'POST',
      headers,
      body
    })

    localStorage.setItem('access_token', response.access_token)
    userStore.loadFromToken()
    navigateTo('/')
  } catch (err: any) {
    console.error('Auth error:', err)
    errorMessage.value =
      err?.data?.detail || err?.message || 'Authentication failed'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Custom animations */
@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

@keyframes glow-text {
  0%, 100% { text-shadow: 0 0 10px rgba(251, 191, 36, 0.5); }
  50% { text-shadow: 0 0 20px rgba(251, 191, 36, 0.8); }
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.7; }
}

.animate-flicker {
  animation: flicker 2s infinite;
}

.animate-glow-text {
  animation: glow-text 3s infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 5s infinite;
}

.shadow-glow {
  box-shadow: 0 0 15px rgba(251, 191, 36, 0.3);
}

.shadow-glow:hover {
  box-shadow: 0 0 25px rgba(251, 191, 36, 0.5);
}
</style>
```