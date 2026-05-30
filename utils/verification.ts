import pointsConfig from '~/data/competition/points-config.json'
import segmentsJson from '~/data/segments.json'

// Verification audit-trail resolver (#476).
//
// A verification record names a `target` (a stable address into the canonical
// data) and a snapshot of the field values that were verified. resolveTarget()
// returns the LIVE object the target addresses, so the assertion can compare the
// recorded snapshot against current data and detect a silent edit to a verified
// field. Keep this purely mechanical — it is an integrity check, not prose.
//
// Supported target forms:
//   points-config:climb:<name>   -> the climbs[] entry with that canonical name
//   segments:<segmentNumber>     -> the segments.json entry with that segment id
// Extend here (not in the manifest or the test) when a new target kind is needed.

export interface VerificationRecord {
  target: string
  fields: string[]
  values: Record<string, unknown>
  verifiedOn: string
  pr: string
  source: string
}

type LiveObject = Record<string, unknown> | null

export function resolveTarget(target: string): LiveObject {
  const [kind, ...rest] = target.split(':')

  if (kind === 'points-config' && rest[0] === 'climb') {
    const name = rest.slice(1).join(':')
    const climb = (pointsConfig.climbs as Array<Record<string, unknown>>).find(
      c => c.name === name,
    )
    return climb ?? null
  }

  if (kind === 'segments') {
    const segNo = Number(rest[0])
    const seg = (segmentsJson as Array<Record<string, unknown>>).find(
      s => s.segment === segNo,
    )
    return seg ?? null
  }

  return null
}

export interface FieldDrift {
  field: string
  recorded: unknown
  live: unknown
}

// Returns the fields whose live value differs from the recorded snapshot, plus
// any field that is missing from the resolved object. An empty array means the
// verification is still valid.
export function driftedFields(record: VerificationRecord, live: LiveObject): FieldDrift[] {
  if (live === null) {
    return record.fields.map(field => ({ field, recorded: record.values[field], live: undefined }))
  }
  const drift: FieldDrift[] = []
  for (const field of record.fields) {
    if (live[field] !== record.values[field]) {
      drift.push({ field, recorded: record.values[field], live: live[field] })
    }
  }
  return drift
}
