<template>
  <div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      <div class="lg:col-span-2 space-y-3">
        <section class="flex items-center gap-4">
          <img
            src="/images/introduction/marian_segment0.png"
            alt="Malemort to Ussel - Tour de France 2026 Virtual Challenge - 185km"
            class="w-20 h-20 sm:w-24 sm:h-24 rounded-lg shadow-md flex-shrink-0 object-cover"
          >
          <div>
            <h1 class="text-2xl sm:text-4xl font-serif font-semibold text-correze-red tracking-wide">
              Malemort to Ussel
            </h1>
            <p class="text-sm sm:text-base text-stone-600 font-serif leading-snug mt-1">
              Stage 9 of the 2026 Tour de France, 185km through Correze.
            </p>
          </div>
        </section>

        <StageSummary :latest-segment="latestSegment" />

        <section>
          <h2 class="text-2xl font-serif font-bold text-stone-800 mb-3">Latest Entries</h2>
          <div v-if="entries && entries.length" class="space-y-3">
            <article v-for="entry in entries" :key="entry.path || entry._path" class="group bg-white rounded-lg shadow-sm p-4 hover:shadow-md hover:bg-stone-50 hover:border-l-4 hover:border-correze-red cursor-pointer transition-all border-l-4 border-transparent">
              <NuxtLink :to="entry.path || entry._path" class="flex gap-4 items-start">
                <img
                  v-if="entry.images && entry.images.length"
                  :src="entry.images[0].src"
                  :alt="entry.images[0].alt || ''"
                  loading="lazy"
                  class="w-20 h-20 sm:w-28 sm:h-28 rounded object-cover flex-shrink-0"
                >
                <div class="min-w-0 flex-1">
                  <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
                    Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
                  </span>
                  <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
                  <h3 class="text-xl font-serif font-bold text-stone-900 group-hover:text-correze-red transition-colors mt-1">{{ entry.title }}</h3>
                  <p v-if="entry.subtitle" class="text-stone-600 mt-1">{{ entry.subtitle }}</p>
                  <time class="text-sm text-stone-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
                </div>
              </NuxtLink>
            </article>
          </div>
          <p v-else class="text-stone-500 italic">No entries published yet.</p>
          <p v-if="entries && entries.length" class="mt-3 text-right">
            <NuxtLink to="/entries" class="text-sm text-correze-red font-semibold hover:underline">See all entries &rarr;</NuxtLink>
          </p>
        </section>

        <StageRaceInfo class="lg:hidden" />

        <section>
          <h2 class="text-2xl font-serif font-bold text-stone-800 mb-4">The Route</h2>
          <SegmentMap
            :segment="0"
            :segments="segments"
            :route-coords="routeCoords"
            :town-coords="townCoords"
            :rider-stats="riderStats"
            :rider-config="riderConfig"
          />
          <p class="text-xs text-stone-400 mt-2">
            Full 185km route. Use layer controls for topo, cycling, and satellite views.
          </p>
          <ClientOnly>
            <ElevationChart :elevation-data="overviewElevation" :segments="segments" :current-segment="0" :rider-stats="riderStats" :rider-config="riderConfig" :rider-points="riderPointsData" class="mt-6" />
          </ClientOnly>
        </section>
      </div>

      <aside class="space-y-4">
        <DayCounter />
        <RiderDashboard />
        <StageRaceInfo class="hidden lg:block" />
        <PublishSchedule v-if="isDev" />
        <StageDetails :current-km="latestKmEnd" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'
import townCoordsJson from '~/data/town-coords.json'
import riderConfigJson from '~/data/riders/rider-config.json'

const isDev = import.meta.dev
const today = new Date().toISOString().split('T')[0]

const segments = segmentsJson
const townCoords = townCoordsJson
const riderConfig = riderConfigJson

const riderStats = ref(null)
const riderPointsData = ref(null)
try {
  const data = await import('~/data/riders/stats.json')
  riderStats.value = data.default || data
} catch {
  riderStats.value = null
}
try {
  const data = await import('~/data/riders/points.json')
  riderPointsData.value = data.default || data
} catch {
  // points.json may not exist yet
}

const overviewElevation = ref(null)
try {
  const data = await import('~/data/elevation/segment-00.json')
  overviewElevation.value = data.default || data
} catch {
  overviewElevation.value = null
}

const routeCoords = ref([])
try {
  const routeData = await import('~/data/route.json')
  const data = routeData.default || routeData
  routeCoords.value = data.features?.[0]?.geometry?.coordinates || []
} catch {
  routeCoords.value = []
}

const { data: entries } = await useAsyncData('entries', () =>
  queryCollection('entries')
    .where('draft', '=', false)
    .where('publishDate', '<=', today)
    .order('publishDate', 'DESC')
    .limit(5)
    .all()
)

const latestEntry = computed(() => entries.value?.[0])
const latestKmEnd = computed(() => latestEntry.value?.kmEnd || 0)
const latestSegment = computed(() => latestEntry.value?.segment || 0)

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
