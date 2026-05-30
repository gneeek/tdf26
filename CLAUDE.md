# Corrèze Travelogue — Project Specification

> **Keep this file to load-bearing every-session instruction.** Bulk reference appendices (cycling history, CC image sources, historical/cultural sources by area) were relocated under #627 to `docs/reference/` and the `content/research/` dossiers. Do not re-add large reference tables or source lists here; add a pointer instead. See the `## References` section near the end for the map.

## Project Overview

A cycling travelogue blog following the 185km route of Stage 9 of the 2026 Tour de France, from Malemort to Ussel through the Corrèze department of France. The route is divided into 27 segments with alternating lengths (odd-numbered ~8km, even-numbered ~6km, per `processing/split_gpx.py`). One blog entry per segment is published twice weekly from early April to early July 2026, building anticipation toward the actual stage on Sunday, July 12, 2026.

The project has four pillars:
1. **Route data processing** — GPX parsing, segment splitting, elevation profiles, power estimates
2. **Static blog site** — Nuxt 3 with Nuxt Content, Leaflet maps, elevation charts, image galleries
3. **Rider stats tracker** — 4 riders log daily distances; stats are calculated and displayed per entry
4. **Publish-day pipeline** — weather data injection, rider stats update, site regeneration, deployment

## Agent Ownership

This project uses a two-agent ownership model for its repositories:

- **Tully** owns `gneeek/tdf26` (this repo). Biased toward project-specific craft, voice, and publisher experience. Has tie-breaking authority on tdf26 decisions.
- **Piers** owns `gneeek/unfold` (the portable-practices companion site, shipping in v1.3.5). Biased toward structure, distillation, and what travels across projects. Has tie-breaking authority on unfold decisions.

Both voices contribute to any discussion. The owning voice's judgment is authoritative for its repo. When a proposed change fits one repo better than the other, the right answer is often "direct it to the other repo" rather than "force it in here."

See `feedback_agent_ownership.md` in the memory system for the full model including push-back criteria and deference rules.

## Tech Stack

- **Runtime:** Node.js 22+ (Nuxt/Vue), Python 3.11+ (data processing)
- **Framework:** Nuxt 3 with Nuxt Content module
- **Maps:** Leaflet.js with OpenStreetMap tiles
- **Charts:** Chart.js or D3.js for elevation profiles and rider stats
- **Data processing:** Python with gpxpy, geopy, numpy, matplotlib, Pillow
- **Hosting:** Static site deployed to a Linux VPS (Ubuntu 24, DigitalOcean or OVH)
- **Deployment:** Git push → simple CI/CD (e.g., a post-receive hook or GitHub Actions) → `nuxt generate` on server
- **Weather API:** OpenWeatherMap or Météo-France API (free tier)
- **Image sources:** Wikimedia Commons API, Unsplash, Flickr Creative Commons

## Directory Structure

```
correze-travelogue/
├── CLAUDE.md                    # This file
├── nuxt.config.ts
├── package.json
├── content/
│   └── entries/                 # Markdown blog entries (one per segment)
│       ├── 01-malemort-departure.md
│       ├── 02-toward-turenne.md
│       └── ...
├── data/
│   ├── master.gpx               # Full Stage 9 GPX file (uploaded by user)
│   ├── segments/                 # Generated: 26 individual GPX files
│   │   ├── segment-01.gpx
│   │   └── ...
│   ├── segments.json             # Generated: master segment metadata
│   ├── elevation/                # Generated: per-segment elevation + power data
│   │   ├── segment-01.json
│   │   └── ...
│   └── riders/
│       ├── daily-log.json        # Daily distance entries for all 4 riders
│       ├── stats.json            # Generated: calculated rider stats
│       └── rider-config.json     # Rider names, colors, display preferences
├── processing/                   # Python data pipeline
│   ├── requirements.txt
│   ├── split_gpx.py              # Parse master GPX → 26 segment GPX files + segments.json
│   ├── elevation_profile.py      # Generate elevation + power data per segment
│   ├── rider_stats.py            # Calculate rider stats from daily-log.json
│   ├── weather.py                # Fetch weather data for publish day
│   └── suggest_images.py         # Query Wikimedia Commons by segment coordinates
├── components/
│   ├── ElevationChart.vue        # Elevation profile with gradient coloring
│   ├── PowerStats.vue            # Estimated watts for a reference cyclist
│   ├── SegmentMap.vue            # Leaflet map rendering segment GPX track
│   ├── ImageGallery.vue          # CC-licensed images with attribution
│   ├── WeatherWidget.vue         # Current weather at segment location
│   ├── RiderDashboard.vue        # Rider stats table and charts
│   └── PublishSchedule.vue       # Visual timeline of entries and publish dates
├── layouts/
│   └── default.vue
├── pages/
│   ├── index.vue                 # Homepage with route overview map + latest entry
│   └── entries/
│       └── [...slug].vue         # Dynamic entry pages
├── public/
│   ├── images/                   # Downloaded CC images with attribution files
│   └── gpx/                      # Segment GPX files (for user download)
├── scripts/
│   ├── publish.sh                # Publish-day script: weather + rider stats + generate
│   └── add-rider-data.sh         # Helper to input daily rider distances
└── server/                       # Nuxt server routes (if needed for API endpoints)
```

