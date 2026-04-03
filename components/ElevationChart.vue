<template>
  <div
    class="bg-white rounded-lg shadow-sm relative"
    :class="isFullscreen ? 'z-[9999] overflow-hidden p-12' : 'p-4'"
    :style="isFullscreen ? 'position:fixed;top:0;left:0;width:100vw;height:100vh' : ''"
  >
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-gray-700">Elevation Profile</h3>
      <div class="flex items-center gap-2">
        <button
          v-if="isZoomed"
          @click="resetZoom"
          class="text-xs text-blue-600 hover:underline cursor-pointer"
        >
          Reset zoom
        </button>
        <button
          @click="toggleFullscreen"
          class="w-8 h-8 flex items-center justify-center rounded border text-lg font-bold cursor-pointer transition-colors"
          :class="isFullscreen ? 'bg-red-600 text-white border-red-600 hover:bg-red-700' : 'bg-gray-100 text-gray-500 border-gray-300 hover:bg-gray-200'"
          :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
        >
          {{ isFullscreen ? '✕' : '⛶' }}
        </button>
      </div>
    </div>
    <div v-if="chartData" :class="isFullscreen ? 'h-[calc(100vh-160px)]' : 'h-[250px]'">
      <Line ref="chartRef" :data="chartData" :options="chartOptions" />
    </div>
    <p v-else class="text-gray-400 italic text-sm">Elevation data not available.</p>
    <p v-if="chartData" class="text-xs text-gray-400 mt-2">Scroll to zoom, drag to pan. Double-click to reset.</p>
  </div>
</template>

<script setup>
import { computed, ref, nextTick, onMounted, onUnmounted } from 'vue'
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

const zoomReady = ref(false)
onMounted(async () => {
  const mod = await import('chartjs-plugin-zoom')
  ChartJS.register(mod.default)
  zoomReady.value = true
})

const props = defineProps({
  elevationData: { type: Object, default: null }
})

const chartRef = ref(null)
const isFullscreen = ref(false)
const isZoomed = ref(false)

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
  nextTick(() => {
    setTimeout(() => {
      if (chartRef.value?.chart) chartRef.value.chart.resize()
    }, 100)
  })
}

function resetZoom() {
  if (chartRef.value?.chart) {
    chartRef.value.chart.resetZoom()
    isZoomed.value = false
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && isFullscreen.value) {
    isFullscreen.value = false
    nextTick(() => {
      setTimeout(() => {
        if (chartRef.value?.chart) chartRef.value.chart.resize()
      }, 100)
    })
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('keydown', onKeydown)
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))
}

function gradientColor(grade) {
  const g = Math.abs(grade)
  if (g < 3) return 'rgba(34, 197, 94, 0.6)'
  if (g < 6) return 'rgba(234, 179, 8, 0.6)'
  if (g < 9) return 'rgba(249, 115, 22, 0.6)'
  return 'rgba(239, 68, 68, 0.6)'
}

const chartData = computed(() => {
  if (!props.elevationData) return null
  const { distance, elevation, gradient } = props.elevationData

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
    },
    zoom: {
      pan: {
        enabled: true,
        mode: 'x'
      },
      zoom: {
        wheel: { enabled: true },
        pinch: { enabled: true },
        mode: 'x',
        onZoom: () => { isZoomed.value = true },
        onZoomComplete: () => { isZoomed.value = true }
      }
    }
  },
  scales: {
    x: {
      title: { display: true, text: 'Distance (km)' },
      ticks: { maxTicksLimit: 8 }
    },
    y: {
      title: { display: true, text: 'Elevation (m)' },
      beginAtZero: false
    }
  }
}))
</script>
