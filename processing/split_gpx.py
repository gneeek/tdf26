#!/usr/bin/env python3
"""Parse main.gpx, split into 26 segments, output segment GPX files and segments.json."""

import argparse
import json
import math
import os

import gpxpy
import gpxpy.gpx

# Known waypoints with approximate km positions along the route
KNOWN_TOWNS = {
    "Malemort": 0,
    "Turenne": 17,
    "Collonges-la-Rouge": 23.5,
    "Beynat": 37.5,
    "Tulle": 65.5,
    "Naves": 73.5,
    "Chaumeil": 90,
    "Treignac": 116.5,
    "Bugeat": 130,
    "Meymac": 157.5,
    "Ussel": 182.5,
}

POINTS_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "competition", "points-config.json"
)


def load_known_climbs(path=POINTS_CONFIG_PATH):
    """Load climbs from points-config.json as {name: {km_start, km_end, gradient}}.

    The summit km is `km` in points-config. length_km may be null, in which case
    the climb is treated as a point-mark (km_start == km_end == summit).
    """
    with open(path) as f:
        config = json.load(f)
    climbs = {}
    for c in config["climbs"]:
        summit = c["km"]
        length = c.get("length_km")
        if length is None:
            km_start = summit
            km_end = summit
        else:
            km_start = summit - length
            km_end = summit
        climbs[c["name"]] = {
            "km_start": km_start,
            "km_end": km_end,
            "gradient": c.get("gradient"),
        }
    return climbs


