<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-correze-red text-white">
      <nav class="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-xl font-serif font-bold hover:text-yellow-300 transition-colors">
          Corrèze Travelogue
        </NuxtLink>
        <span class="text-sm text-red-200">Tour de France 2026 — Stage 9</span>
      </nav>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-8">
      <slot />
    </main>

    <footer class="bg-gray-800 text-gray-400 mt-16">
      <div class="max-w-5xl mx-auto px-4 py-8 text-sm text-center">
        <p>Corrèze Travelogue — Malemort to Ussel, 185km</p>
        <p class="mt-1">Stage 9, Tour de France 2026 — Sunday, July 12</p>
      </div>
    </footer>
  </div>
</template>
