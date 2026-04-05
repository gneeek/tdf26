import { computed, type Ref, type ComputedRef } from 'vue'

interface RiderEntry {
  id: string
  [key: string]: any
}

interface PointsData {
  sprintPoints: number
  climbPoints: number
  totalPoints: number
}

interface JerseyAssignments {
  yellow: string | null
  green: string | null
  polkaDot: string | null
  red: string | null
}

/**
 * Compute jersey assignments using Tour de France precedence rules.
 *
 * Precedence: yellow (race leader) > green (sprint) > polka dot (climbing) > red (lanterne rouge).
 * A rider can only hold one jersey; if they lead multiple classifications,
 * the less prestigious jersey passes to the next eligible rider.
 *
 * @param rankedRiders - riders sorted by place (1st to last), each with an `id` field
 * @param getPoints - function returning points data for a rider id
 * @param hasPoints - whether any riders have classification points yet
 */
export function useJerseys(
  rankedRiders: Ref<RiderEntry[]> | ComputedRef<RiderEntry[]>,
  getPoints: (riderId: string) => PointsData,
  hasPoints: Ref<boolean> | ComputedRef<boolean>,
): ComputedRef<JerseyAssignments> {
  return computed(() => {
    const riders = rankedRiders.value
    if (!riders.length) return { yellow: null, green: null, polkaDot: null, red: null }

    const taken = new Set<string>()

    // Yellow: race leader (place 1)
    const yellow = riders[0]?.id || null
    if (yellow) taken.add(yellow)

    // Green: highest sprint points, skipping riders with a more prestigious jersey
    let green: string | null = null
    if (hasPoints.value) {
      const sprintSorted = [...riders].sort((a, b) =>
        getPoints(b.id).sprintPoints - getPoints(a.id).sprintPoints
      )
      for (const r of sprintSorted) {
        if (getPoints(r.id).sprintPoints > 0 && !taken.has(r.id)) {
          green = r.id
          taken.add(r.id)
          break
        }
      }
    }

    // Polka dot: highest climb points
    let polkaDot: string | null = null
    if (hasPoints.value) {
      const climbSorted = [...riders].sort((a, b) =>
        getPoints(b.id).climbPoints - getPoints(a.id).climbPoints
      )
      for (const r of climbSorted) {
        if (getPoints(r.id).climbPoints > 0 && !taken.has(r.id)) {
          polkaDot = r.id
          taken.add(r.id)
          break
        }
      }
    }

    // Red (lanterne rouge): last place, only if not wearing another jersey
    let red: string | null = null
    if (riders.length > 1) {
      const lastRider = riders[riders.length - 1]?.id
      if (lastRider && !taken.has(lastRider)) {
        red = lastRider
      }
    }

    return { yellow, green, polkaDot, red }
  })
}

const jerseyEmojis: Record<string, string> = {
  yellow: '🟡',
  green: '🟢',
  polkaDot: '🔴',
  red: '🔻',
}

/**
 * Get the emoji for a rider's jersey, or empty string if they don't hold one.
 */
export function jerseyEmoji(
  jerseys: JerseyAssignments,
  riderId: string,
): string {
  for (const [type, holderId] of Object.entries(jerseys)) {
    if (holderId === riderId) return jerseyEmojis[type] || ''
  }
  return ''
}
