<template>
  <div
    class="bg-white rounded-lg shadow-sm relative"
    :class="isFullscreen ? 'z-[1200] overflow-hidden p-12' : 'p-4'"
    :style="isFullscreen ? 'position:fixed;top:0;left:0;width:100vw;height:100vh;margin:0' : ''"
  >
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-stone-700">Elevation Profile</h3>
      <div class="flex items-center gap-2">
        <button
          class="w-7 h-7 flex items-center justify-center rounded border text-sm font-bold cursor-pointer bg-stone-100 text-stone-500 border-stone-300 hover:bg-stone-200"
          title="Zoom in"
          @click="zoomIn"
        >
          +
        </button>
        <button
          class="w-7 h-7 flex items-center justify-center rounded border text-sm font-bold cursor-pointer bg-stone-100 text-stone-500 border-stone-300 hover:bg-stone-200"
          title="Zoom out"
          @click="zoomOut"
        >
          -
        </button>
        <button
          v-if="isZoomed"
          class="text-xs text-blue-600 hover:underline cursor-pointer"
          @click="resetZoom"
        >
          Reset
        </button>
        <button
          class="w-8 h-8 flex items-center justify-center rounded border text-lg font-bold cursor-pointer transition-colors"
          :class="isFullscreen ? 'bg-red-600 text-white border-red-600 hover:bg-red-700' : 'bg-stone-100 text-stone-500 border-stone-300 hover:bg-stone-200'"
          :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
          @click="toggleFullscreen"
        >
          {{ isFullscreen ? '✕' : '⛶' }}
        </button>
      </div>
    </div>
    <div v-if="chartData" :class="isFullscreen ? 'h-[calc(100vh-160px)]' : 'h-[250px]'">
      <Line ref="chartRef" :data="chartData" :options="chartOptions" />
    </div>
    <p v-else class="text-stone-400 italic text-sm">Elevation data not available.</p>
    <p v-if="chartData" class="text-xs text-stone-400 mt-2">Scroll to zoom, drag to pan. Double-click to reset.</p>
  </div>
</template>

<script setup>
import { computed, ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useJerseys, jerseyEmoji } from '~/composables/useJerseys'
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
import annotationPlugin from 'chartjs-plugin-annotation'
import { townKmPositions } from '~/data/town-positions'
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip, annotationPlugin)

const zoomReady = ref(false)

// Custom plugin to draw town/climb labels directly on canvas
const labelPlugin = {
  id: 'elevationLabels',
  afterDraw(chart) {
    const ctx = chart.ctx
    const xScale = chart.scales.x
    const yScale = chart.scales.y
    const dataset = chart.data.datasets[0]
    const labels = chart.options.plugins.elevationLabels?.items || []

    ctx.save()
    for (const label of labels) {
      const xPixel = xScale.getPixelForValue(label.xIdx)
      if (xPixel === undefined || isNaN(xPixel)) continue

      // Get the elevation value at this index and position label relative to it
      const elevation = dataset.data[label.xIdx]
      if (elevation === undefined) continue
      const elevPixel = yScale.getPixelForValue(elevation)

      // Draw emoji centered on the elevation point
      const emojiY = label.type === 'climb'
        ? elevPixel - 8
        : elevPixel + 8
      ctx.font = '12px sans-serif'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(label.emoji, xPixel, emojiY)

      // Draw name below/above the emoji
      const nameY = label.type === 'climb'
        ? emojiY - 14
        : emojiY + 14 + (label.extraOffset || 0)
      ctx.font = '10px sans-serif'
      ctx.textBaseline = 'middle'
      ctx.fillStyle = label.color
      ctx.fillText(label.name, xPixel, nameY)
    }
    ctx.restore()
  }
}

ChartJS.register(labelPlugin)

onMounted(async () => {
  const zoomMod = await import('chartjs-plugin-zoom')
  ChartJS.register(zoomMod.default)
  zoomReady.value = true
})

