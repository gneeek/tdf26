import { describe, it, expect } from 'vitest'
import Database from 'better-sqlite3'

describe('better-sqlite3 native binding', () => {
  it('loads and runs a trivial query', () => {
    const db = new Database(':memory:')
    try {
      const row = db.prepare('SELECT 1 AS value').get()
      expect(row).toEqual({ value: 1 })
    } finally {
      db.close()
    }
  })
})
