<template>
  <aside class="w-80 bg-# border-l border-gray-700 p-6 space-y-6 text-sm shadow-2xl rounded-r-lg">
    <h2 class="text-lg font-extrabold uppercase tracking-widest text-white">Parameters</h2>

    <!-- 🧠 Model Selector -->
    <div class="space-y-2.5">
      <label class="block text-sm font-semibold text-gray-200">Model</label>
      <select
        v-model="selected"
        class="w-full bg-black text-white py-2 px-3 rounded-lg border border-yellow-500 shadow-inner focus:outline-none focus:ring-2 focus:ring-yellow-400 transition"
      >
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>
    </div>

    <!-- Temperature -->
    <div class="space-y-2.5">
      <label class="block text-sm font-semibold text-gray-200">Temperature</label>
      <div class="flex items-center space-x-4 w-full">
        <input type="range" min="0" max="2" step="0.1" v-model="temperature" class="range-slider" />
        <span class="range-value">{{ temperature }}</span>
      </div>
    </div>

    <!-- Max Tokens -->
    <div class="space-y-2.5">
      <label class="block text-sm font-semibold text-gray-200">Max Completion Tokens</label>
      <div class="flex items-center space-x-4 w-full">
        <input type="range" min="1" max="4096" step="1" v-model="maxTokens" class="range-slider" />
        <span class="range-value">{{ maxTokens }}</span>
      </div>
    </div>

    <!-- Toggles -->
    <div class="flex items-center justify-between">
      <label class="text-sm font-semibold text-gray-200">Stream Mode</label>
      <div class="w-12 h-4 rounded-full px-1 cursor-pointer transition"
           :class="stream ? 'bg-green-500' : 'bg-gray-700'"
           @click="stream = !stream">
        <div class="w-4 h-4 bg-white rounded-full shadow-md transition-transform"
             :class="stream ? 'translate-x-6' : 'translate-x-0'"></div>
      </div>
    </div>

    <div class="flex items-center justify-between">
      <label class="text-sm font-semibold text-gray-200">JSON Mode</label>
      <div class="w-12 h-4 rounded-full px-1 cursor-pointer transition"
           :class="jsonMode ? 'bg-green-500' : 'bg-gray-700'"
           @click="jsonMode = !jsonMode">
        <div class="w-4 h-4 bg-white rounded-full shadow-md transition-transform"
             :class="jsonMode ? 'translate-x-6' : 'translate-x-0'"></div>
      </div>
    </div>

    <!-- Advanced -->
    <details class="mt-6">
      <summary class="text-sm font-semibold text-gray-200 cursor-pointer hover:text-yellow-400">Advanced</summary>
      <div class="mt-4 space-y-4">

        <div class="flex items-center justify-between">
          <label class="text-sm font-semibold text-gray-200">Moderation</label>
          <div class="w-12 h-4 rounded-full px-1 cursor-pointer transition"
               :class="moderation ? 'bg-green-500' : 'bg-gray-700'"
               @click="moderation = !moderation">
            <div class="w-4 h-4 bg-white rounded-full shadow-md transition-transform"
                 :class="moderation ? 'translate-x-6' : 'translate-x-0'"></div>
          </div>
        </div>

        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Top P</label>
          <div class="flex items-center space-x-4 w-full">
            <input type="range" min="0" max="1" step="0.01" v-model="topP" class="range-slider" />
            <span class="range-value">{{ topP }}</span>
          </div>
        </div>

        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Seed</label>
          <input type="text" v-model="seed"
                 class="w-full px-3 py-2 bg-black border border-gray-600 rounded-md text-white shadow-inner focus:outline-none focus:ring-2 focus:ring-yellow-400" />
        </div>

        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Stop Sequence</label>
          <input type="text" v-model="stopSequence"
                 class="w-full px-3 py-2 bg-black border border-gray-600 rounded-md text-white shadow-inner focus:outline-none focus:ring-2 focus:ring-yellow-400" />
        </div>
      </div>
    </details>

    <!-- Buttons -->
    <div class="mt-6 pt-4 border-t border-gray-700 flex justify-between space-x-3">
      <button @click="applySettings"
              class="flex-1 bg-gradient-to-r from-emerald-500 to-lime-500 text-black font-semibold py-2 rounded-lg shadow-md hover:brightness-110 transition duration-200">
        Применить
      </button>
      <button @click="resetSettings"
              class="flex-1 bg-gradient-to-r from-gray-700 to-gray-900 text-white font-semibold py-2 rounded-lg shadow-md hover:brightness-125 transition duration-200">
        Сбросить
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

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

