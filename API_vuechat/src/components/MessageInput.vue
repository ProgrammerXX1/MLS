<template>
  <form @submit.prevent>
    <input v-model="systemText" type="text" placeholder="System message (optional)" />
    <input v-model="userText" type="text" placeholder="User message (required)" required />
    <input v-model="assistantText" type="text" placeholder="Assistant message (optional)" />

    <div class="buttons">
      <button type="button" @click="send">Send</button>
      <button type="button" @click="refresh">Refresh</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useModelStore } from '../store/modelStore'

const store = useModelStore()
const systemText = ref('')
const userText = ref('')
const assistantText = ref('')

const send = async () => {
  await store.sendRequest({
    system: systemText.value.trim(),
    user: userText.value.trim(),
    assistant: assistantText.value.trim()
  })

  systemText.value = ''
  userText.value = ''
  assistantText.value = ''
}

const refresh = async () => {
  await store.refreshResult()
}
</script>


<style scoped>
form {
  flex-shrink: 0; /* ← не позволяет сжаться */
  display: flex;
  flex-direction: column;
  padding: 1rem;
  gap: 0.5rem;
  background: #1e1e1e;
  border-top: 1px solid #444;
}
input {
  padding: 0.5rem;
  background: #333;
  color: white;
  border: none;
  border-radius: 4px;
}
button {
  padding: 0.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #4338ca;
}
</style>
