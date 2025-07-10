export async function useApiKeys() {
  const store = useApiKeyStore()
  const response = await apiFetch('/api/keys/list')

  const adapted = response.map((k: any) => ({
    id: k.id,
    name: `key-${k.id}`,
    secret: `gsk_...${k.key.slice(-6)}`,
    created: k.created_at,
    last_used: k.last_used_at ?? null,
    usage: k.usage_24h ?? 0
  }))

  store.setKeys(adapted)

  return adapted // ⬅️ добавь это
}
