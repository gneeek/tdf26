import { describe, it, expect } from 'vitest'
import { sanitizeAttributionText } from '~/utils/sanitize'

describe('sanitizeAttributionText', () => {
  it('returns empty string for empty / null / undefined input', () => {
    expect(sanitizeAttributionText('')).toBe('')
    expect(sanitizeAttributionText(null)).toBe('')
    expect(sanitizeAttributionText(undefined)).toBe('')
  })

  it('passes plain text through unchanged', () => {
    expect(sanitizeAttributionText('Jean Dupont')).toBe('Jean Dupont')
    expect(sanitizeAttributionText('  Author Name  ')).toBe('Author Name')
  })

  it('strips a single tag wrapping an artist name (the common Wikipedia attribution shape)', () => {
    const input = '<a href="//commons.wikimedia.org/wiki/User:Jean">Jean Dupont</a>'
    expect(sanitizeAttributionText(input)).toBe('Jean Dupont')
  })

  it('strips nested-looking <<script>script> patterns (closes CodeQL js/incomplete-multi-character-sanitization)', () => {
    // A single-pass /<[^>]*>/g leaves "<script" in the output.
    // The fix is to loop until stable; the assertion is that no "<script"
    // substring survives.
    const result = sanitizeAttributionText('<<script>script>alert(1)<</script>/script>')
    expect(result.toLowerCase()).not.toContain('<script')
    expect(result.toLowerCase()).not.toContain('</script')
  })

  it('decodes &amp;amp; to &amp; (closes CodeQL js/double-escaping)', () => {
    // Naive: replace(/&amp;/g, '&') applied after stripping turns "&amp;amp;"
    // into "&" via two passes. The fix is single-pass entity decoding.
    expect(sanitizeAttributionText('&amp;amp;')).toBe('&amp;')
  })

  it('decodes the standard named entities exactly once', () => {
    expect(sanitizeAttributionText('Tom &amp; Jerry')).toBe('Tom & Jerry')
    expect(sanitizeAttributionText('a &lt; b')).toBe('a < b')
    expect(sanitizeAttributionText('a &gt; b')).toBe('a > b')
    expect(sanitizeAttributionText('she said &quot;hi&quot;')).toBe('she said "hi"')
    expect(sanitizeAttributionText('it&apos;s')).toBe("it's")
  })

  it('decodes numeric entities (decimal and hex)', () => {
    expect(sanitizeAttributionText('it&#39;s')).toBe("it's")
    expect(sanitizeAttributionText('it&#x27;s')).toBe("it's")
    expect(sanitizeAttributionText('caf&#233;')).toBe('café')
  })

  it('strips tags first, then decodes entities (so &lt;script&gt; survives as text)', () => {
    // After strip there are no "<...>" substrings to remove. Decoding then
    // gives back the literal text "<script>". Vue's text interpolation
    // re-escapes this at render time, so it is safe to leave as text.
    expect(sanitizeAttributionText('&lt;script&gt;')).toBe('<script>')
  })

  it('handles a realistic Wikipedia Artist field with mixed markup and entities', () => {
    const input = '<a href="//commons.wikimedia.org/wiki/User:Marie">Marie &amp; Pierre Curie</a>'
    expect(sanitizeAttributionText(input)).toBe('Marie & Pierre Curie')
  })

  it('trims surrounding whitespace left after tag removal', () => {
    expect(sanitizeAttributionText('  <span>Hello</span>  ')).toBe('Hello')
  })
})
