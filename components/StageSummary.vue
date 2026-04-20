<template>
  <div class="bg-white rounded-lg border border-stone-200 px-4 py-3">
    <div class="flex flex-wrap gap-x-3 gap-y-1 text-xs sm:text-sm text-stone-600">
      <span><span class="font-semibold text-stone-800">{{ totalDistanceKm }} km</span></span>
      <span class="text-stone-300">&middot;</span>
      <span>+{{ formatNumber(totals.totalElevationGain) }} m climb</span>
      <span class="text-stone-300">&middot;</span>
      <span>{{ totals.uniqueCategorizedClimbs.length }} climbs <span class="text-stone-400">(Mont Bessou 977m)</span></span>
      <span class="text-stone-300">&middot;</span>
      <span>{{ totals.uniqueTowns.length }} towns</span>
      <span class="text-stone-300">&middot;</span>
      <span class="text-stone-500">Sun 12 Jul 2026</span>
    </div>

    <div class="mt-3">
      <div class="relative h-1.5 bg-stone-200 rounded-full overflow-hidden">
        <div
          class="absolute inset-y-0 left-0 bg-correze-red rounded-full transition-all"
          :style="{ width: `${progressPercent}%` }"
        />
      </div>
      <div v-if="progress.kmRidden > 0" class="mt-1.5 flex flex-wrap gap-x-3 gap-y-0.5 text-xs text-stone-500">
        <span>{{ Math.round(progress.kmRidden) }} km ridden</span>
        <span class="text-stone-300">&middot;</span>
        <span>+{{ formatNumber(progress.elevationClimbed) }} m climbed</span>
        <span class="text-stone-300">&middot;</span>
        <span>{{ progress.categorizedClimbsPassed.length }} {{ progress.categorizedClimbsPassed.length === 1 ? 'climb' : 'climbs' }} passed</span>
      </div>
      <div v-else class="mt-1.5 text-xs text-stone-500 italic">
        The journey begins soon.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import segmentsJson from '~/data/segments.json'
import { deriveTotals, journeyThroughSegment } from '~/utils/stage-totals'

const props = defineProps<{
  latestSegment?: number | null
}>()

const totals = deriveTotals(segmentsJson)

const totalDistanceKm = computed(() => Math.round(totals.totalDistance))

const progress = computed(() => {
  const seg = props.latestSegment ?? 0
  return journeyThroughSegment(segmentsJson, seg)
})

const progressPercent = computed(() => {
  if (totals.totalDistance <= 0) return 0
  return Math.min(100, Math.max(0, (progress.value.kmRidden / totals.totalDistance) * 100))
})

function formatNumber(n: number): string {
  return n.toLocaleString('en-US')
}
</script>
