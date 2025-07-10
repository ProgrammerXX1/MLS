<template>
  <div class="min-h-screen bg-[#131313] text-white">
    <Header />

    <main class="max-w-6xl mx-auto px-6 py-10">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold">API Keys</h1>
          <p class="text-sm text-gray-400 mt-1">
            Manage your API keys. Remember to keep your API keys safe to prevent unauthorized access.
          </p>
        </div>

        <button
          @click="createKey"
          class="bg-white text-black font-medium px-4 py-2 rounded-md hover:bg-gray-200 transition"
        >
          Create API Key
        </button>
      </div>

      <div v-if="isLoading" class="text-gray-400">Loading...</div>
      <div v-if="error" class="text-red-500">{{ error }}</div>

      <div v-if="keys.length" class="overflow-hidden rounded-lg shadow border border-neutral-700">
        <table class="w-full text-sm">
          <thead class="bg-[#1a1a1a] text-gray-400 border-b border-neutral-700 text-left">
            <tr>
              <th class="px-6 py-3">Name</th>
              <th class="px-6 py-3">Secret Key</th>
              <th class="px-6 py-3">Created</th>
              <th class="px-6 py-3">Last Used</th>
              <th class="px-6 py-3">Usage (24hrs)</th>
              <th class="px-6 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="key in keys"
              :key="key.id"
              class="hover:bg-[#2a2a2a] transition"
            >
              <td class="px-6 py-4">{{ key.name }}</td>
              <td class="px-6 py-4 font-mono">{{ key.secret }}</td>
              <td class="px-6 py-4">{{ formatDate(key.created) }}</td>
              <td class="px-6 py-4">{{ formatDate(key.last_used) }}</td>
              <td class="px-6 py-4">{{ key.usage }} API calls</td>
              <td class="px-6 py-4 text-right space-x-2">
                <button
                  @click="deleteKey(key.id)"
                  class="bg-red-800 p-2 rounded hover:bg-red-700"
                  title="Delete"
                >
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="!isLoading" class="text-gray-400 mt-4">No API keys found.</div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Header from '~/components/Header.vue'
import { useApiKeys } from '~/composables/useApiKeys'
import { useApiKeyStore } from '~/stores/apiKeys'
import { apiFetch } from '~/utils/api'
import type { ApiKey } from '~/stores/apiKeys' // ✅ добавлен импорт типа

const apiKeyStore = useApiKeyStore()
const keys = ref<ApiKey[]>([])
const isLoading = ref(false)
const error = ref('')

// Загрузка ключей при монтировании
onMounted(async () => {
  isLoading.value = true
  try {
    await useApiKeys() // эта функция запишет ключи в store
    keys.value = apiKeyStore.keys // читаем их отсюда
  } catch (err: any) {
    error.value = err?.message || 'Failed to load API keys'
  } finally {
    isLoading.value = false
  }
})

// Форматирование даты
function formatDate(dateStr: string | null): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return isNaN(date.getTime()) ? '-' : date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

// Создание нового API-ключа
async function createKey() {
  try {
    const newKey = await apiFetch('/api/keys/create', { method: 'POST' })
    const formattedKey: ApiKey = {
      id: newKey.id,
      name: `key-${newKey.id}`,
      secret: `gsk_...${newKey.key.slice(-6)}`,
      created: newKey.created_at,
      last_used: newKey.last_used_at ?? null,
      usage: newKey.usage_24h ?? 0
    }
    apiKeyStore.setKeys([formattedKey, ...apiKeyStore.keys])
    keys.value = apiKeyStore.keys // обновляем локальный список
  } catch (err) {
    alert('Failed to create key')
  }
}

// Удаление API-ключа
async function deleteKey(id: number) {
  try {
    await apiFetch(`/api/keys/${id}`, { method: 'DELETE' })
    const updated = apiKeyStore.keys.filter(k => k.id !== id)
    apiKeyStore.setKeys(updated)
    keys.value = updated
  } catch (err) {
    alert('Failed to delete key')
  }
}
</script>
