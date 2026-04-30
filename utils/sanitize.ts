// Wikipedia attribution metadata may carry HTML markup and entity escapes.
// We render those values as plain text (Vue {{ }} interpolation, never v-html),
// so the goal of this module is "give me a clean text version."
//
// Two failure modes the previous hand-rolled regex hit (CodeQL #4-#10):
//   - Single-pass /<[^>]*>/g leaves nested patterns like "<<script>script>"
//     partially intact. Fix: loop until the strip is stable. This is the
//     canonical fix recommended by the CodeQL js/incomplete-multi-character-
//     sanitization rule documentation.
//   - Decoding "&amp;" after stripping turns "&amp;amp;" into "&" via two
//     passes — fresh "&" characters that an earlier escape meant to neutralise
//     get re-decoded. Fix: single-pass entity decoding via one regex with a
//     replacer, no rescans.
//
// Order matters: strip tags first, decode entities second. That way "&lt;script&gt;"
// survives the strip (it has no real "<...>" substrings), then decodes to the
// literal text "<script>". Vue re-escapes that at render time.

const NAMED_ENTITIES: Record<string, string> = {
  amp: '&',
  lt: '<',
  gt: '>',
  quot: '"',
  apos: "'",
}

function decodeEntitiesOnce(input: string): string {
  return input.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (match, name: string) => {
    const lower = name.toLowerCase()
    if (lower.startsWith('#x')) {
      const code = parseInt(lower.slice(2), 16)
      return Number.isFinite(code) ? String.fromCodePoint(code) : match
    }
    if (lower.startsWith('#')) {
      const code = parseInt(lower.slice(1), 10)
      return Number.isFinite(code) ? String.fromCodePoint(code) : match
    }
    return NAMED_ENTITIES[lower] ?? match
  })
}

function stripTagsUntilStable(input: string): string {
  let prev: string
  let s = input
  do {
    prev = s
    s = s.replace(/<[^>]*>/g, '')
  } while (s !== prev)
  return s
}

export function sanitizeAttributionText(input: string | null | undefined): string {
  if (!input) return ''
  return decodeEntitiesOnce(stripTagsUntilStable(input)).trim()
}
