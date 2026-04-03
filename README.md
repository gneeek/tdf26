# Correze Travelogue

A cycling travelogue blog following the 185km route of Stage 9 of the 2026 Tour de France, from Malemort to Ussel through the Correze department of France.

26 blog entries, one per 7km segment, published twice weekly (Sunday and Wednesday) from April to July 2026. The peloton rides this road on Sunday, July 12.

## The Route

Malemort-sur-Correze to Ussel, 185km northeast through the Massif Central. Through the medieval villages of Turenne and Collonges-la-Rouge, over the departmental capital of Tulle, up the Suc au May (3.8km at 7.7%), across the Plateau de Millevaches, past Mont Bessou (977m, highest point in Correze), and down to the finish at Place Voltaire in Ussel.

9 categorized climbs. 2 "Plus Beaux Villages de France." 4 riders logging daily kilometers from home.

## Tech Stack

- **Site:** Nuxt 3, Nuxt Content, Tailwind CSS
- **Maps:** Leaflet.js with OpenStreetMap tiles
- **Charts:** Chart.js for elevation profiles
- **Data processing:** Python 3.11+ (gpxpy, numpy)
- **Hosting:** Static site (nuxt generate)

## Getting Started

Requires Node.js 22+ and Python 3.11+.

```bash
# Use correct Node version (if using nvm)
nvm use

# Install Node.js dependencies
npm install

# Run dev server
npx nuxt dev

# Build static site
npx nuxt generate
```

### Python data pipeline

```bash
# Set up Python environment
python3 -m venv processing/.venv
processing/.venv/bin/pip install -r processing/requirements.txt

# Split GPX into 26 segments
processing/.venv/bin/python processing/split_gpx.py

# Generate elevation profiles and power estimates
processing/.venv/bin/python processing/elevation_profile.py

# Suggest CC images from Wikimedia Commons
processing/.venv/bin/python processing/suggest_images.py

# Calculate rider stats
processing/.venv/bin/python processing/rider_stats.py

# Fetch weather (requires API key)
OPENWEATHERMAP_API_KEY=xxx processing/.venv/bin/python processing/weather.py --entry current
```

### Rider data

```bash
# Add daily rider distances (interactive)
./scripts/add-rider-data.sh

# Add for a specific date
./scripts/add-rider-data.sh 2026-04-05
```

### Publishing

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your DEPLOY_TARGET and OPENWEATHERMAP_API_KEY
```

```bash
# Full publish pipeline (stats + weather + build + deploy)
./scripts/publish.sh

# Build only, no deploy
./scripts/publish.sh --skip-deploy
```

## Four Riders

Justin, Marian, Nan, and Wally log daily cycling distances from April through July. Each day, up to 2km counts toward the 185km route (unused cap rolls over). Progress is tracked in every entry.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details. Images sourced from Wikimedia Commons retain their original Creative Commons licenses.
