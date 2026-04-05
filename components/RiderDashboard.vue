<template>
  <div
    v-if="stats && Object.keys(stats.riders).length"
    class="bg-white rounded-lg shadow-sm mt-8 relative"
    :class="isFullscreen ? 'z-[9999] overflow-auto p-12 text-lg' : 'p-6 text-sm'"
    :style="isFullscreen ? 'position:fixed;top:0;left:0;width:100vw;height:100vh' : ''"
  >
    <DayCounter v-if="isFullscreen" class="mb-4" />
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 :class="isFullscreen ? 'text-2xl' : 'text-lg'" class="font-semibold text-stone-700">Rider Standings</h3>
        <p v-if="statsDate" class="text-xs text-stone-400">as of {{ formatStatsDate(statsDate) }}</p>
      </div>
      <button
        class="w-8 h-8 flex items-center justify-center rounded border text-lg font-bold cursor-pointer transition-colors"
        :class="isFullscreen ? 'bg-red-600 text-white border-red-600 hover:bg-red-700' : 'bg-stone-100 text-stone-500 border-stone-300 hover:bg-stone-200'"
        :title="isFullscreen ? 'Exit fullscreen' : 'Fullscreen'"
        @click="toggleFullscreen"
      >
        {{ isFullscreen ? '✕' : '⛶' }}
      </button>
    </div>

    <!-- Progress bars -->
    <div class="space-y-3 mb-6">
      <div v-for="rider in rankedRiders" :key="rider.id" class="flex items-center gap-3">
        <div class="w-24 flex items-center gap-1 shrink-0">
          <span class="text-sm font-medium truncate" :style="{ color: rider.textColor }">{{ rider.name }}</span>
          <JerseyIcon v-if="jerseys.yellow === rider.id" type="yellow" size="xs" title="Yellow Jersey" class="shrink-0" />
          <JerseyIcon v-if="jerseys.green === rider.id" type="green" size="xs" title="Green Jersey" class="shrink-0" />
          <JerseyIcon v-if="jerseys.polkaDot === rider.id" type="polkaDot" size="xs" title="Polka Dot Jersey" class="shrink-0" />
          <JerseyIcon v-if="jerseys.red === rider.id" type="red" size="xs" title="Lanterne Rouge" class="shrink-0" />
        </div>
        <div class="flex-1 bg-stone-100 rounded-full relative overflow-hidden" :class="isFullscreen ? 'h-8' : 'h-5'">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{
              width: (rider.stats.totalDistanceCapped / totalDistance * 100) + '%',
              backgroundColor: rider.color,
              minWidth: rider.stats.totalDistanceCapped > 0 ? '8px' : '0'
            }"
          />
          <span
