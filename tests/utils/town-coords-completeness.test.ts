import { describe, it, expect } from 'vitest'
import townCoords from '~/data/town-coords.json'
import segmentsJson from '~/data/segments.json'
import pointsConfig from '~/data/competition/points-config.json'

// Completeness assertion for #487.
//
// town-coords.json is the coordinate source the map/labels resolve town and
// climb positions against. Every town named in segments.json[].towns[] and
// every climb named in points-config.json#climbs[].name must therefore have a
// key here — otherwise a declared place silently has no coordinate and cannot
// be placed. This guard fires red the moment a new town/climb name is declared
// without a matching coord (the parallel-source-of-truth detector pattern).

const coordKeys = new Set(Object.keys(townCoords as Record<string, unknown>))

// Documented allowlist: climbs declared in points-config that intentionally
// have no town-coords entry. Each MUST reference an open issue tracking whether
// it is an intended omission or a genuine gap — never patch town-coords.json
// silently inside a test strand.
//
// - 'Côte de Malemort' (#655): km-5 cat-4 marker (aso:false). Disposition
//   (add coord vs intended omission) tracked in #655.
const CLIMB_COORD_ALLOWLIST = new Set<string>(['Côte de Malemort'])

describe('town-coords completeness (#487)', () => {
  it('every segments.json town has a town-coords entry', () => {
    const towns = new Set<string>()
    for (const seg of segmentsJson as Array<{ towns?: string[] }>) {
      for (const t of seg.towns || []) towns.add(t)
    }
    const missing = [...towns].filter(t => !coordKeys.has(t)).sort()
    expect(missing, `towns missing a town-coords entry: ${missing.join(', ')}`).toEqual([])
  })

  it('every points-config climb has a town-coords entry (except documented allowlist)', () => {
    const missing = pointsConfig.climbs
      .map(c => c.name)
      .filter(name => !coordKeys.has(name) && !CLIMB_COORD_ALLOWLIST.has(name))
      .sort()
    expect(missing, `climbs missing a town-coords entry: ${missing.join(', ')}`).toEqual([])
  })

  it('allowlisted climbs are still genuinely absent (prune the allowlist once they gain a coord)', () => {
    // Keeps the allowlist honest: if #655 adds the coord, this fails and forces
    // removing the allowlist entry rather than leaving dead exceptions behind.
    const stale = [...CLIMB_COORD_ALLOWLIST].filter(name => coordKeys.has(name)).sort()
    expect(stale, `allowlisted climbs that now HAVE a coord — remove from allowlist: ${stale.join(', ')}`).toEqual([])
  })
})
