#!/bin/bash
# Publish-day script: update stats, fetch weather, build site, deploy
#
# Usage: ./scripts/publish.sh [--dry-run] [--skip-deploy]
#
# Environment variables:
#   OPENWEATHERMAP_API_KEY  - API key for weather data (optional)
#   DEPLOY_TARGET           - rsync target (e.g., user@vps:/var/www/correze-travelogue/)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_DIR/processing/.venv/bin/python"

DRY_RUN=false
SKIP_DEPLOY=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        -h|--help)
            echo "Usage: ./scripts/publish.sh [OPTIONS]"
            echo ""
            echo "Publish-day script: update stats, fetch weather, build site, deploy."
            echo ""
            echo "Options:"
            echo "  --dry-run       Run everything except deploy"
            echo "  --skip-deploy   Skip the rsync deployment step"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  OPENWEATHERMAP_API_KEY  API key for weather data (optional)"
            echo "  DEPLOY_TARGET           rsync target (e.g., user@vps:/var/www/site/)"
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            SKIP_DEPLOY=true
            ;;
        --skip-deploy)
            SKIP_DEPLOY=true
            ;;
    esac
done

echo "=== Correze Travelogue - Publish ==="
echo "Date: $(date +%Y-%m-%d)"
echo ""

# Check dependencies
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python venv not found."
    echo "Run: python3 -m venv processing/.venv && processing/.venv/bin/pip install -r processing/requirements.txt"
    exit 1
fi

# Step 1: Update rider stats
echo "--- Step 1: Updating rider stats ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/rider_stats.py" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --output "$PROJECT_DIR/data/riders/stats.json"
echo ""

# Step 2: Fetch weather for current entry
echo "--- Step 2: Fetching weather ---"
if [ -n "$OPENWEATHERMAP_API_KEY" ]; then
    "$VENV_PYTHON" "$PROJECT_DIR/processing/weather.py" \
        --entry current \
        --api-key "$OPENWEATHERMAP_API_KEY" \
        --segments-json "$PROJECT_DIR/data/segments.json" \
        --entries-dir "$PROJECT_DIR/content/entries"
else
    echo "No OPENWEATHERMAP_API_KEY set, skipping weather."
fi
echo ""

# Step 3: Generate static site
echo "--- Step 3: Building static site ---"
cd "$PROJECT_DIR"

# Source nvm if available
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

npx nuxt generate
echo ""

# Step 4: Deploy
if [ "$SKIP_DEPLOY" = true ]; then
    echo "--- Step 4: Deploy skipped ---"
elif [ -n "$DEPLOY_TARGET" ]; then
    echo "--- Step 4: Deploying to $DEPLOY_TARGET ---"
    if [ "$DRY_RUN" = true ]; then
        echo "(dry run - not deploying)"
    else
        rsync -avz --delete .output/public/ "$DEPLOY_TARGET"
    fi
else
    echo "--- Step 4: No DEPLOY_TARGET set, skipping deploy ---"
    echo "Set DEPLOY_TARGET to deploy (e.g., user@vps:/var/www/correze-travelogue/)"
fi

echo ""
echo "=== Done ==="