const props = defineProps({
  elevationData: { type: Object, default: null },
  segments: { type: Array, default: () => [] },
  currentSegment: { type: Number, default: 0 },
  riderStats: { type: Object, default: null },
  riderConfig: { type: Object, default: null },
  riderPoints: { type: Object, default: null },
})

// Jersey assignments via shared composable
const elevRankedRiders = computed(() => {
  if (!props.riderStats?.riders || !props.riderConfig?.riders) return []
  return [...props.riderConfig.riders]
    .map(r => ({ ...r, stats: props.riderStats.riders[r.id] || {} }))
    .sort((a, b) => (a.stats.place || 99) - (b.stats.place || 99))
})

function elevGetPoints(riderId) {
  const pts = props.riderPoints?.riders || {}
  return pts[riderId] || { sprintPoints: 0, climbPoints: 0, totalPoints: 0 }
}

const elevHasPoints = computed(() =>
  Object.values(props.riderPoints?.riders || {}).some(r => r.totalPoints > 0)
)

const jerseys = useJerseys(elevRankedRiders, elevGetPoints, elevHasPoints)

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

function zoomIn() {
  if (chartRef.value?.chart) {
    chartRef.value.chart.zoom(1.5)
    isZoomed.value = true
  }
}

function zoomOut() {
  if (chartRef.value?.chart) {
    chartRef.value.chart.zoom(0.67)
  }
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

const chartData = computed(() => {
  if (!props.elevationData) return null
  const { distance, elevation } = props.elevationData

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

// townKmPositions is imported from ~/data/town-positions (shared with StageDetails.vue)

// Known climb summit positions (km_end from KNOWN_CLIMBS)
const climbSummitKm = {
  'Cote de Malemort': 5,
  'Puy Boubou': 30.6,
  'Cote de Lagleygeolle': 43.2, 'Côte de Lagleygeolle': 43.2,
  'Cote de Miel': 51.1, 'Côte de Miel': 51.1,
  'Cote des Naves': 74.8, 'Côte des Naves': 74.8,
  'Puy de Lachaud': 85.6,
  'Suc au May': 104.8,
  'Cote de la Croix de Pey': 127, 'Côte de la Croix de Pey': 127,
  'Mont Bessou': 153,
  'Cote des Gardes': 167.2, 'Côte des Gardes': 167.2,
}

function buildLabelItems() {
  if (!props.segments.length || !props.elevationData) return []

  const distances = props.elevationData.distance
  const items = []
  const placed = new Set()
  let idx = 0

  // For individual segments, offset km positions
  const kmOffset = props.currentSegment > 0
    ? (props.segments.find(s => s.segment === props.currentSegment)?.km_start || 0)
    : 0

  for (const seg of props.segments) {
    if (props.currentSegment > 0 && seg.segment !== props.currentSegment) continue

    if (seg.towns?.length) {
      for (const town of seg.towns) {
        if (placed.has(town)) continue
        placed.add(town)
        // Use known km position if available, otherwise segment midpoint
        const townKm = (townKmPositions[town] ?? ((seg.km_start + seg.km_end) / 2)) - kmOffset
        // Find closest x index
        let bestIdx = 0
        let bestDist = Infinity
        for (let i = 0; i < distances.length; i++) {
          const d = Math.abs(distances[i] - townKm)
          if (d < bestDist) { bestDist = d; bestIdx = i }
        }
        items.push({
          xIdx: bestIdx,
          emoji: '🏘️',
          name: town,
          color: '#2563eb',
          type: 'town',
          extraOffset: idx === 0 ? 12 : 0
        })
        idx++
      }
    }
    if (seg.climbs?.length) {
      for (const climb of seg.climbs) {
        if (placed.has(climb)) continue
        placed.add(climb)
        // Use known summit km if available, otherwise find peak in segment range
        const summitKm = climbSummitKm[climb]
        let peakIdx = 0
        if (summitKm != null) {
          const targetKm = summitKm - kmOffset
          let bestDist = Infinity
          for (let i = 0; i < distances.length; i++) {
            const d = Math.abs(distances[i] - targetKm)
            if (d < bestDist) { bestDist = d; peakIdx = i }
          }
        } else {
          const elevations = props.elevationData.elevation
          let peakElev = -Infinity
          for (let i = 0; i < distances.length; i++) {
            if (distances[i] >= seg.km_start - kmOffset && distances[i] <= seg.km_end - kmOffset) {
              if (elevations[i] > peakElev) {
                peakElev = elevations[i]
                peakIdx = i
              }
            }
          }
        }
        items.push({
          xIdx: peakIdx,
          emoji: '⛰️',
          name: climb,
          color: '#dc2626',
          type: 'climb',
          extraOffset: 0
        })
        idx++
      }
    }
  }
  return items
}

function getJerseyEmoji(riderId) {
  return jerseyEmoji(jerseys.value, riderId)
}

function buildRiderAnnotations() {
  if (!props.riderStats?.riders || !props.riderConfig?.riders || !props.elevationData) return {}

  const distances = props.elevationData.distance
  const kmOffset = props.currentSegment > 0
    ? (props.segments.find(s => s.segment === props.currentSegment)?.km_start || 0)
    : 0

  // Collect rider positions first to detect overlaps
  const riderPositions = []
  for (const rider of props.riderConfig.riders) {
    const stats = props.riderStats.riders[rider.id]
    if (!stats || stats.totalDistanceCapped == null) continue

    const riderKm = stats.totalDistanceCapped - kmOffset
    if (riderKm < 0 || riderKm > distances[distances.length - 1]) continue

    let bestIdx = 0
    let bestDist = Infinity
    for (let i = 0; i < distances.length; i++) {
      const d = Math.abs(distances[i] - riderKm)
      if (d < bestDist) { bestDist = d; bestIdx = i }
    }

    riderPositions.push({ rider, bestIdx, riderKm })
  }

  // Sort by position for consistent staggering
  riderPositions.sort((a, b) => a.riderKm - b.riderKm)

  // Stagger labels vertically using position percentage
  const labelPositions = ['5%', '20%', '35%', '50%']
  const annotations = {}
  riderPositions.forEach((rp, i) => {
    const jersey = getJerseyEmoji(rp.rider.id)
    const labelText = jersey ? `${jersey} ${rp.rider.name}` : rp.rider.name

    annotations[`rider-${rp.rider.id}`] = {
      type: 'line',
      xMin: rp.bestIdx,
      xMax: rp.bestIdx,
      borderColor: rp.rider.color,
      borderWidth: 2,
      borderDash: [4, 2],
      label: {
        display: true,
        content: labelText,
        position: labelPositions[i % labelPositions.length],
        backgroundColor: rp.rider.color,
        color: 'white',
        font: { size: 10, weight: 'bold' },
        padding: { top: 2, bottom: 2, left: 4, right: 4 },
        borderRadius: 3,
        xAdjust: 8,
      }
    }
  })
  return annotations
}

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
    },
    annotation: {
      annotations: buildRiderAnnotations()
    },
    elevationLabels: {
      items: buildLabelItems()
    },
  },
  scales: {
    x: {
      title: { display: true, text: 'Distance (km)' },
      ticks: {
        maxTicksLimit: 8,
        callback: function(value, index, ticks) {
          // Always show last tick
          if (index === ticks.length - 1 && props.elevationData) {
            const dists = props.elevationData.distance
            return dists[dists.length - 1].toFixed(0) + ' km'
          }
          return this.getLabelForValue(value)
        }
      }
    },
    y: {
      title: { display: true, text: 'Elevation (m)' },
      beginAtZero: false
    }
  }
}))
</script>
