<template>
  <div class="min-h-screen flex flex-col bg-[#0f0f0f] text-white">
    <Header />

    <div class="flex flex-1 min-h-0">
      <Sidebar />

      <section class="flex-1 p-6 overflow-auto relative">
        <!-- Top Title and Button -->
        <div class="flex justify-between items-center mb-10">
          <div>
            <h1 class="text-lg font-semibold mb-1">Batch</h1>
            <p class="text-sm text-neutral-400 max-w-3xl">
              Create large batches of API requests for asynchronous processing.
              The Batch API returns completions within 24 hours for a 50% discount.
            </p>
          </div>
          <button
            class="bg-gray-700 hover:bg-gray-600 text-white text-sm px-4 py-2 rounded transition-colors"
          >
            Create Batch
          </button>
        </div>

        <!-- Upgrade Block -->
        <div class="flex flex-col items-center justify-center text-center mt-20 space-y-4">
          <IconBolt class="text-red-500 w-10 h-10" />
          <h2 class="text-red-500 text-xl font-semibold">Enable Batch Processing</h2>
          <p class="text-sm text-neutral-400 max-w-md">
            Batch processing allows you to run multiple requests efficiently.
            Upgrade your plan to unlock this powerful feature
          </p>
          <button class="px-4 py-2 border border-neutral-600 rounded hover:bg-white hover:text-black transition-colors">
            Upgrade
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Header.vue'
import Sidebar from '~/components/Sidebar_Dash.vue'
import { Bolt } from 'lucide-vue-next'

const IconBolt = Bolt
</script>
