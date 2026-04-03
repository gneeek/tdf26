<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Publish</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Build and Deploy</h2>
      <p class="text-sm text-gray-500 mb-4">
        Regenerates rider stats, builds the static site, and optionally deploys to the production server.
      </p>

      <div class="flex items-center gap-4 mb-4">
        <label class="flex items-center gap-2 text-sm">
          <input v-model="skipDeploy" type="checkbox" class="rounded" />
          Skip deploy
        </label>
        <label class="flex items-center gap-2 text-sm">
          <input v-model="dryRun" type="checkbox" class="rounded" />
          Dry run
        </label>
      </div>

      <div class="flex items-center gap-4">
        <button
          @click="runPublish"
          :disabled="running"
          class="bg-gray-900 text-white px-6 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
        >
          {{ running ? 'Running...' : 'Publish' }}
        </button>
        <span v-if="running" class="text-sm text-gray-500">This may take a minute...</span>
      </div>
    </div>

    <div v-if="logs.length" class="bg-gray-900 rounded-lg shadow-sm p-6">
      <h2 class="text-sm font-semibold text-gray-400 mb-3">Output</h2>
      <pre class="text-sm font-mono text-green-400 whitespace-pre-wrap max-h-[500px] overflow-auto">{{ logs.join('\n') }}</pre>
      <div class="mt-4 pt-3 border-t border-gray-700">
        <span class="text-sm" :class="success ? 'text-green-400' : 'text-red-400'">
          {{ success ? '✓ Publish complete' : '✗ Publish failed' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const skipDeploy = ref(true)
const dryRun = ref(false)
const running = ref(false)
const logs = ref([])
const success = ref(false)

async function runPublish() {
  running.value = true
  logs.value = ['Starting publish pipeline...']
  success.value = false

  try {
    const result = await $fetch('/api/publish', {
      method: 'POST',
      body: {
        skipDeploy: skipDeploy.value,
        dryRun: dryRun.value
      }
    })
    logs.value = result.logs
    success.value = true
  } catch (err) {
    if (err.data?.data?.logs) {
      logs.value = err.data.data.logs
    } else {
      logs.value.push(`Error: ${err.data?.message || err.message}`)
    }
    success.value = false
  } finally {
    running.value = false
  }
}
</script>