// Props & Emits
const props = defineProps<{
  models: string[]
  selectedModel: string
  modelSettings: ModelSettings
}>()

const emit = defineEmits<{
  (e: 'update:selectedModel', value: string): void
  (e: 'update:modelSettings', value: ModelSettings): void
}>()

// 🔁 Модель (v-model для select)
const selected = ref(props.selectedModel)
watch(() => props.selectedModel, val => {
  if (val !== selected.value) selected.value = val
})
watch(selected, val => {
  if (val !== props.selectedModel) emit('update:selectedModel', val)
})

// 🔧 Model Settings
const temperature = ref(props.modelSettings.temperature)
const maxTokens = ref(props.modelSettings.maxTokens)
const stream = ref(props.modelSettings.stream)
const jsonMode = ref(props.modelSettings.jsonMode)
const moderation = ref(props.modelSettings.moderation)
const topP = ref(props.modelSettings.topP)
const seed = ref(props.modelSettings.seed)
const stopSequence = ref(props.modelSettings.stopSequence)

// 📤 Emit helper
const emitSettings = () => {
  emit('update:modelSettings', {
    temperature: temperature.value,
    maxTokens: maxTokens.value,
    stream: stream.value,
    jsonMode: jsonMode.value,
    moderation: moderation.value,
    topP: topP.value,
    seed: seed.value,
    stopSequence: stopSequence.value,
  })
}

// Авто-emit при изменении параметров
watch(
  [temperature, maxTokens, stream, jsonMode, moderation, topP, seed, stopSequence],
  emitSettings,
  { immediate: true }
)

// Обновление при входящих props.modelSettings
watch(() => props.modelSettings, (newVal) => {
  temperature.value = newVal.temperature
  maxTokens.value = newVal.maxTokens
  stream.value = newVal.stream
  jsonMode.value = newVal.jsonMode
  moderation.value = newVal.moderation
  topP.value = newVal.topP
  seed.value = newVal.seed
  stopSequence.value = newVal.stopSequence
}, { deep: true })

// 🧪 Кнопка "Применить"
const applySettings = () => {
  emitSettings()
  console.log('[ControlPanel] Settings applied:', {
    temperature: temperature.value,
    maxTokens: maxTokens.value,
    stream: stream.value,
    jsonMode: jsonMode.value,
    moderation: moderation.value,
    topP: topP.value,
    seed: seed.value,
    stopSequence: stopSequence.value,
  })
}

// ♻️ Сброс к дефолту
const resetSettings = () => {
  temperature.value = 1
  maxTokens.value = 1024
  stream.value = false
  jsonMode.value = false
  moderation.value = false
  topP.value = 0.75
  seed.value = ''
  stopSequence.value = ''
  emitSettings()
}
</script>

<style scoped>
.range-slider {
  width: 100%;
  height: 8px;
  appearance: none;
  background: linear-gradient(to right, #2563eb, #f97316);
  border-radius: 9999px;
  position: relative;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.6);
  transition: all 0.2s ease;
}
.range-slider::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  background-color: #ffffff;
  border: 2px solid #facc15;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(255, 204, 0, 0.6);
  transition: transform 0.2s;
}
.range-slider:hover::-webkit-slider-thumb {
  transform: scale(1.3);
}
.range-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background-color: #ffffff;
  border: 2px solid #facc15;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(255, 204, 0, 0.6);
  transition: transform 0.2s;
}
.range-slider:hover::-moz-range-thumb {
  transform: scale(1.3);
}
.range-value {
  min-width: 50px;
  text-align: center;
  background: linear-gradient(to right, #111827, #000);
  color: white;
  padding: 0.4rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  box-shadow: 0 0 4px rgba(255, 255, 255, 0.1);
}
</style>
