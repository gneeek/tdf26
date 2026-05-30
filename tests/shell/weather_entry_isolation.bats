#!/usr/bin/env bats
#
# #619 weather --entry isolation (processing/weather.py).
#
# Regression intent: `weather.py --entry N` must inject weather into ONLY the
# entry whose frontmatter segment: equals N, leaving every other entry file
# byte-identical. The pre-#619 pipeline passed `--entry current`, which during
# a publish run resolved to segment N-1 and rewrote the wrong (already
# published) entry; targeting --entry N fixes that.
#
# Red-green: patch weather.py's re.sub so it writes ALL entries (drop count=1
# / loop every file) -> entries 1 and 3 change and this test goes red; git
# checkout -- restores green.
#
# DEVIATIONS from the #508 brief (real flags/behaviour on main, b857802):
#   * the flag is --segments-json, not --segments.
#   * with no --api-key weather.py prints a warning and writes NOTHING (no
#     stub forecast). So to exercise the actual injection path we run weather.py
#     with a stubbed urllib so the OpenWeatherMap call returns canned data
#     without network access, and pass a dummy --api-key.

load test_helper

setup() {
    TMPDIR_TEST="$(mktemp -d)"
    ENTRIES_DIR="$TMPDIR_TEST/entries"
    mkdir -p "$ENTRIES_DIR"
    PY="$(pick_python)"

    # Three entries, segments 1/2/3, each weather: null.
    for n in 1 2 3; do
        nn=$(printf '%02d' "$n")
        cat > "$ENTRIES_DIR/$nn-seg.md" <<EOF
---
segment: $n
title: "Segment $n"
publishDate: 2026-05-29
weather: null
draft: false
---

# Segment $n
EOF
    done

    # segments.json with coords for segments 1-3.
    cat > "$TMPDIR_TEST/segments.json" <<'EOF'
[
  {"segment": 1, "start_lat": 45.10, "start_lng": 1.50, "end_lat": 45.11, "end_lng": 1.51},
  {"segment": 2, "start_lat": 45.20, "start_lng": 1.60, "end_lat": 45.21, "end_lng": 1.61},
  {"segment": 3, "start_lat": 45.30, "start_lng": 1.70, "end_lat": 45.31, "end_lng": 1.71}
]
EOF

    # Runner that stubs urllib so get_weather() returns canned JSON offline,
    # then invokes weather.py's main() with the requested args.
    cat > "$TMPDIR_TEST/run_weather.py" <<EOF
import json, sys, io, urllib.request, runpy

class _Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False

def _fake_urlopen(req, timeout=10):
    payload = {
        "main": {"temp": 17.4},
        "weather": [{"description": "partly cloudy"}],
        "wind": {"speed": 3.0, "deg": 200},
    }
    return _Resp(json.dumps(payload).encode())

urllib.request.urlopen = _fake_urlopen

sys.argv = [
    "weather.py",
    "--entry", "${ENTRY_ARG:-2}",
    "--segments-json", "$TMPDIR_TEST/segments.json",
    "--entries-dir", "$ENTRIES_DIR",
    "--api-key", "dummy",
]
runpy.run_path("$WEATHER_PY", run_name="__main__")
EOF
}

teardown() {
    rm -rf "$TMPDIR_TEST"
}

@test "weather --entry 2 changes only segment 2, leaves 1 and 3 byte-identical" {
    md5_before_1="$(md5sum "$ENTRIES_DIR/01-seg.md" | cut -d' ' -f1)"
    md5_before_3="$(md5sum "$ENTRIES_DIR/03-seg.md" | cut -d' ' -f1)"

    ENTRY_ARG=2 run "$PY" "$TMPDIR_TEST/run_weather.py"
    [ "$status" -eq 0 ]

    # Segment 2 got a real weather value (no longer null).
    grep -q '^weather: null' "$ENTRIES_DIR/02-seg.md" && false
    grep -q '"temp": 17' "$ENTRIES_DIR/02-seg.md"

    # Segments 1 and 3 are byte-for-byte unchanged.
    md5_after_1="$(md5sum "$ENTRIES_DIR/01-seg.md" | cut -d' ' -f1)"
    md5_after_3="$(md5sum "$ENTRIES_DIR/03-seg.md" | cut -d' ' -f1)"
    [ "$md5_before_1" = "$md5_after_1" ]
    [ "$md5_before_3" = "$md5_after_3" ]
}
