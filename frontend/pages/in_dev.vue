<template>
  <div class="min-h-screen bg-[#1e1e1e] text-white flex flex-col items-center justify-center">
    <Header />

    <div class="flex-1 flex flex-col items-center justify-center space-y-6">
      <h1 class="text-4xl font-bold text-green-500 animate-pulse">🛠 Страница в разработке</h1>
      <p class="text-lg text-neutral-400">Мы активно работаем над этой функцией. Загляните позже!</p>
      <NuxtLink to="/" class="px-6 py-2 rounded-lg bg-green-600 text-white hover:bg-red-600 transition">
        Вернуться на главную
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Header.vue'
</script>
