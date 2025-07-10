<template>
  <aside class="min-h-screen w-64 bg-[#1e1e1e] border-r border-neutral-800 pt-6 text-sm text-neutral-400 flex flex-col">
    <nav class="space-y-4 px-4 flex-1">
      <NuxtLink
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        class="block px-2 py-1.5 rounded hover:text-red-500"
        :class="{ 'text-orange-500 font-medium': route.path === item.to }"
      >
        {{ item.label }}
      </NuxtLink>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from '#app'
const route = useRoute()

const items = [
  { label: 'Metrics', to: '/dashboard/metrics' },
  { label: 'Usage', to: '/dashboard/usage' },
  { label: 'Logs', to: '/dashboard/logs' },
  { label: 'Batch', to: '/dashboard/batch' },
  { label: 'Limits', to: '/dashboard/limits' },
]
</script>
