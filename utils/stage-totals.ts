import pointsConfig from '~/data/competition/points-config.json'

interface Segment {
  segment: number
  km_start: number
  km_end: number
  elevation_gain: number
  elevation_loss: number
  towns?: string[]
  climbs?: string[]
}

// Derived from points-config.json's climbs[].name, which self-describes as the
// single source of truth for climb identity. Adding/removing/renaming a climb
// in points-config flows through to stage-details rendering with no second
// edit. tests/utils/stage-totals.test.ts asserts this set stays in sync.
export const CATEGORIZED_CLIMBS: Set<string> = new Set(
  pointsConfig.climbs.map(c => c.name),
)

// Per-climb display values (summit km, length, gradient) derived directly from
// points-config.json keyed by the canonical climb name. This is the single
// derivation consumed by both StageDetails.vue (gradient + summit km) and
// ElevationChart.vue (summit km label placement). It replaces the hand-kept
// `climbData` / `climbSummitKm` literals those components used to carry, which
// drifted from points-config (#517 #588 #486) and broke on accent/rename of the
// lookup key. Deriving by the canonical name removes the key-drift surface
// entirely. tests/utils/climb-display.test.ts asserts this map stays byte-equal
// to points-config so a re-introduced literal would fire red.
export interface ClimbDisplay {
  name: string
  /** Cumulative km of the scored summit along the full stage. */
  km: number
  /** Climb length in km; null where points-config leaves it unset. */
  length_km: number | null
  /** Average gradient, per cent. */
  gradient: number
}

export const CLIMB_DISPLAY: Map<string, ClimbDisplay> = new Map(
  pointsConfig.climbs.map(c => [
    c.name,
    { name: c.name, km: c.km, length_km: c.length_km, gradient: c.gradient },
  ]),
)

export interface StageTotals {
  totalDistance: number
  totalElevationGain: number
  totalElevationLoss: number
  uniqueTowns: string[]
  uniqueClimbs: string[]
  uniqueCategorizedClimbs: string[]
}

export interface JourneyProgress {
  kmRidden: number
  elevationClimbed: number
  climbsPassed: string[]
  categorizedClimbsPassed: string[]
  townsVisited: string[]
}

export function deriveTotals(segments: Segment[]): StageTotals {
  const towns = new Set<string>()
  const climbs = new Set<string>()
  let totalElevationGain = 0
  let totalElevationLoss = 0

  for (const seg of segments) {
    for (const t of seg.towns || []) towns.add(t)
    for (const c of seg.climbs || []) climbs.add(c)
    totalElevationGain += seg.elevation_gain
    totalElevationLoss += seg.elevation_loss
  }

  return {
    totalDistance: segments.length ? segments[segments.length - 1].km_end : 0,
    totalElevationGain,
    totalElevationLoss,
    uniqueTowns: Array.from(towns),
    uniqueClimbs: Array.from(climbs),
    uniqueCategorizedClimbs: Array.from(climbs).filter(c => CATEGORIZED_CLIMBS.has(c)),
  }
}

export function journeyThroughSegment(segments: Segment[], latestSegmentNumber: number): JourneyProgress {
  const passed = segments.filter(s => s.segment <= latestSegmentNumber)
  const climbs = new Set<string>()
  const towns = new Set<string>()
  let elevationClimbed = 0
  let kmRidden = 0

  for (const seg of passed) {
    for (const c of seg.climbs || []) climbs.add(c)
    for (const t of seg.towns || []) towns.add(t)
    elevationClimbed += seg.elevation_gain
    kmRidden = seg.km_end
  }

  return {
    kmRidden,
    elevationClimbed,
    climbsPassed: Array.from(climbs),
    categorizedClimbsPassed: Array.from(climbs).filter(c => CATEGORIZED_CLIMBS.has(c)),
    townsVisited: Array.from(towns),
  }
}
