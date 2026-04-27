#!/bin/bash
# Publish-day script: update stats, calculate points, snapshot, fetch weather,
# build site, deploy, and commit the frontmatter changes this script produced
# so main is reconciled with the deployed artifact before the script exits.
#
# Usage: ./scripts/publish.sh [--segment N] [--skip-deploy] [--skip-weather] [--skip-commit]
#
# Environment variables (loaded from .env if present):
#   OPENWEATHERMAP_API_KEY  - API key for weather data (optional)
#   DEPLOY_TARGET           - SSH target (e.g., correze:/var/www/correze-travelogue/)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_DIR/processing/.venv/bin/python"

# Load .env if it exists
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

SKIP_DEPLOY=false
SKIP_WEATHER=false
SKIP_COMMIT=false
SEGMENT=""

# Parse arguments
for arg in "$@"; do
    case $arg in
        -h|--help)
            echo "Usage: ./scripts/publish.sh [OPTIONS]"
            echo ""
            echo "Publish-day script: update stats, calculate points, snapshot, fetch weather,"
            echo "build, deploy, and commit frontmatter changes to main."
            echo ""
            echo "Options:"
            echo "  --segment N     Segment number to publish (auto-detects if omitted)"
            echo "  --skip-deploy   Skip the deployment step (also skips the commit step)"
            echo "  --skip-weather  Skip weather fetch"
            echo "  --skip-commit   Deploy but do not commit frontmatter to main"
            echo "                  (advanced: for deploys run from a branch or in a"
            echo "                  workflow where the commit is handled separately)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  OPENWEATHERMAP_API_KEY  API key for weather data (optional)"
            echo "  DEPLOY_TARGET           SSH target (e.g., correze:/var/www/site/)"
            exit 0
            ;;
        --skip-deploy)
            SKIP_DEPLOY=true
            ;;
        --skip-weather)
            SKIP_WEATHER=true
            ;;
        --skip-commit)
            SKIP_COMMIT=true
            ;;
        --segment)
            shift_next=true
            ;;
        *)
            if [ "$shift_next" = true ]; then
                SEGMENT="$arg"
                shift_next=false
            fi
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

