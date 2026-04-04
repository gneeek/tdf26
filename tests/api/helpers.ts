/**
 * Test helpers for server API endpoint tests.
 */

/** Create a mock H3 event with optional query and body. */
export function mockEvent(opts: { query?: Record<string, string>; body?: any } = {}) {
  return {
    _query: opts.query || {},
    _body: opts.body || {},
  }
}
