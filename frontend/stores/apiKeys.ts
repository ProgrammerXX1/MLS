// stores/apiKeys.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface ApiKey {
  id: number
  name: string
  secret: string
  created: string
  last_used: string
  usage: string
}

export const useApiKeyStore = defineStore('apiKeys', () => {
  const keys = ref<ApiKey[]>([])

  const setKeys = (newKeys: ApiKey[]) => {
    keys.value = newKeys
  }

  const count = computed(() => keys.value.length)

  return { keys, count, setKeys }
})