## Phase 1: Data Foundation (Python)

### 1a. GPX Parsing and Segment Splitting (`split_gpx.py`)

- Read `data/master.gpx` using `gpxpy`
- Calculate cumulative distance along the full track
- Split into 27 segments with alternating lengths (odd-numbered ~8km, even-numbered ~6km; default `num_segments=27` in `split_gpx.py`)
- For each segment, output:
  - A standalone GPX file (`data/segments/segment-NN.gpx`)
  - Metadata entry in `data/segments.json`:
    ```json
    {
      "segment": 1,
      "km_start": 0,
      "km_end": 7.1,
      "start_lat": 45.1567,
      "start_lng": 1.5234,
      "end_lat": 45.1890,
      "end_lng": 1.5678,
      "elevation_gain": 142,
      "elevation_loss": 87,
      "min_elevation": 114,
      "max_elevation": 312,
      "notable_points": [],
      "towns": [],
      "climbs": []
    }
    ```
- Cross-reference known waypoints (Turenne, Collonges-la-Rouge, Beynat, Tulle, Naves, Chaumeil, Treignac, Bugeat, Meymac, Ussel) and known climbs (Puy Boubou, Côte de Lagleygeolle, Côte de Miel, Côte des Naves, Puy de Lachaud, Suc au May, Côte de la Croix de Pey, Mont Bessou, Côte des Gardes) to populate `notable_points`, `towns`, and `climbs` fields

### 1b. Elevation Profiles and Power Estimates (`elevation_profile.py`)

- For each segment, generate:
  - Elevation profile data as JSON (distance vs elevation arrays)
  - Gradient calculations (smoothed over 100m intervals)
  - Gradient-colored profile data for the chart component
- Power estimates using standard cycling physics:
  - Reference rider: 70kg rider + 8kg bike, CdA 0.35, Crr 0.005
  - Calculate instantaneous power at each point for speeds of 30, 35, 40 km/h
  - Output: average power, normalized power, peak power per segment
  - These are "what would a strong amateur need" estimates, not pro watts

### 1c. Image Suggestions (`suggest_images.py`)

- For each segment, query Wikimedia Commons API using segment midpoint coordinates
- Filter for CC-licensed landscape/architecture photos
- Output a suggestions file per segment listing URLs, licenses, and descriptions
- Final image selection is manual (human picks the best ones)

## Phase 2: Nuxt Site Scaffold

### 2a. Project Setup

- Initialize Nuxt 3 project with:
  - `@nuxt/content` module
  - `@nuxtjs/tailwindcss` for styling
  - `vue-leaflet` or raw Leaflet for maps
  - `chart.js` with `vue-chartjs` for elevation and stats charts
- Configure Nuxt Content to read from `content/entries/`
- Set up static generation (`nuxt generate`)

### 2b. Core Components

