import { describe, it, expect } from 'vitest'

import segmentsJson from '~/data/segments.json'
import { townKmPositions } from '~/data/town-positions'

// Drift detector. Every town named in segments.json[].towns must have a
// corresponding km position in townKmPositions, otherwise StageDetails.vue
// and ElevationChart.vue fall back to seg.km_start (a coarse approximation)
// when rendering the town. Off-route landmarks (e.g. Brive-la-Gaillarde,
// which doesn't appear in segments.json[].towns) are intentionally allowed
// as extras — this is a coverage assertion, not an equality assertion.
//
// This was added when #474 surfaced that 'Sainte-Fortunade' (a seg-9 town
// added in v1.4.x) had no townKmPositions entry and was therefore being
// rendered at seg.km_start = 56 instead of its actual route km of 60.02.
describe('townKmPositions vs segments.json', () => {
  const segmentTowns = new Set<string>(
    segmentsJson.flatMap((s: { towns?: string[] }) => s.towns ?? []),
  )

  it('covers every town named in segments.json[].towns', () => {
    for (const town of segmentTowns) {
      expect(
        townKmPositions[town],
        `missing townKmPositions entry for "${town}"`,
      ).toBeTypeOf('number')
    }
  })
})