class="absolute inset-0 flex items-center justify-center text-xs font-mono"
                :class="rider.stats.totalDistanceCapped > totalDistance * 0.4 ? 'text-white' : 'text-stone-600'">
            {{ rider.stats.totalDistanceCapped }} km
          </span>
        </div>
        <span class="w-8 text-xs text-stone-400 text-right">#{{ rider.stats.place }}</span>
      </div>
    </div>

    <!-- Classification standings -->
    <div v-if="hasPoints" class="grid grid-cols-2 gap-3 mb-6">
      <div class="bg-green-50 rounded-lg p-3 border border-green-200">
        <div class="flex items-center gap-2 mb-2">
          <JerseyIcon type="green" size="sm" />
          <span class="text-sm font-semibold text-green-800">Points</span>
        </div>
        <div class="space-y-1">
          <div v-for="r in sprintRanking" :key="r.id" class="flex items-center justify-between text-sm">
            <span :class="r.rank === 1 ? 'font-bold text-green-700' : 'text-stone-600'">{{ r.name }}</span>
            <span class="font-mono" :class="r.rank === 1 ? 'font-bold text-green-700' : 'text-stone-500'">{{ r.points }}</span>
          </div>
        </div>
      </div>
      <div class="bg-red-50 rounded-lg p-3 border border-red-200">
        <div class="flex items-center gap-2 mb-2">
          <JerseyIcon type="polkaDot" size="sm" />
          <span class="text-sm font-semibold text-red-800">KOM</span>
        </div>
        <div class="space-y-1">
          <div v-for="r in climbRanking" :key="r.id" class="flex items-center justify-between text-sm">
            <span :class="r.rank === 1 ? 'font-bold text-red-700' : 'text-stone-600'">{{ r.name }}</span>
            <span class="font-mono" :class="r.rank === 1 ? 'font-bold text-red-700' : 'text-stone-500'">{{ r.points }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats table -->
    <div class="overflow-x-auto">
      <table class="w-full" :class="isFullscreen ? 'text-xl' : 'text-sm'">
        <thead>
          <tr class="bg-amber-100 border-b border-stone-200">
            <th class="text-left py-2 pr-2 text-stone-600 font-medium">Stat</th>
            <th
              v-for="rider in rankedRiders"
              :key="rider.id"
              class="text-center font-medium border-l border-stone-200"
              :class="isFullscreen ? 'py-2 px-3' : 'py-1 px-1 text-xs'"
              :style="{ color: rider.textColor }"
            >
              <span
                v-if="isFullscreen"
                class="inline-flex items-center justify-center w-8 h-8 rounded-full text-base mb-1"
                :style="{ backgroundColor: rider.color }"
              >🚴</span>
              <br v-if="isFullscreen">
              {{ rider.name }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-stone-100 [&>tr:nth-child(even)]:bg-stone-50">
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Total (capped)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.totalDistanceCapped }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Daily avg (actual)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.dailyAverageActual }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Daily avg (capped)</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.dailyAverageCapped }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Longest day</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.longestDay }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Best 3-day</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.bestThreeDayCombo }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Recent 5-day avg</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.recentFiveDayAverage }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Days &lt;3km</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.daysBelowThreeKm }}
            </td>
          </tr>
          <tr v-if="hasPoints">
            <td class="py-1.5 pr-2 text-stone-500">Sprint pts</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              <span :class="jerseys.green === r.id ? 'text-green-600 font-bold' : ''">{{ riderPoints(r.id).sprintPoints }}</span>
            </td>
          </tr>
          <tr v-if="hasPoints">
            <td class="py-1.5 pr-2 text-stone-500">Climb pts</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              <span :class="jerseys.polkaDot === r.id ? 'text-red-600 font-bold' : ''">{{ riderPoints(r.id).climbPoints }}</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Remaining</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center font-mono border-l border-stone-200" :class="isFullscreen ? 'py-1.5 px-3' : 'py-1 px-1 text-xs'">
              {{ r.stats.distanceRemaining }}<br><span class="text-stone-400">km</span>
            </td>
          </tr>
          <tr>
            <td class="py-1.5 pr-2 text-stone-500">Est. finish</td>
            <td v-for="r in rankedRiders" :key="r.id" class="text-center py-1.5 px-2 font-mono text-xs">
              <template v-if="r.stats.estimatedFinishDate">
                <span class="text-stone-400 block" :class="isFullscreen ? 'text-base' : 'text-[0.65rem]'" style="line-height:1">{{ formatFinishMonth(r.stats.estimatedFinishDate) }}</span>
                <span class="block" :class="isFullscreen ? 'text-2xl' : ''">{{ formatFinishDay(r.stats.estimatedFinishDate) }}</span>
              </template>
              <template v-else>-</template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Sparklines -->
    <div v-if="dailyLog.entries.length > 1" class="mt-6 border-t pt-4">
      <h4 class="text-sm font-semibold text-stone-600 mb-3">Daily Distance</h4>
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
      <div class="flex items-center gap-3 mt-1">
        <span class="w-16"/>
        <div class="flex-1 flex justify-between text-[9px] text-stone-400">
          <span v-for="label in sparklineDateLabels" :key="label">{{ label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onUnmounted } from 'vue'

import riderConfigJson from '~/data/riders/rider-config.json'
import statsJson from '~/data/riders/stats.json'
import dailyLogJson from '~/data/riders/daily-log.json'

const props = defineProps({
  snapshot: { type: Object, default: null },
})

const isFullscreen = ref(false)

const statsDate = computed(() => stats.asOf || null)

function formatStatsDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric'
  })
}

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

