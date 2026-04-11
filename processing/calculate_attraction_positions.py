#!/usr/bin/env python3
"""
Compute per-attraction route proximity for Stage 9.

Reads all per-segment GPX files from data/segments/, concatenates them into
a continuous track with cumulative km measured from Malemort, then for each
attraction in data/attractions.json finds the closest point on the track.

Adds two fields to each attraction:
  - nearest_km: cumulative km along the route at the closest track point
  - nearest_distance_m: straight-line (haversine) distance in meters from
    the attraction to that closest point

The output is written back to data/attractions.json in place.

Downstream consumers (components/NearbyAttractions.vue, pages/admin/images.vue)
then assign each attraction to the segment whose [km_start, km_end) range
contains its nearest_km, and filter out attractions whose nearest_distance_m
exceeds a "too far from route to be nearby" threshold.

Related: issue #344 (this fix), issue #321 (same class of fix for town positions),
issue #341 (root-cause script fix for bounding-box assignment in split_gpx.py).
"""

import argparse
import json
import math
import os
import xml.etree.ElementTree as ET

GPX_NS = "http://www.topografix.com/GPX/1/1"


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in kilometers between two lat/lon points."""
    R = 6371.0088
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def parse_gpx(path):
    """Parse a GPX file and return an ordered list of (lat, lon) tuples."""
    tree = ET.parse(path)
    root = tree.getroot()
    points = []
    for trkpt in root.iter(f"{{{GPX_NS}}}trkpt"):
        lat = float(trkpt.get("lat"))
        lon = float(trkpt.get("lon"))
        points.append((lat, lon))
    return points


def build_master_track(segments_dir):
    """
    Concatenate all segment GPX files into one track with cumulative km
    measured from the first point of segment 1.

    Returns a list of (lat, lon, cum_km) tuples.
    """
    track = []
    cum_km = 0.0
    for i in range(1, 27):
        path = os.path.join(segments_dir, f"segment-{i:02d}.gpx")
        if not os.path.exists(path):
            print(f"  warning: {path} not found, skipping")
            continue
        points = parse_gpx(path)
        if not points:
            continue
        for j, (lat, lon) in enumerate(points):
            if not track:
                track.append((lat, lon, 0.0))
                continue
            prev_lat, prev_lon, _prev_km = track[-1]
            step = haversine_km(prev_lat, prev_lon, lat, lon)
            # Skip exact duplicate points at segment boundaries
            if j == 0 and step < 1e-6:
                continue
            cum_km += step
            track.append((lat, lon, cum_km))
    return track


def nearest_track_point(track, lat, lon):
    """
    Find the closest track point to (lat, lon).

    Linear scan. O(len(track)) per call, fast enough for 44 attractions
    against ~25k trkpts (~1.1 million haversine calls, a few seconds in
    pure Python).
    """
    best_km = 0.0
    best_dist = float("inf")
    for trk_lat, trk_lon, trk_km in track:
        d = haversine_km(trk_lat, trk_lon, lat, lon)
        if d < best_dist:
            best_dist = d
            best_km = trk_km
    return best_km, best_dist


def main():
    parser = argparse.ArgumentParser(description="Compute route proximity for Stage 9 attractions")
    parser.add_argument("--attractions", default="data/attractions.json", help="Path to attractions.json")
    parser.add_argument("--segments-dir", default="data/segments", help="Directory of per-segment GPX files")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing")
    args = parser.parse_args()

    print(f"Building master track from {args.segments_dir}/")
    track = build_master_track(args.segments_dir)
    if not track:
        print("  ERROR: no GPX points loaded")
        return 1
    total_km = track[-1][2]
    print(f"  {len(track)} points, total {total_km:.2f} km")

    print(f"\nLoading attractions from {args.attractions}")
    with open(args.attractions) as f:
        attractions = json.load(f)
    print(f"  {len(attractions)} attractions")

    print("\nComputing route proximity for each attraction")
    for poi in attractions:
        cum_km, dist_km = nearest_track_point(track, poi["lat"], poi["lng"])
        poi["nearest_km"] = round(cum_km, 2)
        poi["nearest_distance_m"] = round(dist_km * 1000)

    print("\n--- results (sorted by nearest_km) ---")
    for poi in sorted(attractions, key=lambda p: p["nearest_km"]):
        print(f"  km {poi['nearest_km']:6.2f}, {poi['nearest_distance_m']:6d}m  [{poi['category']:12}] {poi['name']}")

    if args.dry_run:
        print("\n(dry run, not writing)")
        return 0

    with open(args.attractions, "w") as f:
        json.dump(attractions, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nWrote updated {args.attractions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
