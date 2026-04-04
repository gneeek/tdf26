<template>
  <div v-if="summary" class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Power Stats</h3>
    <p class="text-xs text-stone-400 mb-4">Reference: 70kg rider + 8kg bike, CdA 0.35, Crr 0.005</p>

    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
      <div class="text-center p-3 bg-stone-50 rounded">
        <div class="text-xl font-bold text-stone-700">{{ summary.avg_gradient }}%</div>
        <div class="text-xs text-stone-500">Avg Gradient</div>
      </div>
      <div class="text-center p-3 bg-stone-50 rounded">
        <div class="text-xl font-bold text-red-700">{{ summary.max_gradient }}%</div>
        <div class="text-xs text-stone-500">Max Gradient</div>
      </div>
      <div class="text-center p-3 bg-stone-50 rounded">
        <div class="text-xl font-bold text-correze-green">+{{ summary.elevation_gain }}m</div>
        <div class="text-xs text-stone-500">Elevation Gain</div>
      </div>
      <div class="text-center p-3 bg-stone-50 rounded">
        <div class="text-xl font-bold text-blue-600">-{{ summary.elevation_loss }}m</div>
        <div class="text-xs text-stone-500">Elevation Loss</div>
      </div>
      <div class="text-center p-3 bg-correze-red/5 rounded col-span-2 md:col-span-1">
        <div class="text-xl font-bold text-correze-red">{{ summary.avg_power_35kmh }}W</div>
        <div class="text-xs text-stone-500">Avg Power @35km/h</div>
      </div>
    </div>

    <div class="mt-4 border-t pt-4">
      <h4 class="text-sm font-semibold text-stone-600 mb-2 bg-amber-100 -mx-6 px-6 py-1.5">Estimated Time</h4>
      <div class="flex gap-4 text-sm">
        <div class="flex-1 text-center">
          <div class="font-mono font-bold text-stone-600">{{ summary.estimated_time_30kmh }}</div>
          <div class="text-xs text-stone-400">{{ timeUnit(summary.estimated_time_30kmh) }}</div>
          <div class="text-xs text-stone-400">@30 km/h</div>
        </div>
        <div class="flex-1 text-center">
          <div class="font-mono font-bold text-correze-red">{{ summary.estimated_time_35kmh }}</div>
          <div class="text-xs text-stone-400">{{ timeUnit(summary.estimated_time_35kmh) }}</div>
          <div class="text-xs text-stone-400">@35 km/h</div>
        </div>
        <div class="flex-1 text-center">
          <div class="font-mono font-bold text-stone-600">{{ summary.estimated_time_40kmh }}</div>
          <div class="text-xs text-stone-400">{{ timeUnit(summary.estimated_time_40kmh) }}</div>
          <div class="text-xs text-stone-400">@40 km/h</div>
        </div>
        <div class="flex-1 text-center">
          <div class="font-mono font-bold text-stone-600">{{ summary.estimated_time_50kmh || '-' }}</div>
          <div class="text-xs text-stone-400">{{ timeUnit(summary.estimated_time_50kmh) }}</div>
          <div class="text-xs text-stone-400">@50 km/h</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  elevationData: { type: Object, default: null }
})

function timeUnit(timeStr) {
  if (!timeStr) return ''
  const mins = parseInt(timeStr.split(':')[0])
  return mins >= 60 ? 'hr:min' : 'min:sec'
}

const summary = computed(() => props.elevationData?.summary || null)
</script>
