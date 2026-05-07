<template>
  <div class="max-w-3xl">
    <header class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-correze-red tracking-wide">All entries</h1>
      <p class="text-stone-600 font-serif mt-2">
        Every published segment of the Corrèze travelogue, newest first.
      </p>
    </header>

    <section v-if="entries && entries.length" class="space-y-3">
      <EntryCard
        v-for="entry in entries"
        :key="entry.path || entry._path"
        :entry="entry"
        density="compact"
        :heading-level="2"
      />
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
</script>
