<template>
  <div class="bg-white rounded-lg shadow-sm p-4">
    <h3 class="text-lg font-semibold text-gray-700 mb-3">Elevation Profile</h3>
    <div v-if="chartData" class="h-[250px]">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <p v-else class="text-gray-400 italic text-sm">Elevation data not available.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip
} from 'chart.js'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip)

const props = defineProps({
  elevationData: { type: Object, default: null }
})

function gradientColor(grade) {
  const g = Math.abs(grade)
  if (g < 3) return 'rgba(34, 197, 94, 0.6)'   // green
  if (g < 6) return 'rgba(234, 179, 8, 0.6)'    // yellow
  if (g < 9) return 'rgba(249, 115, 22, 0.6)'   // orange
  return 'rgba(239, 68, 68, 0.6)'                // red
}

const chartData = computed(() => {
  if (!props.elevationData) return null
  const { distance, elevation, gradient } = props.elevationData

  // Create segment colors based on gradient
  const segmentColors = gradient.map(g => gradientColor(g))

  return {
    labels: distance.map(d => d.toFixed(1)),
    datasets: [{
      label: 'Elevation (m)',
      data: elevation,
      fill: true,
      borderColor: '#8B2500',
      borderWidth: 2,
      backgroundColor: (ctx) => {
        if (!ctx.chart.chartArea) return 'rgba(139, 37, 0, 0.1)'
        const chart = ctx.chart
        const { ctx: canvasCtx, chartArea: { top, bottom } } = chart
        const grad = canvasCtx.createLinearGradient(0, top, 0, bottom)
        grad.addColorStop(0, 'rgba(139, 37, 0, 0.3)')
        grad.addColorStop(1, 'rgba(139, 37, 0, 0.02)')
        return grad
      },
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: '#8B2500',
      tension: 0.3
    }]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: 'index'
  },
  plugins: {
    tooltip: {
      callbacks: {
        title: (items) => {
          const idx = items[0].dataIndex
          return `Km ${props.elevationData.distance[idx].toFixed(1)}`
        },
        label: (item) => {
          const idx = item.dataIndex
          const elev = props.elevationData.elevation[idx]
          const grad = props.elevationData.gradient[idx]
          const power = props.elevationData.power_35kmh?.[idx]
          const lines = [
            `Elevation: ${elev}m`,
            `Gradient: ${grad.toFixed(1)}%`
          ]
          if (power) lines.push(`Est. power @35km/h: ${power}W`)
          return lines
        }
      }
    }
  },
  scales: {
    x: {
      title: { display: true, text: 'Distance (km)' },
      ticks: {
        maxTicksLimit: 8
      }
    },
    y: {
      title: { display: true, text: 'Elevation (m)' },
      beginAtZero: false
    }
  }
}))
</script>
