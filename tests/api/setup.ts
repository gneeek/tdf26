/**
 * Vitest setup file for API tests.
 * Sets up Nuxt server auto-import globals before any test modules load.
 */

// defineEventHandler just returns the handler function
;(globalThis as any).defineEventHandler = (fn: Function) => fn

// readBody returns the event's body
;(globalThis as any).readBody = (event: any) => Promise.resolve(event._body)

// getQuery returns the event's query
;(globalThis as any).getQuery = (event: any) => event._query

// createError creates an Error with statusCode
;(globalThis as any).createError = (opts: { statusCode: number; message: string }) => {
  const err = new Error(opts.message) as any
  err.statusCode = opts.statusCode
  return err
}
