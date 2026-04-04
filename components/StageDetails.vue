<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Stage Details</h3>

    <div class="mb-5">
      <h4 class="text-sm font-semibold text-stone-500 mb-2">Towns</h4>
      <div class="space-y-1">
        <div v-for="town in towns" :key="town.name" class="flex justify-between text-sm">
          <span class="text-stone-700">{{ town.name }}</span>
          <span class="font-mono text-stone-400">km {{ town.km }} &middot; {{ town.elevation }}m</span>
        </div>
      </div>
    </div>

    <div>
      <h4 class="text-sm font-semibold text-stone-500 mb-2">Climbs</h4>
      <div class="space-y-1">
        <div v-for="climb in climbs" :key="climb.name" class="flex justify-between text-sm">
          <span class="text-stone-700">{{ climb.name }}</span>
          <span class="font-mono text-stone-400">km {{ climb.km }} &middot; {{ climb.gradient }}%</span>
        </div>
      </div>
    </div>

    <div class="mt-4 pt-3 border-t border-stone-100 text-xs text-stone-400">
      185 km &middot; 9 climbs &middot; +3,390m elevation
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'

// Known climb details from CLAUDE.md
const climbData = {
  'Puy Boubou': { length: 2.8, gradient: 4.1 },
  'Côte de Lagleygeolle': { length: 5.2, gradient: 3.9 },
  'Côte de Miel': { length: 6.6, gradient: 3.9 },
  'Côte des Naves': { length: 2.8, gradient: 6.7 },
  'Puy de Lachaud': { length: 3.6, gradient: 5.3 },
  'Suc au May': { length: 3.8, gradient: 7.7 },
  'Côte de la Croix de Pey': { length: 7.0, gradient: 4.9 },
  'Mont Bessou': { length: 5.0, gradient: 3.5 },
  'Côte des Gardes': { length: 2.2, gradient: 4.8 },
}

// Extract towns with their approximate km and elevation
const townSet = new Map()
for (const seg of segmentsJson) {
  if (seg.towns?.length) {
    for (const town of seg.towns) {
      if (!townSet.has(town)) {
        townSet.set(town, {
          name: town,
          km: seg.km_start.toFixed(0),
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
      if (!climbSet.has(climb)) {
        const data = climbData[climb] || {}
        climbSet.set(climb, {
          name: climb,
          km: seg.km_start.toFixed(0),
          gradient: data.gradient || '?',
          length: data.length || '?'
        })
      }
    }
  }
}
const climbs = Array.from(climbSet.values())
</script>
