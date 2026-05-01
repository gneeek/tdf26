#!/bin/bash
# Tag HEAD and create a GitHub Release for it.
#
# Usage:
#   ./scripts/create-release.sh <tag> [--title <title>]
#
# Example:
#   ./scripts/create-release.sh v1.4.14
#   ./scripts/create-release.sh v1.4.14 --title "v1.4.14 - Segment 9 publication"
#
# The release body is auto-generated from the git log between the previous tag
# and HEAD, plus a retro-link placeholder. The publisher can edit the body and
# title on GitHub afterwards (the tag and release exist after this script runs;
# their content is editable).
#
# Refuses to act if the tag already exists locally or as a GitHub Release.

set -e

TAG=""
TITLE=""

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        --title)
            TITLE="$2"
            shift 2
            ;;
        -*)
            echo "ERROR: unknown flag: $1" >&2
            exit 1
            ;;
        *)
            if [ -z "$TAG" ]; then
                TAG="$1"
            else
                echo "ERROR: unexpected positional arg: $1" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$TAG" ]; then
    echo "Usage: $0 <tag> [--title <title>]" >&2
    exit 1
fi

if ! [[ "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "ERROR: tag must match v<major>.<minor>.<patch> (got: $TAG)" >&2
    exit 1
fi

if [ -z "$TITLE" ]; then
    TITLE="$TAG"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if git -C "$PROJECT_DIR" rev-parse "$TAG" >/dev/null 2>&1; then
    echo "ERROR: tag $TAG already exists locally." >&2
    exit 1
fi

if gh release view "$TAG" >/dev/null 2>&1; then
    echo "ERROR: GitHub Release $TAG already exists." >&2
    exit 1
fi

PREVIOUS_TAG=$(git -C "$PROJECT_DIR" describe --tags --abbrev=0 2>/dev/null || true)
HEAD_SHA=$(git -C "$PROJECT_DIR" rev-parse --short HEAD)

NOTES_FILE=$(mktemp)
trap 'rm -f "$NOTES_FILE"' EXIT

{
    echo "## What shipped"
    echo ""
    if [ -n "$PREVIOUS_TAG" ]; then
        echo "Commits since [$PREVIOUS_TAG](https://github.com/gneeek/tdf26/releases/tag/$PREVIOUS_TAG):"
        echo ""
        git -C "$PROJECT_DIR" log --pretty=format:'- %s' "$PREVIOUS_TAG..HEAD"
        echo ""
    else
        echo "Recent commits (no previous tag found):"
        echo ""
        git -C "$PROJECT_DIR" log --pretty=format:'- %s' -20
        echo ""
    fi
    echo ""
    echo "## Retro"
    echo ""
    echo "Retro link will be added when the retro is filed: https://github.com/gneeek/tdf26/wiki/Retrospectives"
} > "$NOTES_FILE"

echo "Tagging $HEAD_SHA as $TAG..."
git -C "$PROJECT_DIR" tag -a "$TAG" -m "Release $TAG"
git -C "$PROJECT_DIR" push origin "$TAG"

echo "Creating GitHub Release $TAG..."
gh release create "$TAG" --title "$TITLE" --notes-file "$NOTES_FILE"

echo ""
echo "Release created: https://github.com/gneeek/tdf26/releases/tag/$TAG"
echo "Edit the release on GitHub to expand the framing and add the retro link as needed."
