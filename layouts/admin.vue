<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-gray-900 text-white">
      <nav class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-6">
          <NuxtLink to="/admin" class="text-lg font-bold hover:text-yellow-300 transition-colors">
            Admin
          </NuxtLink>
          <div class="hidden md:flex items-center gap-4 text-sm">
            <NuxtLink to="/admin/riders" class="text-gray-300 hover:text-white">Riders</NuxtLink>
            <NuxtLink to="/admin/entries" class="text-gray-300 hover:text-white">Entries</NuxtLink>
            <NuxtLink to="/admin/images" class="text-gray-300 hover:text-white">Images</NuxtLink>
            <NuxtLink to="/admin/weather" class="text-gray-300 hover:text-white">Weather</NuxtLink>
            <NuxtLink to="/admin/schedule" class="text-gray-300 hover:text-white">Schedule</NuxtLink>
            <NuxtLink to="/admin/publish" class="text-gray-300 hover:text-white">Publish</NuxtLink>
            <NuxtLink to="/admin/settings" class="text-gray-300 hover:text-white">Settings</NuxtLink>
          </div>
        </div>
        <NuxtLink to="/" class="text-sm text-gray-400 hover:text-white">
          View Site &rarr;
        </NuxtLink>
      </nav>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>
