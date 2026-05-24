<template>
  <article class="group bg-white rounded-lg shadow-sm p-4 hover:shadow-md hover:bg-stone-50 hover:border-l-4 hover:border-correze-red cursor-pointer transition-all border-l-4 border-transparent">
    <NuxtLink :to="entry.path || entry._path" :class="showThumbnail ? 'flex gap-4 items-start' : 'block'">
      <template v-if="showThumbnail">
        <img
          :src="thumbnailImage.src"
          :alt="thumbnailImage.alt || ''"
          loading="lazy"
          class="w-20 h-20 sm:w-28 sm:h-28 rounded object-cover flex-shrink-0"
          :style="thumbnailImage.objectPosition ? { objectPosition: thumbnailImage.objectPosition } : null"
        >
        <div class="min-w-0 flex-1">
          <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
            Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
          </span>
          <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
          <component :is="`h${headingLevel}`" class="text-xl font-serif font-bold text-stone-900 group-hover:text-correze-red transition-colors mt-1">{{ entry.title }}</component>
          <p v-if="entry.subtitle" class="text-stone-600 mt-1">{{ entry.subtitle }}</p>
          <time class="text-sm text-stone-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
        </div>
      </template>
      <template v-else>
        <span v-if="entry.segment > 0" class="text-sm text-correze-red font-semibold">
          Segment {{ entry.segment }} - Km {{ entry.kmStart }}-{{ entry.kmEnd }}
        </span>
        <span v-else class="text-sm text-correze-red font-semibold">Preview</span>
        <component :is="`h${headingLevel}`" class="text-xl font-serif font-bold text-stone-900 group-hover:text-correze-red transition-colors mt-1">{{ entry.title }}</component>
        <p v-if="entry.subtitle" class="text-stone-600 mt-1">{{ entry.subtitle }}</p>
        <time class="text-sm text-stone-400 mt-2 block">{{ formatDate(entry.publishDate) }}</time>
      </template>
    </NuxtLink>
  </article>
</template>

<script setup>
import thumbnailManifest from '~/data/entry-thumbnails.json'

const props = defineProps({
  entry: { type: Object, required: true },
  density: { type: String, default: 'standard', validator: v => ['standard', 'compact'].includes(v) },
  headingLevel: { type: Number, default: 3, validator: v => [2, 3].includes(v) },
})

const { formatDate } = useFormatDate()

const showThumbnail = computed(() =>
  props.density === 'standard' && props.entry.images && props.entry.images.length > 0,
)

const thumbnailImage = computed(() => {
  const images = props.entry.images || []
  const manifestEntry = thumbnailManifest[String(props.entry.segment)]
  if (manifestEntry) {
    const match = images.find(img => img.src === manifestEntry.src)
    if (match) return match
  }
  return images[0]
})
</script>
