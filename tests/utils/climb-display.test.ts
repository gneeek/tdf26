import { describe, it, expect } from 'vitest'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { CLIMB_DISPLAY } from '~/utils/stage-totals'
import pointsConfig from '~/data/competition/points-config.json'

// Drift detector for the data-to-display consolidation (#517 #588 #486).
//
// StageDetails.vue (climb gradient + summit km) and ElevationChart.vue (summit
// km label placement) used to carry hand-maintained literal maps that disagreed
// with points-config.json on every gradient and on most summit km, and broke on
// accent/rename of the lookup key. They now derive from CLIMB_DISPLAY, which is
// built from points-config by the canonical climb name. These assertions fire
// red if (a) CLIMB_DISPLAY stops matching points-config, or (b) a component
// re-introduces a hardcoded climb literal — the two ways the old bug returns.

const COMPONENTS_DIR = resolve(__dirname, '..', '..', 'components')
const COMPONENTS = ['StageDetails.vue', 'ElevationChart.vue']

describe('CLIMB_DISPLAY is faithful to points-config', () => {
  it('exposes exactly the points-config climbs, keyed by canonical name', () => {
    const pcNames = pointsConfig.climbs.map(c => c.name).sort()
    const mapNames = [...CLIMB_DISPLAY.keys()].sort()
    expect(mapNames).toEqual(pcNames)
  })

  it('reports km, length_km and gradient byte-equal to points-config', () => {
    for (const c of pointsConfig.climbs) {
      const d = CLIMB_DISPLAY.get(c.name)
      expect(d, `${c.name} missing from CLIMB_DISPLAY`).toBeDefined()
      expect(d!.km, `${c.name} km`).toBe(c.km)
      expect(d!.length_km, `${c.name} length_km`).toBe(c.length_km)
      expect(d!.gradient, `${c.name} gradient`).toBe(c.gradient)
    }
  })
})

describe('components carry no hardcoded climb literal (consume CLIMB_DISPLAY only)', () => {
  for (const file of COMPONENTS) {
    it(`${file} imports CLIMB_DISPLAY and holds no climb-keyed literal`, () => {
      const src = readFileSync(resolve(COMPONENTS_DIR, file), 'utf-8')

      // Must consume the single derivation.
      expect(src, `${file} should import CLIMB_DISPLAY`).toMatch(/CLIMB_DISPLAY/)

      // Must NOT re-introduce a literal that maps a climb name to a number or an
      // object — the shape of the old climbData / climbSummitKm maps. Catches
      // e.g.  'Suc au May': 104.8  or  'Puy Boubou': { gradient: 9.9 }.
      const climbLiteral = /'(Côte|Puy|Suc|Mont)[^']*'\s*:\s*[{0-9]/
      expect(
        climbLiteral.test(src),
        `${file} contains a hardcoded climb literal; derive from CLIMB_DISPLAY instead`,
      ).toBe(false)

      // The retired variable names must not come back either.
      expect(src).not.toMatch(/\bclimbData\b/)
      expect(src).not.toMatch(/\bclimbSummitKm\b/)
    })
  }
})
