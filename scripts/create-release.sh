#!/bin/bash
# Tag HEAD and create a GitHub Release for it.
#
# Usage:
#   ./scripts/create-release.sh <tag> [--title <title>] [--update-roadmap]
#                               [--milestone <n>] [--dry-run] [--wiki-url <url>]
#
# Tag format is date-based, year-implicit (this is tdf26):
#   Publication deploys:     W<NN>-seg<N>   (e.g. W19-seg11)
#   Non-publication deploys: W<NN>.<N>      (e.g. W19.1)
#
# Flags:
#   --title <title>     Release title (defaults to the tag).
#   --update-roadmap    After the release is created, move it to the wiki
#                       Roadmap's '## Completed' section (clone wiki over HTTPS,
#                       append a Completed bullet, commit, push). Idempotent: a
#                       Completed row already mentioning the tag is left as-is.
#                       Does NOT rewrite the '## Now' prose block; it only warns
#                       that the block needs a manual trim.
#   --milestone <n>     Milestone number, linked by number in the Completed
#                       bullet (per feedback_milestone_urls). Optional.
#   --dry-run           Print the tag/release commands and the Roadmap diff
#                       without tagging, releasing, or pushing anything.
#   --wiki-url <url>    Wiki clone URL (default the gneeek/tdf26 wiki over HTTPS).
#                       Point at a scratch clone/branch for testing.
#
# Example:
#   ./scripts/create-release.sh W19-seg11
#   ./scripts/create-release.sh W19-seg11 --title "W19-seg11 - Segment 11 publication"
#   ./scripts/create-release.sh W19.1 --update-roadmap --milestone 53
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
UPDATE_ROADMAP=false
MILESTONE=""
DRY_RUN=false
WIKI_URL="https://github.com/gneeek/tdf26.wiki.git"
REPO_URL="https://github.com/gneeek/tdf26"

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
        --update-roadmap)
            UPDATE_ROADMAP=true
            shift
            ;;
        --milestone)
            MILESTONE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --wiki-url)
            WIKI_URL="$2"
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

if ! [[ "$TAG" =~ ^W[0-9]{2}(-seg[0-9]+|\.[0-9]+)$ ]]; then
    echo "ERROR: tag must match W<NN>-seg<N> (publication) or W<NN>.<N> (non-publication) (got: $TAG)" >&2
    exit 1
fi

if [ -z "$TITLE" ]; then
    TITLE="$TAG"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Move the just-shipped release into the wiki Roadmap's '## Completed' section.
