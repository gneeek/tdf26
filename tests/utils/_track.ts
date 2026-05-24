import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import segmentsJson from '~/data/segments.json'

export interface Segment {
  segment: number
  km_start: number
  km_end: number
}

export interface ElevationFile {
  distance: number[]
  elevation: number[]
}

const repoRoot = resolve(__dirname, '..', '..')

export function loadElevation(segNum: number): ElevationFile {
  const p = resolve(repoRoot, `data/elevation/segment-${String(segNum).padStart(2, '0')}.json`)
  return JSON.parse(readFileSync(p, 'utf8')) as ElevationFile
}

export function buildTrack(): Array<[number, number]> {
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

export function elevationAt(track: Array<[number, number]>, km: number): number {
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
