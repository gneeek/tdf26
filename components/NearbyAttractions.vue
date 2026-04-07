<template>
  <div v-if="nearby.length" class="bg-white rounded-lg shadow-sm p-6 mt-8">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Nearby Attractions</h3>
    <div class="space-y-3">
      <div v-for="poi in nearby" :key="poi.name" class="flex items-start gap-3">
        <span class="text-xl shrink-0 mt-0.5">{{ categoryEmoji[poi.category] || '📍' }}</span>
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

const props = defineProps({
  segment: { type: Number, required: true },
})

const categoryEmoji = {
  food: '🍷', cheese: '🧀', market: '🛒', castle: '🏰', church: '⛪', abbey: '⛪',
  museum: '🏛️', nature: '🌿', bridge: '🌉', archaeology: '🏺',
  memorial: '🕯️', industrial: '🏭', craft: '🔨',
}

const nearby = computed(() => {
  const seg = segmentsJson.find(s => s.segment === props.segment)
  if (!seg) return []

  const midLat = (seg.start_lat + seg.end_lat) / 2
  const midLng = (seg.start_lng + seg.end_lng) / 2

  return attractionsData
    .filter(poi => {
      const dist = Math.sqrt((poi.lat - midLat) ** 2 + (poi.lng - midLng) ** 2)
      return dist <= 0.15
    })
    .sort((a, b) => {
      const dA = Math.sqrt((a.lat - midLat) ** 2 + (a.lng - midLng) ** 2)
      const dB = Math.sqrt((b.lat - midLat) ** 2 + (b.lng - midLng) ** 2)
      return dA - dB
    })
})
</script>
