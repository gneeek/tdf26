<template>
  <div v-if="nearby.length" class="bg-white rounded-lg shadow-sm p-6 mt-8">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Nearby Attractions</h3>
    <div class="space-y-3">
      <div v-for="poi in nearby" :key="poi.name" class="flex items-start gap-3">
        <span class="text-xl shrink-0 mt-0.5">{{ emojiFor(poi.category) }}</span>
        <div>
          <span class="font-medium text-stone-800">{{ poi.name }}</span>
          <p class="text-sm text-stone-500 mt-0.5">{{ poi.description }}</p>
          <div v-if="poi.links && poi.links.length" class="flex gap-3 mt-1">
            <a
              v-for="link in poi.links"
              :key="link.url"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs text-correze-red hover:underline"
            >
              {{ link.label }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

import attractionsData from '~/data/attractions.json'
import segmentsJson from '~/data/segments.json'
import { emojiFor } from '~/utils/attractions'

const props = defineProps({
  segment: { type: Number, required: true },
})

// Segment boundary tolerance: attractions within 0.5 km of a segment's km_start
// or km_end also appear in the adjacent segment. This prevents boundary cases
// like Collonges-la-Rouge (first route arrival at km 21.75, just inside segment 3)
// from disappearing from segment 4's entry page where the Collonges content lives.
const TOLERANCE_KM = 0.5

// Attractions more than this far from the actual route aren't "nearby" to any
// segment and are excluded from every entry page.
const MAX_DISTANCE_M = 5000

const nearby = computed(() => {
  const seg = segmentsJson.find(s => s.segment === props.segment)
  if (!seg) return []

  return attractionsData
    .filter(poi => {
      // Route-proximity fields are precomputed by
      // processing/calculate_attraction_positions.py. Skip POIs that haven't
      // been processed yet (defensive; in practice all POIs should have them).
      if (typeof poi.nearest_km !== 'number' || typeof poi.nearest_distance_m !== 'number') {
        return false
      }
      if (poi.nearest_distance_m > MAX_DISTANCE_M) {
        return false
      }
      return poi.nearest_km >= (seg.km_start - TOLERANCE_KM)
          && poi.nearest_km <= (seg.km_end + TOLERANCE_KM)
    })
    .sort((a, b) => a.nearest_distance_m - b.nearest_distance_m)
})
</script>
