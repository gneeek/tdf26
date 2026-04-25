#!/usr/bin/env python3
"""Validate that climb and sprint assignments in points-config.json agree with segments.json.

points-config.json is the single source of truth for climb and sprint identity,
summit/sprint km, and (for climbs) span via length_km. segments.json is generated
by split_gpx.py and carries a derived `climbs` list per segment.

This script enforces two invariants:

1. Every climb's summit km falls within the km range of its declared segment.
2. Every climb name appears in the `climbs` list of every segment whose km range
   intersects the climb's span (from km - length_km to km). Climbs with length_km
   null are treated as summit-only and must appear in exactly the summit segment.

Sprints are checked for invariant 1 only (they are points, not spans, and are
not currently materialised in segments.json).

#369: also cross-checks climb summit km against GPX elevation data:

3. The route was climbing into the declared summit (elevation 1km before summit
   is not higher than elevation at summit). Catches summits declared on a
   descending flank past the actual peak.
4. Declared length and gradient match the GPX elevation gain over the climb's
   span — actual gain over [summit_km - length, summit_km] is within tolerance
   of length * gradient / 100.

Exits non-zero if any invariant is violated.
"""

import argparse
import json
import os
import sys


def load_json(path):
    with open(path) as f:
        return json.load(f)


# Tolerances for the elevation cross-check (#369).
# A summit can sit a few metres below the elevation 1 km earlier (rounding
# noise, smoothing artefacts), but a descent of more than this means the
# declared summit is on a descending flank past the real peak.
ELEVATION_RISING_INTO_SUMMIT_TOL_M = 5.0
# Relative tolerance for gradient consistency: actual gain over the climb span
# may differ from `length × gradient / 100` by this fraction. 20% accommodates
# rounding in the gradient field (one decimal place) plus the elevation-data
# smoothing window in elevation_profile.py.
GRADIENT_CONSISTENCY_REL_TOL = 0.20


def load_elevation_track(elevation_dir, segments):
    """Concatenate per-segment elevation files into a single (cum_km, ele) sequence.

    Each `data/elevation/segment-NN.json` carries segment-relative distances;
    we lift them to cumulative km using the segment's km_start.
    """
    track = []
    for s in segments:
        path = os.path.join(elevation_dir, f"segment-{s['segment']:02d}.json")
        if not os.path.exists(path):
            continue
        d = load_json(path)
        for dist, ele in zip(d.get("distance", []), d.get("elevation", [])):
            track.append((s["km_start"] + dist, ele))
    track.sort()
    return track


def elevation_at_km(track, target_km):
    """Linearly interpolate elevation at target_km."""
    if not track:
        return None
    if target_km <= track[0][0]:
        return track[0][1]
    if target_km >= track[-1][0]:
        return track[-1][1]
    for i in range(len(track) - 1):
        if track[i][0] <= target_km <= track[i + 1][0]:
            span = track[i + 1][0] - track[i][0]
            t = (target_km - track[i][0]) / span if span else 0
            return track[i][1] + t * (track[i + 1][1] - track[i][1])
    return track[-1][1]


