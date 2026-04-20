interface Segment {
  segment: number
  km_start: number
  km_end: number
  elevation_gain: number
  elevation_loss: number
  towns?: string[]
  climbs?: string[]
}

export const CATEGORIZED_CLIMBS = new Set([
  'Puy Boubou',
  'Côte de Lagleygeolle',
  'Côte de Miel',
  'Côte des Naves',
  'Puy de Lachaud',
  'Suc au May',
  'Côte de la Croix de Pey',
  'Mont Bessou',
  'Côte des Gardes',
])

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
