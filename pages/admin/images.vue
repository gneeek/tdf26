<template>
  <div>
    <h1 class="text-2xl font-bold text-stone-800 mb-6">Image Selector</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <div class="flex items-center gap-4">
        <label class="text-sm font-medium text-stone-600">Segment</label>
        <select v-model.number="selectedSegment" class="border border-stone-300 rounded px-3 py-2 text-sm">
          <option v-for="n in 27" :key="n" :value="n">{{ n }} - {{ segmentTitle(n) }}</option>
        </select>
        <button
          class="bg-stone-900 text-white px-4 py-2 rounded text-sm hover:bg-stone-700"
          @click="loadImages"
        >
          Load
        </button>
        <button
          :disabled="fetching"
          class="text-sm text-blue-600 hover:underline disabled:opacity-50"
          @click="fetchSuggestions"
        >
          {{ fetching ? 'Fetching...' : 'Fetch from Wikimedia' }}
        </button>
      </div>
    </div>

    <!-- Selected images -->
    <div v-if="selected.length" class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-stone-700">Selected ({{ selected.length }})</h2>
        <button
          :disabled="saving"
          class="bg-stone-900 text-white px-4 py-2 rounded text-sm hover:bg-stone-700 disabled:opacity-50"
          @click="saveSelection"
        >
          {{ saving ? 'Saving...' : 'Save to Entry' }}
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="(img, idx) in selected" :key="idx" class="relative group">
          <img :src="img.src" :alt="img.alt" class="w-full h-32 object-cover rounded border-2 border-green-500" >
          <button
            class="absolute top-1 right-1 bg-red-600 text-white w-5 h-5 rounded-full text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            @click="removeSelected(idx)"
          >
            x
          </button>
          <p class="text-xs text-stone-500 mt-1 truncate">{{ img.alt }}</p>
        </div>
      </div>
      <span v-if="saveMessage" class="block mt-3 text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
        {{ saveMessage }}
      </span>
    </div>

    <!-- Suggestions grid -->
    <div v-if="suggestions.length" class="bg-white rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold text-stone-700 mb-4">
        Suggestions ({{ suggestions.length }})
      </h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="(img, idx) in suggestions"
          :key="idx"
          class="cursor-pointer group"
          @click="toggleImage(img)"
        >
          <div
            class="relative overflow-hidden rounded border-2 transition-all"
            :class="isSelected(img) ? 'border-green-500 opacity-70' : 'border-stone-200 hover:border-blue-400'"
          >
            <img
              :src="img.url"
              :alt="img.description || img.title"
              class="w-full h-36 object-cover"
              loading="lazy"
            >
            <!-- Green checkmark for selected -->
            <div v-if="isSelected(img)" class="absolute top-1 left-1 bg-green-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shadow">
              &#10003;
            </div>
            <!-- Hover overlay for unselected -->
            <div v-else class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
              <span class="text-white text-xs bg-blue-600 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                Select
              </span>
            </div>
          </div>
          <p class="text-xs text-stone-600 mt-1 truncate">{{ img.title }}</p>
          <p class="text-xs text-stone-400 truncate">{{ img.license }} - {{ img.width }}x{{ img.height }}</p>
        </div>
      </div>
    </div>

    <p v-else-if="loaded && !fetching" class="text-stone-400 italic text-sm">
      No suggestions found. Click "Fetch from Wikimedia" to search.
    </p>

    <!-- Attraction search suggestions -->
    <div v-if="nearbyAttractions.length" class="bg-white rounded-lg shadow-sm p-6 mt-6">
      <h2 class="text-lg font-semibold text-stone-700 mb-3">Search by Nearby Attraction</h2>
      <p class="text-sm text-stone-500 mb-3">Click to search Wikipedia for images of attractions near this segment:</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="poi in nearbyAttractions"
          :key="poi.name"
          class="text-sm px-3 py-1.5 rounded-full border border-stone-300 hover:border-correze-red hover:text-correze-red transition-colors cursor-pointer"
          @click="searchAttractionWikipedia(poi.name)"
        >
          {{ categoryEmoji[poi.category] || '📍' }} {{ poi.name }}
        </button>
      </div>
    </div>

    <!-- Wikipedia image search -->
    <div class="bg-white rounded-lg shadow-sm p-6 mt-6">
      <h2 class="text-lg font-semibold text-stone-700 mb-4">Wikipedia Article Images</h2>
      <div class="flex items-center gap-3 mb-4">
        <input
          v-model="wikiQuery"
          type="text"
          placeholder="Search Wikipedia (e.g. Turenne, Collonges-la-Rouge)..."
          class="flex-1 border border-stone-300 rounded px-3 py-2 text-sm"
          @keyup.enter="searchWikipedia"
        >
        <button
          :disabled="wikiSearching"
          class="bg-stone-900 text-white px-4 py-2 rounded text-sm hover:bg-stone-700 disabled:opacity-50"
          @click="searchWikipedia"
        >
          {{ wikiSearching ? 'Searching...' : 'Search' }}
        </button>
      </div>
      <div v-if="wikiResults.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="img in wikiResults"
          :key="img.title"
          class="cursor-pointer group"
          @click="selectWikiImage(img)"
        >
          <div
            class="relative overflow-hidden rounded border-2 transition-all"
            :class="isSelected({ url: img.url }) ? 'border-green-500 opacity-70' : 'border-stone-200 hover:border-blue-400'"
          >
            <img
              :src="img.url"
              :alt="img.title"
              class="w-full h-36 object-cover"
              loading="lazy"
            >
            <div v-if="isSelected({ url: img.url })" class="absolute top-1 left-1 bg-green-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shadow">
              &#10003;
            </div>
            <div v-else class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
              <span class="text-white text-xs bg-blue-600 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">Select</span>
            </div>
          </div>
          <p class="text-xs text-stone-600 mt-1 truncate">{{ img.title }}</p>
          <a :href="img.articleUrl" target="_blank" rel="noopener" class="text-xs text-correze-red hover:underline">Wikipedia article</a>
        </div>
      </div>
      <p v-if="wikiSearched && !wikiResults.length && !wikiSearching" class="text-stone-400 italic text-sm">
        No Wikipedia images found.
      </p>
      <p v-if="wikiError" class="text-red-600 text-sm mt-2">{{ wikiError }}</p>
    </div>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'
