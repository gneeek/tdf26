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

Exits non-zero if any invariant is violated.
"""

import argparse
import json
import os
import sys


def load_json(path):
    with open(path) as f:
        return json.load(f)


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
    args = parser.parse_args()

    errors = validate(load_json(args.points_config), load_json(args.segments))

    if errors:
        print(f"FAIL: {len(errors)} divergence(s) between points-config.json and segments.json:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: points-config.json and segments.json agree on all climbs and sprints.")


if __name__ == "__main__":
    main()
