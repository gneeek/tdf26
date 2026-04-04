<template>
  <div v-if="images && images.length" class="mt-8">
    <h3 class="text-lg font-semibold text-gray-700 mb-4">Gallery</h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <figure v-for="(img, idx) in images" :key="idx" class="bg-white rounded-lg shadow-sm overflow-hidden">
        <a :href="img.src" target="_blank" rel="noopener noreferrer">
          <img
            :src="img.src"
            :alt="img.alt"
            class="w-full h-48 object-cover cursor-pointer hover:opacity-90 transition-opacity"
            loading="lazy"
          >
        </a>
        <figcaption class="p-3">
          <p class="text-sm text-gray-700">{{ img.alt }}</p>
          <p v-if="img.attribution" class="text-xs text-gray-400 mt-1">{{ stripHtml(img.attribution) }}</p>
        </figcaption>
      </figure>
    </div>
  </div>
</template>

<script setup>
defineProps({
  images: { type: Array, default: () => [] }
})

function stripHtml(str) {
  if (!str) return ''
  return str.replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
}
</script>
