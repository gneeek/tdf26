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

    <div class="flex gap-2" style="height: calc(100vh - 180px)">
      <!-- Editor pane -->
      <div class="flex flex-col overflow-hidden" :style="{ width: editorWidth + '%' }">
        <div class="bg-white rounded-lg shadow-sm p-4 mb-4 flex-shrink-0">
          <h2 class="text-sm font-semibold text-gray-600 mb-2">Frontmatter</h2>
          <textarea
            v-model="frontmatter"
            class="w-full font-mono text-xs border border-gray-300 rounded p-3 bg-gray-50"
            rows="6"
            spellcheck="false"
          />
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4 flex-1 flex flex-col overflow-hidden">
          <h2 class="text-sm font-semibold text-gray-600 mb-2">Content (Markdown)</h2>
          <!-- Toolbar -->
          <div class="flex gap-1 mb-2 flex-shrink-0">
            <button @click="insertLinePrefix('# ')" class="toolbar-btn font-bold" title="Heading 1">H1</button>
            <button @click="insertLinePrefix('## ')" class="toolbar-btn font-bold" title="Heading 2">H2</button>
            <button @click="insertLinePrefix('### ')" class="toolbar-btn font-bold" title="Heading 3">H3</button>
            <span class="w-px bg-gray-300 mx-1"></span>
            <button @click="wrapMd('**', '**')" class="toolbar-btn font-bold" title="Bold">B</button>
            <button @click="wrapMd('*', '*')" class="toolbar-btn italic" title="Italic">I</button>
            <span class="w-px bg-gray-300 mx-1"></span>
            <button @click="insertLinePrefix('> ')" class="toolbar-btn" title="Quote">&ldquo;</button>
            <button @click="wrapMd('[', '](url)')" class="toolbar-btn" title="Link">Link</button>
          </div>
          <textarea
            ref="editorRef"
            v-model="body"
            class="w-full font-mono text-sm border border-gray-300 rounded p-3 flex-1 resize-none"
            spellcheck="true"
          />
        </div>
      </div>

      <!-- Resize handle -->
      <div
        class="w-2 cursor-col-resize flex-shrink-0 flex items-center justify-center hover:bg-gray-300 rounded"
        @mousedown="startResize"
      >
        <div class="w-0.5 h-8 bg-gray-400 rounded"></div>
      </div>

      <!-- Preview pane -->
      <div class="flex-1 overflow-auto">
        <div class="bg-white rounded-lg shadow-sm p-6 h-full overflow-auto">
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
const filename = String(route.params.filename)

const frontmatter = ref('')
const body = ref('')
const entryTitle = ref('')
const saving = ref(false)
const saveMessage = ref('')
const saveError = ref(false)
const editorRef = ref(null)
const editorWidth = ref(50)

// --- Resize ---
function startResize(e) {
  e.preventDefault()
  const startX = e.clientX
  const startWidth = editorWidth.value
  const containerWidth = e.target.parentElement.offsetWidth

  function onMove(e) {
    const delta = e.clientX - startX
    const pct = (delta / containerWidth) * 100
    editorWidth.value = Math.min(80, Math.max(20, startWidth + pct))
  }
  function onUp() {
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
  }
  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
}

// --- Toolbar ---
function insertLinePrefix(prefix) {
  const el = editorRef.value
  if (!el) return
  const start = el.selectionStart
  const end = el.selectionEnd

  // Find the start of the current line
  const lineStart = body.value.lastIndexOf('\n', start - 1) + 1
  const lineContent = body.value.slice(lineStart, end)

  // Check if already has this prefix — toggle off
  if (lineContent.startsWith(prefix)) {
    body.value = body.value.slice(0, lineStart) + lineContent.slice(prefix.length) + body.value.slice(end)
    nextTick(() => {
      el.selectionStart = Math.max(lineStart, start - prefix.length)
      el.selectionEnd = Math.max(lineStart, end - prefix.length)
      el.focus()
    })
    return
  }

  // Strip any existing heading/quote prefix before adding new one
  const stripped = lineContent.replace(/^#{1,3} |^> /, '')
  body.value = body.value.slice(0, lineStart) + prefix + stripped + body.value.slice(end)
  const offset = prefix.length + stripped.length - lineContent.length
  nextTick(() => {
    el.selectionStart = start + offset
    el.selectionEnd = end + offset
    el.focus()
  })
}

function wrapMd(before, after) {
  const el = editorRef.value
  if (!el) return
  const start = el.selectionStart
  const end = el.selectionEnd
  const selected = body.value.slice(start, end) || 'text'

  // Check if already wrapped — if so, unwrap
  const prefixStart = start - before.length
  const suffixEnd = end + after.length
  if (
    prefixStart >= 0 &&
    suffixEnd <= body.value.length &&
    body.value.slice(prefixStart, start) === before &&
    body.value.slice(end, suffixEnd) === after
  ) {
    // Unwrap
    body.value = body.value.slice(0, prefixStart) + selected + body.value.slice(suffixEnd)
    nextTick(() => {
      el.selectionStart = prefixStart
      el.selectionEnd = prefixStart + selected.length
      el.focus()
    })
    return
  }

  // Wrap
  body.value = body.value.slice(0, start) + before + selected + after + body.value.slice(end)
  nextTick(() => {
    el.selectionStart = start + before.length
    el.selectionEnd = start + before.length + selected.length
    el.focus()
  })
}

// --- Markdown preview ---
import { marked } from 'marked'

const renderedPreview = computed(() => marked(body.value || ''))

async function loadEntry() {
  const data = await $fetch('/api/entry-content', {
    params: { filename }
  })
  frontmatter.value = data.frontmatter
  body.value = data.body

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

<style scoped>
.toolbar-btn {
  @apply px-2 py-1 text-xs border border-gray-300 rounded hover:bg-gray-100 text-gray-700 cursor-pointer;
}
</style>
