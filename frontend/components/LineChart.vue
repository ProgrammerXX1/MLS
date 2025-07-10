<!-- components/LineChart.vue -->
<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  LineElement, PointElement,
  LinearScale, CategoryScale,
  Filler,
} from 'chart.js'

ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, PointElement,
  LinearScale, CategoryScale,
  Filler
)

defineProps<{
  chartData: any
  chartOptions: any
}>()
</script>
