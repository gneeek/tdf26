#!/usr/bin/env python3
"""Generate fictional race narrative for point locations in a segment."""

import argparse
import json
import random


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def rider_name(rider_id, rider_config):
    """Look up rider display name from config."""
    for r in rider_config["riders"]:
        if r["id"] == rider_id:
            return r["name"]
    return rider_id


SPRINT_TEMPLATES = [
    "At the intermediate sprint in {name} (km {km}), {first} powered through first to claim {pts1} points{rest}.",
    "The sprint at {name} (km {km}) saw {first} surge ahead for {pts1} points{rest}.",
    "{first} took the sprint at {name} (km {km}), picking up {pts1} points{rest}.",
    "Through {name} (km {km}), {first} hit the line first for {pts1} sprint points{rest}.",
]

CLIMB_TEMPLATES = [
    "On the slopes of {name} (km {km}, {cat}), {first} crested first, taking {pts1} climbing points{rest}.",
    "{first} reached the summit of {name} (km {km}, {cat}) first for {pts1} points{rest}.",
    "The {cat} climb at {name} (km {km}) went to {first} with {pts1} points{rest}.",
    "At the top of {name} (km {km}, {cat}), {first} crossed first to claim {pts1} climbing points{rest}.",
]

NO_POINTS_TEMPLATES = [
    "No points were contested in this segment. The riders pressed on through the terrain.",
    "This stretch of road held no sprints or summits. The riders settled into their rhythm.",
    "With no points on offer, the riders focused on the road ahead.",
]

NOT_REACHED_TEMPLATES = [
    "The {type} at {name} (km {km}) awaits - no riders have reached it yet.",
    "Ahead lies the {type} at {name} (km {km}), still unclaimed.",
]


def format_category(category):
    """Format climb category for display."""
    if category == "HC":
        return "Hors Categorie"
    return f"Cat {category}"


def format_rest(awards, rider_config):
    """Format the rest of the finishers after 1st place."""
    if len(awards) < 2:
        return ". No other riders had reached this far"

    parts = []
    for award in awards[1:]:
        if award["points"] > 0:
            name = rider_name(award["rider"], rider_config)
            parts.append(f"{name} for {award['points']}")

    if not parts:
        return ""

    if len(parts) == 1:
        return f", with {parts[0]}"

    return ", with " + ", ".join(parts[:-1]) + f" and {parts[-1]}"


def generate_narrative(points_data, rider_config, segment, seed=42):
    """Generate narrative text for point locations in a segment.

    Returns a string with one paragraph per point location, or a
    brief message if no points are in this segment.
    """
    rng = random.Random(seed)

    locations = [
        loc for loc in points_data.get("locations", [])
        if loc["segment"] == segment
    ]

    if not locations:
        return rng.choice(NO_POINTS_TEMPLATES)

    paragraphs = []
    for loc in locations:
        if not loc["reached"] or not loc["awards"]:
            template = rng.choice(NOT_REACHED_TEMPLATES)
            paragraphs.append(template.format(
                type="sprint" if loc["type"] == "sprint" else "climb",
                name=loc["name"],
                km=loc["km"],
            ))
            continue

        first_award = loc["awards"][0]
        first_name = rider_name(first_award["rider"], rider_config)
        rest_text = format_rest(loc["awards"], rider_config)

        if loc["type"] == "sprint":
            template = rng.choice(SPRINT_TEMPLATES)
            paragraphs.append(template.format(
                name=loc["name"],
                km=loc["km"],
                first=first_name,
                pts1=first_award["points"],
                rest=rest_text,
            ))
        else:
            cat = format_category(loc.get("category", "?"))
            template = rng.choice(CLIMB_TEMPLATES)
            paragraphs.append(template.format(
                name=loc["name"],
                km=loc["km"],
                cat=cat,
                first=first_name,
                pts1=first_award["points"],
                rest=rest_text,
            ))

    return "\n\n".join(paragraphs)


def main():
    parser = argparse.ArgumentParser(description="Generate segment race narrative")
    parser.add_argument("--points", default="data/riders/points.json")
    parser.add_argument("--rider-config", default="data/riders/rider-config.json")
    parser.add_argument("--segment", type=int, required=True, help="Segment number")
    parser.add_argument("--output", help="Optional output file (default: stdout)")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    points_data = load_json(args.points)
    rider_config = load_json(args.rider_config)

    narrative = generate_narrative(points_data, rider_config, args.segment, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(narrative)
        print(f"Wrote narrative for segment {args.segment} to {args.output}")
    else:
        print(narrative)


if __name__ == "__main__":
    main()
