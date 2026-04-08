#!/usr/bin/env python3
"""Snapshot rider stats and points for a specific segment at publish time."""

import argparse
import json
import os

from rider_stats import calculate_stats


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def create_snapshot(stats_path, points_path, log_path, segment, output_dir, data_cutoff=None, rider_config_path=None):
    """Create a snapshot of current rider data for a segment."""
    stats = load_json(stats_path)
    log = load_json(log_path)

    points = {"riders": {}, "locations": []}
    if os.path.exists(points_path):
        points = load_json(points_path)

    # Filter log entries to those on or before the data cutoff
    if data_cutoff and log.get("entries"):
        log["entries"] = [e for e in log["entries"] if e["date"] <= data_cutoff]

    # Recalculate stats from filtered log so numbers match the displayed data
    if data_cutoff and rider_config_path and os.path.exists(rider_config_path):
        rider_config = load_json(rider_config_path)
        stats = calculate_stats(log, rider_config)

    # Override asOf to match the last log entry date
    if log.get("entries"):
        stats["asOf"] = log["entries"][-1]["date"]

    snapshot = {
        "segment": segment,
        "stats": stats,
        "points": points,
        "log": log,
    }

    os.makedirs(output_dir, exist_ok=True)
    seg_str = str(segment).zfill(2)
    output_path = os.path.join(output_dir, f"snapshot-{seg_str}.json")

    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot for segment {segment} written to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Snapshot rider stats for a segment")
    parser.add_argument("--stats", default="data/riders/stats.json")
    parser.add_argument("--points", default="data/riders/points.json")
    parser.add_argument("--daily-log", default="data/riders/daily-log.json")
    parser.add_argument("--segment", type=int, required=True)
    parser.add_argument("--output-dir", default="data/riders/snapshots")
    parser.add_argument("--rider-config", default="data/riders/rider-config.json")
    parser.add_argument("--data-cutoff", default=None, help="Filter log to entries on or before this date (YYYY-MM-DD). From entry frontmatter dataCutoff.")
    args = parser.parse_args()

    create_snapshot(args.stats, args.points, args.daily_log, args.segment, args.output_dir, args.data_cutoff, args.rider_config)


if __name__ == "__main__":
    main()
