import { describe, it, expect } from 'vitest'
import manifest from '~/data/verification.json'
import { resolveTarget, driftedFields, type VerificationRecord } from '~/utils/verification'

// Verification audit-trail assertion (#476).
//
// data/verification.json snapshots the verified field values of canonical-data
// targets (currently the climbs corrected & verified by geometry-drift #650).
// This test re-resolves each target against live data and fails if a verified
// field changed without the snapshot (and its provenance) being updated in the
// same change. That is the mechanism that makes a silent edit to verified data
// detectable: you cannot quietly change a points-config climb gradient/km/length
// without this going red and forcing a re-audit bump.

const records = manifest.records as VerificationRecord[]

describe('verification audit-trail (#476)', () => {
  it('has at least one verification record (the trail is live, not empty)', () => {
    expect(records.length).toBeGreaterThan(0)
  })

  it('every record carries complete provenance', () => {
    const isoDate = /^\d{4}-\d{2}-\d{2}$/
    for (const r of records) {
      expect(r.target, 'record.target').toBeTruthy()
      expect(Array.isArray(r.fields) && r.fields.length > 0, `${r.target} fields`).toBe(true)
      expect(r.verifiedOn, `${r.target} verifiedOn`).toMatch(isoDate)
      expect(r.pr, `${r.target} pr`).toBeTruthy()
      expect(r.source, `${r.target} source`).toBeTruthy()
    }
  })

  it('every record target resolves to live data', () => {
    const unresolved = records.filter(r => resolveTarget(r.target) === null).map(r => r.target)
    expect(unresolved, `unresolved verification targets: ${unresolved.join(', ')}`).toEqual([])
  })

  it('no verified field has changed without a re-audit bump', () => {
    const offenders: string[] = []
    for (const r of records) {
      const live = resolveTarget(r.target)
      for (const d of driftedFields(r, live)) {
        offenders.push(`${r.target}.${d.field}: verified ${JSON.stringify(d.recorded)} -> live ${JSON.stringify(d.live)}`)
      }
    }
    expect(
      offenders,
      offenders.length
        ? `Verified field(s) changed without updating data/verification.json (value + verifiedOn/pr/source):\n  ${offenders.join('\n  ')}`
        : '',
    ).toEqual([])
  })
})
