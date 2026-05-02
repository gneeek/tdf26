<template>
  <div v-if="images && images.length" class="mt-8">
    <h3 class="text-lg font-semibold text-stone-700 mb-4">Gallery</h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <figure v-for="(img, idx) in images" :key="idx" class="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          type="button"
          class="block w-full p-0 border-0 bg-transparent cursor-pointer"
          :aria-label="`Open ${img.alt || 'image'} in viewer`"
          @click="show(img)"
        >
          <img
            :src="img.src"
            :alt="img.alt"
            class="w-full h-48 object-cover hover:opacity-90 transition-opacity"
            loading="lazy"
          >
        </button>
        <figcaption class="p-3">
          <p class="text-sm text-stone-700">{{ img.alt }}</p>
          <p v-if="img.author" class="text-xs text-stone-400 mt-1">
            Photo by
            <a v-if="img.authorUrl" :href="img.authorUrl" target="_blank" rel="noopener noreferrer" class="text-correze-red hover:underline">{{ sanitizeAttributionText(img.author) }}</a>
            <span v-else>{{ sanitizeAttributionText(img.author) }}</span>
            <template v-if="img.license">
              &middot;
              <a v-if="img.licenseUrl" :href="img.licenseUrl" target="_blank" rel="noopener noreferrer" class="hover:underline">{{ img.license }}</a>
              <span v-else>{{ img.license }}</span>
            </template>
            <template v-if="img.sourceUrl">
              &middot;
              <a :href="img.sourceUrl" target="_blank" rel="noopener noreferrer" class="hover:underline">Source</a>
            </template>
          </p>
          <p v-else-if="img.attribution" class="text-xs text-stone-400 mt-1">{{ sanitizeAttributionText(img.attribution) }}</p>
        </figcaption>
      </figure>
    </div>
  </div>
</template>

<script setup>
import { sanitizeAttributionText } from '~/utils/sanitize'
import { useImageLightbox } from '~/composables/useImageLightbox'

defineProps({
  images: { type: Array, default: () => [] }
})

const { show } = useImageLightbox()
</script>