**SegmentMap.vue**
- Renders a Leaflet map with OpenStreetMap tiles
- Loads segment GPX file and displays the track as a colored polyline
- Shows start/end markers and notable point markers
- Optionally shows the full route in light gray with current segment highlighted
- Responsive; works on mobile

**ElevationChart.vue**
- Renders elevation profile from segment JSON data
- X-axis: distance (km), Y-axis: elevation (m)
- Color-coded by gradient (green < 3%, yellow 3-6%, orange 6-9%, red > 9%)
- Hover shows elevation, gradient, and estimated power at that point

**PowerStats.vue**
- Displays a summary card with:
  - Average gradient for the segment
  - Estimated average power at 35 km/h for reference rider
  - Total elevation gain/loss
  - Estimated time for the segment at different paces

**ImageGallery.vue**
- Displays CC-licensed images in a responsive grid or carousel
- Shows attribution (author, license, source link) for each image
- Supports optional short video embeds (YouTube/Vimeo CC content)

**WeatherWidget.vue**
- Displays weather at the segment's approximate location
- Data injected at publish time from weather API
- Shows temperature, conditions, wind — "what it's like there today"
- Falls back gracefully if weather data is unavailable

**RiderDashboard.vue**
- Displays the rider stats table (see Phase 3 below)
- Visual elements: bar chart of cumulative distance, sparklines of daily effort
- Color-coded per rider (configurable in rider-config.json)

### 2c. Layout and Pages

- Clean, magazine-style layout optimized for reading
- Homepage shows: full route map with published segments highlighted, latest entry preview, rider standings, publish schedule
- Entry pages show: segment map, elevation chart, power stats, narrative content, image gallery, weather widget, rider dashboard
- Navigation: previous/next entry, jump to any published entry
- Responsive design for mobile sharing

### 2d. Blog Entry Format (Markdown + Frontmatter)

Each entry in `content/entries/` follows this structure:

```markdown
---
segment: 1
title: "Malemort — Where Pain Meets Death"
subtitle: "Km 0–7.1: Departure from the Corrèze lowlands"
publishDate: 2026-04-02
kmStart: 0
kmEnd: 7.1
gpxFile: /gpx/segment-01.gpx
elevationData: /data/elevation/segment-01.json
images: [{"src": "/images/segment-01/malemort-centre.jpg", "alt": "Malemort town centre", "attribution": "Photo by Jean Dupont, CC BY-SA 4.0, Wikimedia Commons"}, {"src": "/images/segment-01/brive-panorama.jpg", "alt": "View toward Brive-la-Gaillarde", "attribution": "Photo by Marie Claire, CC BY 2.0, Flickr"}]
weather: null  # Populated by publish script
draft: false
---

# Malemort — Where Pain Meets Death

The name alone should give our four riders pause...

[Narrative content here — scenery, history, culture, cycling context]
```

**Image frontmatter convention — use inline JSON.** The `images` field must be a single-line JSON array of objects (`images: [{"src": ..., "alt": ..., "attribution": ...}]`), as shown above — not a multi-line YAML block list. Rationale: the frontmatter parsers are currently regex-based, and only the inline-JSON form yields real per-image fields. `processing/validate_entries.py` accepts the YAML block-list form but parses it crudely (it counts `- src:` lines and drops `alt`/`attribution`), and this fragility is the class of bug behind the seg-9 publish-day crash. Full YAML-list support is gated on #326 (consolidation onto a single real parser); until that lands, inline JSON is the required form for every new entry.

## Phase 3: Rider Stats Tracker

### 3a. Data Model

**rider-config.json:**
```json
{
  "riders": [
    { "id": "justin", "name": "Justin", "color": "#DAA520" },
    { "id": "marian", "name": "Marian", "color": "#4682B4" },
    { "id": "nan", "name": "Nan", "color": "#FF00FF" },
    { "id": "wally", "name": "Wally", "color": "#8B0000" }
  ],
  "totalDistance": 185,
  "dailyCap": 2,
  "startDate": "2026-04-02"
}
```

**daily-log.json:**
```json
{
  "entries": [
    {
      "date": "2026-04-02",
      "distances": {
        "justin": 3.2,
        "marian": 2.8,
        "nan": 4.1,
        "wally": 1.5
      }
    }
  ]
}
```

