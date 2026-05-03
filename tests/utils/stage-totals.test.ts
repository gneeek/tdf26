import { describe, it, expect } from 'vitest'

import pointsConfig from '~/data/competition/points-config.json'
import { CATEGORIZED_CLIMBS } from '~/utils/stage-totals'

// Drift detector. CATEGORIZED_CLIMBS must equal points-config.json's
// climbs[].name. #369 surfaced exactly this drift: Côte de Malemort was added
// to points-config (so KOM points were awarded) but stayed out of the
// hand-maintained set, so the seg-1 stage-details card silently omitted it.
// This test is the structural guarantee — failing here means the two surfaces
// have diverged again.
describe('CATEGORIZED_CLIMBS vs points-config.json', () => {
  const declared = new Set<string>(pointsConfig.climbs.map(c => c.name))

  it('contains every climb declared in points-config.json', () => {
    for (const name of declared) {
      expect(CATEGORIZED_CLIMBS.has(name)).toBe(true)
    }
  })

  it('contains no climbs not declared in points-config.json', () => {
    for (const name of CATEGORIZED_CLIMBS) {
      expect(declared.has(name)).toBe(true)
    }
  })

  it('has the same size as the declared set', () => {
    expect(CATEGORIZED_CLIMBS.size).toBe(declared.size)
  })
})
