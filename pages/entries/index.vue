<template>
  <div class="max-w-3xl">
    <header class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-correze-red tracking-wide">All entries</h1>
      <p class="text-stone-600 font-serif mt-2">
        Every published segment of the Corrèze travelogue, newest first.
      </p>
    </header>

    <section v-if="entries && entries.length" class="space-y-3">
      <article v-for="entry in entries" :key="entry.path || entry._path" class="group bg-white rounded-lg shadow-sm p-4 hover:shadow-md hover:bg-stone-50 hover:border-l-4 hover:border-correze-red cursor-pointer transition-all border-l-4 border-transparent">
        <NuxtLink :to="entry.path || entry._path" class="block">
          <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
            Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
          </span>
          <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
          <h2 class="text-xl font-serif font-bold text-stone-900 group-hover:text-correze-red transition-colors mt-1">{{ entry.title }}</h2>
          <p v-if="entry.subtitle" class="text-stone-600 mt-1">{{ entry.subtitle }}</p>
          <time class="text-sm text-stone-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
        </NuxtLink>
      </article>
    </section>
    <p v-else class="text-stone-500 italic">No entries published yet.</p>

    <p class="mt-6">
      <NuxtLink to="/" class="text-correze-red hover:underline">&larr; Back to homepage</NuxtLink>
    </p>
  </div>
</template>

<script setup>
const today = new Date().toISOString().split('T')[0]

const { data: entries } = await useAsyncData('all-entries', () =>
  queryCollection('entries')
    .where('draft', '=', false)
    .where('publishDate', '<=', today)
    .order('publishDate', 'DESC')
    .all()
)

useHead({ title: 'All entries - Corrèze Travelogue' })

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
