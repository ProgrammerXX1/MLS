<template>
  <div class="chat-window" ref="chatRef">
    <div
      v-for="(msg, index) in store.current?.messages"
      :key="index"
      :class="[
        'message',
        isModelResponse(msg) ? 'left' : 'right',
        msg.role
      ]"
    >
     <div
  class="bubble"
  :class="{ 'model-response': isModelResponse(msg) }"
>
        <strong>{{ msg.role.toUpperCase() }}</strong>
        <pre class="whitespace-pre-wrap">{{ msg.text }}</pre>
        <small>{{ msg.time }}</small>
      </div>
    </div>

    <button class="clear-btn" @click="store.clearChat(store.current?.id)">🗑 Стереть чат</button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'
import { useModelStore } from '../store/modelStore'

const store = useModelStore()
const chatRef = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  if (chatRef.value) {
    chatRef.value.scrollTop = chatRef.value.scrollHeight
  }
}

onMounted(scrollToBottom)
onUpdated(scrollToBottom)

// Определяем, является ли сообщение ответом от модели
const isModelResponse = (msg: { role: string; text: string }) => {
  try {
    const parsed = JSON.parse(msg.text)
    // если внутри текст — весь JSON от model, это считается ответом
    return msg.role === 'assistant' && typeof parsed === 'object'
  } catch (e) {
    return false
  }
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  overflow-y: auto;
  height: 100%;
}

.message {
  display: flex;
  width: 100%;
}

.message.user,
.message.system {
  justify-content: flex-end; /* справа */
}

.message.assistant {
  justify-content: flex-start; /* слева */
}
pre {
  max-width: 100%;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  word-break: break-word;
}
.bubble {
  max-width: 60%;
  padding: 12px;
  border-radius: 10px;
  background-color: #222;
  color: #fff;
  white-space: pre-wrap;       /* Перенос строк */
  word-wrap: break-word;       /* Разрыв слов */
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.model-response {
  margin-bottom: 24px;
}
.message.user .bubble {
  background-color: #444;
}

.message.system .bubble {
  background-color: #555;
  font-size: 13px;
  font-family: monospace;
}

.message.assistant .bubble {
  background-color: #2c2c2c;
}
.clear-btn {
  margin-top: 12px;
  align-self: center;
  padding: 8px 12px;
  border: none;
  background: #444;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}
</style>
