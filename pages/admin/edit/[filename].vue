<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <NuxtLink to="/admin/entries" class="text-sm text-gray-500 hover:underline">&larr; Back to entries</NuxtLink>
        <h1 class="text-2xl font-bold text-gray-800 mt-1">{{ entryTitle || 'Edit Entry' }}</h1>
      </div>
      <div class="flex items-center gap-3">
        <span v-if="saveMessage" class="text-sm" :class="saveError ? 'text-red-600' : 'text-green-600'">
          {{ saveMessage }}
        </span>
        <button
          @click="saveEntry"
          :disabled="saving"
          class="bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
        >
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Editor -->
      <div>
        <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
          <h2 class="text-sm font-semibold text-gray-600 mb-2">Frontmatter</h2>
          <textarea
            v-model="frontmatter"
            class="w-full font-mono text-xs border border-gray-300 rounded p-3 bg-gray-50"
            rows="8"
            spellcheck="false"
          />
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4">
          <h2 class="text-sm font-semibold text-gray-600 mb-2">Content (Markdown)</h2>
          <textarea
            v-model="body"
            class="w-full font-mono text-sm border border-gray-300 rounded p-3 min-h-[500px]"
            spellcheck="true"
          />
        </div>
      </div>

      <!-- Preview -->
      <div>
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-sm font-semibold text-gray-600 mb-4">Preview</h2>
          <div class="prose prose-lg max-w-none font-serif" v-html="renderedPreview" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const route = useRoute()
const filename = route.params.filename as string

const frontmatter = ref('')
const body = ref('')
const entryTitle = ref('')
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref(false)

// Simple markdown to HTML for preview
function markdownToHtml(md: string): string {
  return md
    // Headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold and italic
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Links
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
    // Paragraphs
    .replace(/\n\n/g, '</p><p>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
}

const renderedPreview = computed(() => markdownToHtml(body.value))

async function loadEntry() {
  const data = await $fetch('/api/entry-content', {
    params: { filename }
  })
  frontmatter.value = data.frontmatter
  body.value = data.body

  // Extract title from frontmatter
  const titleMatch = data.frontmatter.match(/^title:\s*"?(.+?)"?\s*$/m)
  if (titleMatch) entryTitle.value = titleMatch[1]
}

async function saveEntry() {
  saving.value = true
  saveMessage.value = ''
  saveError.value = false

  try {
    await $fetch('/api/entry-content', {
      method: 'POST',
      body: {
        filename,
        frontmatter: frontmatter.value,
        content: body.value
      }
    })
    saveMessage.value = 'Saved'
    setTimeout(() => { saveMessage.value = '' }, 3000)
  } catch {
    saveMessage.value = 'Error saving'
    saveError.value = true
  } finally {
    saving.value = false
  }
}

onMounted(() => loadEntry())
</script>
