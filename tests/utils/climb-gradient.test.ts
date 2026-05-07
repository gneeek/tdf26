import { describe, it, expect } from 'vitest'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import pointsConfig from '~/data/competition/points-config.json'
import segmentsJson from '~/data/segments.json'

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
// wrong (e.g., on a rising flank past the actual GPX peak); that is a
// different invariant and the subject of a separate follow-up.
//
// Second instance of the per-source-of-truth detector pattern — first instance
// landed in PR #448 (stage-totals derives uniqueCategorizedClimbs from the
// same source as CATEGORIZED_CLIMBS, asserting they agree). #490+#492 strand
// extends the regime to gradient × length × GPX-gain agreement.

interface Segment {
  segment: number
  km_start: number
  km_end: number
}

interface ElevationFile {
  distance: number[]
  elevation: number[]
}

const repoRoot = resolve(__dirname, '..', '..')

function loadElevation(segNum: number): ElevationFile {
  const p = resolve(repoRoot, `data/elevation/segment-${String(segNum).padStart(2, '0')}.json`)
  return JSON.parse(readFileSync(p, 'utf8')) as ElevationFile
}

function buildTrack(): Array<[number, number]> {
  const track: Array<[number, number]> = []
  for (const s of segmentsJson as Segment[]) {
    const ev = loadElevation(s.segment)
    for (let i = 0; i < ev.distance.length; i++) {
      track.push([s.km_start + ev.distance[i], ev.elevation[i]])
    }
  }
  track.sort((a, b) => a[0] - b[0])
  return track
}

function elevationAt(track: Array<[number, number]>, km: number): number {
  if (km <= track[0][0]) return track[0][1]
  if (km >= track[track.length - 1][0]) return track[track.length - 1][1]
  for (let i = 0; i < track.length - 1; i++) {
    if (track[i][0] <= km && km <= track[i + 1][0]) {
      const span = track[i + 1][0] - track[i][0]
      const t = span ? (km - track[i][0]) / span : 0
      return track[i][1] + t * (track[i + 1][1] - track[i][1])
    }
  }
  return track[track.length - 1][1]
}

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
