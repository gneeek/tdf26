#!/bin/bash
# List local branches that appear to be squash-merged into main and are safe to delete.
#
# Heuristic: GitHub records each merged PR's head ref. A local branch whose name
# matches a merged PR's head ref is almost certainly the squash-merged branch and
# can be deleted. Branches without a name match fall through and are listed
# separately for manual review (they may be pre-PR hotfixes or orphaned work).
#
# Usage:
#   ./scripts/list-stale-branches.sh              # report only
#   ./scripts/list-stale-branches.sh --delete     # delete the name-matched branches locally
#   ./scripts/list-stale-branches.sh --delete --push-remote  # also push-delete remote branches
#
# Requires: gh CLI authenticated for the current repo.

set -e

DELETE=0
PUSH_REMOTE=0
for arg in "$@"; do
    case "$arg" in
        --delete) DELETE=1 ;;
        --push-remote) PUSH_REMOTE=1 ;;
        -h|--help)
            sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "Unknown option: $arg" >&2
            exit 2
            ;;
    esac
done

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

git fetch --prune origin >/dev/null 2>&1

gh pr list --state merged --limit 500 --json headRefName --jq '.[].headRefName' \
    | sort -u > "$tmpdir/merged.txt"

git branch --format '%(refname:short)' | grep -v '^main$' | sort -u > "$tmpdir/local.txt"

comm -12 "$tmpdir/local.txt" "$tmpdir/merged.txt" > "$tmpdir/safe.txt"
comm -23 "$tmpdir/local.txt" "$tmpdir/merged.txt" > "$tmpdir/ambiguous.txt"

echo "=== Safe to delete (name matches merged PR): $(wc -l < "$tmpdir/safe.txt") ==="
cat "$tmpdir/safe.txt"
echo ""
echo "=== Ambiguous (no PR name match, review manually): $(wc -l < "$tmpdir/ambiguous.txt") ==="
cat "$tmpdir/ambiguous.txt"

if [ "$DELETE" = "1" ]; then
    echo ""
    echo "=== Deleting local branches ==="
    while read -r b; do [ -n "$b" ] && git branch -D "$b"; done < "$tmpdir/safe.txt"
fi

if [ "$PUSH_REMOTE" = "1" ]; then
    git branch -r --format '%(refname:short)' | sed 's|^origin/||' \
        | grep -v '^HEAD' | grep -v '^main$' | sort -u > "$tmpdir/remote.txt"
    comm -12 "$tmpdir/remote.txt" "$tmpdir/merged.txt" > "$tmpdir/remote_safe.txt"
    if [ -s "$tmpdir/remote_safe.txt" ]; then
        echo ""
        echo "=== Deleting remote branches ==="
        refs=$(sed 's|^|:|' "$tmpdir/remote_safe.txt" | tr '\n' ' ')
        git push origin $refs
    fi
fi
