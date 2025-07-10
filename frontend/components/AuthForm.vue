<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-zinc-900 via-orange-900 to-amber-900 text-white relative overflow-hidden">
    <NeuralMesh />
    <Card class="w-full max-w-md bg-orange-950/30 border border-amber-800/50 shadow-2xl rounded-xl backdrop-blur-lg p-6">
      <CardHeader>
        <CardTitle class="text-2xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent animate-flicker">
          {{ isLogin ? 'Login to NeuralNet AI' : 'Register for NeuralNet AI' }}
        </CardTitle>
        <CardDescription class="text-amber-200 animate-glow-text">
          {{ isLogin ? 'Enter your credentials to continue' : 'Create your account to begin' }}
        </CardDescription>
      </CardHeader>

      <CardContent>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <label for="username" class="text-amber-200 animate-glow-text">Username</label>
            <input
              id="username"
              v-model="username"
              placeholder="you@example.com or username"
              class="bg-orange-900/20 text-white border-amber-800/50 focus:border-amber-500 transition-all duration-300 shadow-glow"
            />
          </div>

          <div class="grid gap-2">
            <label for="password" class="text-amber-200 animate-glow-text">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="bg-orange-900/20 text-white border-amber-800/50 focus:border-amber-500 transition-all duration-300 shadow-glow"
            />
          </div>

          <!-- Ошибка -->
          <p v-if="errorMessage" class="text-red-500 text-sm text-center -mt-2">
            {{ errorMessage }}
          </p>

          <Button
            :disabled="isLoading"
            @click="submit"
            class="bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white transition-all duration-300 shadow-glow"
          >
            <span v-if="isLoading" class="animate-pulse">
              {{ isLogin ? 'Logging in...' : 'Registering...' }}
            </span>
            <span v-else>
              {{ isLogin ? 'Login' : 'Register' }}
            </span>
          </Button>

          <div class="text-center text-sm text-amber-300">
            <span>
              {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
            </span>
            <NuxtLink
              :to="isLogin ? '/register' : '/login'"
              class="text-amber-400 hover:text-amber-300 ml-1"
            >
              {{ isLogin ? 'Register' : 'Login' }}
            </NuxtLink>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, navigateTo } from '#app'
import { apiFetch } from '~/utils/api'
import { useUserStore } from '@/stores/user'

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

    // ✅ сохранить токен
    localStorage.setItem('access_token', response.access_token)

    // ✅ обновить состояние из токена
    userStore.loadFromToken()

    // ✅ перейти на главную
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
