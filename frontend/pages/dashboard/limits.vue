<template>
  <div class="min-h-screen flex flex-col bg-[#0f0f0f] text-white">
    <Header />

    <div class="flex flex-1">
      <Sidebar />

      <section class="flex-1 p-6 overflow-auto">
        <!-- Page Title -->
        <div class="mb-6">
          <h1 class="text-lg font-semibold mb-2">Limits</h1>
          <p class="text-sm text-neutral-400">
            These are the rate limits for your organization
          </p>
        </div>

        <!-- Table Title -->
        <h2 class="text-base font-semibold mb-3">Chat Completion</h2>

        <!-- Limits Table -->
        <div class="overflow-x-auto border border-neutral-800 rounded-lg">
          <table class="w-full text-sm text-left text-white">
            <thead class="bg-[#1a1a1a] text-neutral-400">
              <tr>
                <th class="px-4 py-2 font-medium">ID</th>
                <th class="px-4 py-2 font-medium">Requests per Minute</th>
                <th class="px-4 py-2 font-medium">Requests per Day</th>
                <th class="px-4 py-2 font-medium">Tokens per Minute</th>
                <th class="px-4 py-2 font-medium">Tokens per Day</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(limit, index) in limits"
                :key="index"
                class="border-t border-neutral-800 hover:bg-[#2a2a2a] transition-colors"
              >
                <td class="px-4 py-2">{{ limit.id }}</td>
                <td class="px-4 py-2">{{ limit.reqPerMin }}</td>
                <td class="px-4 py-2">{{ limit.reqPerDay }}</td>
                <td class="px-4 py-2">{{ limit.tokensPerMin }}</td>
                <td class="px-4 py-2 text-neutral-400">
                  {{ limit.tokensPerDay || '(No limit)' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Header.vue'
import Sidebar from '~/components/Sidebar_Dash.vue'

const limits = [
  { id: 'allam-2-7b', reqPerMin: 30, reqPerDay: 7000, tokensPerMin: 6000, tokensPerDay: null },
  { id: 'compound-beta', reqPerMin: 15, reqPerDay: 200, tokensPerMin: 70000, tokensPerDay: null },
  { id: 'compound-beta-mini', reqPerMin: 15, reqPerDay: 200, tokensPerMin: 70000, tokensPerDay: null },
  { id: 'deepseek-r1-distill-llama-70b', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 6000, tokensPerDay: null },
  { id: 'gemma2-9b-it', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 15000, tokensPerDay: '500 000' },
  { id: 'llama-3.1-8b-instant', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 6000, tokensPerDay: '500 000' },
  { id: 'llama-3.3-70b-versatile', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 12000, tokensPerDay: '100 000' },
  { id: 'llama3-70b-8192', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 6000, tokensPerDay: '500 000' },
  { id: 'llama3-8b-8192', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 6000, tokensPerDay: '500 000' },
  { id: 'meta-llama/llama-4-maverick-17b-128e-instruct', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 6000, tokensPerDay: '500 000' },
  { id: 'meta-llama/llama-4-scout-17b-16e-instruct', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 30000, tokensPerDay: '500 000' },
  { id: 'meta-llama/llama-guard-4-12b', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 15000, tokensPerDay: '500 000' },
  { id: 'meta-llama/llama-prompt-guard-2-22m', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 15000, tokensPerDay: '500 000' },
  { id: 'meta-llama/llama-prompt-guard-2-86m', reqPerMin: 30, reqPerDay: 14400, tokensPerMin: 15000, tokensPerDay: '500 000' },
  { id: 'mistral-saba-24b', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 6000, tokensPerDay: '500 000' },
  { id: 'qwen-qwq-32b', reqPerMin: 30, reqPerDay: 1000, tokensPerMin: 6000, tokensPerDay: '500 000' },
]
</script>
