<template>
  <figure class="bg-white rounded-lg shadow-sm p-4 mt-8 mb-8">
    <div class="relative w-full overflow-hidden rounded" style="padding-top: 56.25%">
      <iframe
        :src="embedUrl"
        class="absolute inset-0 w-full h-full border-0"
        :title="iframeTitle"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade"
      />
    </div>
    <figcaption v-if="caption" class="text-sm text-stone-600 mt-3 italic">
      {{ caption }}
    </figcaption>
    <p class="text-xs text-stone-400 mt-2">
      Interactive view. Imagery &copy; Google Street View.
    </p>
  </figure>
</template>

<script setup>
const props = defineProps({
  embedUrl: { type: String, required: true },
  caption: { type: String, default: '' },
})

const iframeTitle = computed(() =>
  props.caption ? `Street View: ${props.caption}` : 'Google Street View'
)
</script>
