<template>
  <svg :class="sizeClass" viewBox="0 0 32 32" :title="title">
    <!-- Jersey body with sleeves and collar -->
    <path
      d="M16 2 L12 4 L8 3 L4 6 L4 12 L8 11 L8 28 L24 28 L24 11 L28 12 L28 6 L24 3 L20 4 L16 2Z"
      :fill="fill"
      :stroke="stroke"
      stroke-width="1.2"
      stroke-linejoin="round"
    />
    <!-- Collar -->
    <path
      d="M13 3.5 Q16 6 19 3.5"
      fill="none"
      :stroke="stroke"
      stroke-width="0.8"
    />
    <!-- Polka dots (only for polkaDot type) -->
    <template v-if="type === 'polkaDot'">
      <circle cx="12" cy="12" r="2" fill="#DC2626" />
      <circle cx="20" cy="12" r="2" fill="#DC2626" />
      <circle cx="16" cy="17" r="2" fill="#DC2626" />
      <circle cx="12" cy="22" r="2" fill="#DC2626" />
      <circle cx="20" cy="22" r="2" fill="#DC2626" />
    </template>
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, required: true },
  size: { type: String, default: 'sm' },
  title: { type: String, default: '' },
})

const sizeClass = computed(() => {
  const sizes = { xs: 'w-4 h-4', sm: 'w-5 h-5', md: 'w-6 h-6', lg: 'w-8 h-8' }
  return sizes[props.size] || sizes.sm
})

const fill = computed(() => {
  const fills = {
    yellow: '#FFD100',
    green: '#22C55E',
    polkaDot: 'white',
    red: '#DC2626',
  }
  return fills[props.type] || '#999'
})

const stroke = computed(() => {
  const strokes = {
    yellow: '#B8960A',
    green: '#16A34A',
    polkaDot: '#DC2626',
    red: '#991B1B',
  }
  return strokes[props.type] || '#666'
})
</script>
