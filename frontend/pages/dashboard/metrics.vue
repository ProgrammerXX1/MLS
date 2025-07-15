<template>
  <div class="min-h-screen flex flex-col bg-[#1e1e1e] text-white">
    <Header />

    <div class="flex flex-1">
      <Sidebar />

      <section class="flex-1 h-full p-6 overflow-auto">
        <h1 class="text-white text-lg font-semibold mb-6">Metrics</h1>

        <div class="flex flex-wrap items-center gap-4 mb-6">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-neutral-300">Show Limits</span>
            <input
              type="checkbox"
              class="form-checkbox rounded text-green-500 bg-[#1e1e1e] border-neutral-700"
            />
          </div>

          <select class="bg-[#2c2c2c] text-sm text-white border border-neutral-700 rounded px-3 py-1">
            <option>Last 30 minutes</option>
            <option>Last 1 hour</option>
          </select>

          <select class="bg-[#2c2c2c] text-sm text-white border border-neutral-700 rounded px-3 py-1">
            <option>Show all Models</option>
          </select>

          <select class="bg-[#2c2c2c] text-sm text-white border border-neutral-700 rounded px-3 py-1">
            <option>Show all API Keys</option>
          </select>
        </div>

        <div class="bg-[#131313] border border-neutral-800 rounded-lg p-4">
          <p class="text-sm text-white mb-2 font-semibold">HTTP Status Codes</p>
          <div
            class="w-full h-48 flex items-center justify-center text-neutral-600 text-sm italic"
          >
            (Chart placeholder)
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Header.vue'
import Sidebar from '~/components/Sidebar_Dash.vue'
</script>