import attractionsData from '~/data/attractions.json'

definePageMeta({ layout: 'admin' })

const { data: entries } = await useAsyncData('admin-picker-entry-titles', () =>
  queryCollection('entries').all()
)

const selectedSegment = ref(1)
const suggestions = ref([])
const selected = ref([])
const entryFilename = ref('')
const loaded = ref(false)
const fetching = ref(false)
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref(false)

function segmentTitle(n) {
  const entry = entries.value?.find(e => e.segment === n)
  if (entry?.title) return entry.title
  const seg = segmentsJson.find(s => s.segment === n)
  if (seg?.towns?.length) return seg.towns[0]
  if (seg?.climbs?.length) return seg.climbs[0]
  return `Segment ${n}`
}

async function loadImages() {
  loaded.value = false
  saveMessage.value = ''
  const data = await $fetch('/api/images', { params: { segment: selectedSegment.value } })
  suggestions.value = data.suggestions
  selected.value = data.entryImages || []
  entryFilename.value = data.entryFilename
  loaded.value = true
}

async function fetchSuggestions() {
  fetching.value = true
  try {
    await $fetch('/api/images-suggest', {
      method: 'POST',
      body: { segment: selectedSegment.value }
    })
    await loadImages()
  } catch {
    saveMessage.value = 'Error fetching suggestions'
    saveError.value = true
  } finally {
    fetching.value = false
  }
}

function isSelected(img) {
  return selected.value.some(s => s.src === img.url)
}