KNOWN_CLIMBS = load_known_climbs()


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in meters between two lat/lon points."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_gpx(gpx_path):
    """Parse GPX file, return list of (lat, lon, ele, cumulative_dist_km) tuples."""
    with open(gpx_path, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    cum_dist = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            for i, pt in enumerate(segment.points):
                if i > 0:
                    prev = segment.points[i - 1]
                    cum_dist += haversine(prev.latitude, prev.longitude, pt.latitude, pt.longitude)
                points.append({
                    "lat": pt.latitude,
                    "lon": pt.longitude,
                    "ele": pt.elevation or 0,
                    "cum_km": cum_dist / 1000,
                })

    return points


def load_existing_towns(path):
    """Return {segment_number: [towns]} from an existing segments.json if present.

    Used to preserve hand-verified town assignments (#342) that the km-bbox logic
    below would otherwise regress. The structural fix for town assignment is
    tracked in #341.
    """
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        data = json.load(f)
    return {s["segment"]: s.get("towns", []) for s in data}


def split_into_segments(points, num_segments=27, odd_length=8.0, even_length=6.0, existing_towns=None):
    """Split points into segments with alternating lengths.

    Odd segments (1,3,5,...) are odd_length km.
    Even segments (2,4,6,...) are even_length km.
    The final segment gets the remainder.
    """
    total_km = points[-1]["cum_km"]

    # Build km boundaries
    boundaries = [0.0]
    km = 0.0
    for seg_num in range(1, num_segments + 1):
        if seg_num == num_segments:
            km = total_km
        else:
            km += odd_length if seg_num % 2 == 1 else even_length
            if km >= total_km:
                km = total_km
        boundaries.append(km)

    actual_segments = len(boundaries) - 1
    print(f"Total distance: {total_km:.1f} km, {actual_segments} segments (odd={odd_length}km, even={even_length}km, final={total_km - boundaries[-2]:.1f}km)")

    segments = []
    seg_start_idx = 0

    for seg_num in range(1, actual_segments + 1):
        km_start = boundaries[seg_num - 1]
        km_end = boundaries[seg_num]

        # Find points in this segment
        seg_points = []
        seg_end_idx = seg_start_idx
        for j in range(seg_start_idx, len(points)):
            if points[j]["cum_km"] >= km_start and points[j]["cum_km"] <= km_end + 0.01:
                seg_points.append(points[j])
                seg_end_idx = j
            elif points[j]["cum_km"] > km_end + 0.01:
                break

        if not seg_points:
            continue

        elevations = [p["ele"] for p in seg_points]
        ele_gain = sum(
            max(0, seg_points[i]["ele"] - seg_points[i - 1]["ele"])
            for i in range(1, len(seg_points))
        )
        ele_loss = sum(
            max(0, seg_points[i - 1]["ele"] - seg_points[i]["ele"])
            for i in range(1, len(seg_points))
        )

        # Find towns in this segment. Prefer hand-verified assignments from an
        # existing segments.json (see #342) over the km-bbox heuristic, since
        # the heuristic is known-wrong and its structural fix is tracked in #341.
        if existing_towns and seg_num in existing_towns:
            towns = existing_towns[seg_num]
        else:
            towns = [
                name for name, km in KNOWN_TOWNS.items()
                if km_start <= km <= km_end
            ]

        # Find climbs in this segment
        climbs = [
            name for name, info in KNOWN_CLIMBS.items()
            if info["km_start"] < km_end and info["km_end"] > km_start
        ]

        segments.append({
            "segment": seg_num,
            "km_start": round(km_start, 1),
            "km_end": round(km_end, 1),
            "start_lat": seg_points[0]["lat"],
            "start_lng": seg_points[0]["lon"],
            "end_lat": seg_points[-1]["lat"],
            "end_lng": seg_points[-1]["lon"],
            "elevation_gain": round(ele_gain),
            "elevation_loss": round(ele_loss),
            "min_elevation": round(min(elevations)),
            "max_elevation": round(max(elevations)),
            "notable_points": [],
            "towns": towns,
            "climbs": climbs,
            "points": seg_points,  # kept for GPX output, removed from JSON
        })

        # Next segment starts where this one left off
        seg_start_idx = max(0, seg_end_idx - 1)

    return segments


def write_segment_gpx(segment, output_dir):
    """Write a standalone GPX file for one segment."""
    gpx = gpxpy.gpx.GPX()
    track = gpxpy.gpx.GPXTrack(name=f"Stage 9 - Segment {segment['segment']}")
    gpx.tracks.append(track)
    seg = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(seg)

    for pt in segment["points"]:
        seg.points.append(
            gpxpy.gpx.GPXTrackPoint(pt["lat"], pt["lon"], elevation=pt["ele"])
        )

    seg_num = str(segment["segment"]).zfill(2)
    output_path = os.path.join(output_dir, f"segment-{seg_num}.gpx")
    with open(output_path, "w") as f:
        f.write(gpx.to_xml())

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Split GPX into segments")
    parser.add_argument("--gpx", default="data/main.gpx", help="Path to main GPX file")
    parser.add_argument("--output-dir", default="data/segments", help="Output directory for segment GPX files")
    parser.add_argument("--json-output", default="data/segments.json", help="Output path for segments metadata JSON")
    parser.add_argument("--num-segments", type=int, default=27, help="Number of segments")
    parser.add_argument("--odd-length", type=float, default=8.0, help="Length of odd segments (km)")
    parser.add_argument("--even-length", type=float, default=6.0, help="Length of even segments (km)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Parsing {args.gpx}...")
    points = parse_gpx(args.gpx)
    print(f"Parsed {len(points)} trackpoints")

    existing_towns = load_existing_towns(args.json_output)
    segments = split_into_segments(
        points, args.num_segments, args.odd_length, args.even_length,
        existing_towns=existing_towns,
    )
    print(f"Created {len(segments)} segments")

    # Write individual segment GPX files
    for seg in segments:
        path = write_segment_gpx(seg, args.output_dir)
        print(f"  Segment {seg['segment']}: {path} ({len(seg['points'])} points, "
              f"+{seg['elevation_gain']}m/-{seg['elevation_loss']}m, "
              f"towns: {seg['towns']}, climbs: {seg['climbs']})")

    # Write segments.json (without the raw points)
    json_segments = []
    for seg in segments:
        s = {k: v for k, v in seg.items() if k != "points"}
        json_segments.append(s)

    with open(args.json_output, "w") as f:
        json.dump(json_segments, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {args.json_output}")


if __name__ == "__main__":
    main()
