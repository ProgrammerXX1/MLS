<template>
  <div class="flex items-center justify-between w-full space-x-4">
    <div class="flex items-center space-x-4">
      <h1 class="text-xl font-semibold text-white">Playground</h1>
      <div class="flex items-center bg-[#2e2e2e] rounded-full px-1 py-1 space-x-1 border border-[#3a3a3a]">
        <button
          class="px-3 py-1 rounded-full text-xs"
          :class="mode === 'chat' ? 'bg-black text-white' : 'text-gray-400'"
          @click="emit('update:mode', 'chat')"
        >
          Chat
        </button>
        <button
          class="px-3 py-1 rounded-full text-xs"
          :class="mode === 'studio' ? 'bg-black text-white' : 'text-gray-400'"
          @click="emit('update:mode', 'studio')"
        >
          Studio
        </button>
      </div>
    </div>
    <div class="flex items-center space-x-2">
      <select
        v-model="internalModel"
        @change="onModelChange"
        class="bg-[#2e2e2e] text-white text-sm rounded-md px-3 py-1 focus:outline-none border border-neutral-700 max-w-xs truncate"
      >
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>
      <button
        @click="emit('toggle-code')"
        class="flex items-center space-x-2 px-3 py-1 rounded-md border border-green-700 text-green-700 hover:bg-green-700 hover:text-white transition text-sm"
      >
        <Icon icon="lucide:code" class="text-sm" />
        <span>{{ showCode ? 'Hide code' : 'View code' }}</span>
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  mode: 'chat' | 'studio'
  selectedModel: string
  models: string[]
  showCode: boolean
}>()

const emit = defineEmits<{
  (e: 'update:mode', value: 'chat' | 'studio'): void
  (e: 'update:selectedModel', value: string): void
  (e: 'toggle-code'): void
}>()

const internalModel = ref(props.selectedModel)

// 🔄 Следим за обновлением пропса
watch(() => props.selectedModel, (val) => {
  internalModel.value = val
})

// 📤 Отправка новой модели наружу
const onModelChange = (event: Event) => {
  emit('update:selectedModel', (event.target as HTMLSelectElement).value)
}

// Следим за обновлением моделей (если пришли асинхронно)
watch(
  () => props.models,
  (newModels) => {
    if (!internalModel.value && newModels.length > 0) {
      internalModel.value = newModels[0]
      emit('update:selectedModel', newModels[0])
    }
  },
  { immediate: true }
)


</script>

