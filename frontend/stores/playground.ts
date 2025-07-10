import { defineStore } from 'pinia'

interface Message {
  id: number
  role: 'system' | 'user' | 'assistant'
  content: string
}

export const usePlaygroundStore = defineStore('playground', {
  state: () => ({
    mode: 'chat' as 'chat' | 'studio',
    messages: [] as Message[],
    studioMessages: [] as string[],       // 🟢 Студийные ответы (массив)
    studioResponse: '' as string,         // 🟡 Последний ответ (по желанию)
  }),

  actions: {
    // 🧠 Mode переключение
    setMode(newMode: 'chat' | 'studio') {
      this.mode = newMode
    },

    // 📨 Ответ (если нужно только последний)
    setStudioResponse(response: string) {
      this.studioResponse = response
    },
    clearStudioResponse() {
      this.studioResponse = ''
    },

    // 💬 Сообщения чата
    setMessages(msgs: Message[]) {
      this.messages = msgs
    },
    addMessage(msg: Message) {
      this.messages.push(msg)
    },
    clearMessages() {
      this.messages = [{
        id: 0,
        role: 'system',
        content: ''
      }]
    },
    deleteMessage(index: number) {
      const systemCount = this.messages.filter(m => m.role === 'system').length
      const isSystem = this.messages[index].role === 'system'
      if (!isSystem || (isSystem && systemCount > 1)) {
        this.messages.splice(index, 1)
      }
    },

    // 🧪 Studio-режим — добавление и очистка ответов
    addStudioMessage(text: string) {
      this.studioMessages.push(text)
    },
    clearStudioMessages() {
      this.studioMessages = []
    }
  }
})
