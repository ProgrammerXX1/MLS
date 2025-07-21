<template>
  <div class="flex flex-col h-full">
    <!-- Chat Messages -->
    <div class="flex-grow overflow-y-auto p-6 space-y-4">
      <div
        v-for="(msg, index) in messages"
        :key="msg.id"
        class="relative group border border-neutral-700 rounded-md p-4 bg-[#1a1a1a]"
      >
        <label class="text-xs text-neutral-400 font-semibold uppercase">
          {{ msg.role }}
        </label>
        <textarea
          v-model="msg.content"
          rows="4"
          :placeholder="`Enter ${msg.role} message...`"
          class="w-full mt-1 px-4 py-2 rounded-md bg-[#1a1a1a] border border-[#333] text-sm text-white resize-none"
        ></textarea>

        <button
          v-if="!(msg.role === 'system' && isMainSystem(index))"
          class="absolute top-2 right-2 text-neutral-500 hover:text-red-500 hidden group-hover:block"
          @click="deleteMessage(index)"
        >
          −
        </button>
      </div>
    </div>

    <!-- Buttons -->
<div class="px-4 py-3 border-t border-neutral-800 flex justify-between items-center">
  <!-- Left -->
  <div class="flex space-x-2">
    <button
      @click="addMessage"
      class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-red-500 hover:border-red-500 transition"
    >
      <span class="mr-2">⊕</span> Create
    </button>
    <button
      v-if="mode === 'chat'"
      @click="clearMessages"
      class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-blue-500 hover:border-blue-500 transition"
    >
      Clear
    </button>
  </div>
  <!-- Right -->
  <div>
    <button
      v-if="mode === 'chat'"
      @click="submitMessages"
      class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-green-500 hover:border-green-500 transition"
    >
      Submit <span class="ml-2 text-xs text-neutral-400">Ctrl + ⏎</span>
    </button>

    <button
      v-if="mode === 'studio'"
      @click="clearMessages"
      class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-blue-500 hover:border-blue-500 transition"
    >
      Clear
    </button>
  </div>
</div>
</div>
</template>
<script setup lang="ts">
import { inject, ref, computed, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useNuxtApp } from '#app'
import { usePlaygroundStore } from '../../stores/playground'

const { $api } = useNuxtApp()
const store = usePlaygroundStore()

interface Message {
  id: number
  role: 'system' | 'user' | 'assistant'
  content: string
}

const props = defineProps<{
  mode: 'chat' | 'studio'
  model: string
  onStudioResponse?: (text: string) => void
  modelSettings: {
    temperature: number
    maxTokens: number
    stream: boolean
    jsonMode: boolean
    moderation: boolean
    topP: number
    seed: string
    stopSequence: string
  }
}>()

const injected = inject<Ref<Message[]>>('chatMessages')
const messages = computed({
  get: () => injected?.value ?? store.messages,
  set: (val) => {
    if (injected) injected.value = val
    else store.setMessages(val)
  }
})

let idCounter = messages.value.length > 0 ? Math.max(...messages.value.map(m => m.id)) + 1 : 1
let roleStep = 0

const isMainSystem = (index: number) => {
  const systemIndexes = messages.value
    .map((m, i) => (m.role === 'system' ? i : -1))
    .filter(i => i !== -1)
  return index === systemIndexes[0]
}

const getNextRole = (): Message['role'] => {
  const role = roleStep === 0 ? 'user' : roleStep === 1 ? 'assistant' : 'system'
  roleStep = (roleStep + 1) % 3
  return role
}

const addMessage = () => {
  const msg: Message = {
    id: idCounter++,
    role: getNextRole(),
    content: '',
  }
  if (injected) injected.value.push(msg)
  else store.addMessage(msg)
}

const deleteMessage = (index: number) => {
  const isSystem = messages.value[index].role === 'system'
  const systemCount = messages.value.filter(m => m.role === 'system').length
  if (!isSystem || (isSystem && systemCount > 1)) {
    messages.value.splice(index, 1)
  }
}

const clearMessages = () => {
  messages.value.splice(0, messages.value.length, {
    id: 0,
    role: 'system',
    content: '',
  })
  idCounter = 1
  roleStep = 0
}

onMounted(() => {
  store.clearMessages()
})

const submitMessages = async () => {
  console.log('[Submit] Start')

  const hasValidMessages = messages.value.some(msg => msg.content.trim() !== '')
  if (!hasValidMessages) return

  const hasUserInput = messages.value.some(msg => msg.role === 'user' && msg.content.trim() !== '')
  if (!hasUserInput) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    console.warn('[Submit] No auth token found.')
    return
  }

  try {
    while (
      messages.value.length &&
      messages.value[messages.value.length - 1].role === 'assistant' &&
      messages.value[messages.value.length - 1].content.trim() === ''
    ) {
      messages.value.pop()
    }

    const payloadMessages = messages.value
      .filter(msg => msg.content.trim() !== '')
      .map(msg => ({
        role: msg.role,
        content: msg.content.trim(),
      }))

    const payload = {
      messages: payloadMessages,
      model: props.model,
      temperature: props.modelSettings.temperature,
      max_tokens: props.modelSettings.maxTokens,
      stream: false,  // ❗ стрим отключаем при async-режиме
      response_format: props.modelSettings.jsonMode ? 'json' : 'text',
      moderation: props.modelSettings.moderation,
      top_p: props.modelSettings.topP,
      seed: props.modelSettings.seed || undefined,
      stop: props.modelSettings.stopSequence || undefined,
    }

    const res = await $api.post('/chat/send', payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    const taskId = res.data.task_id
    console.log('[Submit] Task ID получен:', taskId)

    const reply = await pollTaskResult(taskId)
    console.log('[Submit] Ответ от воркера:', reply)

    if (props.onStudioResponse) {
      props.onStudioResponse(reply)
    } else {
      messages.value.push({
        id: idCounter++,
        role: 'assistant',
        content: reply,
      })
    }

  } catch (err) {
    console.error('[Submit] Ошибка отправки:', err)
  }
}
async function pollTaskResult(taskId: string): Promise<string> {
  const maxRetries = 60
  const delay = 1000 // 1 секунда между попытками

  for (let i = 0; i < maxRetries; i++) {
    const res = await $api.get(`/chat/result/${taskId}`)

    if (res.data.status === 'done') {
      return res.data.response_text
    }

    if (res.data.status === 'failed') {
      return '⚠️ Ошибка при выполнении задачи'
    }

    await new Promise(resolve => setTimeout(resolve, delay))
  }

  return '⚠️ Истекло время ожидания ответа от модели'
}


defineExpose({ submitMessages })
</script>
