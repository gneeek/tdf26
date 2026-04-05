<template>
  <div>
    <section class="mb-12">
      <img
        src="/images/introduction/marian_segment0.png"
        alt="Malemort to Ussel - Tour de France 2026 Virtual Challenge - 185km"
        class="w-full max-w-md sm:max-w-lg mx-auto rounded-lg shadow-md mb-6"
      >
      <h1 class="text-3xl sm:text-4xl font-serif font-semibold text-correze-red mb-4 tracking-wide">
        Malemort to Ussel
      </h1>
      <p class="text-xl text-stone-600 font-serif leading-relaxed">
        A cycling travelogue following the 185km route of Stage 9 of the 2026 Tour de France,
        through the hills, valleys, and villages of Correze.
      </p>
      <p class="mt-2 text-stone-500">
        Published twice weekly, Sunday and Wednesday mornings.
        The peloton rides this road on Sunday, July 12.
      </p>
      <div class="mt-4 p-4 bg-amber-100 rounded-lg text-sm text-stone-700">
        <p class="font-semibold text-stone-800 mb-2">The Race</p>
        <p>
          Four riders are virtually cycling from the comfort of their homes. Starting in April,
          each logs daily kilometres from their own rides, and we track their progress along the
          185km Stage 9 parcours. Each day, up to 2km counts toward their position on the route -
          but unused cap rolls over, rewarding rest days followed by big efforts. Four jerseys are
          contested:
          <svg class="w-4 h-4 inline-block mx-0.5" viewBox="0 0 24 24"><path d="M12 2L8 5H4v4l-2 2v9h20v-9l-2-2V5h-4l-4-3z" fill="#FFD100" stroke="#B8960A" stroke-width="1"/></svg> yellow for the race leader,
          <svg class="w-4 h-4 inline-block mx-0.5" viewBox="0 0 24 24"><path d="M12 2L8 5H4v4l-2 2v9h20v-9l-2-2V5h-4l-4-3z" fill="#22C55E" stroke="#16A34A" stroke-width="1"/></svg> green for sprint points,
          <svg class="w-4 h-4 inline-block mx-0.5" viewBox="0 0 24 24"><path d="M12 2L8 5H4v4l-2 2v9h20v-9l-2-2V5h-4l-4-3z" fill="white" stroke="#DC2626" stroke-width="1"/><circle cx="9" cy="10" r="1.5" fill="#DC2626"/><circle cx="15" cy="10" r="1.5" fill="#DC2626"/><circle cx="12" cy="14" r="1.5" fill="#DC2626"/></svg> polka dot for climbing points,
          and the
          <svg class="w-4 h-4 inline-block mx-0.5" viewBox="0 0 24 24"><path d="M12 2L8 5H4v4l-2 2v9h20v-9l-2-2V5h-4l-4-3z" fill="#DC2626" stroke="#991B1B" stroke-width="1"/></svg> lanterne rouge for last place.
        </p>
        <NuxtLink to="/rules" class="inline-block mt-2 text-correze-red hover:underline font-medium">
          Full competition rules
        </NuxtLink>
      </div>
      <DayCounter class="mt-4" />
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      <div class="lg:col-span-2">
        <section class="mb-8">
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
            <ElevationChart :elevation-data="overviewElevation" :segments="segments" :current-segment="0" :rider-stats="riderStats" :rider-config="riderConfig" class="mt-6" />
          </ClientOnly>
        </section>

        <section>
          <h2 class="text-2xl font-serif font-bold text-stone-800 mb-6">Latest Entries</h2>
          <div v-if="entries && entries.length" class="space-y-6">
            <article v-for="entry in entries" :key="entry.path || entry._path" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
              <NuxtLink :to="entry.path || entry._path" class="block">
                <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
                  Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
                </span>
                <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
                <h3 class="text-xl font-serif font-bold text-stone-900 mt-1">{{ entry.title }}</h3>
                <p v-if="entry.subtitle" class="text-stone-600 mt-1">{{ entry.subtitle }}</p>
                <time class="text-sm text-stone-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
              </NuxtLink>
            </article>
          </div>
          <p v-else class="text-stone-500 italic">No entries published yet.</p>
        </section>
      </div>

      <aside>
        <RiderDashboard />
        <div class="mt-6">
          <PublishSchedule v-if="isDev" />
          <StageDetails v-else />
        </div>
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
try {
  const data = await import('~/data/riders/stats.json')
  riderStats.value = data.default || data
} catch {
  riderStats.value = null
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
