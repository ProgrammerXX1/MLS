<template>
  <div class="app">
    <Sidebar />
    <div class="chat-area">
      <ChatWindow />
      <MessageInput />
    </div>
    <ModelSettingsPanel />
  </div>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import ChatWindow from './components/ChatWindow.vue'
import MessageInput from './components/MessageInput.vue'
import ModelSettingsPanel from './components/ModelSettingsPanel.vue'
</script>

<style scoped>
.app {
  display: flex;
  height: 98vh; /* вместо 90vh */
  overflow: hidden; /* запрет скролла всей страницы */
}
.chat-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}
</style>
