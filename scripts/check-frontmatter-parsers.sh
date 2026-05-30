#!/usr/bin/env bash
#
# Anti-regression guard for issue #326.
#
# Every consumer must read and write entry frontmatter through the two
# canonical parsers -- processing/frontmatter.py and
# server/utils/frontmatter.ts -- never a new hand-rolled regex. Before #326 the
# same parser was reimplemented in ~10 places, each drifting independently (the
# class of bug behind the seg-9 publish crash and the v1.3.4 date corruption).
#
# This guard fails CI when production code outside the two canonical modules
# contains a frontmatter fence regex (`^---\n`) or a per-field frontmatter-key
# regex (`^segment:`, `^weather:`, ...). Test files are exempt: the byte-
# identical parity proofs intentionally embed the old patterns.
#
# Red-green: add e.g. `re.search(r'^weather:', s)` to any processing/*.py and
# this guard fails; remove it and it passes.
set -euo pipefail

KEYS='segment|title|subtitle|publishDate|kmStart|kmEnd|gpxFile|elevationData|images|weather|draft|dataCutoff|imagesOptional'

# A regex/string literal opening with the fence (^---\n) or a field line
# (^<key>:). The trailing \n on the fence avoids matching markdown rules
# (-----) and PEM headers in vendored code.
PATTERN="[\"'/]\\^(---\\\\n|(${KEYS}):)"

# The canonical parsers legitimately contain the fence regex; this guard
# documents the forbidden patterns in its own comments.
ALLOW='processing/frontmatter\.py|server/utils/frontmatter\.ts|scripts/check-frontmatter-parsers\.sh'

hits="$(
  grep -rnE "$PATTERN" processing scripts server \
    --include='*.py' --include='*.sh' --include='*.ts' --include='*.mjs' 2>/dev/null \
    | grep -vE '\.venv/|node_modules/|/tests/|\.test\.(ts|js)' \
    | grep -vE "$ALLOW" \
    || true
)"

if [ -n "$hits" ]; then
  echo "ERROR: hand-rolled frontmatter parsing found outside the canonical parsers (issue #326)." >&2
  echo "Use processing/frontmatter.py or server/utils/frontmatter.ts instead:" >&2
  echo "$hits" >&2
  exit 1
fi

echo "OK: no hand-rolled frontmatter parsing outside the canonical parsers."
