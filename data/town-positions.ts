// Canonical km positions for towns along the Stage 9 route.
//
// Each value is the cumulative km along the route GPX track, measured from
// the closest approach of the route to the town center. This is the authoritative
// source for `town -> km` used by both ElevationChart.vue (for elevation chart labels)
// and StageDetails.vue (for the stage details card town list).
//
// Values marked "verified" were measured by running the master GPX track against
// the town coordinates during the investigation for issue #321 on 2026-04-11.
// Other values are carried forward unchanged from the previous hardcoded table
// in ElevationChart.vue and are approximate. A separate audit of those values
// is tracked in issue #341 (processing/split_gpx.py root-cause fix).

export const townKmPositions: Record<string, number> = {
  'Malemort': 0,
  'Brive-la-Gaillarde': 4.5,
  'Turenne': 11.91,          // verified 2026-04-11, closest approach 91m from castle
  'Ligneyrac': 17.11,        // verified 2026-04-11, 628m south of route
  'Collonges-la-Rouge': 21.75, // verified 2026-04-11, first arrival (219m from village)
  'Meyssac': 23.70,          // verified 2026-04-11, 277m from village
  'Lanteuil': 38.35,         // verified 2026-04-21, 115m from village (seg 6)
  'Beynat': 46.23,           // verified 2026-04-21, 75m from village (seg 7; previously mispinned at 37.5)
  'Tulle': 65.5,
  'Naves': 73.5,
  'Chaumeil': 90,
  'Treignac': 116.5,
  'Bugeat': 130,
  'Meymac': 157.5,
  'Ussel': 182.5,
}
