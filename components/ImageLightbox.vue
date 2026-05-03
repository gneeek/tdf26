<template>
  <div
    v-if="isOpen && image"
    class="fixed inset-0 z-[1300] flex items-center justify-center bg-black/85 p-4 sm:p-8"
    role="dialog"
    aria-modal="true"
    :aria-label="image.alt || 'Image viewer'"
    @click.self="close"
  >
    <button
      type="button"
      class="absolute top-3 right-3 sm:top-4 sm:right-4 w-10 h-10 flex items-center justify-center rounded-full bg-white/10 text-white text-xl font-bold hover:bg-white/20 transition-colors cursor-pointer"
      aria-label="Close image viewer"
      @click="close"
    >
      ✕
    </button>
    <button
      v-if="hasSiblings"
      type="button"
      class="absolute left-3 sm:left-4 top-1/2 -translate-y-1/2 w-12 h-12 flex items-center justify-center rounded-full bg-white/10 text-white text-2xl font-bold hover:bg-white/20 transition-colors cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-white/10"
      aria-label="Previous image"
      :disabled="!hasPrev"
      @click.stop="prev"
    >
      ‹
    </button>
    <button
      v-if="hasSiblings"
      type="button"
      class="absolute right-3 sm:right-4 top-1/2 -translate-y-1/2 w-12 h-12 flex items-center justify-center rounded-full bg-white/10 text-white text-2xl font-bold hover:bg-white/20 transition-colors cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-white/10"
      aria-label="Next image"
      :disabled="!hasNext"
      @click.stop="next"
    >
      ›
    </button>
    <figure class="max-w-full max-h-full flex flex-col items-center gap-3" @click.self="close">
      <img
        :src="image.src"
        :alt="image.alt || ''"
        class="max-w-full max-h-[80vh] object-contain rounded shadow-lg"
      >
      <figcaption v-if="hasAttribution || hasSiblings" class="text-center text-stone-200 text-sm max-w-2xl px-2">
        <p v-if="image.caption || image.alt" class="text-stone-100">{{ image.caption || image.alt }}</p>
        <p v-if="image.author" class="text-xs text-stone-400 mt-1">
          Photo by
          <a v-if="image.authorUrl" :href="image.authorUrl" target="_blank" rel="noopener noreferrer" class="text-correze-red hover:underline" @click.stop>{{ sanitizeAttributionText(image.author) }}</a>
          <span v-else>{{ sanitizeAttributionText(image.author) }}</span>
          <template v-if="image.license">
            &middot;
            <a v-if="image.licenseUrl" :href="image.licenseUrl" target="_blank" rel="noopener noreferrer" class="hover:underline" @click.stop>{{ image.license }}</a>
            <span v-else>{{ image.license }}</span>
          </template>
          <template v-if="image.sourceUrl">
            &middot;
            <a :href="image.sourceUrl" target="_blank" rel="noopener noreferrer" class="hover:underline" @click.stop>Source</a>
          </template>
        </p>
        <p v-else-if="image.attribution" class="text-xs text-stone-400 mt-1">{{ sanitizeAttributionText(image.attribution) }}</p>
        <p v-if="hasSiblings" class="text-xs text-stone-500 mt-1">{{ currentIndex + 1 }} / {{ siblings.length }}</p>
      </figcaption>
    </figure>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { sanitizeAttributionText } from '~/utils/sanitize'
import { useImageLightbox } from '~/composables/useImageLightbox'

const { image, siblings, currentIndex, isOpen, hasSiblings, hasPrev, hasNext, close, next, prev } = useImageLightbox()

const hasAttribution = computed(() => {
  if (!image.value) return false
  return Boolean(image.value.caption || image.value.alt || image.value.author || image.value.attribution)
})

function onKeydown(e: KeyboardEvent) {
  if (!isOpen.value) return
  if (e.key === 'Escape') close()
  else if (e.key === 'ArrowRight' && hasNext.value) next()
  else if (e.key === 'ArrowLeft' && hasPrev.value) prev()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

watch(isOpen, (open) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = open ? 'hidden' : ''
})
</script>
