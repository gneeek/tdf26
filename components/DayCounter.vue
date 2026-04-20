<template>
  <div class="flex items-center gap-3 text-sm">
    <span class="bg-correze-red text-white font-bold px-3 py-1.5 rounded-lg text-lg flex-shrink-0">
      Day {{ raceDay }}
    </span>
    <div class="flex flex-col gap-0.5">
      <span v-if="daysUntilTour > 0" class="text-stone-500">
        Tour starts in <span class="font-semibold text-stone-700">{{ daysUntilTour }}</span> days
      </span>
      <span v-if="daysUntilStage > 0" class="text-stone-500">
        Stage 9 in <span class="font-semibold text-stone-700">{{ daysUntilStage }}</span> days
      </span>
      <span v-if="daysUntilStage <= 0" class="text-correze-red font-semibold">
        Stage 9 is today!
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const raceStart = new Date('2026-04-01T00:00:00')
const tourStart = new Date('2026-07-04T00:00:00')
const stage9Date = new Date('2026-07-12T00:00:00')

const now = new Date()
const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())

const raceDay = computed(() => {
  const diff = Math.floor((today.getTime() - raceStart.getTime()) / (1000 * 60 * 60 * 24)) + 1
  return Math.max(1, diff)
})

const daysUntilTour = computed(() => {
  return Math.ceil((tourStart.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
})

const daysUntilStage = computed(() => {
  return Math.ceil((stage9Date.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
})
</script>
