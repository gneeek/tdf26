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
    <figure class="max-w-full max-h-full flex flex-col items-center gap-3" @click.self="close">
      <img
        :src="image.src"
        :alt="image.alt || ''"
        class="max-w-full max-h-[80vh] object-contain rounded shadow-lg"
      >
      <figcaption v-if="hasAttribution" class="text-center text-stone-200 text-sm max-w-2xl px-2">
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
      </figcaption>
    </figure>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { sanitizeAttributionText } from '~/utils/sanitize'
import { useImageLightbox } from '~/composables/useImageLightbox'

const { image, isOpen, close } = useImageLightbox()

const hasAttribution = computed(() => {
  if (!image.value) return false
  return Boolean(image.value.caption || image.value.alt || image.value.author || image.value.attribution)
})

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && isOpen.value) close()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

watch(isOpen, (open) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = open ? 'hidden' : ''
})
</script>
