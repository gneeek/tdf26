<template>
  <a
    :href="url"
    target="_blank"
    rel="noopener noreferrer"
    class="block bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow my-8 not-prose border-l-4 border-correze-red overflow-hidden"
  >
    <div class="p-4 sm:p-5">
      <p class="text-xs uppercase tracking-wider text-correze-red font-semibold mb-2">
        Press coverage
      </p>
      <p class="text-sm text-stone-500 mb-1">
        <span class="font-medium text-stone-700">{{ publication }}</span>
        <template v-if="date">
          <span class="mx-1">&middot;</span>{{ date }}
        </template>
      </p>
      <p class="text-base sm:text-lg text-stone-800 leading-snug">
        {{ headline }}
        <svg class="inline-block w-4 h-4 ml-1 text-stone-400 -mt-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
          <polyline points="15 3 21 3 21 9"/>
          <line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
      </p>
      <p v-if="summary" class="text-sm text-stone-600 mt-2">
        {{ summary }}
      </p>
    </div>
  </a>
</template>

<script setup>
defineProps({
  url: { type: String, required: true },
  publication: { type: String, required: true },
  headline: { type: String, required: true },
  date: { type: String, default: '' },
  summary: { type: String, default: '' },
})
</script>
