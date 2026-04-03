<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Entry Publish Controls</h1>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-2 pr-2 text-gray-500 font-medium w-10">#</th>
              <th class="text-left py-2 pr-2 text-gray-500 font-medium">Title</th>
              <th class="text-center py-2 px-2 text-gray-500 font-medium w-32">Publish Date</th>
              <th class="text-center py-2 px-2 text-gray-500 font-medium w-24">Status</th>
              <th class="text-center py-2 px-2 text-gray-500 font-medium w-20">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="entry in entries" :key="entry.filename" :class="entry.draft ? 'opacity-60' : ''">
              <td class="py-2 pr-2 font-mono text-gray-400">{{ entry.segment }}</td>
              <td class="py-2 pr-2">
                <span class="text-gray-800">{{ entry.title }}</span>
                <span class="text-xs text-gray-400 ml-2">{{ entry.filename }}</span>
              </td>
              <td class="text-center py-2 px-2">
                <input
                  :value="entry.publishDate"
                  @change="updateDate(entry, $event)"
                  type="date"
                  class="border border-gray-300 rounded px-2 py-1 text-xs w-full"
                />
              </td>
              <td class="text-center py-2 px-2">
                <span
                  class="inline-block px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="entry.draft ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'"
                >
                  {{ entry.draft ? 'Draft' : 'Published' }}
                </span>
              </td>
              <td class="text-center py-2 px-2 space-x-2">
                <button
                  @click="toggleDraft(entry)"
                  class="text-xs hover:underline"
                  :class="entry.draft ? 'text-green-600' : 'text-yellow-600'"
                >
                  {{ entry.draft ? 'Publish' : 'Unpublish' }}
                </button>
                <NuxtLink
                  :to="`/admin/edit/${entry.filename}`"
                  class="text-xs text-blue-600 hover:underline"
                >
                  Edit
                </NuxtLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-4 flex gap-4">
      <button @click="setAllDraft(true)" class="text-sm text-yellow-600 hover:underline">
        Set all to draft
      </button>
      <button @click="setAllDraft(false)" class="text-sm text-green-600 hover:underline">
        Publish all
      </button>
    </div>

    <span v-if="saveMessage" class="block mt-2 text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
      {{ saveMessage }}
    </span>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const entries = ref([])
const saveMessage = ref('')
const saveError = ref(false)

async function loadEntries() {
  const data = await $fetch('/api/entries')
  entries.value = data.entries
}

async function updateEntry(entry, updates) {
  saveMessage.value = ''
  saveError.value = false
  try {
    await $fetch('/api/entry-status', {
      method: 'POST',
      body: { filename: entry.filename, ...updates }
    })
    Object.assign(entry, updates)
    saveMessage.value = `Updated ${entry.filename}`
  } catch {
    saveMessage.value = `Error updating ${entry.filename}`
    saveError.value = true
  }
}

function toggleDraft(entry) {
  updateEntry(entry, { draft: !entry.draft })
}

function updateDate(entry, event) {
  updateEntry(entry, { publishDate: event.target.value })
}

async function setAllDraft(draft) {
  for (const entry of entries.value) {
    if (entry.draft !== draft) {
      await updateEntry(entry, { draft })
    }
  }
  saveMessage.value = draft ? 'All entries set to draft' : 'All entries published'
}

onMounted(() => loadEntries())
</script>
