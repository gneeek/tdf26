<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Image Selector</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <div class="flex items-center gap-4">
        <label class="text-sm font-medium text-gray-600">Segment</label>
        <select v-model.number="selectedSegment" class="border border-gray-300 rounded px-3 py-2 text-sm">
          <option v-for="n in 26" :key="n" :value="n">{{ n }} - {{ segmentTitle(n) }}</option>
        </select>
        <button
          @click="loadImages"
          class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700"
        >
          Load
        </button>
        <button
          @click="fetchSuggestions"
          :disabled="fetching"
          class="text-sm text-blue-600 hover:underline disabled:opacity-50"
        >
          {{ fetching ? 'Fetching...' : 'Fetch from Wikimedia' }}
        </button>
      </div>
    </div>

    <!-- Selected images -->
    <div v-if="selected.length" class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-700">Selected ({{ selected.length }})</h2>
        <button
          @click="saveSelection"
          :disabled="saving"
          class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
        >
          {{ saving ? 'Saving...' : 'Save to Entry' }}
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="(img, idx) in selected" :key="idx" class="relative group">
          <img :src="img.src" :alt="img.alt" class="w-full h-32 object-cover rounded border-2 border-green-500" />
          <button
            @click="removeSelected(idx)"
            class="absolute top-1 right-1 bg-red-600 text-white w-5 h-5 rounded-full text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
          >
            x
          </button>
          <p class="text-xs text-gray-500 mt-1 truncate">{{ img.alt }}</p>
        </div>
      </div>
      <span v-if="saveMessage" class="block mt-3 text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
        {{ saveMessage }}
      </span>
    </div>

    <!-- Suggestions grid -->
    <div v-if="suggestions.length" class="bg-white rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">
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
            :class="isSelected(img) ? 'border-green-500 opacity-70' : 'border-gray-200 hover:border-blue-400'"
          >
            <img
              :src="img.url"
              :alt="img.description || img.title"
              class="w-full h-36 object-cover"
              loading="lazy"
            />
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
          <p class="text-xs text-gray-600 mt-1 truncate">{{ img.title }}</p>
          <p class="text-xs text-gray-400 truncate">{{ img.license }} - {{ img.width }}x{{ img.height }}</p>
        </div>
      </div>
    </div>

    <p v-else-if="loaded && !fetching" class="text-gray-400 italic text-sm">
      No suggestions found. Click "Fetch from Wikimedia" to search.
    </p>
  </div>
</template>

<script setup>
import segmentsJson from '~/data/segments.json'

definePageMeta({ layout: 'admin' })

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
  const seg = segmentsJson.find(s => s.segment === n)
  if (!seg) return ''
  if (seg.towns?.length) return seg.towns[0]
  if (seg.climbs?.length) return seg.climbs[0]
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
  } catch (err) {
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
      attribution: `${artist}, ${img.license}, Wikimedia Commons`
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

onMounted(() => loadImages())
</script>
