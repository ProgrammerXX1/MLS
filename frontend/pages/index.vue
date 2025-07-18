<template>
  <div class="min-h-screen bg-transparent text-white text-[130%] relative z-10">
    <!-- Header -->
    <Header />
    <div class="flex h-[calc(100vh-56px)] relative">
      <!-- Left Section -->
      <div class="flex flex-col w-[85%] border-r border-neutral-800 p-6 transition-all duration-300 ease-in-out h-full bg-[#0d0d0d]">
        <div class="flex flex-col w-full flex-1 min-h-0 space-y-4">
          <!-- Header + Mode Toggle -->
          <PlaygroundHeader
          class="bg-[#0d0d0d] text-white rounded-xl p-4 w-full"
            :mode="mode"
            :selected-model="selectedModel"
            :models="models"
            :show-code="showCode"
            @update:mode="mode = $event"
            @update:selectedModel="selectedModel = $event"
            @toggle-code="showCode = !showCode"
          />

          <!-- Main Panels -->
          <div class="flex flex-row flex-1 w-full min-h-0 space-x-4 items-stretch">
            <ChatPanel
              class="bg-[#0d0d0d] text-white rounded-xl p-4 w-full"
              v-if="mode === 'chat' || mode === 'studio'"
              ref="chatPanelRef"
              :class="panelClass('chat')"
              :mode="mode"
              :on-studio-response="handleStudioResponse"
              :model="selectedModel"
              :model-settings="modelSettings"
            />
            <StudioPanel
              class="bg-[#0d0d0d] text-white rounded-xl p-4 w-full"
              v-if="mode === 'studio'"
              ref="studioPanelRef"
              :class="panelClass('studio')"
              :on-submit="handleStudioSubmit"
            />
            <CodePanel
              class="bg-[#0d0d0d] text-white rounded-xl p-4 w-full"
              v-if="showCode"
              :class="panelClass('code')"
              :model="selectedModel"
              @update:selectedModel="selectedModel = $event"
              @update:modelSettings="modelSettings = $event"
            />
          </div>
        </div>
      </div>

      <!-- Right Section -->
      <div class="w-100 flex-shrink-0 bg-[#1e1e1e] border-l border-neutral-800">
        <ControlPanel 
            :models="models"
            :selected-model="selectedModel"
            :model-settings="modelSettings"
            @update:selectedModel="selectedModel = $event"
            @update:modelSettings="modelSettings = $event"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted, watch } from 'vue'
import { useNuxtApp } from '#app'

import Header from '~/components/Header.vue'
import PlaygroundHeader from '~/components/PlaygroundHeader.vue'
import ChatPanel from '~/components/Playground/ChatPanel.vue'
import StudioPanel from '~/components/Playground/StudioPanel.vue'
import CodePanel from '~/components/Playground/CodePanel.vue'
import ControlPanel from '~/components/ControlPanel.vue'

const { $api } = useNuxtApp()

// UI state
const mode = ref<'chat' | 'studio'>('studio')
const showCode = ref(true)
const selectedModel = ref('')

// Модели и настройки
const models = ref<{ name: string; supports: string[] }[]>([])
const modelSettings = ref({
  temperature: 1,
  maxTokens: 1024,
  stream: false,
  jsonMode: false,
  moderation: false,
  topP: 0.75,
  seed: '',
  stopSequence: ''
})

// Чат
const chatMessages = ref([{ id: 1, role: 'system', content: '' }])
provide('chatMessages', chatMessages)

// Панели
const chatPanelRef = ref<InstanceType<typeof ChatPanel> | null>(null)
const studioPanelRef = ref<InstanceType<typeof StudioPanel> | null>(null)

const handleStudioResponse = (text: string) => {
  console.log('[index.vue] Received studio response:', text)
  studioPanelRef.value?.addResponse(text)
}

const handleStudioSubmit = () => {
  if (chatPanelRef.value?.submitMessages) {
    chatPanelRef.value.submitMessages()
  } else {
    console.warn('[index.vue] chatPanelRef is not ready or missing submitMessages')
  }
}

// Классы панелей
const panelClass = (panel: 'chat' | 'studio' | 'code') => {
  const activePanels = [
    mode.value === 'chat' || mode.value === 'studio' ? 'chat' : '',
    mode.value === 'studio' ? 'studio' : '',
    showCode.value ? 'code' : ''
  ].filter(Boolean)

  const basis =
    activePanels.length === 1 ? 'basis-full'
    : activePanels.length === 2 ? 'basis-1/2'
    : 'basis-1/3'

  return `${basis} flex flex-col h-full border border-neutral-700 rounded-md overflow-hidden`
}

// 🔄 Загрузка моделей
onMounted(async () => {
  try {
    const res = await $api.get('/models')
    models.value = res.data.models || []
  } catch (err) {
    console.error('[index.vue] Ошибка загрузки моделей:', err)
  }
})

// ✅ Автоматически выбираем первую модель
watch(models, (newModels) => {
  if (!selectedModel.value && newModels.length > 0) {
    selectedModel.value = newModels[0].name
  }
})
</script>



<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
