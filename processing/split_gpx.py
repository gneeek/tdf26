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
    "Brive-la-Gaillarde": 4.5,
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

KNOWN_CLIMBS = {
    "Puy Boubou": {"km_start": 30, "km_end": 32.8, "gradient": 4.1},
    "Côte de Lagleygeolle": {"km_start": 38, "km_end": 43.2, "gradient": 3.9},
    "Côte de Miel": {"km_start": 50, "km_end": 56.6, "gradient": 3.9},
    "Côte des Naves": {"km_start": 72, "km_end": 74.8, "gradient": 6.7},
    "Puy de Lachaud": {"km_start": 82, "km_end": 85.6, "gradient": 5.3},
    "Suc au May": {"km_start": 101, "km_end": 104.8, "gradient": 7.7},
    "Côte de la Croix de Pey": {"km_start": 120, "km_end": 127, "gradient": 4.9},
    "Mont Bessou": {"km_start": 148, "km_end": 153, "gradient": 3.5},
    "Côte des Gardes": {"km_start": 165, "km_end": 167.2, "gradient": 4.8},
}


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


def split_into_segments(points, num_segments=26):
    """Split points into N segments of roughly equal distance."""
    total_km = points[-1]["cum_km"]
    segment_length = total_km / num_segments
    print(f"Total distance: {total_km:.1f} km, segment length: {segment_length:.1f} km")

    segments = []
    seg_start_idx = 0

    for seg_num in range(1, num_segments + 1):
        km_start = (seg_num - 1) * segment_length
        km_end = seg_num * segment_length if seg_num < num_segments else total_km

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

        # Find towns in this segment
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
    parser = argparse.ArgumentParser(description="Split GPX into 26 segments")
    parser.add_argument("--gpx", default="data/main.gpx", help="Path to main GPX file")
    parser.add_argument("--output-dir", default="data/segments", help="Output directory for segment GPX files")
    parser.add_argument("--json-output", default="data/segments.json", help="Output path for segments metadata JSON")
    parser.add_argument("--num-segments", type=int, default=26, help="Number of segments")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Parsing {args.gpx}...")
    points = parse_gpx(args.gpx)
    print(f"Parsed {len(points)} trackpoints")

    segments = split_into_segments(points, args.num_segments)
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
