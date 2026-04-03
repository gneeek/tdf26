<template>
  <article v-if="page" class="max-w-3xl mx-auto">
    <header class="mb-8">
      <span class="text-sm text-correze-red font-semibold">
        Segment {{ page.segment }} — Km {{ page.kmStart }}–{{ page.kmEnd }}
      </span>
      <h1 class="text-4xl font-serif font-bold text-gray-900 mt-2">{{ page.title }}</h1>
      <p v-if="page.subtitle" class="text-xl text-gray-500 mt-2 font-serif">{{ page.subtitle }}</p>
      <time class="text-sm text-gray-400 mt-3 block">{{ formatDate(page.publishDate) }}</time>
    </header>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-700 mb-3">Segment Stats</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div>
          <div class="text-2xl font-bold text-correze-red">{{ (page.kmEnd - page.kmStart).toFixed(1) }} km</div>
          <div class="text-xs text-gray-500">Distance</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-correze-green">{{ elevationData?.summary?.elevation_gain || '—' }} m</div>
          <div class="text-xs text-gray-500">Elevation Gain</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-600">{{ elevationData?.summary?.avg_gradient || '—' }}%</div>
          <div class="text-xs text-gray-500">Avg Gradient</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-correze-gold">{{ elevationData?.summary?.avg_power_35kmh || '—' }} W</div>
          <div class="text-xs text-gray-500">Est. Power @35km/h</div>
        </div>
      </div>
    </div>

    <div class="prose prose-lg max-w-none font-serif">
      <ContentRenderer :value="page" />
    </div>

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
const route = useRoute()
const { data: page } = await useAsyncData(`entry-${route.path}`, () =>
  queryContent(route.path).findOne()
)

const today = new Date().toISOString().split('T')[0]

const { data: prev } = await useAsyncData(`prev-${route.path}`, () =>
  queryContent('entries')
    .where({ segment: { $lt: page.value?.segment }, draft: false, publishDate: { $lte: today } })
    .sort({ segment: -1 })
    .limit(1)
    .findOne()
)

const { data: next } = await useAsyncData(`next-${route.path}`, () =>
  queryContent('entries')
    .where({ segment: { $gt: page.value?.segment }, draft: false, publishDate: { $lte: today } })
    .sort({ segment: 1 })
    .limit(1)
    .findOne()
)

const elevationData = ref(null)
if (page.value?.segment) {
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