# Clones the wiki over HTTPS, inserts a Completed bullet as the newest entry,
# commits and pushes. Idempotent (a row already mentioning the tag is left
# untouched). Deliberately does NOT touch the '## Now' prose block — it only
# warns that the block needs a manual trim, preserving the goals-and-outcomes
# Roadmap voice (feedback_roadmap_style.md).
update_roadmap() {
    local tag="$1" title="$2" milestone="$3" dry_run="$4" wiki_url="$5"
    local release_url="$REPO_URL/releases/tag/$tag"
    local milestone_link=""
    if [ -n "$milestone" ]; then
        milestone_link=" | [milestone]($REPO_URL/milestone/$milestone)"
    fi

    # Factual, link-bearing bullet. Prose enrichment is left to the publisher;
    # the automation does not invent the goals-and-outcomes summary.
    local bullet
    bullet="- **$title** — released as \`$tag\` ([release]($release_url) | retro: _pending_$milestone_link). _Roadmap summary pending manual edit._"

    local wiki_dir
    wiki_dir=$(mktemp -d)

    echo "Cloning wiki ($wiki_url) to update the Roadmap..."
    if ! git clone --depth 1 "$wiki_url" "$wiki_dir" >/dev/null 2>&1; then
        echo "ERROR: failed to clone wiki at $wiki_url." >&2
        echo "       Release $tag exists; the Roadmap must be updated manually." >&2
        rm -rf "$wiki_dir"
        return 1
    fi

    local roadmap="$wiki_dir/Roadmap.md"
    if [ ! -f "$roadmap" ]; then
        echo "ERROR: Roadmap.md not found in the wiki clone; update manually." >&2
        rm -rf "$wiki_dir"
        return 1
    fi

    # Idempotency: a Completed row already mentioning this tag → no duplicate.
    if grep -qF "\`$tag\`" "$roadmap"; then
        echo "Roadmap already references \`$tag\` — no duplicate row added (idempotent)."
        rm -rf "$wiki_dir"
        return 0
    fi

    if ! grep -qx "## Completed" "$roadmap"; then
        echo "ERROR: '## Completed' heading not found in Roadmap.md; update manually." >&2
        rm -rf "$wiki_dir"
        return 1
    fi

    # Insert the bullet as the first entry under '## Completed' (newest-first).
    # ENVIRON avoids awk -v escape processing of backticks/em-dashes in the bullet.
    BULLET="$bullet" awk '
        flag && /^- / { print ENVIRON["BULLET"]; flag=0 }
        /^## Completed$/ { flag=1 }
        { print }
        END { if (flag) print ENVIRON["BULLET"] }
    ' "$roadmap" > "$roadmap.new"
    mv "$roadmap.new" "$roadmap"

    if [ "$dry_run" = true ]; then
        echo "--- DRY RUN: Roadmap.md diff (not committed, not pushed) ---"
        git -C "$wiki_dir" --no-pager diff -- Roadmap.md
        echo "--- DRY RUN: would commit and push the above to $wiki_url ---"
        rm -rf "$wiki_dir"
        return 0
    fi

    # A fresh wiki clone carries no committer identity, and this project sets
    # git identity per-repo (local), not globally — so the commit would abort
    # with "Author identity unknown". Carry the main repo's identity onto the
    # wiki commit so it is attributed consistently with the release's commits.
    local git_name git_email
    git_name=$(git -C "$PROJECT_DIR" config user.name 2>/dev/null || true)
    git_email=$(git -C "$PROJECT_DIR" config user.email 2>/dev/null || true)
    if [ -z "$git_name" ] || [ -z "$git_email" ]; then
        echo "ERROR: no git user.name/user.email configured in $PROJECT_DIR;" >&2
        echo "       cannot attribute the wiki Roadmap commit. Set them and rerun." >&2
        rm -rf "$wiki_dir"
        return 1
    fi

    git -C "$wiki_dir" add Roadmap.md
    if ! git -C "$wiki_dir" \
            -c user.name="$git_name" -c user.email="$git_email" \
            commit -m "Roadmap: move $tag to Completed" >/dev/null; then
        echo "ERROR: wiki Roadmap commit failed (see above)." >&2
        rm -rf "$wiki_dir"
        return 1
    fi
    if ! git -C "$wiki_dir" push origin HEAD >/dev/null 2>&1; then
        echo "ERROR: push of the Roadmap commit failed for $wiki_url." >&2
        echo "       The Completed bullet is committed locally at $wiki_dir but NOT pushed." >&2
        echo "       Push it manually, then remove $wiki_dir." >&2
        return 1
    fi
    rm -rf "$wiki_dir"

    echo "Roadmap updated: \`$tag\` added to '## Completed'."
    echo ""
    echo "WARNING: the '## Now' Roadmap block still describes the just-shipped"
    echo "         release. Trim/rewrite it manually to reflect what is now in flight."
}

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

if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: would tag $HEAD_SHA as $TAG and create GitHub Release '$TITLE'."
    echo "  git tag -a $TAG -m \"Release $TAG\" && git push origin $TAG"
    echo "  gh release create $TAG --title \"$TITLE\" --notes-file <generated notes>"
else
    echo "Tagging $HEAD_SHA as $TAG..."
    git -C "$PROJECT_DIR" tag -a "$TAG" -m "Release $TAG"
    git -C "$PROJECT_DIR" push origin "$TAG"

    echo "Creating GitHub Release $TAG..."
    gh release create "$TAG" --title "$TITLE" --notes-file "$NOTES_FILE"

    echo ""
    echo "Release created: $REPO_URL/releases/tag/$TAG"
    echo "Edit the release on GitHub to expand the framing and add the retro link as needed."
fi

if [ "$UPDATE_ROADMAP" = true ]; then
    echo ""
    echo "--- Updating wiki Roadmap ---"
    update_roadmap "$TAG" "$TITLE" "$MILESTONE" "$DRY_RUN" "$WIKI_URL" \
        || { echo "ERROR: Roadmap update failed (see above). The release itself succeeded; reconcile the Roadmap manually."; exit 1; }
fi
