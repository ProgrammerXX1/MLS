<template>
  <div class="min-h-screen flex flex-col bg-[#0f0f0f] text-white">
    <Header />

    <div class="flex flex-1 min-h-0">
      <Sidebar />

      <section class="flex-1 p-4 sm:p-6 md:p-8 overflow-auto">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <h1 class="text-xl font-semibold text-purple-400">Logs Dashboard</h1>
          <div class="flex items-center space-x-4">
            <label class="flex items-center">
              <input
                type="checkbox"
                class="mr-2 accent-purple-500 h-4 w-4"
                v-model="showErrorsOnly"
              />
              <span class="text-sm text-neutral-400">Show Errors Only</span>
            </label>
            <button
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm font-medium transition-colors"
              @click="downloadLogs"
            >
              Download Logs <span class="ml-1">↓</span>
            </button>
          </div>
        </div>

        <!-- Loading Spinner -->
        <div v-if="loading" class="text-neutral-400 text-sm flex items-center justify-center">
          <svg class="animate-spin h-5 w-5 mr-2 text-purple-500" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
          Loading logs...
        </div>

        <!-- Empty State -->
        <div
          v-else-if="!filteredLogs.length"
          class="text-neutral-500 text-sm p-6 bg-[#131313] border border-neutral-800 rounded-lg text-center"
        >
          No logs found.
        </div>

        <!-- Logs Table -->
        <div v-else class="bg-[#131313] border border-neutral-800 rounded-lg overflow-x-auto">
          <table class="w-full text-xs min-w-[1100px]">
            <thead class="bg-[#1a1a1a] text-left text-neutral-400 sticky top-0 z-10">
              <tr>
                <th class="p-3 font-medium">Created</th>
                <th class="p-3 font-medium">Model</th>
                <th class="p-3 font-medium">API Key</th>
                <th class="p-3 font-medium">Code</th>
                <th class="p-3 font-medium">TTFT (ms)</th>
                <th class="p-3 font-medium">Latency</th>
                <th class="p-3 font-medium">Input Tokens</th>
                <th class="p-3 font-medium">Output Tokens</th>
                <th class="p-3 font-medium">Audio Seconds</th>
                <th class="p-3 font-medium">Request ID</th>
                <th class="p-3 font-medium">Error</th>
                <th class="p-3 font-medium">Latency Trend</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="log in filteredLogs"
                :key="log.requestId"
                class="border-t border-neutral-800 hover:bg-[#2d2d2d] transition-colors"
              >
                <td class="p-3">{{ formatDate(log.created) }}</td>
                <td class="p-3">{{ log.model || 'N/A' }}</td>
                <td class="p-3">{{ log.apiKey || 'N/A' }}</td>
                <td
                  class="p-3"
                  :class="{
                    'text-red-500': log.code >= 400,
                    'text-green-500': log.code < 400
                  }"
                >
                  {{ log.code || 'N/A' }}
                </td>
                <td class="p-3">{{ log.ttft ? `${log.ttft} ms` : 'N/A' }}</td>
                <td class="p-3">{{ log.latency ? `${log.latency} ms` : 'N/A' }}</td>
                <td class="p-3">{{ log.inputTokens ?? 'N/A' }}</td>
                <td class="p-3">{{ log.outputTokens ?? 'N/A' }}</td>
                <td class="p-3">{{ log.audioSeconds ?? 'N/A' }}</td>
                <td class="p-3">{{ log.requestId || 'N/A' }}</td>
                <td class="p-3 text-red-500">{{ log.error || 'None' }}</td>
                <td class="p-3">
                  <div class="w-24 h-12">
                    <LineChart
                      :chart-data="getMiniChartData(log.latency)"
                      :chart-options="miniChartOptions"
                    />
                  </div>
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
import { ref, computed, onMounted } from 'vue'
import Header from '~/components/Header.vue'
import Sidebar from '~/components/Sidebar_Dash.vue'
import LineChart from '~/components/LineChart.vue'
import { useLogStore } from '~/stores/dashboard'

const showErrorsOnly = ref(false)
const loading = ref(true)
const logStore = useLogStore()

// Fetch logs
onMounted(async () => {
  try {
    const data = await $fetch('http://localhost:8000/dash/log')
    logStore.setLogs(data)
  } catch (error) {
    console.error('Error fetching logs:', error)
    logStore.clearLogs()
  } finally {
    loading.value = false
  }
})

// Filter logs
const filteredLogs = computed(() =>
  showErrorsOnly.value ? logStore.errorLogs : logStore.logs
)

// Format time with local offset (+3 for you)
const formatDate = (date: string | Date) => {
  const d = new Date(date)
  d.setHours(d.getHours() + 5) // Apply UTC+3
  return d.toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

// Download logs
const downloadLogs = () => {
  const json = JSON.stringify(filteredLogs.value, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'logs.json'
  a.click()
  URL.revokeObjectURL(url)
}

// Mini sparkline data
const getMiniChartData = (latency?: string | number) => {
  const value = Number(latency) || 0
  const data = [
    value * 0.6,
    value * 0.8,
    value,
    value * 1.2,
    value * 0.95
  ]
  return {
    labels: ['', '', '', '', ''],
    datasets: [
      {
        label: 'Latency',
        data,
        borderColor: '#a855f7',
        backgroundColor: 'rgba(168, 85, 247, 0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 1
      }
    ]
  }
}

// Chart options
const miniChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false }
  },
  scales: {
    x: { display: false },
    y: { display: false }
  },
  animation: { duration: 0 }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
}

th,
td {
  vertical-align: middle;
}

tr:hover {
  transition: background-color 0.3s;
}

input[type="checkbox"] {
  transition: background-color 0.3s, border-color 0.3s;
}
</style>
