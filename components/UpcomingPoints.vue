<template>
  <div v-if="points.length" class="bg-white rounded-lg shadow-sm p-6 mt-8">
    <h3 class="text-lg font-semibold text-stone-700 mb-3">Coming Up Next</h3>
    <p class="text-sm text-stone-500 mb-4">Points available in the next segment:</p>
    <div class="space-y-2">
      <div v-for="pt in points" :key="pt.name" class="flex items-center justify-between text-sm">
        <div class="flex items-center gap-2">
          <span v-if="pt.type === 'sprint'" class="text-green-600 font-semibold">Sprint</span>
          <span v-else class="text-red-600 font-semibold">{{ formatCategory(pt.category) }}</span>
          <span class="text-stone-700">{{ pt.name }}</span>
          <span class="text-stone-400 text-xs">km {{ pt.km }}</span>
        </div>
        <div class="font-mono text-stone-500">
          {{ pt.points.filter(p => p > 0).join('/') }} pts
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

import pointsConfig from '~/data/competition/points-config.json'

const props = defineProps({
  segment: { type: Number, required: true },
})

function formatCategory(cat) {
  if (cat === 'HC') return 'HC'
  return `Cat ${cat}`
}

const nextSegment = computed(() => props.segment + 1)

const points = computed(() => {
  const sprints = pointsConfig.sprints.filter(s => s.segment === nextSegment.value)
  const climbs = pointsConfig.climbs.filter(c => c.segment === nextSegment.value)
  return [...sprints.map(s => ({ ...s, type: 'sprint' })), ...climbs.map(c => ({ ...c, type: 'climb' }))]
    .sort((a, b) => a.km - b.km)
})
</script>
