<template>
  <div v-if="weather" class="bg-white rounded-lg shadow-sm p-4 mt-8">
    <h3 class="text-lg font-semibold text-gray-700 mb-3">Weather at this location</h3>
    <div class="flex items-center gap-6">
      <div class="text-3xl font-bold text-gray-800">
        {{ weather.current.temp }}&deg;C
      </div>
      <div class="text-sm text-gray-600">
        <div>{{ weather.current.conditions }}</div>
        <div class="text-gray-400">Wind: {{ weather.current.wind }}</div>
      </div>
    </div>
    <p v-if="weather.forecast" class="text-sm text-gray-500 mt-3 italic">
      {{ weather.forecast }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  weather: { type: Object, default: null }
})
</script>
