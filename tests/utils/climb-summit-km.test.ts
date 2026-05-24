import { describe, it, expect } from 'vitest'

import pointsConfig from '~/data/competition/points-config.json'
import { buildTrack, elevationAt } from './_track'

// Per-source-of-truth assertion for the declared climb summit km. For every
// climb with non-null length_km, the GPX elevation argmax within
// [summit_km - length_km, summit_km + UPPER_PAD_KM] must sit within
// ±TOLERANCE_KM and ±TOLERANCE_M of the declared summit. Catches the bug
// class where the declared summit km sits on a rising flank, missing the
// actual local elevation peak (Naves pre-PR-#516: declared 76.59, true
// peak at 77.45, +30 m higher).
//
// Sibling to climb-gradient.test.ts (#490+#492). Where that assertion checks
// the gradient × length × GPX-gain agreement over the declared span, this
// assertion checks the placement of the summit point itself. They are
// orthogonal — Naves passed gradient internal-consistency at its pre-fix
// position (the declared span [73.79, 76.59] derived 5.54% against declared
// 5.6%); only this assertion catches summit-km drift.
//
// Window design (strand #518): asymmetric `[summit - length_km, summit + 1.5]`.
// Symmetric ±length_km crosses into adjacent terrain on this stage (climbs
// sit 5-20 km apart, length_km up to 7 km), so the argmax picks up an
// unrelated later peak. The 1.5 km upper pad catches Naves-class drift
// (~0.86 km) with margin and stays inside Naves's local terrain (the
// adjacent rise at km 79.82 sits 2.37 km past the post-fix Naves summit,
// safely outside the upper pad).
//
// Tolerance rationale: elevation sample spacing is ~0.25–0.31 km, which is
// a structural floor on km-tolerance. 0.35 km sits just above the floor;
// 10 m elevation tolerance is ~2× the typical peak-to-adjacent-sample drop
// at the climbs in this dataset.

interface Climb {
  name: string
  segment: number
  km: number
  length_km: number | null
  gradient: number
}

const TOLERANCE_KM = 0.35
const TOLERANCE_M = 10
const UPPER_PAD_KM = 1.5

// Climbs whose declared summit km is known to drift from the GPX argmax.
// Each maps to the follow-up issue tracking the data fix. The assertion
// is asserted-but-skipped for these; remove from the map when the data
// fix lands (see PR that closes the referenced issue).
const KNOWN_FAILING: Record<string, number> = {
  'Côte de Lagleygeolle': 589,
  'Puy de Lachaud': 590,
  'Côte de la Croix de Pey': 591,
}

describe('points-config climb summit km vs GPX argmax', () => {
  const track = buildTrack()

  for (const climb of pointsConfig.climbs as Climb[]) {
    if (climb.length_km == null) continue
    const winLow = climb.km - climb.length_km
    const winHigh = climb.km + UPPER_PAD_KM
    const knownFailIssue = KNOWN_FAILING[climb.name]
    const testFn = knownFailIssue ? it.skip : it
    const titleSuffix = knownFailIssue ? ` [skipped: #${knownFailIssue}]` : ''
    testFn(`${climb.name}: declared summit km ${climb.km} matches GPX argmax in [${winLow.toFixed(2)}, ${winHigh.toFixed(2)}] within ±${TOLERANCE_KM} km / ±${TOLERANCE_M} m${titleSuffix}`, () => {
      let argmaxKm = climb.km
      let argmaxElev = -Infinity
      for (const [k, e] of track) {
        if (k < winLow) continue
        if (k > winHigh) break
        if (e > argmaxElev) {
          argmaxElev = e
          argmaxKm = k
        }
      }
      const declaredElev = elevationAt(track, climb.km)
      const dKm = argmaxKm - climb.km
      const dElev = argmaxElev - declaredElev

      const message = `argmax ${argmaxKm.toFixed(2)} km / ${argmaxElev.toFixed(1)} m vs declared ${climb.km} km / ${declaredElev.toFixed(1)} m; Δkm ${dKm >= 0 ? '+' : ''}${dKm.toFixed(2)}, Δelev ${dElev >= 0 ? '+' : ''}${dElev.toFixed(1)}`

      expect(Math.abs(dKm), `km drift: ${message}`).toBeLessThanOrEqual(TOLERANCE_KM)
      expect(Math.abs(dElev), `elevation drift: ${message}`).toBeLessThanOrEqual(TOLERANCE_M)
    })
  }
})
