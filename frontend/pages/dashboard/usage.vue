<template>
  <div class="min-h-screen flex flex-col bg-[#0f0f0f] text-white">
    <Header />
    <div class="flex flex-1">
      <Sidebar />
      <section class="flex-1 h-full p-4 sm:p-6 md:p-8 overflow-auto">
        <h1 class="text-xl font-semibold mb-4 text-purple-400">Usage Dashboard</h1>
        <p class="text-xs text-neutral-400 mb-6">
          Note: Data can be delayed by up to 15 minutes
        </p>

        <!-- Chart Controls -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div class="flex items-center bg-[#2c2c2c] rounded-lg overflow-hidden text-sm font-medium">
            <button
              @click="currentView = 'cost'"
              :class="[
                'px-4 py-2 transition-colors',
                currentView === 'cost' ? 'text-black bg-purple-500' : 'text-white hover:bg-gray-700'
              ]"
            >
              Cost
            </button>
            <button
              @click="currentView = 'activity'"
              :class="[
                'px-4 py-2 transition-colors',
                currentView === 'activity' ? 'text-black bg-purple-500' : 'text-white hover:bg-gray-700'
              ]"
            >
              Activity
            </button>
          </div>
          <div class="flex items-center text-sm text-neutral-300 bg-[#2c2c2c] rounded-lg px-2 py-1">
            <button @click="previousPeriod" class="px-2 hover:text-purple-400">&lt;</button>
            <span class="px-3">{{ currentMonth }}</span>
            <button @click="nextPeriod" class="px-2 hover:text-purple-400">&gt;</button>
          </div>
        </div>

        <!-- Time Granularity Switcher -->
        <div class="flex items-center gap-2 text-sm text-neutral-300 mb-6">
          <span class="text-white font-medium">Data:</span>
          <button
            v-for="option in ['day', 'hour', 'minute']"
            :key="option"
            @click="granularity = option"
            :class="[
              'px-3 py-1 rounded-md transition-all',
              granularity === option ? 'bg-purple-500 text-white' : 'hover:bg-[#333] text-neutral-400'
            ]"
          >
            {{ option }}
          </button>
        </div>

        <!-- Scrollable content -->
        <div class="flex flex-col lg:flex-row gap-6 overflow-auto max-h-[calc(100vh-200px)] pr-2 pb-32">
          <div class="flex-1 space-y-6 overflow-auto">
            <!-- Activity View -->
            <div v-if="currentView === 'activity'">
              <div
                v-for="chart in modelCharts"
                :key="chart.model"
                class="bg-[#131313] border border-neutral-800 rounded-lg p-6 w-full"
              >
                <p class="text-sm font-semibold mb-4 text-purple-400">{{ chart.model }}</p>
                <div class="w-full" style="height: 280px;">
                  <LineChart
                    :chart-data="getLineChartData(chart)"
                    :chart-options="chartOptions"
                    :style="{ width: '100%', height: '100%' }"
                  />
                </div>
              </div>
            </div>

            <!-- Cost View -->
            <div v-else>
              <div
                v-for="chart in modelCharts"
                :key="chart.model"
                class="bg-[#131313] border border-neutral-800 rounded-lg p-6 w-full"
              >
                <p class="text-sm font-semibold mb-1 text-purple-400">{{ chart.model }}</p>
                <p class="text-xl font-bold mb-2 text-green-400">
                  ${{ getModelCost(chart.tokens).toFixed(4) }} USD
                </p>
                <p class="text-xs text-neutral-400 mb-4">Cost = tokens × 0.00001</p>
                <div class="w-full" style="height: 280px;">
                  <LineChart
                    :chart-data="getLineChartData(chart)"
                    :chart-options="chartOptions"
                    :style="{ width: '100%', height: '100%' }"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Right Panel -->
          <div class="w-full lg:w-80 shrink-0 space-y-6">
            <div class="bg-[#1a1a1a] border border-neutral-800 rounded-lg p-4">
              <p class="text-sm font-semibold mb-2 text-purple-400">Request Count</p>
              <p class="text-xs text-neutral-400">Playground</p>
              <p class="text-sm text-green-400">{{ userStore.username }}</p>
            </div>
            <div class="bg-[#1a1a1a] border border-neutral-800 rounded-lg p-4">
              <p class="text-sm font-semibold mb-2 text-purple-400">API Key</p>
              <p class="text-sm text-green-400">{{ apiKeyStore.count }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, watchEffect, onMounted } from 'vue'