def validate_elevation(climbs, track):
    """Cross-check climb summit km against the GPX elevation profile.

    Catches the original Puy Boubou bug (summit declared on a descending flank
    past the real peak): if elevation 1 km before the declared summit is higher
    than elevation at the summit, the declaration is wrong.

    Also cross-checks length × gradient against the actual GPX gain over the
    climb span. Climbs with length_km=None (point-summit climbs) skip the
    second check.
    """
    errors = []
    if not track:
        return errors
    for c in climbs:
        name = c["name"]
        summit_km = c["km"]
        length = c.get("length_km")
        gradient = c.get("gradient")

        ele_at_summit = elevation_at_km(track, summit_km)
        ele_1km_before = elevation_at_km(track, summit_km - 1.0)
        if ele_at_summit is None or ele_1km_before is None:
            continue

        if ele_at_summit < ele_1km_before - ELEVATION_RISING_INTO_SUMMIT_TOL_M:
            errors.append(
                f"climb {name!r}: summit km {summit_km} elevation {ele_at_summit:.0f}m "
                f"is below elevation 1km earlier ({ele_1km_before:.0f}m) — "
                f"declared summit may be on a descending flank past the real peak"
            )

        if length is not None and gradient is not None and length > 0:
            ele_at_start = elevation_at_km(track, summit_km - length)
            if ele_at_start is None:
                continue
            actual_gain = ele_at_summit - ele_at_start
            expected_gain = length * gradient * 10  # length(km) * gradient(%) * 10 = m
            if abs(expected_gain) > 1.0:
                rel_err = (actual_gain - expected_gain) / abs(expected_gain)
                if abs(rel_err) > GRADIENT_CONSISTENCY_REL_TOL:
                    errors.append(
                        f"climb {name!r}: declared {gradient}% over {length}km expects "
                        f"{expected_gain:.0f}m gain; GPX shows {actual_gain:.0f}m "
                        f"({rel_err * 100:+.0f}% from expected, tolerance ±{int(GRADIENT_CONSISTENCY_REL_TOL * 100)}%)"
                    )
    return errors


def segment_containing_km(segments, km):
    """Return the segment dict whose [km_start, km_end] contains km, or None."""
    for s in segments:
        if s["km_start"] <= km <= s["km_end"]:
            return s
    return None


def validate(points_config, segments):
    errors = []
    segments_by_number = {s["segment"]: s for s in segments}

    for climb in points_config.get("climbs", []):
        name = climb["name"]
        declared_seg = climb["segment"]
        summit_km = climb["km"]
        length_km = climb.get("length_km")

        seg = segments_by_number.get(declared_seg)
        if seg is None:
            errors.append(f"climb {name!r}: declared segment {declared_seg} not found in segments.json")
            continue

        if not (seg["km_start"] <= summit_km <= seg["km_end"]):
            errors.append(
                f"climb {name!r}: summit km {summit_km} falls outside declared "
                f"segment {declared_seg} range [{seg['km_start']}, {seg['km_end']}]"
            )

        if length_km is None:
            expected_segments = {declared_seg}
        else:
            km_start = summit_km - length_km
            km_end = summit_km
            expected_segments = {
                s["segment"] for s in segments
                if s["km_start"] < km_end and s["km_end"] > km_start
            }

        actual_segments = {
            s["segment"] for s in segments if name in (s.get("climbs") or [])
        }

        missing = expected_segments - actual_segments
        extra = actual_segments - expected_segments
        if missing:
            errors.append(
                f"climb {name!r}: missing from segments {sorted(missing)} "
                f"(expected on all segments its span crosses)"
            )
        if extra:
            errors.append(
                f"climb {name!r}: present on segments {sorted(extra)} outside its span"
            )

    for sprint in points_config.get("sprints", []):
        name = sprint["name"]
        declared_seg = sprint["segment"]
        km = sprint["km"]
        seg = segments_by_number.get(declared_seg)
        if seg is None:
            errors.append(f"sprint {name!r}: declared segment {declared_seg} not found in segments.json")
            continue
        if not (seg["km_start"] <= km <= seg["km_end"]):
            errors.append(
                f"sprint {name!r}: km {km} falls outside declared "
                f"segment {declared_seg} range [{seg['km_start']}, {seg['km_end']}]"
            )

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    parser.add_argument("--points-config", default=os.path.join(default_root, "data", "competition", "points-config.json"))
    parser.add_argument("--segments", default=os.path.join(default_root, "data", "segments.json"))
    parser.add_argument("--elevation-dir", default=os.path.join(default_root, "data", "elevation"))
    args = parser.parse_args()

    points_config = load_json(args.points_config)
    segments = load_json(args.segments)
    track = load_elevation_track(args.elevation_dir, segments)

    errors = validate(points_config, segments)
    errors += validate_elevation(points_config.get("climbs", []), track)

    if errors:
        print(f"FAIL: {len(errors)} divergence(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: points-config.json, segments.json, and GPX elevation agree on all climbs and sprints.")


if __name__ == "__main__":
    main()