### 3b. Stats Calculations (`rider_stats.py`)

The script reads `daily-log.json` and `rider-config.json` and outputs `stats.json`.

**Stats using ACTUAL daily distances (uncapped):**
- Longest Day: max single-day distance
- Shortest Day: min single-day distance (excluding zero/rest days, or including — TBD)
- Best 3 Day Combo: highest sum of any 3 consecutive days
- Most Recent 5 Day Average: average of last 5 logged days
- Most Consistent: lowest standard deviation of daily distances (reward steady effort)
- Days Below 3km: count of days where distance < 3km

**Stats using CAPPED daily distances (max 2km/day):**
- Total Distance Covered: sum of min(actual, 2.0) per day
- Daily Average (capped): mean of capped distances
- Distance Remaining: 185 - total capped distance
- Estimated Days to Finish: distance remaining / average capped daily distance
- Estimated Finish Date: today + estimated days to finish

**Ranking:**
- Place: ranked by total capped distance covered (ties allowed)
- Points: scoring system TBD (could be based on daily rankings, consistency bonuses, etc.)

**Output (`stats.json`):**
```json
{
  "asOf": "2026-05-15",
  "entryNumber": 12,
  "riders": {
    "justin": {
      "place": 1,
      "points": 71,
      "totalDistanceCapped": 141,
      "dailyAverageCapped": 3.0,
      "longestDay": 5.7,
      "shortestDay": 0.5,
      "daysBelowThreeKm": 5,
      "mostConsistentRank": 3,
      "bestThreeDayCombo": 12.4,
      "recentFiveDayAverage": 3.0,
      "distanceRemaining": 29,
      "estimatedDaysToFinish": 10,
      "estimatedFinishDate": "2026-07-07"
    }
  }
}
```

### 3c. Data Entry Helper (`add-rider-data.sh`)

A simple CLI script that:
- Prompts for the date (defaults to today)
- Prompts for each rider's distance
- Appends to `daily-log.json`
- Runs `rider_stats.py` to regenerate `stats.json`
- Shows updated standings in the terminal

### 3d. Dashboard Display

The `RiderDashboard.vue` component renders:
- A stats table matching the spreadsheet layout from the 2025 version (see screenshot reference)
- Color-coded per rider
- Cumulative distance bar chart showing each rider's progress along the 185km route
- Optional: sparkline per rider showing daily distance over time

## Phase 4: Publishing Pipeline

### 4a. Publish-Day Workflow (`publish.sh`)

Run on the morning of each publish day (Tuesdays and Fridays, or whatever schedule is chosen):

```bash
#!/bin/bash
# 1. Ensure rider data is up to date
python processing/rider_stats.py

# 2. Fetch weather for current entry's segment location
python processing/weather.py --entry current

# 3. Regenerate static site
npx nuxt generate

# 4. Deploy to VPS
rsync -avz .output/public/ user@vps:/var/www/correze-travelogue/

# 5. Commit frontmatter changes (dataCutoff, weather) to main so main
#    matches the deployed artifact immediately after deploy
git add content/entries/<entry>.md && git commit -m "..." && git push origin main
```

The actual script (`scripts/publish.sh`) has additional steps for points calculation, per-segment stats snapshots, race narrative generation, and image validation. Run `./scripts/publish.sh --help` for current flags.

### 4b. Weather Integration (`weather.py`)

- Reads `segments.json` to find the current entry's segment midpoint coordinates
- Calls OpenWeatherMap API (or Météo-France) for current conditions and 3-day forecast
- Writes weather data into the entry's frontmatter `weather` field
- Weather data structure:
  ```json
  {
    "current": { "temp": 18, "conditions": "Partly cloudy", "wind": "12 km/h SW" },
    "forecast": "Warm and dry through the weekend"
  }
  ```

### 4c. Deployment

- VPS runs Nginx serving the static site from `/var/www/correze-travelogue/`
- SSL via Let's Encrypt / Certbot
- Domain: TBD (user to configure)
- Simple rsync deploy from local build, or git-based with a post-receive hook