import { format } from 'date-fns'
import Header from '~/components/Header.vue'
import Sidebar from '~/components/Sidebar_Dash.vue'
import LineChart from '~/components/LineChart.vue'

import { useLogStore } from '~/stores/dashboard'
import { useApiKeyStore } from '~/stores/apiKeys'
import { useApiKeys } from '~/composables/useApiKeys'
import { useUserStore } from '~/stores/user'

defineOptions({ inheritAttrs: false })

// === Stores ===
const apiKeyStore = useApiKeyStore()
const logStore = useLogStore()
const userStore = useUserStore()

// === Стейты ===
const currentView = ref<'cost' | 'activity'>('cost')
const currentMonth = ref('July')
const currentPeriod = ref(0)
const granularity = ref<'day' | 'hour' | 'minute'>('minute')

const modelCharts = ref<ModelChartData[]>([])

const previousPeriod = () => {
  currentPeriod.value--
  currentMonth.value = `Month ${currentPeriod.value}`
}

const nextPeriod = () => {
  currentPeriod.value++
  currentMonth.value = `Month ${currentPeriod.value}`
}

const getModelCost = (tokens: number) => tokens * 0.00001

type ModelChartData = {
  model: string
  tokens: number
  requests: Record<string, number>
  tokensPerUnit: Record<string, number>
}

// 🔄 Загрузка данных при монтировании
onMounted(async () => {
  await useApiKeys()

  // 🔄 Загрузка логов, если они ещё не загружены
  if (logStore.logs.length === 0 && typeof logStore.fetchLogs === 'function') {
    await logStore.fetchLogs()
  }
})

// 🔄 Обновление графиков при изменении логов или детализации
watchEffect(() => {
  const result: Record<string, ModelChartData> = {}

  for (const log of logStore.logs) {
    const model = log.model || 'unknown-model'

    const baseDate = new Date(log.created)
    if (isNaN(baseDate.getTime())) {
      console.warn('⚠️ Invalid date:', log.created)
      continue
    }

    // ⏱ +5 часов (если нужно локальное смещение)
    const date = new Date(baseDate.getTime() + 5 * 60 * 60 * 1000)

    // 🧩 Формируем ключ агрегации
    let key = ''
    if (granularity.value === 'day') key = format(date, 'EEE')           // Mon, Tue, ...
    else if (granularity.value === 'hour') key = format(date, 'HH:00')   // 14:00
    else if (granularity.value === 'minute') key = format(date, 'HH:mm') // 14:32

    // ⚙️ Инициализация модели
    if (!result[model]) {
      result[model] = {
        model,
        tokens: 0,
        requests: {},
        tokensPerUnit: {}
      }
    }

    // 📊 Подсчёт токенов и запросов
    const tokens = (log.inputTokens || 0) + (log.outputTokens || 0)
    result[model].tokens += tokens
    result[model].requests[key] = (result[model].requests[key] || 0) + 1
    result[model].tokensPerUnit[key] = (result[model].tokensPerUnit[key] || 0) + tokens
  }

  modelCharts.value = Object.values(result)

  // ✅ Отладка (можно убрать)
  console.log('📈 Model charts:', modelCharts.value)
})



// 📊 Данные для LineChart
const getLineChartData = (modelData: ModelChartData) => {
  let allKeys = Object.keys(modelData.requests).sort()

  if (granularity.value === 'minute' && allKeys.length > 200) {
    const step = Math.ceil(allKeys.length / 200)
    allKeys = allKeys.filter((_, i) => i % step === 0)
  }

  return {
    labels: allKeys,
    datasets: [
      {
        label: 'Requests',
        data: allKeys.map(k => modelData.requests[k] || 0),
        borderColor: '#a855f7',
        backgroundColor: 'rgba(168, 85, 247, 0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
      {
        label: 'Tokens',
        data: allKeys.map(k => modelData.tokensPerUnit[k] || 0),
        borderColor: '#22c55e',
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
      }
    ]
  }
}
</script>


<style scoped>
button:hover {
  transition: background-color 0.3s, color 0.3s;
}
</style>
