// stores/logStore.ts
import { defineStore } from 'pinia'

export interface LogEntry {
  created: string
  model: string
  apiKey: string
  code: number
  ttft: string
  latency: string
  inputTokens: number
  outputTokens: number
  audioSeconds: string
  requestId: string
  error: string
}

export const useLogStore = defineStore('logStore', {
  state: () => ({
    logs: [] as LogEntry[],
  }),
  getters: {
    errorLogs: (state) => state.logs.filter((log) => log.error !== '-'),
  },
  actions: {
    setLogs(logs: LogEntry[]) {
      this.logs = logs
    },
    clearLogs() {
      this.logs = []
    },
  },
})
