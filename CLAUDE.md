# Corrèze Travelogue — Project Specification

## Project Overview

A cycling travelogue blog following the 185km route of Stage 9 of the 2026 Tour de France, from Malemort to Ussel through the Corrèze department of France. The route is divided into 26 segments of approximately 7.1km each. One blog entry per segment is published twice weekly from early April to early July 2026, building anticipation toward the actual stage on Sunday, July 12, 2026.

The project has four pillars:
1. **Route data processing** — GPX parsing, segment splitting, elevation profiles, power estimates
2. **Static blog site** — Nuxt 3 with Nuxt Content, Leaflet maps, elevation charts, image galleries
3. **Rider stats tracker** — 4 riders log daily distances; stats are calculated and displayed per entry
4. **Publish-day pipeline** — weather data injection, rider stats update, site regeneration, deployment

## Tech Stack

- **Runtime:** Node.js 20+ (Nuxt/Vue), Python 3.11+ (data processing)
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
- Split into 26 segments of approximately 7.1km each (185km / 26)
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
images:
  - src: /images/segment-01/malemort-centre.jpg
    alt: "Malemort town centre"
    attribution: "Photo by Jean Dupont, CC BY-SA 4.0, Wikimedia Commons"
  - src: /images/segment-01/brive-panorama.jpg
    alt: "View toward Brive-la-Gaillarde"
    attribution: "Photo by Marie Claire, CC BY 2.0, Flickr"
weather: null  # Populated by publish script
draft: false
---

# Malemort — Where Pain Meets Death

The name alone should give our four riders pause...

