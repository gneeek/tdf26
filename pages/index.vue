<template>
  <div>
    <section class="mb-12">
      <h1 class="text-4xl font-serif font-bold text-correze-red mb-4">
        Malemort to Ussel
      </h1>
      <p class="text-xl text-gray-600 font-serif leading-relaxed">
        A cycling travelogue following the 185km route of Stage 9 of the 2026 Tour de France,
        through the hills, valleys, and villages of Corrèze.
      </p>
      <p class="mt-4 text-gray-500">
        26 entries, published twice weekly from April to July 2026.
        The peloton rides this road on Sunday, July 12.
      </p>
    </section>

    <section class="mb-12">
      <h2 class="text-2xl font-serif font-bold text-gray-800 mb-6">Latest Entries</h2>
      <div v-if="entries && entries.length" class="space-y-6">
        <article v-for="entry in entries" :key="entry._path" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
          <NuxtLink :to="entry._path" class="block">
            <span class="text-sm text-correze-red font-semibold">
              Segment {{ entry.segment }} — Km {{ entry.kmStart }}–{{ entry.kmEnd }}
            </span>
            <h3 class="text-xl font-serif font-bold text-gray-900 mt-1">{{ entry.title }}</h3>
            <p v-if="entry.subtitle" class="text-gray-600 mt-1">{{ entry.subtitle }}</p>
            <time class="text-sm text-gray-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
          </NuxtLink>
        </article>
      </div>
      <p v-else class="text-gray-500 italic">No entries published yet.</p>
    </section>

    <section>
      <h2 class="text-2xl font-serif font-bold text-gray-800 mb-4">The Route</h2>
      <div class="bg-white rounded-lg shadow-sm p-6">
        <p class="text-gray-600">
          185 kilometers from Malemort-sur-Corrèze to Ussel, crossing the Corrèze department
          from southwest to northeast. Through the medieval villages of Turenne and Collonges-la-Rouge,
          over the departmental capital of Tulle, up the fierce Suc au May in the Monédières,
          across the wild Plateau de Millevaches, past the highest point in Corrèze at Mont Bessou,
          and down to the finish at Place Voltaire in Ussel.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
const today = new Date().toISOString().split('T')[0]

const { data: entries } = await useAsyncData('entries', () =>
  queryContent('entries')
    .where({ draft: false, publishDate: { $lte: today } })
    .sort({ segment: -1 })
    .limit(5)
    .find()
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
