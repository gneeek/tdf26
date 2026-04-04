<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Rider Daily Distances</h1>

    <!-- Entry form -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Add / Edit Entry</h2>
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-600 mb-1">Date</label>
        <input
          v-model="entryDate"
          type="date"
          class="border border-gray-300 rounded px-3 py-2 text-sm w-48"
        >
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div v-for="rider in riders" :key="rider.id">
          <label class="block text-sm font-medium mb-1" :style="{ color: displayColor(rider.color) }">
            {{ rider.name }} (km)
          </label>
          <input
            v-model.number="entryDistances[rider.id]"
            type="number"
            step="0.1"
            min="0"
            class="border border-gray-300 rounded px-3 py-2 text-sm w-full"
            placeholder="0"
          >
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button
          :disabled="submitting"
          class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
          @click="submitEntry"
        >
          {{ submitting ? 'Saving...' : 'Save Entry' }}
        </button>
        <span v-if="saveMessage" class="text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
          {{ saveMessage }}
        </span>
      </div>
    </div>

    <!-- History table -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">History</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-2 pr-4 text-gray-500 font-medium">Date</th>
              <th
                v-for="rider in riders"
                :key="rider.id"
                class="text-center py-2 px-2 font-medium"
                :style="{ color: displayColor(rider.color) }"
              >
                {{ rider.name }}
              </th>
              <th class="text-center py-2 px-2 text-gray-500 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="entry in reversedEntries" :key="entry.date">
              <td class="py-2 pr-4 font-mono text-gray-600">{{ entry.date }}</td>
              <td v-for="rider in riders" :key="rider.id" class="text-center py-2 px-2 font-mono">
                {{ entry.distances[rider.id] || 0 }}
              </td>
              <td class="text-center py-2 px-2">
                <button class="text-blue-600 hover:underline text-xs" @click="editEntry(entry)">
                  edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-if="!entries.length" class="text-gray-400 italic text-sm">No entries yet.</p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const riders = ref([])
const entries = ref([])
const entryDate = ref('')
const entryDistances = ref({})
const submitting = ref(false)
const saveMessage = ref('')
const saveError = ref(false)

const reversedEntries = computed(() => [...entries.value].reverse())

async function loadData() {
  const data = await $fetch('/api/riders')
  riders.value = data.config.riders
  entries.value = data.log.entries

  // Default date: day after last entry
  if (data.log.entries.length) {
    const lastDate = data.log.entries[data.log.entries.length - 1].date
    const next = new Date(lastDate + 'T00:00:00')
    next.setDate(next.getDate() + 1)
    entryDate.value = next.toISOString().split('T')[0]
  } else {
    entryDate.value = new Date().toISOString().split('T')[0]
  }

  // Init distances to 0
  for (const r of data.config.riders) {
    if (!(r.id in entryDistances.value)) {
      entryDistances.value[r.id] = 0
    }
  }
}

function editEntry(entry) {
  entryDate.value = entry.date
  entryDistances.value = { ...entry.distances }
}

async function submitEntry() {
  submitting.value = true
  saveMessage.value = ''
  saveError.value = false

  try {
    await $fetch('/api/riders', {
      method: 'POST',
      body: {
        date: entryDate.value,
        distances: { ...entryDistances.value }
      }
    })
    saveMessage.value = 'Saved! Stats updated.'
    await loadData()

    // Reset distances and advance date
    for (const r of riders.value) {
      entryDistances.value[r.id] = 0
    }
  } catch {
    saveMessage.value = 'Error saving entry.'
    saveError.value = true
  } finally {
    submitting.value = false
  }
}

function displayColor(hex) {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  if (luminance > 0.85) {
    return `rgb(${Math.round(r * 0.5)}, ${Math.round(g * 0.5)}, ${Math.round(b * 0.5)})`
  }
  return hex
}

onMounted(() => loadData())
</script>