[Narrative content here — scenery, history, culture, cycling context]
```

## Phase 3: Rider Stats Tracker

### 3a. Data Model

**rider-config.json:**
```json
{
  "riders": [
    { "id": "justin", "name": "Justin", "color": "#DAA520" },
    { "id": "marian", "name": "Marian", "color": "#FFFFFF" },
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
```

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

26 entries, published twice weekly. Example starting April 2, 2026:

| Entry | Segment | Publish Date | Key Feature |
|-------|---------|-------------|-------------|
| 1 | Km 0–7 | Thu Apr 2 | Malemort, Brive-la-Gaillarde |
| 2 | Km 7–14 | Mon Apr 6 | Approach to Turenne |
| 3 | Km 14–21 | Thu Apr 9 | Turenne (Plus Beau Village) |
| 4 | Km 21–28 | Mon Apr 13 | Collonges-la-Rouge |
| 5 | Km 28–35 | Thu Apr 16 | Puy Boubou climb |
| ... | ... | ... | ... |
| 25 | Km 170–178 | Thu Jul 2 | Approach to Ussel |
| 26 | Km 178–185 | Mon Jul 6 | Ussel — Place Voltaire finish |

Full schedule to be generated once GPX is parsed and segments are confirmed.

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

### Major Towns (approximate km)
- Malemort: km 0
- Brive-la-Gaillarde: km 3–6
- Turenne: km 16–18
- Collonges-la-Rouge: km 22–25
- Beynat: km 35–40
- Tulle: km 63–68
- Naves: km 72–75
- Chaumeil: km 88–92
- Treignac: km 115–118
- Bugeat: km 128–132
- Meymac: km 155–160
- Ussel: km 180–185

### Categorized Climbs
- Puy Boubou: 2.8km at 4.1%
- Côte de Lagleygeolle: 5.2km at 3.9%
- Côte de Miel: 6.6km at 3.9%
- Côte des Naves: 2.8km at 6.7%
- Puy de Lachaud: 3.6km at 5.3%
- Suc au May: 3.8km at 7.7% (summit ~km 105, elevation 903m)
- Côte de la Croix de Pey: 7km at 4.9%
- Mont Bessou: summit 977m (highest point in Corrèze)
- Côte des Gardes: 2.2km at 4.8%

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

## References: Cycling History Along the Route

### Tour de France History in the Corridor

**Brive-la-Gaillarde (km 3–6)** — multiple Tour visits:
- **1951 Tour, Stage 11 (Brive → Agen):** Hugo Koblet's legendary 135km solo breakaway, holding off Coppi, Bobet, Bartali, Magni, Géminiani, and Robic. One of the greatest solo rides in Tour history. Source: bikeraceinfo.com/tdf/tdf1951.html
- **1996 Tour, Stage 15:** Departure from Brive to Villeneuve-sur-Lot.
- **2012 Tour, Stage 18 (Blagnac → Brive):** Mark Cavendish sprint victory in the rainbow jersey. Bradley Wiggins in yellow. Source: cyclehistory.wordpress.com and procyclingstats.com

**Tulle (km 63–68)** — the departmental capital has hosted Tour du Limousin stages and is the base for local cycling clubs (Tulle Cyclisme Compétition). The L'Agglomérée cyclosportive departs from Tulle annually and in 2026 covers 40km of the Stage 9 route including Suc au May.

**Nearby/overlapping Tour stages:**
- **2024 Tour, Stage 11 (Évaux-les-Bains → Le Lioran):** 211km through the Massif Central with 4,350m climbing. Vingegaard vs Pogačar battle. Terrain very similar to Stage 9's second half. Dailymotion highlights: dailymotion.com/video/x90ywby
- **2024 Tour, Stage 12 (Aurillac → Villeneuve-sur-Lot):** Passed through the Cantal just south of the Stage 9 route.
- **2026 Tour, Stage 10 (Aurillac → Le Lioran):** Takes place the day after Stage 9, using Cantal roads adjacent to the Corrèze route. Same finale as 2024 where Vingegaard beat Pogačar in a photo finish.

### Regional Cycling Races

**Tour du Limousin** — 4-day professional stage race (UCI 2.1), held annually since 1968. Routes through Corrèze, Haute-Vienne, Creuse, and Dordogne on many of the same roads. Now called Tour du Limousin-Périgord-Nouvelle-Aquitaine. Wikipedia: en.wikipedia.org/wiki/Tour_du_Limousin

**Paris-Corrèze** — defunct professional race (UCI 2.1) that ran through the 2000s with stages finishing in Corrèze towns including Ussel. Archived results: autobus.cyclingnews.com

**L'Agglomérée Cyclosportive (Tulle, April 5, 2026)** — amateur sportive riding 40km of the actual Stage 9 route including the Suc au May climb. 85km and 105km options. Organized by Tulle Cyclisme Compétition. This event falls during the blog's first week of publication — potential tie-in content. Source: lagglomeree.agglo-tulle.fr

**La Corrézienne VTT** — mountain bike tour of the Corrèze department. Source: cyclotourisme-correze.fr

### CycleBlaze Touring Journals

CycleBlaze.com hosts touring journals with photos and ride reports through the exact towns on this route, including Turenne, Collonges-la-Rouge, and Curemonte. These provide ground-level cycling perspectives on the terrain. Example: cycleblaze.com/journals/pyreneesannsteve/turenne-collanges-la-rouge-and-curemonte/ — Check individual journal CC licenses before use.

## References: Creative Commons Image Sources

### Wikimedia Commons Categories (all CC BY-SA)

Primary location categories to query for each segment:

| Segment(s) | Wikimedia Commons Category | Notes |
|------------|---------------------------|-------|
| 1–2 | Category:Malemort, Category:Brive-la-Gaillarde | Town views, river Corrèze |
| 3 | Category:Turenne (Corrèze) | Castle ruins, hilltop village, panoramic views |
| 4 | Category:Collonges-la-Rouge | Extensive collection; red sandstone architecture |
| 5–6 | Category:Beynat | Smaller collection |
| 9–10 | Category:Tulle | River valley, cathedral, town views |
| 11–12 | Category:Naves, Corrèze | Limited |
| 15 | Category:Monédières | Suc au May area, heathland panoramas |
| 17 | Category:Treignac | Medieval bridge, granite town |
| 18–20 | Category:Plateau de Millevaches | Heathland, forests, remote landscapes |
| 19–20 | Category:Bugeat | Small town, Millevaches gateway |
| 22 | Category:Mont Bessou | Summit views (highest point in Corrèze) |
| 23–24 | Category:Meymac | Benedictine abbey, medieval town |
| 25–26 | Category:Ussel, Corrèze | Town centre, Place Voltaire |

### Confirmed CC-Licensed Photographers on Commons

These photographers have Corrèze-specific content confirmed as CC BY-SA:
- **E gargadennec** — Collonges-la-Rouge header images
- **Alertomalibu** — Collonges village streets, Castel de Vassinhac
- **Accrochoc** — Collonges architectural details, tympanum
- **Sail over** — Maison de la Sirène, Collonges

### Other CC/Open Image Sources

- **Unsplash** — search "Corrèze", "Limousin", "Dordogne valley" for landscape photography (Unsplash license, free for all uses)
- **Flickr Creative Commons** — search by geographic coordinates for each segment; filter by CC BY or CC BY-SA
- **Wikimedia Commons geosearch API** — `suggest_images.py` should query: `https://commons.wikimedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=5000&gsnamespace=6&gslimit=50`

### Video Sources

- **Dailymotion / Tour de France official channel** — ASO publishes stage highlight videos. Embeddable but check redistribution terms per video:
  - 2024 TdF Stage 11 highlights (Massif Central): dailymotion.com/video/x90ywby
  - 2024 TdF Stage 11 route preview: dailymotion.com/video/x9sik7s (check — may be 2026 stage 9 preview)
  - 2025 TdF highlights reel: dailymotion.com/video/x9npbe4
- **YouTube** — search "cycling Corrèze", "vélo Corrèze", "Suc au May cycling", "Plateau de Millevaches vélo" for amateur ride-along videos. Many cycling YouTubers post CC-licensed or embeddable content.
- **Tour du Limousin** — official race footage may be available via France 3 Nouvelle-Aquitaine archives or the race's social media channels.

## References: Historical and Cultural Sources for Entry Content

### Key Historical Topics by Area

**Malemort / Brive area (Segments 1–2):**
- Malemort is primarily known for rugby (CA Brive), not cycling — first-ever Tour de France visit
- Brive: Edmond Michelet museum (WWII Resistance), medieval old town
- The 2012 Cavendish sprint finish provides strong cycling narrative content

**Turenne (Segment 3):**
- One of the most powerful viscounties in France; the Turenne viscounts controlled much of the Corrèze from the medieval period until 1738 when sold to Louis XV
- Henri de La Tour d'Auvergne, Marshal of France, born in the castle
- "Plus Beaux Villages de France" designation

**Collonges-la-Rouge (Segment 4):**
- Founded by monks of Charroux Abbey (8th century), pilgrimage stop on the Way of St. James to Santiago de Compostela via Rocamadour
- Red sandstone colored by iron oxide — unique geological feature
- Birthplace of the "Plus Beaux Villages de France" association (founded by mayor Charles Ceyrac)
- Maison de la Sirène belonged to Henry de Jouvenel, husband of the writer Colette

**Tulle (Segments 9–10):**
- Historic lace-making and accordion-manufacturing centre
- WWII: site of the Tulle massacre (June 9, 1944) — 99 men hanged by the SS Das Reich division
- Departmental prefecture; François Hollande was mayor before becoming President of France

**Plateau de Millevaches (Segments 18–20):**
- Name derives from Celtic/Occitan roots meaning "thousand springs" (not "thousand cows")
- One of the least populated areas of France; vast heathland and peat bogs
- Regional Natural Park (Parc naturel régional de Millevaches en Limousin)

**Meymac (Segments 23–24):**
- Benedictine Abbaye Saint-André (founded 1085)
- Centre d'Art Contemporain housed in the abbey

**Ussel (Segments 25–26):**
- Historical gateway between the Limousin lowlands and the Auvergne highlands
- Jacques Chirac began his political career as a municipal councillor here
- Stage finish on Avenue Thiers, sprint judged at Place Voltaire
