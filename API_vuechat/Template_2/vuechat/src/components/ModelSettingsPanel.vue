<template>
  <div class="settings">
    <h3>Model Settings</h3>
    <div v-if="current">
      <label>Temperature
        <input type="number" v-model.number="temp.temperature" min="0" max="2" step="0.1" />
      </label>
      <label>Max Tokens
        <input type="number" v-model.number="temp.maxTokens" min="1" />
      </label>
      <label>Top P
        <input type="number" v-model.number="temp.topP" min="0" max="1" step="0.1" />
      </label>
      <label>Seed
        <input type="text" v-model="temp.seed" />
      </label>
      <label>Stop Sequence
        <input type="text" v-model="temp.stopSequence" />
      </label>
      <label><input type="checkbox" v-model="temp.stream" /> Stream</label>
      <label><input type="checkbox" v-model="temp.jsonMode" /> JSON mode</label>
      <label><input type="checkbox" v-model="temp.moderation" /> Moderation</label>

      <div class="buttons">
        <button @click="applySettings">Применить</button>
        <button @click="resetSettings">Сбросить</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useModelStore, defaultSettings, ModelSettings } from '../store/modelStore'

const store = useModelStore()
const current = computed(() => store.current)
const temp = ref<ModelSettings>({ ...current.value?.settings })

watch(() => store.selectedId, () => {
  if (store.current) {
    temp.value = { ...store.current.settings }
  }
})

function applySettings() {
  if (!store.current) return
  store.current.settings = { ...temp.value } // ✅ Заменяем настройки текущей модели
}

function resetSettings() {
  temp.value = { ...defaultSettings() }
  if (store.current) {
    store.current.settings = { ...temp.value }
  }
}
</script>




<style scoped>
.settings {
  width: 250px;
  background: #1e1e1e;
  color: white;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}
label {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  margin-bottom: 10px;
}
input[type="text"], input[type="number"] {
  background: #333;
  color: white;
  border: none;
  padding: 0.3rem;
}
.buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
button {
  flex: 1;
  background: #4f46e5;
  border: none;
  color: white;
  padding: 0.4rem;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background: #4338ca;
}
</style>