function toggleImage(img) {
  if (isSelected(img)) {
    selected.value = selected.value.filter(s => s.src !== img.url)
  } else {
    const artist = (img.artist || '').replace(/<[^>]*>/g, '').trim()
    selected.value.push({
      src: img.url,
      alt: (img.description || img.title || '').replace(/<[^>]*>/g, '').trim(),
      author: artist,
      authorUrl: img.description_url || null,
      license: img.license || 'Unknown',
      licenseUrl: img.license === 'Public domain' ? null : 'https://creativecommons.org/licenses/by-sa/4.0/',
      sourceUrl: img.description_url || null,
    })
  }
}

function removeSelected(idx) {
  selected.value.splice(idx, 1)
}

async function saveSelection() {
  if (!entryFilename.value) return
  saving.value = true
  saveMessage.value = ''
  saveError.value = false

  try {
    await $fetch('/api/images', {
      method: 'POST',
      body: {
        filename: entryFilename.value,
        images: selected.value
      }
    })
    saveMessage.value = `Saved ${selected.value.length} images to ${entryFilename.value}`
  } catch {
    saveMessage.value = 'Error saving images'
    saveError.value = true
  } finally {
    saving.value = false
  }
}

// --- Nearby attractions for search suggestions ---
const categoryEmoji = {
  food: '🍷', cheese: '🧀', market: '🛒', castle: '🏰', church: '⛪', abbey: '⛪',
  museum: '🏛️', nature: '🌿', bridge: '🌉', archaeology: '🏺',
  memorial: '🕯️', industrial: '🏭', craft: '🔨',
}

// Nearby-attraction suggestions for the Wikipedia search helper. Uses the same
// route-proximity algorithm as components/NearbyAttractions.vue (issue #344)
// so the admin and the published entry pages stay consistent.
const nearbyAttractions = computed(() => {
  const seg = segmentsJson.find(s => s.segment === selectedSegment.value)
  if (!seg) return []
  const TOLERANCE_KM = 0.5
  const MAX_DISTANCE_M = 5000
  return attractionsData
    .filter(poi => {
      if (typeof poi.nearest_km !== 'number' || typeof poi.nearest_distance_m !== 'number') {
        return false
      }
      if (poi.nearest_distance_m > MAX_DISTANCE_M) {
        return false
      }
      return poi.nearest_km >= (seg.km_start - TOLERANCE_KM)
          && poi.nearest_km <= (seg.km_end + TOLERANCE_KM)
    })
    .sort((a, b) => a.nearest_distance_m - b.nearest_distance_m)
})

function searchAttractionWikipedia(name) {
  wikiQuery.value = name
  searchWikipedia()
}

// --- Wikipedia search ---
const wikiQuery = ref('')
const wikiResults = ref([])
const wikiSearching = ref(false)
const wikiSearched = ref(false)
const wikiError = ref('')

async function searchWikipedia() {
  if (!wikiQuery.value) return
  wikiSearching.value = true
  wikiSearched.value = false
  wikiError.value = ''
  try {
    const data = await $fetch('/api/wikipedia-images', {
      method: 'POST',
      body: { query: wikiQuery.value }
    })
    wikiResults.value = data.images
    wikiSearched.value = true
  } catch (err) {
    wikiError.value = err.data?.message || 'Wikipedia search failed'
    wikiResults.value = []
    wikiSearched.value = true
  } finally {
    wikiSearching.value = false
  }
}

function selectWikiImage(img) {
  if (isSelected({ url: img.url })) {
    selected.value = selected.value.filter(s => s.src !== img.url)
  } else {
    const commonsUrl = img.commonsDescriptionUrl || img.articleUrl
    selected.value.push({
      src: img.url,
      alt: img.title,
      author: img.artist || 'Unknown',
      authorUrl: commonsUrl,
      license: img.license || 'Unknown',
      licenseUrl: img.licenseUrl || null,
      sourceUrl: commonsUrl,
    })
  }
}

onMounted(() => loadImages())
</script>
