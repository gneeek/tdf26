#!/usr/bin/env python3
"""Calculate sprint and climbing points for each rider based on capped distance progress."""

import argparse
import json
import random


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def calculate_capped_distances(daily_log, rider_config):
    """Calculate cumulative capped distance per rider per day.

    Returns dict of rider_id -> list of (date, cumulative_capped_km).
    """
    daily_cap = rider_config["dailyCap"]
    entries = sorted(daily_log["entries"], key=lambda e: e["date"])
    rider_ids = [r["id"] for r in rider_config["riders"]]

    result = {}
    for rider_id in rider_ids:
        carry = 0.0
        cumulative = 0.0
        progress = []
        for entry in entries:
            dist = entry.get("distances", {}).get(rider_id, 0)
            available = daily_cap + carry
            credited = min(dist, available)
            cumulative += credited
            carry = available - credited
            progress.append({"date": entry["date"], "cumulative_km": cumulative})
        result[rider_id] = progress

    return result


def find_arrival_day(progress, km_mark):
    """Find the date a rider's cumulative distance first passes a km mark.

    Returns (date, cumulative_km) or None if not yet reached.
    """
    for entry in progress:
        if entry["cumulative_km"] >= km_mark:
            return entry["date"], entry["cumulative_km"]
    return None


def calculate_points(daily_log, rider_config, points_config, seed=42):
    """Calculate all sprint and climbing points.

    Returns dict with per-rider totals and per-location results.
    """
    rider_ids = [r["id"] for r in rider_config["riders"]]
    cumulative = calculate_capped_distances(daily_log, rider_config)

    rng = random.Random(seed)

    all_locations = []
    for sprint in points_config["sprints"]:
        all_locations.append({**sprint, "type": "sprint"})
    for climb in points_config["climbs"]:
        all_locations.append({**climb, "type": "climb"})

    # Initialize per-rider totals
    rider_totals = {}
    for rider_id in rider_ids:
        rider_totals[rider_id] = {
            "sprintPoints": 0,
            "climbPoints": 0,
            "totalPoints": 0,
        }

    # Calculate points per location
    location_results = []
    for loc in all_locations:
        km_mark = loc["km"]
        points_available = loc["points"]

        # Find which riders have passed this point and when
        arrivals = []
        for rider_id in rider_ids:
            result = find_arrival_day(cumulative[rider_id], km_mark)
            if result:
                date, cum_km = result
                arrivals.append({
                    "rider": rider_id,
                    "date": date,
                    "cumulative_km": cum_km,
                })

        if not arrivals:
            location_results.append({
                "name": loc["name"],
                "type": loc["type"],
                "segment": loc["segment"],
                "km": km_mark,
                "awards": [],
                "reached": False,
            })
            continue

        # Sort by arrival date, then by cumulative km (further = arrived earlier
        # in the day conceptually), then random tiebreak
        arrivals.sort(key=lambda a: (a["date"], -a["cumulative_km"], rng.random()))

        awards = []
        for place, arrival in enumerate(arrivals):
            pts = points_available[place] if place < len(points_available) else 0
            awards.append({
                "place": place + 1,
                "rider": arrival["rider"],
                "date": arrival["date"],
                "points": pts,
            })

            # Add to rider totals
            if loc["type"] == "sprint":
                rider_totals[arrival["rider"]]["sprintPoints"] += pts
            else:
                rider_totals[arrival["rider"]]["climbPoints"] += pts
            rider_totals[arrival["rider"]]["totalPoints"] += pts

        location_results.append({
            "name": loc["name"],
            "type": loc["type"],
            "segment": loc["segment"],
            "km": km_mark,
            "awards": awards,
            "reached": True,
        })

    return {
        "riders": rider_totals,
        "locations": location_results,
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate rider competition points")
    parser.add_argument("--daily-log", default="data/riders/daily-log.json")
    parser.add_argument("--rider-config", default="data/riders/rider-config.json")
    parser.add_argument("--points-config", default="data/competition/points-config.json")
    parser.add_argument("--output", default="data/riders/points.json")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for tiebreaking")
    args = parser.parse_args()

    daily_log = load_json(args.daily_log)
    rider_config = load_json(args.rider_config)
    points_config = load_json(args.points_config)

    result = calculate_points(daily_log, rider_config, points_config, seed=args.seed)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Points calculated ({len(result['locations'])} locations)")
    print()
    for rider_id, totals in result["riders"].items():
        rider_name = next(r["name"] for r in rider_config["riders"] if r["id"] == rider_id)
        print(f"  {rider_name}: sprint={totals['sprintPoints']} climb={totals['climbPoints']} total={totals['totalPoints']}")

    reached = sum(1 for loc in result["locations"] if loc["reached"])
    print(f"\n  {reached}/{len(result['locations'])} point locations reached")
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()
