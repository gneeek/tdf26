<template>
  <div class="min-h-screen bg-stone-100">
    <header class="bg-stone-900 text-white">
      <nav class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-6">
          <NuxtLink to="/admin" class="text-lg font-bold hover:text-accent transition-colors">
            Admin
          </NuxtLink>
          <div class="hidden md:flex items-center gap-4 text-sm">
            <NuxtLink to="/admin/riders" class="text-stone-300 hover:text-white">Riders</NuxtLink>
            <NuxtLink to="/admin/rider-config" class="text-stone-300 hover:text-white">Config</NuxtLink>
            <NuxtLink to="/admin/entries" class="text-stone-300 hover:text-white">Entries</NuxtLink>
            <NuxtLink to="/admin/images" class="text-stone-300 hover:text-white">Images</NuxtLink>
            <NuxtLink to="/admin/weather" class="text-stone-300 hover:text-white">Weather</NuxtLink>
            <!-- Schedule nav entry removed in #384 until #73 (publish schedule editor) ships in v1.6.0 -->
            <NuxtLink to="/admin/publish" class="text-stone-300 hover:text-white">Publish</NuxtLink>
            <!-- Settings nav entry removed in #384 until #71 (site settings editor) ships in v1.6.0 -->
          </div>
        </div>
        <NuxtLink to="/" class="text-sm text-stone-400 hover:text-white">
          View Site &rarr;
        </NuxtLink>
      </nav>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>
