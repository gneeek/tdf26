<template>
  <figure class="bg-white rounded-lg shadow-sm overflow-hidden my-8 not-prose">
    <a :href="sourceUrl || src" target="_blank" rel="noopener noreferrer">
      <img
        :src="src"
        :alt="alt"
        class="w-full object-cover cursor-pointer hover:opacity-90 transition-opacity"
        loading="lazy"
      >
    </a>
    <figcaption class="p-3">
      <p v-if="caption" class="text-sm text-stone-700">{{ caption }}</p>
      <p v-if="author || license || sourceUrl" class="text-xs text-stone-400 mt-1">
        <template v-if="author">
          Photo by
          <a v-if="authorUrl" :href="authorUrl" target="_blank" rel="noopener noreferrer" class="text-correze-red hover:underline">{{ sanitizeAttributionText(author) }}</a>
          <span v-else>{{ sanitizeAttributionText(author) }}</span>
        </template>
        <template v-if="license">
          <span v-if="author"> &middot; </span>
          <a v-if="licenseUrl" :href="licenseUrl" target="_blank" rel="noopener noreferrer" class="hover:underline">{{ license }}</a>
          <span v-else>{{ license }}</span>
        </template>
        <template v-if="sourceUrl">
          <span v-if="author || license"> &middot; </span>
          <a :href="sourceUrl" target="_blank" rel="noopener noreferrer" class="hover:underline">Source</a>
        </template>
      </p>
    </figcaption>
  </figure>
</template>

<script setup>
import { sanitizeAttributionText } from '~/utils/sanitize'

defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
  caption: { type: String, default: '' },
  author: { type: String, default: '' },
  authorUrl: { type: String, default: '' },
  license: { type: String, default: '' },
  licenseUrl: { type: String, default: '' },
  sourceUrl: { type: String, default: '' },
})
</script>
