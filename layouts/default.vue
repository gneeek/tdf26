<template>
  <div class="min-h-screen bg-stone-50">
    <header class="bg-correze-red text-white sticky top-0 z-[1100] shadow-md">
      <nav class="max-w-5xl mx-auto px-4 py-3 sm:py-4 flex items-center justify-between">
        <div class="flex items-center gap-3 sm:gap-6">
          <NuxtLink to="/" class="flex items-center gap-2 text-lg sm:text-xl font-serif font-bold hover:text-accent transition-colors">
            <img src="/images/logo.svg" alt="" class="w-6 h-6 sm:w-7 sm:h-7 invert brightness-200">
            Correze Travelogue
          </NuxtLink>
          <div class="flex items-center gap-3">
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
                class="absolute top-full left-0 mt-2 w-72 bg-stone-50 rounded-lg shadow-lg border border-stone-200 py-2 max-h-96 overflow-y-auto"
              >
                <div v-if="entries && entries.length">
                  <NuxtLink
                    v-for="entry in entries"
                    :key="entry.path"
                    :to="entry.path"
                    class="flex items-baseline justify-between gap-3 px-4 py-2 text-sm text-stone-700 hover:bg-amber-100 hover:text-correze-red transition-colors"
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
            <NuxtLink to="/rules" class="text-sm hover:text-accent transition-colors">
              Rules
            </NuxtLink>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-red-200 hidden md:inline">Tour de France 2026 - Stage 9</span>
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

    <footer class="bg-stone-900 text-stone-400 mt-16 relative overflow-hidden">
      <img src="/images/logo.svg" alt="" class="absolute right-4 top-1/2 -translate-y-1/2 w-24 h-24 opacity-5">
      <div class="max-w-5xl mx-auto px-4 py-6 text-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative">
        <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-6">
          <div>
            <p>Correze Travelogue - Malemort to Ussel, 185km</p>
            <p class="mt-1">Stage 9, Tour de France 2026 - Sunday, July 12</p>
          </div>
          <span class="text-stone-600 sm:border-l sm:border-stone-700 sm:pl-6">Designed in Maxwelltown, Dumfries</span>
        </div>
        <div class="flex flex-col items-start sm:items-end gap-2">
          <span class="text-stone-500 text-xs uppercase tracking-wider">Contact</span>
          <div class="flex items-center gap-3">
            <a href="mailto:mtown@iamsosmrt.com" class="text-stone-500 hover:text-white transition-colors" title="Email">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>
            </a>
            <a href="https://github.com/gneeek/tdf26/wiki" target="_blank" rel="noopener noreferrer" class="text-stone-500 hover:text-white transition-colors" title="Wiki">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>
            </a>
            <a href="https://github.com/gneeek/tdf26" target="_blank" rel="noopener noreferrer" class="text-stone-500 hover:text-white transition-colors" title="GitHub">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" /></svg>
            </a>
          </div>
        </div>
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