# Source nvm if available
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Auto-detect current segment if not specified
if [ -z "$SEGMENT" ]; then
    SEGMENT=$("$VENV_PYTHON" -c "
import json, os, re
from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')
entries_dir = '$PROJECT_DIR/content/entries'
best = None
for f in sorted(os.listdir(entries_dir)):
    if not f.endswith('.md'): continue
    content = open(os.path.join(entries_dir, f)).read()
    seg = re.search(r'^segment:\s*(\d+)', content, re.M)
    date = re.search(r'^publishDate:\s*(\S+)', content, re.M)
    draft = re.search(r'^draft:\s*(\S+)', content, re.M)
    if seg and date and draft:
        if draft.group(1) == 'false' and date.group(1) <= today:
            s = int(seg.group(1))
            if best is None or s > best:
                best = s
print(best if best is not None else 0)
")
    echo "Auto-detected current segment: $SEGMENT"
fi
echo ""

# Step 1: Update rider stats
echo "--- Step 1: Updating rider stats ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/rider_stats.py" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --output "$PROJECT_DIR/data/riders/stats.json"
echo ""

# Step 2: Calculate points
echo "--- Step 2: Calculating points ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/calculate_points.py" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --points-config "$PROJECT_DIR/data/competition/points-config.json" \
    --output "$PROJECT_DIR/data/riders/points.json"
echo ""

# Step 3: Snapshot stats for current segment
echo "--- Step 3: Creating stats snapshot for segment $SEGMENT ---"
ENTRY_FILE=$("$VENV_PYTHON" -c "
import os, re
entries_dir = '$PROJECT_DIR/content/entries'
for f in sorted(os.listdir(entries_dir)):
    if not f.endswith('.md'): continue
    content = open(os.path.join(entries_dir, f)).read()
    seg = re.search(r'^segment:\s*(\d+)', content, re.M)
    if seg and int(seg.group(1)) == $SEGMENT:
        print(os.path.join(entries_dir, f))
        break
")
DATA_CUTOFF=$("$VENV_PYTHON" -c "
import re
content = open('$ENTRY_FILE').read()
m = re.search(r'^dataCutoff:\s*(\S+)', content, re.M)
print(m.group(1) if m else '')
")
if [ -z "$DATA_CUTOFF" ]; then
    echo "No dataCutoff set for segment $SEGMENT."
    read -rp "Enter data cutoff date (YYYY-MM-DD), or press Enter for today: " DATA_CUTOFF
    if [ -z "$DATA_CUTOFF" ]; then
        DATA_CUTOFF=$(date +%Y-%m-%d)
    fi
    # Write dataCutoff to frontmatter
    "$VENV_PYTHON" -c "
path = '$ENTRY_FILE'
content = open(path).read()
# Insert dataCutoff before the closing --- of frontmatter
parts = content.split('---', 2)
if len(parts) >= 3:
    parts[1] = parts[1].rstrip() + '\ndataCutoff: $DATA_CUTOFF\n'
    content = '---'.join(parts)
    open(path, 'w').write(content)
    print('Set dataCutoff: $DATA_CUTOFF in ' + path)
else:
    print('ERROR: Could not find frontmatter delimiters in ' + path)
"
fi
echo "Data cutoff for segment $SEGMENT: $DATA_CUTOFF"
"$VENV_PYTHON" "$PROJECT_DIR/processing/snapshot_stats.py" \
    --stats "$PROJECT_DIR/data/riders/stats.json" \
    --points "$PROJECT_DIR/data/riders/points.json" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --segment "$SEGMENT" \
    --output-dir "$PROJECT_DIR/data/riders/snapshots" \
    --data-cutoff "$DATA_CUTOFF"
echo ""

# Step 4: Fetch weather for current entry
echo "--- Step 4: Fetching weather ---"
if [ "$SKIP_WEATHER" = true ]; then
    echo "Skipped."
elif [ -n "$OPENWEATHERMAP_API_KEY" ]; then
    "$VENV_PYTHON" "$PROJECT_DIR/processing/weather.py" \
        --entry current \
        --api-key "$OPENWEATHERMAP_API_KEY" \
        --segments-json "$PROJECT_DIR/data/segments.json" \
        --entries-dir "$PROJECT_DIR/content/entries"
else
    echo "No OPENWEATHERMAP_API_KEY set, skipping weather."
fi
echo ""

# Step 5: Generate race narrative
echo "--- Step 5: Generating race narrative for segment $SEGMENT ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/generate_narrative.py" \
    --points "$PROJECT_DIR/data/riders/points.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --segment "$SEGMENT"
echo ""

# Step 6: Validate entry images
echo "--- Step 6: Validating entry images ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/validate_entries.py" \
    --entries-dir "$PROJECT_DIR/content/entries"
echo ""

# Step 7: Generate static site
echo "--- Step 7: Building static site ---"
cd "$PROJECT_DIR"
npx nuxt generate
echo ""

# Step 8: Deploy
if [ "$SKIP_DEPLOY" = true ]; then
    echo "--- Step 8: Deploy skipped ---"
elif [ -n "$DEPLOY_TARGET" ]; then
    echo "--- Step 8: Deploying to $DEPLOY_TARGET ---"
    echo "Uploading to $DEPLOY_TARGET..."
    # Run under `if !` so set -e cannot bail before we print a step-named
    # failure; subshell-local `set -o pipefail` so a left-side tar failure
    # is not masked by a trailing ssh exit of 0.
    if ! ( set -o pipefail; tar -czf - -C .output/public . | ssh "${DEPLOY_TARGET%%:*}" "mkdir -p ${DEPLOY_TARGET#*:} && tar -xzf - -C ${DEPLOY_TARGET#*:}" ); then
        echo "ERROR: Step 8 deploy failed. Site was NOT uploaded to $DEPLOY_TARGET."
        exit 1
    fi
    echo "Deploy complete."
else
    echo "--- Step 8: No DEPLOY_TARGET set, skipping deploy ---"
    echo "Set DEPLOY_TARGET in .env (e.g., correze:/var/www/correze-travelogue/)"
fi
echo ""

# Step 9: Commit frontmatter changes to main
# Closes the reconciliation gap between the deployed artifact and main. The
# publish script mutates the entry frontmatter in place (dataCutoff, weather,
# sometimes images) and those mutations need to land on main before the script
# exits, or the next fresh clone builds the stub instead of the published entry.
# See issue #383 and the v1.4.5 retrospective.
if [ "$SKIP_DEPLOY" = true ]; then
    echo "--- Step 9: Commit skipped (deploy was skipped) ---"
elif [ "$SKIP_COMMIT" = true ]; then
    echo "--- Step 9: Commit skipped (--skip-commit flag) ---"
elif [ -z "$DEPLOY_TARGET" ]; then
    echo "--- Step 9: Commit skipped (no DEPLOY_TARGET, no deploy happened) ---"
else
    echo "--- Step 9: Committing frontmatter changes to main ---"
    CURRENT_BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD)
    if [ "$CURRENT_BRANCH" != "main" ]; then
        echo "ERROR: publish.sh is not running on main (currently on $CURRENT_BRANCH)."
        echo "Refusing to commit frontmatter changes from a non-main branch."
        echo "The deploy happened but main is not reconciled. Resolve manually:"
        echo "  git checkout main && git add $ENTRY_FILE && git commit && git push"
        exit 1
    fi
    if [ -z "$ENTRY_FILE" ] || [ ! -f "$ENTRY_FILE" ]; then
        echo "ERROR: ENTRY_FILE not set or not found; cannot commit."
        echo "The deploy happened but main is not reconciled. Resolve manually."
        exit 1
    fi
    if git -C "$PROJECT_DIR" diff --quiet -- "$ENTRY_FILE" \
        && git -C "$PROJECT_DIR" diff --staged --quiet -- "$ENTRY_FILE"; then
        echo "No frontmatter changes to commit on $ENTRY_FILE."
    else
        git -C "$PROJECT_DIR" add "$ENTRY_FILE" \
            || { echo "ERROR: git add failed."; exit 1; }
        git -C "$PROJECT_DIR" commit -m "Segment $SEGMENT publish: record frontmatter from publish.sh" \
            || { echo "ERROR: git commit failed. Resolve manually; the deploy already happened."; exit 1; }
        git -C "$PROJECT_DIR" push origin main \
            || { echo "ERROR: git push failed. The deploy happened but main is not reconciled. Resolve manually."; exit 1; }
        echo "Committed and pushed frontmatter changes for segment $SEGMENT."
    fi
fi

echo ""
echo "=== Done ==="
