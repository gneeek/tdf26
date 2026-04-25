#!/usr/bin/env python3
"""Parse main.gpx, split into segments, output per-segment GPX files and segments.json.

Towns are assigned to segments by route-proximity (#341): for each town in
data/town-coords.json the script finds the closest point on the route, records
the cumulative km at that point, and assigns the town to whichever segment
contains that km. Towns more than --town-max-distance from the route are
excluded entirely (catches off-route landmarks like Brive-la-Gaillarde, which
the route passes 2.5 km away).

The closest-approach km is also recorded per segment under `town_positions`,
so downstream consumers (e.g. data/town-positions.ts) can be regenerated
from segments.json instead of hand-maintained.
"""

import argparse
import json
import math
import os

import gpxpy
import gpxpy.gpx

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
POINTS_CONFIG_PATH = os.path.join(DATA_DIR, "competition", "points-config.json")
TOWN_COORDS_PATH = os.path.join(DATA_DIR, "town-coords.json")
DEFAULT_TOWN_MAX_DISTANCE_M = 1000.0


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


def _project_onto_polyline_segment(q_lat, q_lng, a_lat, a_lng, a_km, b_lat, b_lng, b_km):
    """Project Q onto the line segment A->B using a local equirectangular frame.

    Returns (km, distance_m) for the closest point on the segment. Mirrors the
    helper in audit_segment_data.py so split_gpx and the audit agree on
    closest-approach math without forcing a cross-import.
    """
    lat_scale = 111_000.0
    lng_scale = 111_000.0 * math.cos(math.radians(q_lat))
    ax = (a_lng - q_lng) * lng_scale
    ay = (a_lat - q_lat) * lat_scale
    bx = (b_lng - q_lng) * lng_scale
    by = (b_lat - q_lat) * lat_scale
    dx = bx - ax
    dy = by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-12:
        return a_km, math.hypot(ax, ay)
    t = -(ax * dx + ay * dy) / seg_len_sq
    t = max(0.0, min(1.0, t))
    cx = ax + t * dx
    cy = ay + t * dy
    return a_km + t * (b_km - a_km), math.hypot(cx, cy)


def closest_approach(points, lat, lng):
    """Find closest-approach point on the GPX polyline to (lat, lng).

    Returns (km, distance_m). Picks the closest vertex by cheap squared
    distance, then projects onto the two adjacent polyline segments so the
    reported km is precise between vertices rather than snapped to the grid.
    """
    cos_lat = math.cos(math.radians(lat))
    best_i = 0
    best_d_sq = float("inf")
    for i, p in enumerate(points):
        dlat = p["lat"] - lat
        dlng = (p["lon"] - lng) * cos_lat
        d_sq = dlat * dlat + dlng * dlng
        if d_sq < best_d_sq:
            best_d_sq = d_sq
            best_i = i
    candidates = [(
        points[best_i]["cum_km"],
        haversine(points[best_i]["lat"], points[best_i]["lon"], lat, lng),
    )]
    if best_i > 0:
        a, b = points[best_i - 1], points[best_i]
        candidates.append(_project_onto_polyline_segment(
            lat, lng, a["lat"], a["lon"], a["cum_km"], b["lat"], b["lon"], b["cum_km"],
        ))
    if best_i < len(points) - 1:
        a, b = points[best_i], points[best_i + 1]
        candidates.append(_project_onto_polyline_segment(
            lat, lng, a["lat"], a["lon"], a["cum_km"], b["lat"], b["lon"], b["cum_km"],
        ))
    return min(candidates, key=lambda c: c[1])


def load_town_coords(path=TOWN_COORDS_PATH):
    """Load all entries from town-coords.json. Caller filters by `type` field."""
    with open(path) as f:
        return json.load(f)


def compute_town_proximity(points, town_coords):
    """Closest-approach lookup for each town.

    For every entry whose `type` is `town`, returns {km, distance_m}. Climbs
    are skipped (their summit positions are #369's job). The km is the
    cumulative km from the route start to the closest point on the polyline,
    not the nearest vertex.
    """
    result = {}
    for name, info in town_coords.items():
        if info.get("type") != "town":
            continue
        km, dist = closest_approach(points, info["lat"], info["lng"])
        result[name] = {"km": round(km, 2), "distance_m": round(dist)}
    return result


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


def split_into_segments(
    points,
    num_segments=27,
    odd_length=8.0,
    even_length=6.0,
    town_coords=None,
    town_max_distance_m=DEFAULT_TOWN_MAX_DISTANCE_M,
):
    """Split points into segments with alternating lengths.

    Odd segments (1,3,5,...) are odd_length km.
    Even segments (2,4,6,...) are even_length km.
    The final segment gets the remainder.

    Towns are assigned by route-proximity if `town_coords` is provided: each
    town's closest-approach km is computed once against the full polyline and
    used to bucket it into the segment whose [km_start, km_end) contains it.
    Towns farther than `town_max_distance_m` from the route are excluded.
    """
    total_km = points[-1]["cum_km"]
    if town_coords:
        town_proximity = compute_town_proximity(points, town_coords)
    else:
        town_proximity = {}

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

        # Find towns in this segment via route-proximity (#341).
        # Half-open [km_start, km_end) so a town landing exactly on a boundary
        # only appears once.
        towns = []
        town_positions = {}
        for name, prox in town_proximity.items():
            if prox["distance_m"] > town_max_distance_m:
                continue
            km = prox["km"]
            if km_start <= km < km_end:
                towns.append(name)
                town_positions[name] = km

        # Find climbs in this segment (km-range from points-config; #369 will
        # refactor this to summit-from-GPX-elevation-peak).
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
            "town_positions": town_positions,
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
    parser.add_argument("--town-coords", default=TOWN_COORDS_PATH, help="Path to town-coords.json")
    parser.add_argument("--town-max-distance-m", type=float, default=DEFAULT_TOWN_MAX_DISTANCE_M,
                        help="Towns farther than this from the route are excluded from segment assignment")
    parser.add_argument("--num-segments", type=int, default=27, help="Number of segments")
    parser.add_argument("--odd-length", type=float, default=8.0, help="Length of odd segments (km)")
    parser.add_argument("--even-length", type=float, default=6.0, help="Length of even segments (km)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Parsing {args.gpx}...")
    points = parse_gpx(args.gpx)
    print(f"Parsed {len(points)} trackpoints")

    town_coords = load_town_coords(args.town_coords)
    segments = split_into_segments(
        points, args.num_segments, args.odd_length, args.even_length,
        town_coords=town_coords, town_max_distance_m=args.town_max_distance_m,
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
