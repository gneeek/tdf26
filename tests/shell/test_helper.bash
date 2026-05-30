# Shared helpers for the publish-pipeline shell tests (issue #508).
#
# These tests give the three already-merged publish.sh gate fixes
# (#617 draft pre-flight, #618 idempotent merge, #619 weather --entry
# isolation) regression coverage. Each test has a matching red-green demo:
# see tests/shell/README-redgreen.md-equivalent notes in scripts/README.md.

# Absolute path to the repo root, regardless of where bats is invoked from.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PUBLISH_SH="$REPO_ROOT/scripts/publish.sh"
WEATHER_PY="$REPO_ROOT/processing/weather.py"

# A python interpreter that exists in this environment. weather.py and the
# draft-check snippet use only the standard library, so the system python3 is
# sufficient; fall back to the project venv if it is the only one present.
pick_python() {
    local p
    p="$(command -v python3 || true)"
    if [ -n "$p" ]; then
        echo "$p"
    elif [ -x "$REPO_ROOT/processing/.venv/bin/python" ]; then
        echo "$REPO_ROOT/processing/.venv/bin/python"
    else
        command -v python || true
    fi
}

# Create a minimal entry markdown file with the given draft value.
# Usage: make_entry <path> <draft-value>
make_entry() {
    local path="$1" draft="$2"
    cat > "$path" <<EOF
---
segment: 9
title: "Test entry"
publishDate: 2026-05-29
weather: null
draft: $draft
---

# Test entry

Body text.
EOF
}
