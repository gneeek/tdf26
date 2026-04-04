<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Publish Schedule</h3>
    <div class="space-y-1">
      <div
        v-for="entry in schedule"
        :key="entry.segment"
        class="flex items-center gap-3 py-1.5 px-2 rounded text-sm"
        :class="entryClass(entry)"
      >
        <span class="w-6 text-right font-mono text-stone-400">{{ entry.segment }}</span>
        <span class="w-24 font-mono text-xs" :class="entry.published ? 'text-correze-red' : 'text-stone-400'">
          {{ formatDate(entry.date) }}
        </span>
        <component
          :is="entry.published ? 'NuxtLink' : 'span'"
          :to="entry.published ? `/entries/${entry.slug}` : undefined"
          class="flex-1 truncate"
          :class="entry.published ? 'text-correze-red hover:underline font-medium' : 'text-stone-400'"
        >
          {{ entry.title }}
        </component>
        <span v-if="entry.isNext" class="text-xs bg-correze-red text-white px-2 py-0.5 rounded-full">
          next
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'

const today = new Date().toISOString().split('T')[0]

// Generate publish dates: twice weekly (Sun, Wed) starting April 5, 2026
function generateSchedule() {
  const start = new Date('2026-04-05')
  const dates = []
  const current = new Date(start)

  for (let i = 0; i < 26; i++) {
    dates.push(current.toISOString().split('T')[0])
    // Alternate: Sun -> Wed (3 days), Wed -> Sun (4 days)
    const day = current.getDay()
    if (day === 0) {
      // Sunday -> next Wednesday
      current.setDate(current.getDate() + 3)
    } else {
      // Wednesday -> next Sunday
      current.setDate(current.getDate() + 4)
    }
  }
  return dates
}

const publishDates = generateSchedule()

const schedule = segmentsJson.map((seg, i) => {
  const date = publishDates[i] || ''
  const published = date <= today
  const slug = String(seg.segment).padStart(2, '0') + '-' + slugify(segmentTitle(seg))

  return {
    segment: seg.segment,
    date,
    title: segmentTitle(seg),
    slug,
    published,
    isNext: !published && (i === 0 || publishDates[i - 1] <= today),
  }
})

function segmentTitle(seg) {
  if (seg.towns?.length) return seg.towns[0]
  if (seg.climbs?.length) return seg.climbs[0]
  return `Segment ${seg.segment}`
}

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function entryClass(entry) {
  if (entry.published) return 'bg-correze-red-50'
  if (entry.isNext) return 'bg-amber-100'
  return ''
}
</script>
