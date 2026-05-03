<template>
  <div v-if="events.length" class="bg-white rounded-lg shadow-sm p-6 mt-8">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Tour de France History</h3>
    <div class="space-y-4">
      <div v-for="(event, idx) in events" :key="idx" class="border-l-4 border-correze-red pl-4">
        <div v-if="event.year" class="flex items-baseline gap-2 mb-1">
          <span class="font-mono font-bold text-correze-red">{{ event.year }}</span>
          <span v-if="event.stage" class="text-sm text-stone-500">{{ event.stage }}</span>
          <span v-if="event.route" class="text-sm text-stone-400">{{ event.route }}</span>
        </div>
        <p class="text-sm text-stone-600 leading-relaxed">{{ event.description }}</p>
        <a
          v-if="event.videoUrl"
          :href="event.videoUrl"
          target="_blank"
          rel="noopener"
          class="text-sm text-correze-red hover:underline mt-1 inline-block"
        >▶ {{ event.videoTitle || 'Watch on YouTube' }}</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

import historicalData from '~/data/historical-tdf.json'

const props = defineProps({
  segment: { type: Number, required: true },
})

const events = computed(() => {
  const entries = historicalData.filter(h => h.segments.includes(props.segment))
  return entries.flatMap(h => h.events)
})
</script>
