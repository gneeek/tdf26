<template>
  <div>
    <h1 class="text-2xl font-bold text-stone-800 mb-6">Publish</h1>

    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-stone-700 mb-4">Pre-publish Steps</h2>
      <p class="text-sm text-stone-500 mb-4">
        Run data processing steps from here. Build and deploy must be done from the terminal
        (running <code class="bg-stone-100 px-1 rounded">nuxt generate</code> inside the dev server causes conflicts).
      </p>

      <div class="flex flex-wrap gap-3 mb-4">
        <label class="flex items-center gap-2 text-sm">
          <input v-model="runStats" type="checkbox" class="rounded" checked >
          Regenerate rider stats
        </label>
        <label class="flex items-center gap-2 text-sm">
          <input v-model="runWeather" type="checkbox" class="rounded" >
          Fetch weather for current entry
        </label>
      </div>

      <div class="flex items-center gap-4">
        <button
          :disabled="running"
          class="bg-stone-900 text-white px-6 py-2 rounded text-sm hover:bg-stone-700 disabled:opacity-50"
          @click="runSteps"
        >
          {{ running ? 'Running...' : 'Run' }}
        </button>
      </div>
    </div>

    <div v-if="logs.length" class="bg-stone-900 rounded-lg shadow-sm p-6 mb-6">
      <h2 class="text-sm font-semibold text-stone-400 mb-3">Output</h2>
      <pre class="text-sm font-mono text-green-400 whitespace-pre-wrap max-h-[400px] overflow-auto">{{ logs.join('\n') }}</pre>
      <div class="mt-4 pt-3 border-t border-stone-700">
        <span class="text-sm" :class="success ? 'text-green-400' : 'text-red-400'">
          {{ success ? '✓ Complete' : '✗ Failed' }}
        </span>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold text-stone-700 mb-4">Build and Deploy</h2>
      <p class="text-sm text-stone-500 mb-3">Run these commands in your terminal:</p>
      <div class="bg-stone-900 rounded p-4 text-sm font-mono text-green-400 space-y-1">
        <p># Build only (no deploy)</p>
        <p class="text-white">./scripts/publish.sh --skip-deploy</p>
        <p class="mt-3"># Build and deploy to production</p>
        <p class="text-white">./scripts/publish.sh</p>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const runStats = ref(true)
const runWeather = ref(false)
const running = ref(false)
const logs = ref([])
const success = ref(false)

async function runSteps() {
  running.value = true
  logs.value = ['Starting...']
  success.value = false

  const steps = []
  if (runStats.value) steps.push('stats')
  if (runWeather.value) steps.push('weather')

  try {
    const result = await $fetch('/api/publish', {
      method: 'POST',
      body: { steps }
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
