#!/bin/bash
# Add daily rider distances and regenerate stats
#
# Usage: ./scripts/add-rider-data.sh [YYYY-MM-DD]
# If no date is given, defaults to the day after the last logged entry.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DAILY_LOG="$PROJECT_DIR/data/riders/daily-log.json"
VENV_PYTHON="$PROJECT_DIR/processing/.venv/bin/python"
STATS_SCRIPT="$PROJECT_DIR/processing/rider_stats.py"

# Help
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: ./scripts/add-rider-data.sh [OPTIONS] [YYYY-MM-DD]"
    echo ""
    echo "Add daily rider distances and regenerate stats."
    echo ""
    echo "Arguments:"
    echo "  YYYY-MM-DD    Date for the entry (default: day after last logged entry)"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "The script will prompt for each rider's distance in km."
    echo "If an entry already exists for the given date, it will be updated."
    echo "Stats are automatically regenerated after each entry."
    exit 0
fi

# Validate date format if provided
if [ -n "$1" ]; then
    if ! echo "$1" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
        echo "Error: Invalid date format '$1'. Use YYYY-MM-DD (e.g., 2026-04-03)"
        exit 1
    fi
    # Verify it's a real date
    if ! date -d "$1" >/dev/null 2>&1; then
        echo "Error: '$1' is not a valid date."
        exit 1
    fi
fi

# Check dependencies
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python venv not found. Run: python3 -m venv processing/.venv && processing/.venv/bin/pip install -r processing/requirements.txt"
    exit 1
fi

# Date: use argument, or default to day after last logged entry
if [ -n "$1" ]; then
    DATE="$1"
else
    DATE=$("$VENV_PYTHON" -c "
import json
from datetime import datetime, timedelta
with open('$DAILY_LOG', 'r') as f:
    data = json.load(f)
if data['entries']:
    last = max(e['date'] for e in data['entries'])
    next_day = datetime.strptime(last, '%Y-%m-%d') + timedelta(days=1)
    print(next_day.strftime('%Y-%m-%d'))
else:
    print(datetime.now().strftime('%Y-%m-%d'))
")
fi

echo "Adding rider data for $DATE"
echo "---"

# Read distances
read -p "Justin's distance (km): " JUSTIN
read -p "Marian's distance (km): " MARIAN
read -p "Nan's distance (km): " NAN
read -p "Wally's distance (km): " WALLY

# Default to 0 if empty
JUSTIN=${JUSTIN:-0}
MARIAN=${MARIAN:-0}
NAN=${NAN:-0}
WALLY=${WALLY:-0}

echo ""
echo "Adding: Justin=$JUSTIN, Marian=$MARIAN, Nan=$NAN, Wally=$WALLY"

# Append to daily-log.json using Python (safe JSON manipulation)
"$VENV_PYTHON" -c "
import json, sys

log_path = '$DAILY_LOG'
with open(log_path, 'r') as f:
    data = json.load(f)

new_entry = {
    'date': '$DATE',
    'distances': {
        'justin': float($JUSTIN),
        'marian': float($MARIAN),
        'nan': float($NAN),
        'wally': float($WALLY)
    }
}

# Check for duplicate date
existing_dates = [e['date'] for e in data['entries']]
if '$DATE' in existing_dates:
    print(f'Warning: Entry for $DATE already exists. Updating it.')
    data['entries'] = [e for e in data['entries'] if e['date'] != '$DATE']

data['entries'].append(new_entry)
data['entries'].sort(key=lambda e: e['date'])

with open(log_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f'Updated {log_path}')
"

# Regenerate stats
echo ""
"$VENV_PYTHON" "$STATS_SCRIPT" \
    --daily-log "$DAILY_LOG" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --output "$PROJECT_DIR/data/riders/stats.json"
