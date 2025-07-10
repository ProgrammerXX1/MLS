// utils/api.ts
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const baseUrl = 'http://localhost:8000' // или 'http://localhost:8000' если внешний backend

  const token = localStorage.getItem('access_token')
  const headers = new Headers(options.headers || {})

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(baseUrl + endpoint, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || 'API request failed')
  }

  return await response.json()
}
