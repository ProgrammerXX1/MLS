<template>
  <div class="flex flex-col h-full w-full bg-[#0f0f0f] rounded-xl border border-neutral-800">
    <!-- Контент -->
    <div class="flex-grow overflow-y-auto p-6 space-y-4">
      <template v-if="studioMessages.length === 0">
        <!-- Заголовок -->
        <div class="px-6 py-4 border-b border-neutral-800">
          <h2 class="text-xl font-semibold text-white">🧪 Aurus</h2>
        </div>
        <div class="text-neutral-400 text-sm space-y-2">
          <p>👋 Добро пожаловать в <strong class="text-white">Studio</strong>!</p>
          <ul class="list-disc pl-5">
            <li>Создавайте, редактируйте и тестируйте ваши промпты</li>
            <li>Настраивайте параметры вывода модели</li>
            <li>Изучайте примеры использования</li>
          </ul>
        </div>
      </template>

      <template v-else>
        <div
          v-for="(msg, index) in studioMessages"
          :key="index"
          class="bg-neutral-800 p-4 rounded-md border border-neutral-700 text-sm text-white whitespace-pre-wrap"
        >
          {{ msg }}
        </div>
      </template>
    </div>

    <!-- Кнопки -->
    <div class="px-6 py-4 border-t border-neutral-800 flex justify-between items-center">
      <div class="flex space-x-2">
        <button
          class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-red-500 hover:border-red-500 transition"
        >
          <span class="mr-2">⊕</span> Push
        </button>
        <button
          @click="clearResponses"
          class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-blue-500 hover:border-blue-500 transition"
        >
          Clear
        </button>
      </div>
      <div>
        <button
          @click="onSubmit"
          class="px-5 py-2 text-sm rounded-full border border-white text-white hover:bg-orange-500 hover:border-orange-500 transition"
        >
          Submit <span class="ml-2 text-xs text-neutral-400">Ctrl + ⏎</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePlaygroundStore } from '../../stores/playground'


const props = defineProps<{ onSubmit: () => void }>()

// ❗ Обходим типизацию вручную — не трогаем types в Pinia
const rawStore = usePlaygroundStore() as any

// ✅ Получаем сообщения (как computed)
const studioMessages = computed(() => rawStore.studioMessages ?? [])

// ✅ Очистка
const clearResponses = () => {
  rawStore.clearStudioMessages?.()
}

// ✅ Добавление
const addResponse = (text: string) => {
  rawStore.addStudioMessage?.(text)
}

// Экспорт наружу
defineExpose({ clearResponses, addResponse })
</script>

