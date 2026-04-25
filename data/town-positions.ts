// Canonical km positions for towns along the Stage 9 route.
//
// Each value is the cumulative km along the route GPX track, measured from
// the closest approach of the route to the town center. This is the authoritative
// source for `town -> km` used by both ElevationChart.vue (for elevation chart labels)
// and StageDetails.vue (for the stage details card town list).
//
// All values were re-verified against `processing/audit_segment_data.py` on
// 2026-04-25 as part of the v1.4.8 segment-data correctness audit (#413). Six
// mid/late-route values were updated to the audit's computed km after the
// pre-audit values (carried forward from the original ElevationChart.vue
// hardcoded table) drifted by 3-14 km.

export const townKmPositions: Record<string, number> = {
  'Malemort': 0,
  'Brive-la-Gaillarde': 4.5,    // off-route landmark, 2573m north at start
  'Turenne': 11.91,              // 7m from route (closest approach)
  'Ligneyrac': 17.11,            // 628m south of route
  'Collonges-la-Rouge': 21.75,   // 139m from village (first arrival)
  'Meyssac': 23.70,              // 277m from village
  'Lanteuil': 38.35,             // 115m from village (seg 6)
  'Beynat': 46.23,               // 75m from village (seg 7)
  'Tulle': 68.72,                // updated 2026-04-25, 120m from cathedral
  'Naves': 78.19,                // updated 2026-04-25, 373m from village; seg 12
  'Chaumeil': 100.30,            // updated 2026-04-25, 35m from village; seg 15
  'Treignac': 121.95,            // updated 2026-04-25, 22m from village; seg 18
  'Bugeat': 143.67,              // updated 2026-04-25, 23m from village; seg 21
  'Meymac': 168.15,              // updated 2026-04-25, 47m from village; seg 25
  'Ussel': 182.5,                // route-entry point (city centre is 2.5km north of route)
}
