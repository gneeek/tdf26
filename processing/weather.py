#!/usr/bin/env python3
"""Fetch weather data for a segment location and inject into entry frontmatter."""

import argparse
import json
import os
import re
import urllib.request
import urllib.parse


OPENWEATHERMAP_API = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(lat, lng, api_key):
    """Fetch current weather from OpenWeatherMap API."""
    params = {
        "lat": str(lat),
        "lon": str(lng),
        "appid": api_key,
        "units": "metric",
        "lang": "en",
    }
    url = f"{OPENWEATHERMAP_API}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        temp = round(data["main"]["temp"])
        conditions = data["weather"][0]["description"].capitalize()
        wind_speed = round(data["wind"]["speed"] * 3.6)  # m/s to km/h
        wind_deg = data["wind"].get("deg", 0)
        wind_dir = degree_to_compass(wind_deg)

        return {
            "current": {
                "temp": temp,
                "conditions": conditions,
                "wind": f"{wind_speed} km/h {wind_dir}",
            },
            "forecast": None,  # Could add forecast API call here
        }
    except Exception as e:
        print(f"  Warning: weather fetch failed: {e}")
        return None


def degree_to_compass(deg):
    """Convert wind degree to compass direction."""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(deg / 22.5) % 16
    return dirs[idx]


def inject_weather_into_entry(entry_path, weather_data):
    """Update the weather field in an entry's YAML frontmatter."""
    with open(entry_path, "r") as f:
        content = f.read()

    # Replace the weather field in frontmatter
    if weather_data:
        weather_yaml = json.dumps(weather_data)
        content = re.sub(
            r'^weather:.*$',
            f'weather: {weather_yaml}',
            content,
            count=1,
            flags=re.MULTILINE,
        )

    with open(entry_path, "w") as f:
        f.write(content)


def find_current_entry(entries_dir, segments_json):
    """Find the most recent entry that should have weather injected."""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # List all entry files
    entries = []
    for fname in sorted(os.listdir(entries_dir)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(entries_dir, fname)
        with open(path, "r") as f:
            content = f.read()

        # Extract segment number and publishDate from frontmatter
        seg_match = re.search(r'^segment:\s*(\d+)', content, re.MULTILINE)
        date_match = re.search(r'^publishDate:\s*(\S+)', content, re.MULTILINE)
        draft_match = re.search(r'^draft:\s*(\S+)', content, re.MULTILINE)

        if seg_match and date_match:
            seg_num = int(seg_match.group(1))
            pub_date = date_match.group(1)
            is_draft = draft_match.group(1).lower() == "true" if draft_match else False

            if not is_draft and pub_date <= today:
                entries.append((seg_num, pub_date, path))

    if not entries:
        return None

    # Return the most recently published entry
    entries.sort(key=lambda x: x[1], reverse=True)
    seg_num, pub_date, path = entries[0]

    # Find segment data
    with open(segments_json, "r") as f:
        segments = json.load(f)
    seg_data = next((s for s in segments if s["segment"] == seg_num), None)

    return {
        "segment": seg_num,
        "path": path,
        "publish_date": pub_date,
        "lat": (seg_data["start_lat"] + seg_data["end_lat"]) / 2 if seg_data else None,
        "lng": (seg_data["start_lng"] + seg_data["end_lng"]) / 2 if seg_data else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch weather for segment location")
    parser.add_argument("--entry", default="current",
                        help="'current' for most recent entry, or segment number (1-26)")
    parser.add_argument("--segments-json", default="data/segments.json")
    parser.add_argument("--entries-dir", default="content/entries")
    parser.add_argument("--api-key", default=None,
                        help="OpenWeatherMap API key (or set OPENWEATHERMAP_API_KEY env var)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENWEATHERMAP_API_KEY")
    if not api_key:
        print("Warning: No OpenWeatherMap API key provided.")
        print("Set OPENWEATHERMAP_API_KEY env var or use --api-key flag.")
        print("Skipping weather injection.")
        return

    if args.entry == "current":
        entry = find_current_entry(args.entries_dir, args.segments_json)
        if not entry:
            print("No published entry found.")
            return
    else:
        seg_num = int(args.entry)
        with open(args.segments_json, "r") as f:
            segments = json.load(f)
        seg_data = next((s for s in segments if s["segment"] == seg_num), None)
        if not seg_data:
            print(f"Segment {seg_num} not found.")
            return

        seg_str = str(seg_num).zfill(2)
        entry_files = [f for f in os.listdir(args.entries_dir)
                       if f.startswith(seg_str) and f.endswith(".md")]
        if not entry_files:
            print(f"No entry file found for segment {seg_num}.")
            return

        entry = {
            "segment": seg_num,
            "path": os.path.join(args.entries_dir, entry_files[0]),
            "lat": (seg_data["start_lat"] + seg_data["end_lat"]) / 2,
            "lng": (seg_data["start_lng"] + seg_data["end_lng"]) / 2,
        }

    print(f"Fetching weather for segment {entry['segment']} "
          f"({entry['lat']:.4f}, {entry['lng']:.4f})...")

    weather = get_weather(entry["lat"], entry["lng"], api_key)
    if weather:
        print(f"  {weather['current']['temp']}C, "
              f"{weather['current']['conditions']}, "
              f"{weather['current']['wind']}")
        inject_weather_into_entry(entry["path"], weather)
        print(f"  Injected into {entry['path']}")
    else:
        print("  No weather data available.")


if __name__ == "__main__":
    main()
