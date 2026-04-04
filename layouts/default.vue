<template>
  <div class="min-h-screen bg-stone-50">
    <header class="bg-correze-red text-white relative z-50">
      <nav class="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <div class="flex items-center gap-6">
          <NuxtLink to="/" class="text-xl font-serif font-bold hover:text-accent transition-colors">
            Correze Travelogue
          </NuxtLink>
          <div class="relative">
            <button
              class="text-sm font-medium hover:text-accent transition-colors cursor-pointer flex items-center gap-1"
              @click="toggleParcours"
            >
              Parcours
              <svg
                class="w-3 h-3 transition-transform"
                :class="parcoursOpen ? 'rotate-180' : ''"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div
              v-if="parcoursOpen"
              class="absolute top-full left-0 mt-2 w-72 bg-white rounded-lg shadow-lg border border-stone-200 py-2 max-h-96 overflow-y-auto"
            >
              <div v-if="entries && entries.length">
                <NuxtLink
                  v-for="entry in entries"
                  :key="entry.path"
                  :to="entry.path"
                  class="flex items-baseline justify-between gap-3 px-4 py-2 text-sm text-stone-700 hover:bg-accent/10 hover:text-stone-900 transition-colors"
                  @click="parcoursOpen = false"
                >
                  <span>{{ entry.title }}</span>
                  <span class="text-xs text-stone-400 whitespace-nowrap">{{ formatDate(entry.publishDate) }}</span>
                </NuxtLink>
              </div>
              <p v-else class="px-4 py-2 text-sm text-stone-400 italic">
                No entries published yet
              </p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-red-200 hidden sm:inline">Tour de France 2026 - Stage 9</span>
          <NuxtLink
            v-if="isDev"
            to="/admin"
            class="text-xs bg-white/20 px-2 py-1 rounded hover:bg-white/30 transition-colors"
          >
            Admin
          </NuxtLink>
        </div>
      </nav>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-8">
      <slot />
    </main>

    <footer class="bg-stone-900 text-stone-400 mt-16">
      <div class="max-w-5xl mx-auto px-4 py-8 text-sm text-center">
        <p>Correze Travelogue - Malemort to Ussel, 185km</p>
        <p class="mt-1">Stage 9, Tour de France 2026 - Sunday, July 12</p>
        <a href="https://github.com/gneeek/tdf26" target="_blank" rel="noopener noreferrer" class="inline-block mt-3 text-stone-500 hover:text-white transition-colors" title="Source code on GitHub">
          <svg class="w-5 h-5 inline" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" /></svg>
        </a>
      </div>
    </footer>
  </div>
</template>

<script setup>
const isDev = import.meta.dev
const route = useRoute()

const parcoursOpen = ref(false)

const today = new Date().toISOString().split('T')[0]

const { data: entries } = await useAsyncData('parcours-entries', () =>
  queryCollection('entries')
    .where('draft', '=', false)
    .where('publishDate', '<=', today)
    .order('segment', 'ASC')
    .all()
)

function toggleParcours() {
  parcoursOpen.value = !parcoursOpen.value
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })
}

// Close dropdown on click outside
function onClickOutside(e) {
  if (parcoursOpen.value && !e.target.closest('.relative')) {
    parcoursOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))

// Close on route change
watch(() => route.fullPath, () => {
  parcoursOpen.value = false
})
</script>
