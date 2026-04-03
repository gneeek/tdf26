<template>
  <article v-if="page" class="max-w-3xl mx-auto">
    <header class="mb-8">
      <span class="text-sm text-correze-red font-semibold">
        Segment {{ page.segment }} - Km {{ page.kmStart }}-{{ page.kmEnd }}
      </span>
      <h1 class="text-4xl font-serif font-bold text-gray-900 mt-2">{{ page.title }}</h1>
      <p v-if="page.subtitle" class="text-xl text-gray-500 mt-2 font-serif">{{ page.subtitle }}</p>
      <time class="text-sm text-gray-400 mt-3 block">{{ formatDate(page.publishDate) }}</time>
    </header>

    <SegmentMap
      :segment="page.segment"
      :segments="segments"
      :route-coords="routeCoords"
      class="mb-8"
    />

    <ElevationChart :elevation-data="elevationData" class="mb-8" />

    <PowerStats :elevation-data="elevationData" class="mb-8" />

    <div class="prose prose-lg max-w-none font-serif">
      <ContentRenderer :value="page" />
    </div>

    <ImageGallery :images="page.images" />

    <WeatherWidget :weather="page.weather" />

    <RiderDashboard />

    <nav class="mt-12 pt-8 border-t border-gray-200 flex justify-between">
      <NuxtLink
        v-if="prev"
        :to="prev._path"
        class="text-correze-red hover:underline"
      >
        &larr; {{ prev.title }}
      </NuxtLink>
      <span v-else></span>
      <NuxtLink
        v-if="next"
        :to="next._path"
        class="text-correze-red hover:underline"
      >
        {{ next.title }} &rarr;
      </NuxtLink>
    </nav>
  </article>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'

const route = useRoute()
const slug = route.path.replace(/^\//, '')
const { data: page } = await useAsyncData(`entry-${route.path}`, () =>
  queryCollection('entries')
    .path(slug)
    .first()
)

const today = new Date().toISOString().split('T')[0]

const { data: prev } = await useAsyncData(`prev-${route.path}`, () =>
  queryCollection('entries')
    .where('segment', '<', page.value?.segment)
    .where('draft', '=', false)
    .where('publishDate', '<=', today)
    .order('segment', 'DESC')
    .limit(1)
    .first()
)

const { data: next } = await useAsyncData(`next-${route.path}`, () =>
  queryCollection('entries')
    .where('segment', '>', page.value?.segment)
    .where('draft', '=', false)
    .where('publishDate', '<=', today)
    .order('segment', 'ASC')
    .limit(1)
    .first()
)

const segments = segmentsJson

// Load route coordinates
const routeCoords = ref([])
try {
  const routeData = await import('~/data/route.json')
  const data = routeData.default || routeData
  routeCoords.value = data.features?.[0]?.geometry?.coordinates || []
} catch {
  routeCoords.value = []
}

const elevationData = ref(null)
if (page.value?.segment != null) {
  try {
    const segNum = String(page.value.segment).padStart(2, '0')
    const data = await import(`~/data/elevation/segment-${segNum}.json`)
    elevationData.value = data.default || data
  } catch {
    elevationData.value = null
  }
}

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
