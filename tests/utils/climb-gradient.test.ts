import { describe, it, expect } from 'vitest'

import pointsConfig from '~/data/competition/points-config.json'
import { buildTrack, elevationAt } from './_track'

// Per-source-of-truth assertion. For every climb declared in points-config.json
// with a non-null length_km, the declared gradient must match the gradient
// derived from data/elevation/segment-NN.json over the declared span
// [summit_km - length_km, summit_km], within ±0.3 percentage points.
//
// This sits alongside processing/validate_points.py invariant 4 (which uses a
// ±20% relative tolerance, generous enough to admit ~1pp drift on a 5%-grade
// climb). The TS assertion is the tighter sibling — it catches the case where
// the gradient field is rounded incorrectly or stale relative to the declared
// span. It does NOT catch the case where the declared summit km itself is
// wrong (e.g., on a rising flank past the actual GPX peak); the sibling
// assertion in climb-summit-km.test.ts (#518) handles that bug class.
//
// Second instance of the per-source-of-truth detector pattern — first instance
// landed in PR #448 (stage-totals derives uniqueCategorizedClimbs from the
// same source as CATEGORIZED_CLIMBS, asserting they agree). #490+#492 strand
// extends the regime to gradient × length × GPX-gain agreement.

const TOLERANCE_PP = 0.3

describe('points-config climb gradient vs GPX elevation', () => {
  const track = buildTrack()

  for (const climb of pointsConfig.climbs) {
    if (climb.length_km == null) continue
    it(`${climb.name}: declared ${climb.gradient}% matches GPX over [${(climb.km - climb.length_km).toFixed(2)}, ${climb.km}] within ±${TOLERANCE_PP}pp`, () => {
      const summit = elevationAt(track, climb.km)
      const start = elevationAt(track, climb.km - climb.length_km)
      const gain = summit - start
      const derived = (gain / (climb.length_km * 1000)) * 100
      const diff = climb.gradient - derived
      expect(
        Math.abs(diff),
        `declared ${climb.gradient.toFixed(2)}% vs GPX-derived ${derived.toFixed(2)}% (gain ${gain.toFixed(1)}m / ${climb.length_km}km); diff ${diff >= 0 ? '+' : ''}${diff.toFixed(2)}pp`,
      ).toBeLessThanOrEqual(TOLERANCE_PP)
    })
  }
})
