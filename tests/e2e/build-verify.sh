#!/usr/bin/env bash
# End-to-end build verification test
# Verifies that `nuxt generate` produces a working static site
# with expected files and content.
#
# Usage: ./tests/e2e/build-verify.sh [output-dir]
# Default output-dir: .output/public

set -euo pipefail

OUTPUT_DIR="${1:-.output/public}"
PASS=0
FAIL=0

pass() {
  echo "  ✓ $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "  ✗ $1"
  FAIL=$((FAIL + 1))
}

check_file() {
  if [ -f "$OUTPUT_DIR/$1" ]; then
    pass "exists: $1"
  else
    fail "missing: $1"
  fi
}

check_dir() {
  if [ -d "$OUTPUT_DIR/$1" ]; then
    pass "exists: $1/"
  else
    fail "missing: $1/"
  fi
}

check_contains() {
  local file="$OUTPUT_DIR/$1"
  local pattern="$2"
  local label="${3:-$2}"
  if [ -f "$file" ] && grep -q "$pattern" "$file"; then
    pass "$1 contains: $label"
  else
    fail "$1 missing: $label"
  fi
}

check_not_contains() {
  local file="$OUTPUT_DIR/$1"
  local pattern="$2"
  local label="${3:-$2}"
  if [ -f "$file" ] && grep -q "$pattern" "$file"; then
    fail "$1 should not contain: $label"
  else
    pass "$1 does not contain: $label"
  fi
}

echo ""
echo "Build verification: $OUTPUT_DIR"
echo "================================"

# --- Core structure ---
echo ""
echo "Core structure:"
check_file "index.html"
check_file "200.html"
check_file "404.html"
check_dir "_nuxt"
check_file "_payload.json"

# --- Static assets ---
echo ""
echo "Static assets:"
JS_COUNT=$(find "$OUTPUT_DIR/_nuxt" -name "*.js" 2>/dev/null | wc -l)
CSS_COUNT=$(find "$OUTPUT_DIR/_nuxt" -name "*.css" 2>/dev/null | wc -l)
if [ "$JS_COUNT" -gt 0 ]; then
  pass "JS bundles generated ($JS_COUNT files)"
else
  fail "no JS bundles found"
fi
if [ "$CSS_COUNT" -gt 0 ]; then
  pass "CSS bundles generated ($CSS_COUNT files)"
else
  fail "no CSS bundles found"
fi

# --- Homepage ---
echo ""
echo "Homepage:"
check_contains "index.html" "Corrèze" "site title"
check_contains "index.html" "Malemort" "route start town"
check_contains "index.html" "Ussel" "route end town"

# --- Published entries ---
echo ""
echo "Published entries:"
check_dir "entries/00-preview"
check_file "entries/00-preview/index.html"
check_dir "entries/01-malemort-departure"
check_file "entries/01-malemort-departure/index.html"
check_file "entries/01-malemort-departure/_payload.json"

# Verify entry page contains expected content
check_contains "entries/01-malemort-departure/index.html" "Malemort" "entry title"
check_contains "entries/01-malemort-departure/index.html" "Elevation" "elevation section"

# --- Draft entries should NOT be pre-rendered ---
echo ""
echo "Draft filtering:"
# Entries 02-26 are drafts — their directories should not exist
# (or if they do, they should be 404 pages)
DRAFT_RENDERED=0
for i in $(seq 2 26); do
  NUM=$(printf "%02d" "$i")
  DRAFT_DIR=$(find "$OUTPUT_DIR/entries" -maxdepth 1 -type d -name "${NUM}-*" 2>/dev/null | head -1)
  if [ -n "$DRAFT_DIR" ] && [ -f "$DRAFT_DIR/index.html" ]; then
    # Check if it's a real page or a 404
    if grep -q "Page not found" "$DRAFT_DIR/index.html" 2>/dev/null; then
      continue  # 404 page, not actually rendered
    fi
    DRAFT_RENDERED=$((DRAFT_RENDERED + 1))
  fi
done
if [ "$DRAFT_RENDERED" -eq 0 ]; then
  pass "draft entries not pre-rendered as full pages"
else
  fail "$DRAFT_RENDERED draft entries were rendered as full pages"
fi

# --- Admin pages ---
echo ""
echo "Admin pages:"
check_dir "admin"
check_file "admin/index.html"

# --- Content data ---
echo ""
echo "Content data:"
check_dir "__nuxt_content"

# --- Summary ---
echo ""
echo "================================"
TOTAL=$((PASS + FAIL))
echo "Results: $PASS passed, $FAIL failed (of $TOTAL checks)"
echo ""

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
