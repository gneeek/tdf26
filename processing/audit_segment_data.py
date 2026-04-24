#!/usr/bin/env python3
"""Audit segment data: report closest-approach km for every town, climb, sprint, and attraction.

Reads the per-segment GPX files from data/segments/ (concatenated with cumulative
km from Malemort) and, for each entry in

  - data/town-positions.ts           (hardcoded town -> km)
  - data/town-coords.json            (town and climb coordinates)
  - data/segments.json               (per-segment towns / climbs / notable_points)
  - data/attractions.json            (lat/lng plus stored nearest_km)
  - data/competition/points-config.json  (sprints and climbs by segment+km)

computes the closest-approach point on the route polyline, the cumulative km
there, the perpendicular distance in meters, and which segment (by km_start /
km_end) that km falls in. Compares computed values against stored values and
emits a Markdown report.

This script reports; it does not mutate data. Data corrections land in separate
PRs per the v1.4.8 segment-data-correctness epic (#396).

Related:
  #397 (this script), #341 (split_gpx.py root-cause fix), #369 (validate_points.py summit cross-check).
"""

import argparse
import datetime
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

GPX_NS = "http://www.topografix.com/GPX/1/1"

# Tolerance for "computed matches stored" in the recommendation column.
KM_MATCH_TOLERANCE = 0.5
# Distances above this trigger a "far from route" warning in recommendations.
FAR_FROM_ROUTE_M = 5000


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    lat1_r, lon1_r, lat2_r, lon2_r = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def parse_gpx(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return [(float(p.get("lat")), float(p.get("lon")))
            for p in root.iter(f"{{{GPX_NS}}}trkpt")]


def build_master_track(segments_dir):
    """Concatenate every segment-NN.gpx file into one track with cumulative km.

    Segment count is discovered from the filesystem (the project has had both
    26- and 27-segment splits; hardcoding either has burned this script once).
    """
    track = []
    cum_km = 0.0
    i = 1
    while True:
        path = os.path.join(segments_dir, f"segment-{i:02d}.gpx")
        if not os.path.exists(path):
            break
        points = parse_gpx(path)
        for j, (lat, lon) in enumerate(points):
            if not track:
                track.append((lat, lon, 0.0))
                continue
            prev_lat, prev_lon, _ = track[-1]
            step = haversine_km(prev_lat, prev_lon, lat, lon)
            if j == 0 and step < 1e-6:
                continue
            cum_km += step
            track.append((lat, lon, cum_km))
        i += 1
    return track


def project_onto_segment(Q_lat, Q_lng, A_lat, A_lng, A_km, B_lat, B_lng, B_km):
    """Project Q onto the polyline segment A->B using a local equirectangular frame.

    Returns (km, distance_m) of the closest point. The segment endpoints carry
    cumulative km; the returned km interpolates linearly between them.
    """
    lat_scale = 111_000.0
    lng_scale = 111_000.0 * math.cos(math.radians(Q_lat))

    Ax = (A_lng - Q_lng) * lng_scale
    Ay = (A_lat - Q_lat) * lat_scale
    Bx = (B_lng - Q_lng) * lng_scale
    By = (B_lat - Q_lat) * lat_scale

    dx = Bx - Ax
    dy = By - Ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-12:
        return A_km, math.hypot(Ax, Ay)

    t = -(Ax * dx + Ay * dy) / seg_len_sq
    t = max(0.0, min(1.0, t))
    Cx = Ax + t * dx
    Cy = Ay + t * dy
    return A_km + t * (B_km - A_km), math.hypot(Cx, Cy)


def nearest_km_and_distance(track, lat, lng):
    """Find closest-approach km and perpendicular distance along the polyline.

    Finds the closest vertex by cheap squared distance, then projects onto the
    two adjacent polyline segments so the reported km is precise between
    vertices rather than snapped to the grid.
    """
    cos_lat = math.cos(math.radians(lat))
    best_i = 0
    best_d_sq = float("inf")
    for i, (tlat, tlng, _) in enumerate(track):
        dlat = tlat - lat
        dlng = (tlng - lng) * cos_lat
        d_sq = dlat * dlat + dlng * dlng
        if d_sq < best_d_sq:
            best_d_sq = d_sq
            best_i = i

    candidates = [(
        track[best_i][2],
        haversine_km(track[best_i][0], track[best_i][1], lat, lng) * 1000.0,
    )]
    if best_i > 0:
        candidates.append(project_onto_segment(lat, lng, *track[best_i - 1], *track[best_i]))
    if best_i < len(track) - 1:
        candidates.append(project_onto_segment(lat, lng, *track[best_i], *track[best_i + 1]))
    return min(candidates, key=lambda c: c[1])


def segment_containing_km(segments, km):
    """Return the segment number whose [km_start, km_end) contains km.

    The last segment's km_end is inclusive. Cumulative km from the polyline
    can also overshoot the rounded km_end by a few meters at the end of the
    route, so small overshoots past the last segment still resolve to it.
    """
    for s in segments:
        if s["km_start"] <= km < s["km_end"]:
            return s["segment"]
    if segments:
        last = segments[-1]
        if last["km_start"] <= km <= last["km_end"] + 1.0:
            return last["segment"]
    return None


TOWN_POSITIONS_RE = re.compile(r"^\s*'([^']+)':\s*([\d.]+),")


def parse_town_positions_ts(path):
    """Parse the townKmPositions export. Flat object literal, line-regex is enough."""
    result = {}
    with open(path) as f:
        for line in f:
            m = TOWN_POSITIONS_RE.match(line)
            if m:
                result[m.group(1)] = float(m.group(2))
    return result


def load_json(path):
    with open(path) as f:
        return json.load(f)


def _km_delta_note(stored_km, computed_km):
    if stored_km is None:
        return "no stored km"
    delta = computed_km - stored_km
    if abs(delta) <= KM_MATCH_TOLERANCE:
        return f"km matches ({delta:+.2f})"
    return f"km off by {delta:+.2f}"


def _seg_delta_note(computed_seg, stored_segs):
    if not stored_segs:
        return "not listed on any segment"
    if computed_seg is None:
        return f"computed km outside route; stored on {stored_segs}"
    if computed_seg in stored_segs:
        extra = [s for s in stored_segs if s != computed_seg]
        if extra:
            return f"segment matches ({computed_seg}); also listed on {extra}"
        return f"segment matches ({computed_seg})"
    return f"segment mismatch: computed {computed_seg}, stored {stored_segs}"


def audit_towns(track, segments, town_coords, town_positions):
    """Audit every town: closest-approach km, distance, and segment assignment."""
    rows = []
    names_from_segments = {n for s in segments for n in (s.get("towns") or [])}
    all_names = set(town_positions) | {
        n for n, v in town_coords.items() if v.get("type") == "town"
    } | names_from_segments

    stored_segments = {
        name: sorted({s["segment"] for s in segments if name in (s.get("towns") or [])})
        for name in all_names
    }

    for name in sorted(all_names):
        stored_km = town_positions.get(name)
        coords = town_coords.get(name)
        if coords is None or coords.get("type") != "town":
            rows.append({
                "name": name,
                "stored_km": stored_km,
                "computed_km": None,
                "distance_m": None,
                "computed_segment": None,
                "stored_segments": stored_segments[name],
                "notes": "no coords in town-coords.json",
            })
            continue
        km, dist = nearest_km_and_distance(track, coords["lat"], coords["lng"])
        computed_seg = segment_containing_km(segments, km)
        notes = [_km_delta_note(stored_km, km), _seg_delta_note(computed_seg, stored_segments[name])]
        if dist > FAR_FROM_ROUTE_M:
            notes.append(f"{int(dist)}m from route")
        rows.append({
            "name": name,
            "stored_km": stored_km,
            "computed_km": round(km, 2),
            "distance_m": round(dist),
            "computed_segment": computed_seg,
            "stored_segments": stored_segments[name],
            "notes": "; ".join(notes),
        })
    return rows


def audit_climbs(track, segments, town_coords, points_config):
    """Audit every climb in points-config.json against town-coords + segments.json."""
    rows = []
    for climb in points_config.get("climbs", []):
        name = climb["name"]
        coords = town_coords.get(name)
        stored_km = climb["km"]
        stored_seg = climb["segment"]
        length_km = climb.get("length_km")

        stored_on_segments = sorted({s["segment"] for s in segments if name in (s.get("climbs") or [])})

        if coords is None:
            rows.append({
                "name": name,
                "stored_km": stored_km,
                "stored_segment": stored_seg,
                "length_km": length_km,
                "computed_km": None,
                "distance_m": None,
                "computed_segment": None,
                "stored_on_segments": stored_on_segments,
                "notes": "no coords in town-coords.json",
            })
            continue
        km, dist = nearest_km_and_distance(track, coords["lat"], coords["lng"])
        computed_seg = segment_containing_km(segments, km)
        notes = [_km_delta_note(stored_km, km), _seg_delta_note(computed_seg, [stored_seg])]
        if dist > FAR_FROM_ROUTE_M:
            notes.append(f"{int(dist)}m from route")
        rows.append({
            "name": name,
            "stored_km": stored_km,
            "stored_segment": stored_seg,
            "length_km": length_km,
            "computed_km": round(km, 2),
            "distance_m": round(dist),
            "computed_segment": computed_seg,
            "stored_on_segments": stored_on_segments,
            "notes": "; ".join(notes),
        })
    return rows


def audit_sprints(segments, points_config):
    """Sprints have km but no coords; check km is inside declared segment."""
    rows = []
    for sprint in points_config.get("sprints", []):
        name = sprint["name"]
        stored_km = sprint["km"]
        stored_seg = sprint["segment"]
        computed_seg = segment_containing_km(segments, stored_km)
        if computed_seg is None:
            notes = f"km {stored_km} outside route"
        elif computed_seg == stored_seg:
            notes = f"km {stored_km} inside declared segment {stored_seg}"
        else:
            notes = f"segment mismatch: km {stored_km} falls in segment {computed_seg}, declared {stored_seg}"
        rows.append({
            "name": name,
            "stored_km": stored_km,
            "stored_segment": stored_seg,
            "computed_segment": computed_seg,
            "notes": notes,
        })
    return rows


def audit_attractions(track, segments, attractions):
    """Recompute nearest_km and distance for each attraction, compare to stored values."""
    rows = []
    for poi in attractions:
        name = poi["name"]
        lat = poi["lat"]
        lng = poi["lng"]
        stored_km = poi.get("nearest_km")
        stored_dist = poi.get("nearest_distance_m")
        km, dist = nearest_km_and_distance(track, lat, lng)
        computed_seg = segment_containing_km(segments, km)
        notes = []
        if stored_km is None:
            notes.append("no stored nearest_km")
        else:
            dk = km - stored_km
            if abs(dk) > KM_MATCH_TOLERANCE:
                notes.append(f"km drift {dk:+.2f}")
        if stored_dist is not None:
            dd = round(dist) - stored_dist
            if abs(dd) > 50:
                notes.append(f"distance drift {dd:+d}m")
        if not notes:
            notes.append("matches stored")
        if dist > FAR_FROM_ROUTE_M:
            notes.append(f"{int(dist)}m from route")
        rows.append({
            "name": name,
            "category": poi.get("category", ""),
            "stored_km": stored_km,
            "stored_distance_m": stored_dist,
            "computed_km": round(km, 2),
            "distance_m": round(dist),
            "computed_segment": computed_seg,
            "notes": "; ".join(notes),
        })
    return rows


def audit_notable_points(segments):
    """Each segment's notable_points list. Currently all empty; reported for completeness."""
    rows = []
    for s in segments:
        for np in s.get("notable_points") or []:
            rows.append({"segment": s["segment"], "entry": np})
    return rows


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def _fmt_km(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "-"


def _fmt_seg(v):
    if v is None:
        return "-"
    if isinstance(v, list):
        return ",".join(str(s) for s in v) if v else "-"
    return str(v)


def render_towns_table(rows):
    header = "| Name | Stored km | Computed km | Dist (m) | Computed seg | Stored seg(s) | Notes |\n"
    header += "|------|----------:|------------:|---------:|:------------:|:--------------|:------|\n"
    body = []
    for r in sorted(rows, key=lambda r: (r["computed_km"] if r["computed_km"] is not None else 0)):
        body.append(
            f"| {r['name']} | {_fmt_km(r['stored_km'])} | {_fmt_km(r['computed_km'])} | "
            f"{r['distance_m'] if r['distance_m'] is not None else '-'} | "
            f"{_fmt_seg(r['computed_segment'])} | {_fmt_seg(r['stored_segments'])} | {r['notes']} |"
        )
    return header + "\n".join(body) + "\n"


def render_climbs_table(rows):
    header = "| Name | Stored km | Computed km | Dist (m) | Stored seg | Computed seg | Stored on | Length km | Notes |\n"
    header += "|------|----------:|------------:|---------:|:---------:|:------------:|:----------|:---------:|:------|\n"
    body = []
    for r in sorted(rows, key=lambda r: (r["computed_km"] if r["computed_km"] is not None else r["stored_km"])):
        body.append(
            f"| {r['name']} | {_fmt_km(r['stored_km'])} | {_fmt_km(r['computed_km'])} | "
            f"{r['distance_m'] if r['distance_m'] is not None else '-'} | "
            f"{r['stored_segment']} | {_fmt_seg(r['computed_segment'])} | "
            f"{_fmt_seg(r['stored_on_segments'])} | "
            f"{r['length_km'] if r['length_km'] is not None else '-'} | {r['notes']} |"
        )
    return header + "\n".join(body) + "\n"


def render_sprints_table(rows):
    header = "| Name | Stored km | Stored seg | Computed seg | Notes |\n"
    header += "|------|----------:|:---------:|:------------:|:------|\n"
    body = []
    for r in sorted(rows, key=lambda r: r["stored_km"]):
        body.append(
            f"| {r['name']} | {_fmt_km(r['stored_km'])} | {r['stored_segment']} | "
            f"{_fmt_seg(r['computed_segment'])} | {r['notes']} |"
        )
    return header + "\n".join(body) + "\n"


def render_attractions_table(rows):
    header = "| Name | Category | Stored km | Computed km | Stored dist (m) | Computed dist (m) | Seg | Notes |\n"
    header += "|------|----------|----------:|------------:|----------------:|------------------:|:---:|:------|\n"
    body = []
    for r in sorted(rows, key=lambda r: r["computed_km"]):
        body.append(
            f"| {r['name']} | {r['category']} | "
            f"{_fmt_km(r['stored_km']) if r['stored_km'] is not None else '-'} | "
            f"{_fmt_km(r['computed_km'])} | "
            f"{r['stored_distance_m'] if r['stored_distance_m'] is not None else '-'} | "
            f"{r['distance_m']} | {_fmt_seg(r['computed_segment'])} | {r['notes']} |"
        )
    return header + "\n".join(body) + "\n"


def build_report_dict(as_of, track_len, total_km, town_rows, climb_rows, sprint_rows, attraction_rows, notable_rows):
    """Structured form of the audit, suitable for JSON output.

    Consumers (see #341 split_gpx.py route-proximity assignment, #369
    validate_points.py summit-km cross-check) can read this directly instead
    of re-implementing closest-approach math.
    """
    return {
        "as_of": as_of,
        "track": {"points": track_len, "total_km": round(total_km, 2)},
        "tolerances": {
            "km_match": KM_MATCH_TOLERANCE,
            "far_from_route_m": FAR_FROM_ROUTE_M,
        },
        "towns": town_rows,
        "climbs": climb_rows,
        "sprints": sprint_rows,
        "attractions": attraction_rows,
        "notable_points": notable_rows,
    }


def build_report(as_of, track_len, total_km, town_rows, climb_rows, sprint_rows, attraction_rows, notable_rows):
    out = []
    out.append(f"# Segment data audit — {as_of}\n")
    out.append(
        "Generated by `processing/audit_segment_data.py`. For each stored place along the "
        "route, the script recomputes the closest-approach km and segment against the "
        "master GPX and reports divergence from the stored value. Report only; does not mutate.\n"
    )
    out.append(
        f"Master track: {track_len} points, {total_km:.2f} km.\n"
        f"Match tolerance: ±{KM_MATCH_TOLERANCE} km, far-from-route flag: >{FAR_FROM_ROUTE_M} m.\n"
    )

    out.append("## Towns\n")
    out.append("Sources: `data/town-positions.ts` (stored km), `data/town-coords.json` (coords), `data/segments.json` (segment assignments).\n")
    out.append(render_towns_table(town_rows))

    out.append("## Climbs\n")
    out.append("Sources: `data/competition/points-config.json` (stored km + segment), `data/town-coords.json` (coords), `data/segments.json` (segment assignments).\n")
    out.append(render_climbs_table(climb_rows))

    out.append("## Sprints\n")
    out.append("Sprints are km-only (no coords). Checked for range consistency.\n")
    out.append(render_sprints_table(sprint_rows))

    out.append("## Attractions\n")
    out.append("Source: `data/attractions.json`. Compared against stored `nearest_km` and `nearest_distance_m`.\n")
    out.append(render_attractions_table(attraction_rows))

    out.append("## Notable points\n")
    if notable_rows:
        for r in notable_rows:
            out.append(f"- seg {r['segment']}: {r['entry']}")
        out.append("")
    else:
        out.append("(no `notable_points` entries populated in segments.json)\n")

    return "\n".join(out)


def _filter_rows(rows, key, predicate):
    return [r for r in rows if predicate(r.get(key))]


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--segments-dir", default=os.path.join(repo_root, "data", "segments"))
    parser.add_argument("--segments-json", default=os.path.join(repo_root, "data", "segments.json"))
    parser.add_argument("--town-coords", default=os.path.join(repo_root, "data", "town-coords.json"))
    parser.add_argument("--town-positions", default=os.path.join(repo_root, "data", "town-positions.ts"))
    parser.add_argument("--attractions", default=os.path.join(repo_root, "data", "attractions.json"))
    parser.add_argument("--points-config", default=os.path.join(repo_root, "data", "competition", "points-config.json"))
    parser.add_argument("--output", help="Write report to FILE (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown (for #341/#369 to consume)")
    parser.add_argument("--town", help="Filter: only include this town (by exact name)")
    parser.add_argument("--segment", type=int, help="Filter: only include entries assigned to this segment")
    args = parser.parse_args()

    track = build_master_track(args.segments_dir)
    if not track:
        print("ERROR: no track data loaded", file=sys.stderr)
        return 1

    segments = load_json(args.segments_json)
    town_coords = load_json(args.town_coords)
    town_positions = parse_town_positions_ts(args.town_positions)
    attractions = load_json(args.attractions)
    points_config = load_json(args.points_config)

    town_rows = audit_towns(track, segments, town_coords, town_positions)
    climb_rows = audit_climbs(track, segments, town_coords, points_config)
    sprint_rows = audit_sprints(segments, points_config)
    attraction_rows = audit_attractions(track, segments, attractions)
    notable_rows = audit_notable_points(segments)

    if args.town:
        name = args.town
        town_rows = [r for r in town_rows if r["name"] == name]
        climb_rows = [r for r in climb_rows if r["name"] == name]
        sprint_rows = [r for r in sprint_rows if r["name"] == name]
        attraction_rows = [r for r in attraction_rows if r["name"] == name]
        notable_rows = [r for r in notable_rows if r["entry"] == name]

    if args.segment is not None:
        seg = args.segment
        town_rows = [r for r in town_rows if seg in (r["stored_segments"] or []) or r["computed_segment"] == seg]
        climb_rows = [r for r in climb_rows if r["stored_segment"] == seg or r["computed_segment"] == seg]
        sprint_rows = [r for r in sprint_rows if r["stored_segment"] == seg or r["computed_segment"] == seg]
        attraction_rows = [r for r in attraction_rows if r["computed_segment"] == seg]
        notable_rows = [r for r in notable_rows if r["segment"] == seg]

    as_of = datetime.date.today().isoformat()
    common = dict(
        as_of=as_of,
        track_len=len(track),
        total_km=track[-1][2],
        town_rows=town_rows,
        climb_rows=climb_rows,
        sprint_rows=sprint_rows,
        attraction_rows=attraction_rows,
        notable_rows=notable_rows,
    )

    if args.json:
        report = json.dumps(build_report_dict(**common), ensure_ascii=False, indent=2) + "\n"
    else:
        report = build_report(**common)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
