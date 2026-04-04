<template>
  <figure class="my-6">
    <img
      :src="src"
      :alt="alt"
      :width="width"
      :height="height"
      class="w-full rounded-lg shadow-md"
      loading="lazy"
    >
    <figcaption v-if="alt" class="mt-2 text-sm text-stone-500 text-center italic">
      {{ alt }}
    </figcaption>
  </figure>
</template>

<script setup>
defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  width: { type: [String, Number], default: undefined },
  height: { type: [String, Number], default: undefined },
})
</script>
