<template>
  <div
    v-if="stats && Object.keys(stats.riders).length"
    class="bg-white rounded-lg shadow-sm p-6 mt-8 relative"
    :class="isFullscreen ? 'z-50 overflow-auto' : ''"
    :style="isFullscreen ? 'position:fixed;top:0;left:0;width:100vw;height:100vh' : ''"
  >
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-700">Rider Standings</h3>
      <button
        @click="toggleFullscreen"
        class="text-sm font-bold text-gray-500 hover:text-gray-700 cursor-pointer"
        :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
      >
        {{ isFullscreen ? '✕' : '⛶' }}
      </button>
    </div>

    <!-- Progress bars -->
    <div class="space-y-3 mb-6">
      <div v-for="rider in rankedRiders" :key="rider.id" class="flex items-center gap-3">
        <span class="w-16 text-sm font-medium truncate" :style="{ color: rider.textColor }">
          {{ rider.name }}
        </span>
        <div class="flex-1 bg-gray-100 rounded-full h-5 relative overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{
              width: (rider.stats.totalDistanceCapped / totalDistance * 100) + '%',
              backgroundColor: rider.color,
              minWidth: rider.stats.totalDistanceCapped > 0 ? '8px' : '0'
            }"
          />
          <span class="absolute inset-0 flex items-center justify-center text-xs font-mono"
                :class="rider.stats.totalDistanceCapped > totalDistance * 0.4 ? 'text-white' : 'text-gray-600'">
            {{ rider.stats.totalDistanceCapped }} km
          </span>
        </div>
        <span class="w-8 text-xs text-gray-400 text-right">#{{ rider.stats.place }}</span>
      </div>
    </div>

    <!-- Stats table -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-200">
            <th class="text-left py-2 pr-2 text-gray-500 font-medium">Stat</th>
            <th
              v-for="rider in rankedRiders"
              :key="rider.id"
              class="text-center py-2 px-2 font-medium"
              :style="{ color: rider.textColor }"
            >
              {{ rider.name }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Total (capped)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.totalDistanceCapped }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Daily avg (actual)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.dailyAverageActual }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Daily avg (capped)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.dailyAverageCapped }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Longest day</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.longestDay }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Best 3-day</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.bestThreeDayCombo }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Recent 5-day avg</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.recentFiveDayAverage }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Days &lt;3km</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.daysBelowThreeKm }}
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Remaining</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono">
              {{ r.stats.distanceRemaining }} km
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-gray-500">Est. finish</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono text-xs">
              {{ r.stats.estimatedFinishDate || '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Sparklines -->
    <div v-if="dailyLog.entries.length > 1" class="mt-6 border-t pt-4">
      <h4 class="text-sm font-semibold text-gray-600 mb-3">Daily Distance</h4>
      <div class="space-y-2">
        <div v-for="rider in rankedRiders" :key="rider.id" class="flex items-center gap-3">
          <span class="w-16 text-xs truncate" :style="{ color: rider.textColor }">{{ rider.name }}</span>
          <svg class="flex-1 h-6" :viewBox="`0 0 ${sparklineWidth} 24`" preserveAspectRatio="none">
            <polyline
              :points="sparklinePoints(rider.id)"
              fill="none"
              :stroke="rider.color"
              stroke-width="1.5"
              stroke-linejoin="round"
            />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onUnmounted } from 'vue'

const isFullscreen = ref(false)

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
}

function onKeydown(e) {
  if (e.key === 'Escape' && isFullscreen.value) {
    isFullscreen.value = false
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('keydown', onKeydown)
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))
}

function displayColor(hex) {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  if (luminance > 0.85) {
    return `rgb(${Math.round(r * 0.5)}, ${Math.round(g * 0.5)}, ${Math.round(b * 0.5)})`
  }
  return hex
}

import riderConfigJson from '~/data/riders/rider-config.json'
import statsJson from '~/data/riders/stats.json'
import dailyLogJson from '~/data/riders/daily-log.json'

const stats = statsJson
const riderConfig = riderConfigJson
const dailyLog = dailyLogJson
const totalDistance = riderConfig.totalDistance

const rankedRiders = computed(() => {
  return riderConfig.riders
    .map(r => ({
      ...r,
      textColor: displayColor(r.color),
      stats: stats.riders[r.id] || {},
    }))
    .sort((a, b) => (a.stats.place || 99) - (b.stats.place || 99))
})

const sparklineWidth = computed(() => Math.max(dailyLog.entries.length * 4, 100))

function sparklinePoints(riderId) {
  const entries = dailyLog.entries
  if (entries.length < 2) return ''

  const dists = entries.map(e => e.distances[riderId] || 0)
  const maxDist = Math.max(...dists, 1)
  const xStep = sparklineWidth.value / (entries.length - 1)

  return dists
    .map((d, i) => `${i * xStep},${24 - (d / maxDist) * 20}`)
    .join(' ')
}
</script>
