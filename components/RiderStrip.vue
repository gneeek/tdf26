<template>
  <div v-if="rankedRiders.length" class="bg-white rounded-lg shadow-sm p-3 sm:p-4 mb-6">
    <div class="flex items-baseline justify-between mb-2">
      <h2 class="text-sm font-semibold text-stone-700">Standings</h2>
      <a href="#rider-dashboard" class="text-xs text-correze-red font-semibold hover:underline">See full standings &darr;</a>
    </div>
    <div class="space-y-1">
      <div v-for="rider in rankedRiders" :key="rider.id" class="flex items-center gap-2">
        <span class="w-16 sm:w-20 text-xs sm:text-sm font-medium truncate" :style="{ color: rider.textColor }">{{ rider.name }}</span>
        <div class="flex-1 bg-stone-100 rounded-full h-2.5 sm:h-3 relative overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{
              width: (rider.distance / totalDistance * 100) + '%',
              backgroundColor: rider.color,
              minWidth: rider.distance > 0 ? '6px' : '0'
            }"
          />
        </div>
        <span class="w-14 text-xs text-stone-500 text-right font-mono">{{ rider.distance }} km</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

import riderConfigJson from '~/data/riders/rider-config.json'
import statsJson from '~/data/riders/stats.json'

const props = defineProps({
  snapshot: { type: Object, default: null },
})

const stats = props.snapshot?.stats || statsJson
const totalDistance = riderConfigJson.totalDistance

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

const rankedRiders = computed(() => {
  return riderConfigJson.riders
    .map(r => {
      const s = stats?.riders?.[r.id] || {}
      return {
        id: r.id,
        name: r.name,
        color: r.color,
        textColor: displayColor(r.color),
        distance: s.totalDistanceCapped ?? 0,
        place: s.place ?? 99,
      }
    })
    .sort((a, b) => a.place - b.place)
})
</script>
