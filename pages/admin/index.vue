<template>
  <div>
    <h1 class="text-2xl font-bold text-stone-800 mb-6">Admin Dashboard</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <NuxtLink to="/admin/riders" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-semibold text-stone-800">Riders</h2>
        <p class="text-sm text-stone-500 mt-1">Enter daily distances, view standings</p>
      </NuxtLink>
      <NuxtLink to="/admin/entries" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-semibold text-stone-800">Entries</h2>
        <p class="text-sm text-stone-500 mt-1">Edit content, toggle draft/publish</p>
      </NuxtLink>
      <NuxtLink to="/admin/images" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-semibold text-stone-800">Images</h2>
        <p class="text-sm text-stone-500 mt-1">Select CC images per segment</p>
      </NuxtLink>
      <NuxtLink to="/admin/weather" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-semibold text-stone-800">Weather</h2>
        <p class="text-sm text-stone-500 mt-1">Fetch and inject weather data</p>
      </NuxtLink>
      <!-- Schedule dashboard card removed in #384 until #73 (publish schedule editor) ships in v1.6.0 -->
      <NuxtLink to="/admin/publish" class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-semibold text-stone-800">Publish</h2>
        <p class="text-sm text-stone-500 mt-1">Build and deploy the site</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })
</script>