## Publication Schedule

27 entries, published twice weekly on Sundays and Wednesdays starting Sunday April 5, 2026, with the final finish-line entry timed for race-week. Authoritative schedule lives in entry frontmatter (`publishDate:` field of each `content/entries/*.md`); the wiki Roadmap surfaces upcoming cycles.

## Content Topics Per Entry

Each entry (~800–1200 words) should weave together:

1. **Scenery description** — what the riders see in this 7km stretch
2. **Local history** — medieval, Resistance, industrial, religious
3. **Geography and geology** — limestone, red sandstone, granite, river valleys, plateaus
4. **Archaeology** — prehistoric sites, Roman roads, medieval ruins
5. **Culture** — local traditions, cuisine, festivals, accordion/lace-making in Tulle
6. **Famous local people** — historical and contemporary figures from the area
7. **Cycling context** — Tour de France history in the region, stage tactics, climb analysis
8. **The four riders** — brief narrative of their fictional/real progress, stats reference

## Known Waypoints and Climbs (for segment assignment)

Town and climb facts previously listed here have moved to the `data/*.json` files. CLAUDE.md keeps narrative project context; the JSON files are the source of truth for route geometry, town positions, and climb metadata. The pointers below tell you which file to read for which question.

### Major Towns
- **Per-segment town assignments:** `data/segments.json` — each segment object has a `towns` array naming the towns the route passes through.
- **Town coordinates and notes:** `data/town-coords.json` — keyed by town name. Includes a `note` field for towns whose city centre sits off the route polyline (e.g., Ussel).

When you need to answer "what town is in segment N?", read `segments.json`. When you need a coordinate for a town, read `town-coords.json`.

### Categorized Climbs
- **Climb metadata (segment, summit km, length, gradient, ASO category, points):** `data/competition/points-config.json` — `climbs` array. Single source of truth: `processing/split_gpx.py` imports from here, and `data/segments.json` climb assignments are generated accordingly.
- **Climb summit coordinates:** `data/town-coords.json` — climbs share the file with towns; `"type": "climb"` distinguishes them.

Two narrative notes that don't fit a JSON shape:
- **Mont Bessou** is the highest point in Corrèze (summit 977m).
- **Suc au May** summits around km 105 at approximately 903m elevation.

ASO categorisation (HC, Cat 2, etc.) is on each climb in points-config. Whether the points-config climb list matches the official ASO 2026 Stage 9 categorised-climb list is tracked under issue #492.

## Development Notes

- All Python scripts should be runnable independently and as part of the publish pipeline
- Use `argparse` for Python CLI interfaces
- Segment numbering is 1-indexed throughout (segment 1 = first entry)
- All distances are in kilometers, elevations in meters
- Times/dates use ISO 8601 format
- The GPX master file is the single source of truth for route geometry
- Rider stats are recalculated fresh each time from the full daily-log.json
- The site must work fully as a static site — no server-side rendering required at runtime
- Prioritize mobile-responsive design; entries will be shared on social media
- New repositories in this ecosystem use Apache 2.0 for code repos and CC BY-SA 4.0 for content/text repos. The `gh repo create --license` default is Apache 2.0, which is wrong for content-centric repos such as `unfold`; pass the correct flag explicitly at creation time.

## References

The bulk reference appendices that used to live here were relocated under #627 to keep this file to load-bearing every-session instruction. Consult these surfaces when drafting; do not copy their contents back into this file.

- **Cycling history along the route** (Tour de France in the corridor, Tour du Limousin, Paris-Corrèze, L'Agglomérée) → `content/research/tour-history-research.md`. Two items the dossier does not own (La Corrézienne VTT, CycleBlaze touring journals) → `docs/reference/cycling-history.md`.
- **Creative Commons image sources** (per-segment Wikimedia categories, confirmed CC photographers, geosearch API, video sources) → `docs/reference/cc-image-sources.md`.
- **Historical and cultural sources by area** (key topics per area; for segments with a research dossier, that dossier is the source of truth) → `docs/reference/historical-cultural-sources.md`.
