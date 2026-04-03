<template>
  <div>
    <section class="mb-12">
      <h1 class="text-4xl font-serif font-bold text-correze-red mb-4">
        Malemort to Ussel
      </h1>
      <p class="text-xl text-gray-600 font-serif leading-relaxed">
        A cycling travelogue following the 185km route of Stage 9 of the 2026 Tour de France,
        through the hills, valleys, and villages of Correze.
      </p>
      <p class="mt-2 text-gray-500">
        26 entries published twice weekly, Sunday and Wednesday mornings.
        The peloton rides this road on Sunday, July 12.
      </p>
    </section>

    <section class="mb-12">
      <h2 class="text-2xl font-serif font-bold text-gray-800 mb-4">The Route</h2>
      <RouteOverviewMap
        :segments="segments"
        :route-coords="routeCoords"
        :published-segments="publishedSegmentNumbers"
      />
      <p class="text-xs text-gray-400 mt-2">
        Published segments shown in red. Click for details.
      </p>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
      <section class="lg:col-span-2">
        <h2 class="text-2xl font-serif font-bold text-gray-800 mb-6">Latest Entries</h2>
        <div v-if="entries && entries.length" class="space-y-6">
          <article v-for="entry in entries" :key="entry._path" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
            <NuxtLink :to="entry._path" class="block">
              <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
                Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
              </span>
              <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
              <h3 class="text-xl font-serif font-bold text-gray-900 mt-1">{{ entry.title }}</h3>
              <p v-if="entry.subtitle" class="text-gray-600 mt-1">{{ entry.subtitle }}</p>
              <time class="text-sm text-gray-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
            </NuxtLink>
          </article>
        </div>
        <p v-else class="text-gray-500 italic">No entries published yet.</p>
      </section>

      <aside>
        <RiderDashboard />

        <div class="mt-8">
          <PublishSchedule />
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'

const today = new Date().toISOString().split('T')[0]

const segments = segmentsJson

const routeCoords = ref([])
try {
  const routeData = await import('~/data/route.json')
  const data = routeData.default || routeData
  routeCoords.value = data.features?.[0]?.geometry?.coordinates || []
} catch {
  routeCoords.value = []
}

const { data: entries } = await useAsyncData('entries', () =>
  queryContent('entries')
    .where({ draft: false, publishDate: { $lte: today } })
    .sort({ publishDate: -1 })
    .limit(5)
    .find()
)

const publishedSegmentNumbers = computed(() =>
  (entries.value || [])
    .filter(e => e.segment > 0)
    .map(e => e.segment)
)

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
