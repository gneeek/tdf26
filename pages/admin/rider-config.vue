<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Rider Configuration</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Route Settings</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Total Distance (km)</label>
          <div class="border border-gray-200 bg-gray-50 rounded px-3 py-2 text-sm text-gray-500">{{ totalDistance }} km (from GPX)</div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Daily Cap (km)</label>
          <input v-model.number="dailyCap" type="number" step="0.1" class="border border-gray-300 rounded px-3 py-2 text-sm w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Start Date</label>
          <input v-model="startDate" type="date" class="border border-gray-300 rounded px-3 py-2 text-sm w-full" />
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Riders</h2>
      <div class="space-y-4">
        <div v-for="(rider, idx) in riders" :key="idx" class="flex items-center gap-4 p-3 bg-gray-50 rounded">
          <div class="flex-1">
            <label class="block text-xs text-gray-500 mb-1">Name</label>
            <input v-model="rider.name" type="text" class="border border-gray-300 rounded px-3 py-2 text-sm w-full" />
          </div>
          <div class="w-32">
            <label class="block text-xs text-gray-500 mb-1">ID</label>
            <input v-model="rider.id" type="text" class="border border-gray-300 rounded px-3 py-2 text-sm w-full font-mono" />
          </div>
          <div class="w-24">
            <label class="block text-xs text-gray-500 mb-1">Colour</label>
            <div class="flex items-center gap-2">
              <input v-model="rider.color" type="color" class="w-8 h-8 rounded cursor-pointer border-0" />
              <span class="text-xs font-mono text-gray-500">{{ rider.color }}</span>
            </div>
          </div>
          <button
            @click="removeRider(idx)"
            class="text-red-500 hover:text-red-700 text-sm mt-4"
            :disabled="riders.length <= 1"
          >
            Remove
          </button>
        </div>
      </div>
      <button @click="addRider" class="mt-4 text-sm text-blue-600 hover:underline">
        + Add rider
      </button>
    </div>

    <div class="flex items-center gap-4">
      <button
        @click="saveConfig"
        :disabled="saving"
        class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
      >
        {{ saving ? 'Saving...' : 'Save Configuration' }}
      </button>
      <span v-if="saveMessage" class="text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
        {{ saveMessage }}
      </span>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const riders = ref([])
const totalDistance = ref(185)
const dailyCap = ref(2)
const startDate = ref('2026-04-01')
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref(false)

async function loadConfig() {
  const data = await $fetch('/api/riders')
  riders.value = data.config.riders.map(r => ({ ...r }))
  totalDistance.value = data.config.totalDistance
  dailyCap.value = data.config.dailyCap
  startDate.value = data.config.startDate
}

function addRider() {
  const id = 'rider' + (riders.value.length + 1)
  riders.value.push({ id, name: 'New Rider', color: '#888888' })
}

function removeRider(idx) {
  if (riders.value.length > 1) {
    riders.value.splice(idx, 1)
  }
}

async function saveConfig() {
  saving.value = true
  saveMessage.value = ''
  saveError.value = false

  try {
    await $fetch('/api/rider-config', {
      method: 'POST',
      body: {
        riders: riders.value,
        totalDistance: totalDistance.value,
        dailyCap: dailyCap.value,
        startDate: startDate.value
      }
    })
    saveMessage.value = 'Configuration saved.'
  } catch {
    saveMessage.value = 'Error saving configuration.'
    saveError.value = true
  } finally {
    saving.value = false
  }
}

onMounted(() => loadConfig())
</script>
