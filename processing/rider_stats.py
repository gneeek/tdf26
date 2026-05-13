#!/usr/bin/env python3
"""Calculate rider stats from daily-log.json and output stats.json."""

import argparse
import json
import math
import statistics
from datetime import date, datetime, timedelta


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def capped_daily_distances(daily_dists, daily_cap):
    """Apply the rolling daily cap with carry-over to a list of daily distances.

    Each day's cap is the configured daily_cap plus any unused cap carried from
    earlier days. Returns the list of credited (capped) distances, in input order.

    This helper is the single source of truth for carry-over capping; it is
    imported by calculate_points.py so the two scripts cannot drift.
    """
    capped = []
    carry = 0.0
    for d in daily_dists:
        available = daily_cap + carry
        credited = min(d, available)
        capped.append(credited)
        carry = available - credited
    return capped


def calculate_stats(daily_log, rider_config, reference_date=None):
    """Calculate all stats for all riders.

    Parameters
    ----------
    daily_log, rider_config : dict
        Parsed JSON data.
    reference_date : datetime.date, optional
        The date against which "today"-relative outputs (asOf, estimatedFinishDate)
        are computed. Defaults to today's date for backwards compatibility with
        ad-hoc CLI use, but call sites that need reproducible output (publish.sh,
        snapshots, tests) MUST pass this explicitly. A `date` (not `datetime`) by
        design: estimated finish dates are reproducible across hours of the day.
        See issue #541.

    Banker's-rounding rule (see PR for #541, #328):
        Both estimatedDaysToFinish and estimatedFinishDate use math.floor of the
        raw float days. estimatedFinishDate = reference_date + floor(days). This
        matches the seg 11 hotfix and ensures the two displayed values can never
        disagree.
    """
    if reference_date is None:
        reference_date = date.today()
    elif isinstance(reference_date, datetime):
        reference_date = reference_date.date()

    riders = {r["id"]: r for r in rider_config["riders"]}
    total_distance = rider_config["totalDistance"]
    daily_cap = rider_config["dailyCap"]
    entries = daily_log["entries"]

    if not entries:
        return {"asOf": reference_date.isoformat(), "entryNumber": 0, "riders": {}}

    # Sort entries by date
    entries = sorted(entries, key=lambda e: e["date"])
    as_of = reference_date.isoformat()

    result = {
        "asOf": as_of,
        "entryNumber": len(entries),
        "riders": {},
    }

    for rider_id in riders:
        daily_dists = []
        for entry in entries:
            dist = entry.get("distances", {}).get(rider_id, 0)
            daily_dists.append(dist)

        if not daily_dists:
            continue

        # --- Stats using ACTUAL daily distances (uncapped) ---
        nonzero_dists = [d for d in daily_dists if d > 0]

        longest_day = max(daily_dists) if daily_dists else 0
        shortest_day = min(nonzero_dists) if nonzero_dists else 0

        # Best 3-day combo
        best_three_day = 0
        if len(daily_dists) >= 3:
            for i in range(len(daily_dists) - 2):
                combo = sum(daily_dists[i:i + 3])
                best_three_day = max(best_three_day, combo)
        else:
            best_three_day = sum(daily_dists)

        # Most recent 5-day average
        recent_five = daily_dists[-5:] if len(daily_dists) >= 5 else daily_dists
        recent_five_avg = statistics.mean(recent_five) if recent_five else 0

        # Consistency (std dev of daily distances)
        consistency_stdev = statistics.stdev(daily_dists) if len(daily_dists) >= 2 else 0

        # Days below 3km
        days_below_three = sum(1 for d in daily_dists if d < 3)

        # --- Daily average using ACTUAL distances ---
        daily_avg_actual = statistics.mean(daily_dists) if daily_dists else 0

        # --- Stats using CAPPED daily distances with carry-over ---
        capped_dists = capped_daily_distances(daily_dists, daily_cap)

        total_capped = sum(capped_dists)
        daily_avg_capped = statistics.mean(capped_dists) if capped_dists else 0
        distance_remaining = max(0, total_distance - total_capped)

        if daily_avg_capped > 0:
            est_days_raw = distance_remaining / daily_avg_capped
            # Floor rule: both displayed days and finish-date offset use the same
            # integer, so they cannot disagree. See module docstring on rounding.
            est_days_int = math.floor(est_days_raw)
            est_finish_date = (reference_date + timedelta(days=est_days_int)).isoformat()
            est_days_display = est_days_int
        else:
            est_days_display = None
            est_finish_date = None

        result["riders"][rider_id] = {
            "totalDistanceCapped": round(total_capped, 1),
            "dailyAverageActual": round(daily_avg_actual, 2),
            "dailyAverageCapped": round(daily_avg_capped, 2),
            "longestDay": round(longest_day, 1),
            "shortestDay": round(shortest_day, 1),
            "daysBelowThreeKm": days_below_three,
            "consistencyStdev": round(consistency_stdev, 2),
            "bestThreeDayCombo": round(best_three_day, 1),
            "recentFiveDayAverage": round(recent_five_avg, 2),
            "distanceRemaining": round(distance_remaining, 1),
            "estimatedDaysToFinish": est_days_display,
            "estimatedFinishDate": est_finish_date,
        }

    # Calculate rankings by total capped distance
    ranked = sorted(
        result["riders"].items(),
        key=lambda x: x[1]["totalDistanceCapped"],
        reverse=True,
    )
    for place, (rider_id, stats) in enumerate(ranked, 1):
        stats["place"] = place

    return result


def main():
    parser = argparse.ArgumentParser(description="Calculate rider stats")
    parser.add_argument("--daily-log", default="data/riders/daily-log.json")
    parser.add_argument("--rider-config", default="data/riders/rider-config.json")
    parser.add_argument("--output", default="data/riders/stats.json")
    parser.add_argument(
        "--reference-date",
        default=None,
        help="ISO date (YYYY-MM-DD) used for asOf and estimatedFinishDate. Defaults to today.",
    )
    args = parser.parse_args()

    daily_log = load_json(args.daily_log)
    rider_config = load_json(args.rider_config)

    ref = date.fromisoformat(args.reference_date) if args.reference_date else date.today()
    stats = calculate_stats(daily_log, rider_config, reference_date=ref)

    with open(args.output, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"Stats calculated as of {stats['asOf']} ({stats['entryNumber']} log entries)")
    print()

    for rider_id, s in stats["riders"].items():
        rider_name = next(r["name"] for r in rider_config["riders"] if r["id"] == rider_id)
        print(f"  #{s['place']} {rider_name}:")
        print(f"    Total (capped): {s['totalDistanceCapped']} km / {rider_config['totalDistance']} km")
        print(f"    Remaining: {s['distanceRemaining']} km")
        print(f"    Longest day: {s['longestDay']} km | Best 3-day: {s['bestThreeDayCombo']} km")
        if s['estimatedFinishDate']:
            print(f"    Est. finish: {s['estimatedFinishDate']} (~{s['estimatedDaysToFinish']} days)")
        print()

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
