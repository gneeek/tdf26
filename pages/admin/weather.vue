<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Weather Data</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">API Key</h2>
      <div class="flex gap-3 items-center">
        <input
          v-model="apiKey"
          :type="showKey ? 'text' : 'password'"
          placeholder="OpenWeatherMap API key"
          class="border border-gray-300 rounded px-3 py-2 text-sm flex-1 font-mono"
        />
        <button @click="showKey = !showKey" class="text-sm text-gray-500 hover:underline">
          {{ showKey ? 'Hide' : 'Show' }}
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Entries</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-2 pr-2 text-gray-500 font-medium w-10">#</th>
              <th class="text-left py-2 pr-2 text-gray-500 font-medium">Title</th>
              <th class="text-left py-2 px-2 text-gray-500 font-medium">Current Weather</th>
              <th class="text-center py-2 px-2 text-gray-500 font-medium w-32">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="entry in entries" :key="entry.filename">
              <td class="py-2 pr-2 font-mono text-gray-400">{{ entry.segment }}</td>
              <td class="py-2 pr-2 text-gray-800">{{ entry.title }}</td>
              <td class="py-2 px-2">
                <span v-if="entry.weather" class="text-sm text-gray-600">
                  {{ entry.weather.current.temp }}&deg;C, {{ entry.weather.current.conditions }}, {{ entry.weather.current.wind }}
                </span>
                <span v-else class="text-gray-400 italic">None</span>
              </td>
              <td class="text-center py-2 px-2 space-x-2">
                <button
                  @click="fetchWeather(entry)"
                  :disabled="fetching === entry.filename"
                  class="text-xs text-blue-600 hover:underline disabled:opacity-50"
                >
                  {{ fetching === entry.filename ? 'Fetching...' : 'Fetch' }}
                </button>
                <button
                  v-if="preview && preview.filename === entry.filename"
                  @click="injectWeather(entry)"
                  :disabled="injecting === entry.filename"
                  class="text-xs text-green-600 hover:underline disabled:opacity-50"
                >
                  {{ injecting === entry.filename ? 'Saving...' : 'Save' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Preview -->
    <div v-if="preview" class="bg-white rounded-lg shadow-sm p-6 mt-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-3">Preview: {{ preview.title }}</h2>
      <div class="flex items-center gap-6">
        <div class="text-3xl font-bold text-gray-800">
          {{ preview.weather.current.temp }}&deg;C
        </div>
        <div class="text-sm text-gray-600">
          <div>{{ preview.weather.current.conditions }}</div>
          <div class="text-gray-400">Wind: {{ preview.weather.current.wind }}</div>
        </div>
        <div class="text-xs text-gray-400">
          ({{ preview.lat.toFixed(4) }}, {{ preview.lng.toFixed(4) }})
        </div>
      </div>
    </div>

    <span v-if="message" class="block mt-4 text-sm" :class="messageError ? 'text-red-600' : 'text-green-600'">
      {{ message }}
    </span>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const entries = ref([])
const apiKey = ref('')
const showKey = ref(false)
const fetching = ref(null)
const injecting = ref(null)
const preview = ref(null)
const message = ref('')
const messageError = ref(false)

async function loadEntries() {
  const data = await $fetch('/api/weather')
  entries.value = data.entries
}

async function fetchWeather(entry) {
  if (!apiKey.value) {
    message.value = 'Enter an API key first'
    messageError.value = true
    return
  }

  fetching.value = entry.filename
  message.value = ''
  messageError.value = false

  try {
    const result = await $fetch('/api/weather', {
      method: 'POST',
      body: { segment: entry.segment, apiKey: apiKey.value }
    })
    preview.value = {
      filename: entry.filename,
      title: entry.title,
      weather: result.weather,
      lat: result.lat,
      lng: result.lng
    }
    message.value = `Weather fetched for ${entry.title}`
  } catch (err) {
    message.value = `Error: ${err.data?.message || err.message}`
    messageError.value = true
  } finally {
    fetching.value = null
  }
}

async function injectWeather(entry) {
  if (!preview.value) return

  injecting.value = entry.filename
  message.value = ''

  try {
    await $fetch('/api/weather-inject', {
      method: 'POST',
      body: {
        filename: entry.filename,
        weather: preview.value.weather
      }
    })
    entry.weather = preview.value.weather
    preview.value = null
    message.value = `Weather saved to ${entry.filename}`
  } catch {
    message.value = 'Error saving weather'
    messageError.value = true
  } finally {
    injecting.value = null
  }
}

onMounted(() => loadEntries())
</script>
