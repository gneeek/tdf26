/**
 * Canonical frontmatter parser for content/entries/*.md (issue #326).
 *
 * The single source of read/write logic for every server route that touches
 * entry frontmatter (entries.get, weather.get, images.get/post,
 * entry-status.post, weather-inject.post, entry-content.get/post). Replaces the
 * per-route hand-rolled regex parsers those files used to carry.
 *
 * This is the TypeScript twin of processing/frontmatter.py and shares
 * schemas/frontmatter.schema.json with it. Like the Python module it loads YAML
 * with js-yaml's JSON_SCHEMA so a bare ISO date (publishDate, dataCutoff) stays
 * a string instead of becoming a Date -- downstream code compares those as
 * strings.
 */
import yaml from 'js-yaml'

import schema from '~/schemas/frontmatter.schema.json'

// The frontmatter fence: group 1 the opening `---\n`, group 2 the YAML body
// (non-greedy, stops at the first closing fence), group 3 the `\n---`.
const FENCE_RE = /^(---\n)([\s\S]*?)(\n---)/
const HEAD_RE = /^---\n([\s\S]*?)\n---/

/** Frontmatter field names declared by the shared schema. */
export const FIELDS = Object.keys((schema as { properties: Record<string, unknown> }).properties)
/** Required frontmatter field names declared by the shared schema. */
export const REQUIRED = (schema as { required: string[] }).required

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Parse the YAML frontmatter of a markdown string into an object.
 * Returns {} when there is no frontmatter block or it is not a mapping.
 * Bare ISO dates stay strings (see module docstring).
 */
export function parseFrontmatter(content: string): Record<string, any> {
  const m = content.match(HEAD_RE)
  if (!m) return {}
  const data = yaml.load(m[1], { schema: yaml.JSON_SCHEMA })
  if (data === null || typeof data !== 'object' || Array.isArray(data)) return {}
  return data as Record<string, any>
}

/**
 * Split a markdown string into raw frontmatter text and body. Returns
 * { frontmatter: '', body: content } when there is no frontmatter block. The
 * frontmatter is the unparsed text between the fences; the body is everything
 * after the closing `---\n`. This is the shared primitive the entry-content
 * editor round-trip relies on (paired with joinFrontmatter).
 */
export function splitFrontmatter(content: string): { frontmatter: string, body: string } {
  const m = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!m) return { frontmatter: '', body: content }
  return { frontmatter: m[1], body: m[2] }
}

/** Reassemble a markdown file from raw frontmatter text and body. */
export function joinFrontmatter(frontmatter: string, body: string): string {
  return `---\n${frontmatter.trim()}\n---\n${body}`
}

/** True when content has a leading `---` frontmatter block. */
export function hasFrontmatter(content: string): boolean {
  return HEAD_RE.test(content)
}

/**
 * Return content with frontmatter field `key` set to the literal `value`.
 *
 * Surgical and byte-preserving: replaces the `key:` line in the frontmatter
 * block in place, or appends the field as the last frontmatter line (before the
 * closing `---`) when absent. `value` is inserted verbatim -- already formatted
 * by the caller (`true`, an ISO date, or a compact JSON string).
 *
 * If the existing value spans multiple YAML lines -- a block-style list such as
 *   images:
 *     - src: ...
 * -- the indented continuation lines are consumed too, so replacing a block
 * `images:` with an inline JSON array leaves no orphan `- src:` lines. For the
 * single-line fields every other route writes (weather, draft, publishDate,
 * dataCutoff) there are no continuation lines, so the result is byte-identical
 * to the regex replacers this consolidates. Unlike the old images.post it never
 * re-dumps the whole block, so sibling fields (and their exact bytes -- e.g. a
 * bare ISO `publishDate`) are preserved rather than reserialised.
 *
 * Content with no frontmatter block is returned unchanged.
 */
export function setField(content: string, key: string, value: string): string {
  const m = content.match(FENCE_RE)
  if (!m) return content
  const [, head, fmBody, tail] = m
  const rest = content.slice(m[0].length)
  const newLine = `${key}: ${value}`
  const keyRe = new RegExp(`^${escapeRegExp(key)}:`)

  const lines = fmBody.split('\n')
  const idx = lines.findIndex(line => keyRe.test(line))
  if (idx === -1) {
    return `${head}${fmBody}\n${newLine}${tail}${rest}`
  }
  // Consume any indented continuation lines belonging to a block-style value.
  let end = idx + 1
  while (end < lines.length && /^\s/.test(lines[end])) {
    end++
  }
  const newLines = [...lines.slice(0, idx), newLine, ...lines.slice(end)]
  return `${head}${newLines.join('\n')}${tail}${rest}`
}
