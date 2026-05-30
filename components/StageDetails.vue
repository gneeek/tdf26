<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Stage Details</h3>

    <div class="mb-5">
      <h4 class="text-sm font-semibold text-stone-600 mb-2 bg-amber-100 -mx-6 px-6 py-1.5">Towns</h4>
      <div class="space-y-1">
        <div v-for="town in towns" :key="town.name" class="flex justify-between text-sm" :class="isPassed(town.km) ? 'bg-stone-50 rounded px-1 -mx-1' : ''">
          <span :class="isPassed(town.km) ? 'text-correze-red-400' : 'text-stone-700'">{{ town.name }}</span>
          <span class="font-mono" :class="isPassed(town.km) ? 'text-correze-red-300' : 'text-stone-400'">km {{ town.km }} &middot; {{ town.elevation }}m</span>
        </div>
      </div>
    </div>

    <div>
      <h4 class="text-sm font-semibold text-stone-600 mb-2 bg-amber-100 -mx-6 px-6 py-1.5">Climbs</h4>
      <div class="space-y-1">
        <div v-for="climb in climbs" :key="climb.name" class="flex justify-between text-sm" :class="isPassed(climb.km) ? 'bg-stone-50 rounded px-1 -mx-1' : ''">
          <span :class="isPassed(climb.km) ? 'text-correze-red-400' : 'text-stone-700'">{{ climb.name }}</span>
          <span class="font-mono" :class="isPassed(climb.km) ? 'text-correze-red-300' : 'text-stone-400'">km {{ climb.km }} &middot; {{ climb.gradient }}%</span>
        </div>
      </div>
    </div>

    <div class="mt-4 pt-3 border-t border-stone-100 text-xs text-stone-400">
      {{ Math.round(totals.totalDistance) }} km &middot; {{ totals.uniqueCategorizedClimbs.length }} climbs &middot; +{{ totals.totalElevationGain.toLocaleString('en-US') }}m elevation
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'
import { townKmPositions } from '~/data/town-positions'
import { deriveTotals, CATEGORIZED_CLIMBS, CLIMB_DISPLAY } from '~/utils/stage-totals'

const totals = deriveTotals(segmentsJson)

const props = defineProps({
  currentKm: { type: Number, default: 0 },
})

function isPassed(km) {
  return props.currentKm > 0 && Number(km) < props.currentKm
}

// Climb gradient + summit km come from CLIMB_DISPLAY (derived from
// points-config.json by canonical name) — no second copy to drift. See
// utils/stage-totals.ts.

// Extract towns with their approximate km and elevation
const townSet = new Map()
for (const seg of segmentsJson) {
  if (seg.towns?.length) {
    for (const town of seg.towns) {
      if (!townSet.has(town)) {
        const km = townKmPositions[town] ?? seg.km_start
        townSet.set(town, {
          name: town,
          km: km.toFixed(1),
          elevation: seg.min_elevation
        })
      }
    }
  }
}
const towns = Array.from(townSet.values())

// Extract climbs with first appearance km
const climbSet = new Map()
for (const seg of segmentsJson) {
  if (seg.climbs?.length) {
    for (const climb of seg.climbs) {
      if (!CATEGORIZED_CLIMBS.has(climb)) continue
      if (!climbSet.has(climb)) {
        const data = CLIMB_DISPLAY.get(climb)
        climbSet.set(climb, {
          name: climb,
          km: data ? data.km.toFixed(0) : seg.km_start.toFixed(0),
          gradient: data ? data.gradient : '?',
          length: data?.length_km ?? '?'
        })
      }
    }
  }
}
const climbs = Array.from(climbSet.values())
</script>
