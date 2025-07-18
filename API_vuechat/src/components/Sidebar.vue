<template>
  <div class="sidebar">
    <ul>
      <li
        v-for="model in store.models"
        :key="model.id"
        :class="{ active: model.id === store.selectedId }"
        @click="store.selectModel(model.id)"
      >
        {{ model.name }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useModelStore } from '../store/modelStore'
const store = useModelStore()
</script>

<style scoped>
.sidebar {
  width: 200px;
  background: #1e1e1e;
  color: white;
  padding: 1rem;
   height: 100vh; /* ← 100% высоты */
  overflow-y: auto;
}
li {
  cursor: pointer;
  padding: 0.5rem;
}
.active {
  background: #333;
}
</style>