const riderConfig = riderConfigJson
const stats = props.snapshot?.stats || statsJson
const dailyLog = props.snapshot?.log || dailyLogJson
const totalDistance = riderConfig.totalDistance

let pointsData = props.snapshot?.points || { riders: {} }
if (!props.snapshot) {
  try {
    pointsData = await import('~/data/riders/points.json').then(m => m.default || m)
  } catch {
    // points.json may not exist yet
  }
}

const hasPoints = computed(() =>
  Object.values(pointsData.riders).some(r => r.totalPoints > 0)
)

function riderPoints(riderId) {
  return pointsData.riders[riderId] || { sprintPoints: 0, climbPoints: 0, totalPoints: 0 }
}

const sprintRanking = computed(() => {
  return rankedRiders.value
    .map((r, _i) => ({
      id: r.id,
      name: r.name,
      points: riderPoints(r.id).sprintPoints,
    }))
    .sort((a, b) => b.points - a.points)
    .map((r, i) => ({ ...r, rank: i + 1 }))
})

const climbRanking = computed(() => {
  return rankedRiders.value
    .map((r, _i) => ({
      id: r.id,
      name: r.name,
      points: riderPoints(r.id).climbPoints,
    }))
    .sort((a, b) => b.points - a.points)
    .map((r, i) => ({ ...r, rank: i + 1 }))
})

const jerseys = computed(() => {
  const riders = rankedRiders.value
  if (!riders.length) return {}

  // Track which riders already have a more prestigious jersey
  const taken = new Set()

  // Yellow: place 1 (most prestigious - assigned first)
  const yellow = riders[0]?.id || null
  if (yellow) taken.add(yellow)

  // Green: highest sprint points (second most prestigious)
  // If the leader already wears yellow, next rider gets it
  let green = null
  if (hasPoints.value) {
    const sprintSorted = [...riders].sort((a, b) =>
      riderPoints(b.id).sprintPoints - riderPoints(a.id).sprintPoints
    )
    for (const r of sprintSorted) {
      if (riderPoints(r.id).sprintPoints > 0 && !taken.has(r.id)) {
        green = r.id
        taken.add(r.id)
        break
      }
    }
  }

  // Polka dot: highest climb points (third most prestigious)
  let polkaDot = null
  if (hasPoints.value) {
    const climbSorted = [...riders].sort((a, b) =>
      riderPoints(b.id).climbPoints - riderPoints(a.id).climbPoints
    )
    for (const r of climbSorted) {
      if (riderPoints(r.id).climbPoints > 0 && !taken.has(r.id)) {
        polkaDot = r.id
        taken.add(r.id)
        break
      }
    }
  }

  // Red: last place (least prestigious - only if not already wearing another jersey)
  let red = null
  if (riders.length > 1) {
    const lastRider = riders[riders.length - 1]?.id
    if (lastRider && !taken.has(lastRider)) {
      red = lastRider
    }
  }

  return { yellow, green, polkaDot, red }
})

const rankedRiders = computed(() => {
  return riderConfig.riders
    .map(r => ({
      ...r,
      textColor: displayColor(r.color),
      stats: stats.riders[r.id] || {},
    }))
    .sort((a, b) => (a.stats.place || 99) - (b.stats.place || 99))
})

function formatFinishMonth(dateStr) {
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-US', { month: 'short' })
}

function formatFinishDay(dateStr) {
  return parseInt(dateStr.slice(8))
}

const sparklineWidth = computed(() => Math.max(dailyLog.entries.length * 4, 100))

const sparklineDateLabels = computed(() => {
  const entries = dailyLog.entries
  if (entries.length < 2) return []
  const maxLabels = 5
  const step = Math.max(1, Math.floor(entries.length / (maxLabels - 1)))
  const labels = []
  for (let i = 0; i < entries.length; i += step) {
    const d = entries[i].date
    labels.push(d.slice(5)) // MM-DD
  }
  const last = entries[entries.length - 1].date.slice(5)
  if (labels[labels.length - 1] !== last) labels.push(last)
  return labels
})

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
