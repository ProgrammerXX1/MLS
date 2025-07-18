import { defineStore } from 'pinia'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://your-domain.com/api' // Укажи своё внешнее API

export interface Message {
  role: 'user' | 'assistant' | 'system'
  text: string
  time: string
}

export interface ModelSettings {
  temperature: number
  maxTokens: number
  stream: boolean
  jsonMode: boolean
  moderation: boolean
  topP: number
  seed: string
  stopSequence: string
}

export interface ModelChat {
  id: string
  name: string
  model: string
  avatar: string
  messages: Message[]
  settings: ModelSettings
}

export interface APIPayload {
  user_id: number
  api_key: string
  messages: { role: string; content: string }[]
  model: string
  temperature: number
  max_tokens: number
  response_format: string
  moderation: boolean
  top_p: number
  seed?: string
  stop?: string
}

export interface APIResponse {
  status: 'success' | 'error' | 'pending'
  response?: any
  error?: string
}

export function defaultSettings(): ModelSettings {
  return {
    temperature: 1,
    maxTokens: 512,
    stream: false,
    jsonMode: false,
    moderation: false,
    topP: 1,
    seed: '',
    stopSequence: ''
  }
}

export const useModelStore = defineStore('modelStore', {
  state: () => ({
    models: [
      { id: '1', name: 'Phi', model: 'phi:latest', avatar: '', messages: [], settings: defaultSettings() },
      { id: '2', name: 'Gemma', model: 'gemma:2b', avatar: '', messages: [], settings: defaultSettings() },
      { id: '3', name: 'Qwen 14B', model: 'qwen:14b', avatar: '', messages: [], settings: defaultSettings() },
      { id: '4', name: 'Qwen 7B', model: 'qwen:7b', avatar: '', messages: [], settings: defaultSettings() },
      { id: '5', name: 'Deepseek 33B', model: 'deepseek-coder:33b', avatar: '', messages: [], settings: defaultSettings() },
      { id: '6', name: 'Mistral', model: 'mistral:latest', avatar: '', messages: [], settings: defaultSettings() },
      { id: '7', name: 'Deepseek 6.7B', model: 'deepseek-coder:6.7b', avatar: '', messages: [], settings: defaultSettings() },
      { id: '8', name: 'Deepseek (latest)', model: 'deepseek-coder:latest', avatar: '', messages: [], settings: defaultSettings() },
      { id: '9', name: 'LLaMA 3', model: 'llama3:latest', avatar: '', messages: [], settings: defaultSettings() }
    ] as ModelChat[],
    selectedId: '1',
    lastTaskId: ''
  }),

  getters: {
    current: (state) => state.models.find((m) => m.id === state.selectedId)
  },

  actions: {
    selectModel(id: string) {
      this.selectedId = id
    },

    clearChat(chatId: string | undefined) {
      if (!chatId) return
      const chat = this.models.find(m => m.id === chatId)
      if (chat) {
        chat.messages = []
      }
    },

    addMessage(chatId: string, message: Message) {
      const chat = this.models.find((m) => m.id === chatId)
      if (chat) {
        chat.messages.push(message)
      }
    },

    buildPayload(messages: { role: string; content: string }[]): APIPayload {
      const chat = this.current!
      const settings = chat.settings

      return {
        user_id: 2,
        api_key: 'f5bca09b0a796301bfc74ab06e8c551952eec9c4524e17d103e15d2c6b0b63a8',
        messages,
        model: chat.model,
        temperature: settings.temperature,
        max_tokens: settings.maxTokens,
        response_format: settings.jsonMode ? 'json' : 'text',
        moderation: settings.moderation,
        top_p: settings.topP,
        seed: settings.seed || undefined,
        stop: settings.stopSequence || undefined
      }
    },

    async sendRequest(payload: { system: string; user: string; assistant: string }) {
      const chat = this.current
      if (!chat) return

      const time = new Date().toLocaleTimeString()
      const messages: { role: string; content: string }[] = []

      if (payload.system) messages.push({ role: 'system', content: payload.system })
      if (payload.user) messages.push({ role: 'user', content: payload.user })
      if (payload.assistant) messages.push({ role: 'assistant', content: payload.assistant })

      messages.forEach((msg) => {
        chat.messages.push({
          role: msg.role as 'user' | 'assistant' | 'system',
          text: JSON.stringify(msg, null, 2),
          time
        })
      })

      const fullPayload = this.buildPayload(messages)

      chat.messages.push({
        role: 'system',
        text: JSON.stringify(fullPayload, null, 2),
        time
      })

      try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fullPayload)
        })

        const data = await response.json()
        if (data.task_id) {
          this.lastTaskId = data.task_id
        } else {
          chat.messages.push({
            role: 'system',
            text: 'Ошибка: не удалось получить task_id',
            time: new Date().toLocaleTimeString()
          })
        }
      } catch (error) {
        chat.messages.push({
          role: 'system',
          text: 'Ошибка подключения к серверу',
          time: new Date().toLocaleTimeString()
        })
      }
    },

    async refreshResult() {
      const chat = this.current
      if (!chat || !this.lastTaskId) return

      try {
        const res = await fetch(`${API_BASE_URL}/generate/${this.lastTaskId}`)
        const data: APIResponse = await res.json()

        if (data.status === 'success') {
          chat.messages.push({
            role: 'assistant',
            text: JSON.stringify(data.response, null, 2),
            time: new Date().toLocaleTimeString()
          })
          this.lastTaskId = ''
        } else if (data.status === 'error') {
          chat.messages.push({
            role: 'system',
            text: `Ошибка: ${data.error}`,
            time: new Date().toLocaleTimeString()
          })
        } else {
          chat.messages.push({
            role: 'system',
            text: `Статус: ${data.status}`,
            time: new Date().toLocaleTimeString()
          })
        }
      } catch (error) {
        chat.messages.push({
          role: 'system',
          text: 'Ошибка при запросе статуса',
          time: new Date().toLocaleTimeString()
        })
      }
    }
  }
})
