# Processing Scripts

Python data pipeline for the Correze Travelogue.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Scripts

### split_gpx.py

Parses `data/main.gpx` and splits the route into 26 segments.

```bash
.venv/bin/python split_gpx.py
```

**Input:** `data/main.gpx`
**Output:**
- `data/segments/segment-NN.gpx` (26 files)
- `data/segments.json` (segment metadata with coordinates, towns, climbs)

**Options:**
- `--gpx PATH` — GPX file (default: `data/main.gpx`)
- `--output-dir DIR` — segment GPX output (default: `data/segments`)
- `--json-output PATH` — metadata JSON (default: `data/segments.json`)
- `--num-segments N` — number of segments (default: 26)

### elevation_profile.py

Generates elevation profiles, gradient calculations, and power estimates per segment.

```bash
.venv/bin/python elevation_profile.py
```

**Input:** `data/segments/segment-NN.gpx`
**Output:** `data/elevation/segment-NN.json`

Each output file contains distance, elevation, gradient, and power arrays plus a summary with avg/max gradient, elevation gain/loss, average power at 30/35/40 km/h, and estimated times.

**Options:**
- `--segments-dir DIR` — segment GPX directory (default: `data/segments`)
- `--output-dir DIR` — elevation JSON output (default: `data/elevation`)

### rider_stats.py

Calculates rider statistics from the daily distance log.

```bash
.venv/bin/python rider_stats.py
```

**Input:**
- `data/riders/daily-log.json` — daily distance entries
- `data/riders/rider-config.json` — rider names, colours, daily cap

**Output:** `data/riders/stats.json`

Calculates uncapped stats (longest day, best 3-day combo, consistency) and capped stats with rolling carry-over (total distance, daily average, estimated finish date).

**Options:**
- `--daily-log PATH` — daily log file
- `--rider-config PATH` — rider config file
- `--output PATH` — stats output file

### suggest_images.py

Queries Wikimedia Commons for CC-licensed images near each segment.

```bash
.venv/bin/python suggest_images.py
.venv/bin/python suggest_images.py --segment 4  # single segment
```

**Input:** `data/segments.json`
**Output:** `data/image-suggestions/segment-NN.json`

**Options:**
- `--segments-json PATH` — segments metadata
- `--output-dir DIR` — suggestions output
- `--radius N` — search radius in meters (default: 5000)
- `--segment N` — process a single segment

### weather.py

Fetches current weather for a segment location and injects into entry frontmatter.

```bash
OPENWEATHERMAP_API_KEY=xxx .venv/bin/python weather.py --entry current
.venv/bin/python weather.py --entry 4 --api-key xxx
```

**Input:** `data/segments.json`, `content/entries/*.md`
**Output:** Updates `weather` field in entry frontmatter

**Options:**
- `--entry current|N` — most recent entry or segment number
- `--api-key KEY` — OpenWeatherMap API key (or set `OPENWEATHERMAP_API_KEY` env var)
- `--segments-json PATH` — segments metadata
- `--entries-dir DIR` — entries directory

## Data Flow

```
main.gpx
  └─> split_gpx.py
        ├─> segments/*.gpx
        ├─> segments.json
        └─> elevation_profile.py
              └─> elevation/*.json

segments.json
  └─> suggest_images.py
        └─> image-suggestions/*.json
  └─> weather.py
        └─> content/entries/*.md (weather field)

riders/daily-log.json + rider-config.json
  └─> rider_stats.py
        └─> riders/stats.json
```
