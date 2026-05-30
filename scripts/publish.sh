#!/bin/bash
# Publish-day script: update stats, calculate points, snapshot, fetch weather,
# build site, deploy, and commit the frontmatter changes this script produced
# so main is reconciled with the deployed artifact before the script exits.
#
# Usage: ./scripts/publish.sh [--segment N] [--release-tag W<NN>-segN | W<NN>.N]
#                             [--skip-deploy] [--skip-weather] [--skip-commit] [--skip-release]
#
# Environment variables (loaded from .env if present):
#   OPENWEATHERMAP_API_KEY  - API key for weather data (optional)
#   DEPLOY_TARGET           - SSH target (e.g., correze:/var/www/correze-travelogue/)
#
# Fail-fast policy
# - First-time failure modes surface and halt the script (set -e by default).
# - Recurrence-class failures become autonomous-recovery: the script handles them
#   without halting because publisher investigation is complete.
# - Specific recurrence-handled cases (per #496):
#   1. PR auto-merged before script's own merge call.
#   2. read -rp with no TTY for dataCutoff.
#   3. SSH agent benign-noise stutter on deploy.
# - When a new failure mode fires for the first time, halt and surface; promote to
#   autonomous-recovery in the next planning if it recurs.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_DIR/processing/.venv/bin/python"

# --- Testable gate functions (#617, #618) -----------------------------------
# These wrap the publish-pipeline gates so they can be unit-tested in isolation
# (see tests/shell/). The logic is identical to what runs inline in the main
# flow below; the functions exist so the bats harness can source this file and
# exercise each gate without driving a full publish. Sourcing the file defines
# the functions and constants but does NOT run the publish flow (guarded at the
# bottom by the BASH_SOURCE/$0 check).

# #617 draft pre-flight: the target entry must be publishable before any work.
# Bails (exit 1) if the segment resolved to no entry file. If the entry is
# marked draft: true, auto-flips it to draft: false in place so the build does
# not silently exclude it (seg 16 shipped draft:true, nuxt generate filtered
# it, and production 404'd until a manual rebuild). The flip mutates the same
# file Step 9 stages, so it reconciles to main alongside dataCutoff/weather.
# Args: $1 = python interpreter, $2 = entry file path, $3 = segment number.
preflight_draft_check() {
    local py="$1" entry_file="$2" segment="$3"
    if [ -z "$entry_file" ] || [ ! -f "$entry_file" ]; then
        echo "ERROR: no entry file found for segment $segment. Cannot publish."
        exit 1
    fi
    local fm_py="$PROJECT_DIR/processing/frontmatter.py"
    local entry_draft
    entry_draft=$("$py" "$fm_py" get "$entry_file" draft)
    if [ "$entry_draft" = "true" ]; then
        echo "Segment $segment entry is draft: true; flipping to draft: false before build."
        "$py" "$fm_py" set "$entry_file" draft false
        echo "Flipped draft: false in $entry_file"
    fi
}

# #618 idempotent merge decision: returns 0 (skip the merge) when the publish
# branch's work is already on main, so a re-run does not attempt a second
# merge. In the live pipeline the equivalent guard is the gh-PR-state re-query
# (Step 9): if the reconciliation PR is already MERGED, the merge is treated as
# done and the run proceeds to tag/release rather than failing under set -e.
# This function models that "already merged -> skip" decision against a local
# branch using merge-base, so the gate is testable without GitHub. It runs no
# git add/commit/push when the branch is already an ancestor of main.
# Args: $1 = entry file path. Uses git in the current repo.
merge_frontmatter_commit() {
    local entry_file="$1"
    local branch="publish/$(basename "$entry_file" .md)"
    if git merge-base --is-ancestor "$branch" main 2>/dev/null; then
        echo "publish branch $branch already merged; skipping commit/merge step."
        return 0
    fi
    git add "$entry_file"
    git commit -m "publish: reconcile $(basename "$entry_file")"
    git checkout main
    git merge --no-ff "$branch"
    git push origin main
    return 0
}

# Load .env if it exists
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

# Source-guard (#508 testability): when this file is sourced (e.g. by the bats
# shell tests) we stop here, having defined the gate functions and constants
# above but WITHOUT running the publish flow. When executed directly the guard
# is false and the main flow below runs unchanged.
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return 0
fi

SKIP_DEPLOY=false
SKIP_WEATHER=false
SKIP_COMMIT=false
SKIP_RELEASE=false
SEGMENT=""
RELEASE_TAG=""

# Parse arguments
for arg in "$@"; do
    case $arg in
        -h|--help)
            echo "Usage: ./scripts/publish.sh [OPTIONS]"
            echo ""
            echo "Publish-day script: update stats, calculate points, snapshot, fetch weather,"
            echo "build, deploy, commit frontmatter changes to main, and create a GitHub Release."
            echo ""
            echo "Options:"
            echo "  --segment N            Segment number to publish (auto-detects if omitted)"
            echo "  --release-tag TAG      Tag and GitHub Release to create after a successful"
            echo "                         deploy. Date-based, year-implicit (this is tdf26):"
            echo "                           Publication deploys: W<NN>-seg<N>   (e.g. W19-seg11)"
            echo "                           Non-publication:     W<NN>.<N>      (e.g. W19.1)"
            echo "                         Tag must not already exist. Required unless --skip-release."
            echo "  --skip-deploy          Skip the deployment step (also skips commit and release)"
            echo "  --skip-weather         Skip weather fetch"
            echo "  --skip-commit          Deploy but do not commit frontmatter to main"
            echo "                         (advanced: for deploys run from a branch or in a"
            echo "                         workflow where the commit is handled separately)"
            echo "  --skip-release         Deploy but do not create a tag or GitHub Release"
            echo "  -h, --help             Show this help message"
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
        --skip-release)
            SKIP_RELEASE=true
            ;;
        --segment)
            arg_consumer="SEGMENT"
            ;;
        --release-tag)
            arg_consumer="RELEASE_TAG"
            ;;
        *)
            if [ -n "$arg_consumer" ]; then
                printf -v "$arg_consumer" "%s" "$arg"
                arg_consumer=""
            fi
            ;;
    esac
done

# Validate release tag up front so we don't deploy then discover a malformed tag.
if [ "$SKIP_RELEASE" = false ] && [ "$SKIP_DEPLOY" = false ]; then
    if [ -z "$RELEASE_TAG" ]; then
        echo "ERROR: --release-tag is required (or pass --skip-release to suppress)." >&2
        exit 1
    fi
    if ! [[ "$RELEASE_TAG" =~ ^W[0-9]{2}(-seg[0-9]+|\.[0-9]+)$ ]]; then
        echo "ERROR: --release-tag must match W<NN>-seg<N> (publication) or W<NN>.<N> (non-publication) (got: $RELEASE_TAG)." >&2
        exit 1
    fi
    if git rev-parse "$RELEASE_TAG" >/dev/null 2>&1; then
        echo "ERROR: tag $RELEASE_TAG already exists locally." >&2
        exit 1
    fi
    if gh release view "$RELEASE_TAG" >/dev/null 2>&1; then
        echo "ERROR: GitHub Release $RELEASE_TAG already exists." >&2
        exit 1
    fi
fi

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
    SEGMENT=$("$VENV_PYTHON" "$PROJECT_DIR/processing/frontmatter.py" \
        current-segment "$PROJECT_DIR/content/entries")
    echo "Auto-detected current segment: $SEGMENT"
fi
echo ""

# Resolve segment's dataCutoff first, then thread it through every stage so
# the stats/points/snapshot outputs are reproducible against the cutoff (per
# issues #541, #328). The order is: find entry file → resolve cutoff → run
# stats with --reference-date → run points with --data-cutoff → snapshot.
ENTRY_FILE=$("$VENV_PYTHON" "$PROJECT_DIR/processing/frontmatter.py" \
    find-entry "$PROJECT_DIR/content/entries" "$SEGMENT")

# Pre-flight (#617): the target must be publishable before any work happens.
# Bails on a missing entry file and auto-flips draft: true -> false. The logic
# lives in preflight_draft_check() (defined near the top) so it is unit-tested.
preflight_draft_check "$VENV_PYTHON" "$ENTRY_FILE" "$SEGMENT"

DATA_CUTOFF=$("$VENV_PYTHON" "$PROJECT_DIR/processing/frontmatter.py" \
    get "$ENTRY_FILE" dataCutoff)
if [ -z "$DATA_CUTOFF" ]; then
    echo "No dataCutoff set for segment $SEGMENT."
    # Only prompt when stdin is a TTY; non-interactive runs (cron, nohup, background
    # invocation) fall through to today's date. Per #496: a no-TTY `read -rp` exits
    # non-zero and `set -e` killed the v1.4.17 publish before this fallback could fire.
    if [ -t 0 ]; then
        read -rp "Enter data cutoff date (YYYY-MM-DD), or press Enter for today: " DATA_CUTOFF
    fi
    if [ -z "$DATA_CUTOFF" ]; then
        DATA_CUTOFF=$(date +%Y-%m-%d)
    fi
    # Write dataCutoff to frontmatter (inserted before the closing --- by the
    # canonical parser's surgical set_field)
    "$VENV_PYTHON" "$PROJECT_DIR/processing/frontmatter.py" \
        set "$ENTRY_FILE" dataCutoff "$DATA_CUTOFF"
    echo "Set dataCutoff: $DATA_CUTOFF in $ENTRY_FILE"
fi
echo "Data cutoff for segment $SEGMENT: $DATA_CUTOFF"
echo ""

# Step 1: Update rider stats (reference-date = data cutoff for reproducibility)
echo "--- Step 1: Updating rider stats ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/rider_stats.py" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --output "$PROJECT_DIR/data/riders/stats.json" \
    --reference-date "$DATA_CUTOFF"
echo ""

# Step 2: Calculate points (data-cutoff matches stats so the two cannot drift)
echo "--- Step 2: Calculating points ---"
"$VENV_PYTHON" "$PROJECT_DIR/processing/calculate_points.py" \
    --daily-log "$PROJECT_DIR/data/riders/daily-log.json" \
    --rider-config "$PROJECT_DIR/data/riders/rider-config.json" \
    --points-config "$PROJECT_DIR/data/competition/points-config.json" \
    --output "$PROJECT_DIR/data/riders/points.json" \
    --data-cutoff "$DATA_CUTOFF"
echo ""

# Step 3: Snapshot stats for current segment
echo "--- Step 3: Creating stats snapshot for segment $SEGMENT ---"
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
    # Target the segment being published explicitly (#619). Passing "current"
    # resolves to the most recently published (draft:false, date<=today) entry,
    # which during a publish run is segment N-1 if N is still draft at this
    # point: N gets no weather and N-1 gets a retroactive rewrite (content-rule
    # violation). --segment is the authoritative target.
    "$VENV_PYTHON" "$PROJECT_DIR/processing/weather.py" \
        --entry "$SEGMENT" \
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
    #
    # The ssh stderr is filtered through grep -v to drop the benign
    # `sign_and_send_pubkey: signing failed for ED25519 ...: agent refused operation`
    # line that fired on the v1.4.17 publish (per #496). It's noise from the local
    # agent before ssh falls back to the next key; the deploy itself proceeds.
    # Real ssh failures still propagate via the ssh exit code + pipefail + the
    # surrounding `if !`. Filter is anchored on the full benign signature so it
    # does not swallow other agent-related errors.
    if ! ( set -o pipefail; tar -czf - -C .output/public . | ssh "${DEPLOY_TARGET%%:*}" "mkdir -p ${DEPLOY_TARGET#*:} && tar -xzf - -C ${DEPLOY_TARGET#*:}" 2> >(grep -v 'sign_and_send_pubkey: signing failed.*agent refused operation' >&2) ); then
        echo "ERROR: Step 8 deploy failed. Site was NOT uploaded to $DEPLOY_TARGET."
        exit 1
    fi
    echo "Deploy complete."
else
    echo "--- Step 8: No DEPLOY_TARGET set, skipping deploy ---"
    echo "Set DEPLOY_TARGET in .env (e.g., correze:/var/www/correze-travelogue/)"
fi
echo ""

# Step 9: Reconcile frontmatter changes to main via PR
# Closes the gap between the deployed artifact and main. The publish script
# mutates the entry frontmatter in place (dataCutoff, weather, sometimes images)
# and those mutations need to land on main before the script exits, or the next
# fresh clone builds the stub instead of the published entry. See issue #383
# and the v1.4.5 retrospective for the original reconciliation rationale; #451
# for why this now opens a PR rather than pushing direct to main (branch
# protection on main rejects direct pushes).
if [ "$SKIP_DEPLOY" = true ]; then
    echo "--- Step 9: Reconciliation skipped (deploy was skipped) ---"
elif [ "$SKIP_COMMIT" = true ]; then
    echo "--- Step 9: Reconciliation skipped (--skip-commit flag) ---"
elif [ -z "$DEPLOY_TARGET" ]; then
    echo "--- Step 9: Reconciliation skipped (no DEPLOY_TARGET, no deploy happened) ---"
else
    echo "--- Step 9: Reconciling frontmatter to main via PR ---"
    CURRENT_BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD)
    if [ "$CURRENT_BRANCH" != "main" ]; then
        echo "ERROR: publish.sh is not running on main (currently on $CURRENT_BRANCH)."
        echo "Refusing to reconcile from a non-main branch."
        echo "The deploy happened but main is not reconciled. Resolve manually."
        exit 1
    fi
    if [ -z "$ENTRY_FILE" ] || [ ! -f "$ENTRY_FILE" ]; then
        echo "ERROR: ENTRY_FILE not set or not found; cannot reconcile."
        echo "The deploy happened but main is not reconciled. Resolve manually."
        exit 1
    fi
    if git -C "$PROJECT_DIR" diff --quiet -- "$ENTRY_FILE" \
        && git -C "$PROJECT_DIR" diff --staged --quiet -- "$ENTRY_FILE"; then
        echo "No frontmatter changes to reconcile on $ENTRY_FILE."
    else
        TODAY=$(date +%Y%m%d)
        BRANCH_NAME="publish/segment-${SEGMENT}-frontmatter-${TODAY}"
        COMMIT_MSG="Segment $SEGMENT publish: record frontmatter from publish.sh"

        # Clean up any branch from a prior attempt today (local + remote); lets re-runs work cleanly.
        if git -C "$PROJECT_DIR" rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
            echo "Local branch $BRANCH_NAME exists from a prior attempt; deleting."
            git -C "$PROJECT_DIR" branch -D "$BRANCH_NAME"
        fi
        if git -C "$PROJECT_DIR" ls-remote --exit-code --heads origin "$BRANCH_NAME" >/dev/null 2>&1; then
            echo "Remote branch $BRANCH_NAME exists from a prior attempt; deleting."
            git -C "$PROJECT_DIR" push origin --delete "$BRANCH_NAME" \
                || { echo "ERROR: failed to delete prior remote branch. Resolve manually."; exit 1; }
        fi

        git -C "$PROJECT_DIR" checkout -b "$BRANCH_NAME" \
            || { echo "ERROR: git checkout -b failed. Resolve manually; the deploy already happened."; exit 1; }
        git -C "$PROJECT_DIR" add "$ENTRY_FILE" \
            || { echo "ERROR: git add failed. Resolve manually; the deploy already happened."; exit 1; }
        git -C "$PROJECT_DIR" commit -m "$COMMIT_MSG" \
            || { echo "ERROR: git commit failed. Resolve manually; the deploy already happened."; exit 1; }
        git -C "$PROJECT_DIR" push -u origin "$BRANCH_NAME" \
            || { echo "ERROR: git push failed. Resolve manually; the deploy already happened."; exit 1; }

        # Find or open the reconciliation PR
        PR_NUM=$(gh pr list --head "$BRANCH_NAME" --state open --json number --jq '.[0].number' 2>/dev/null || true)
        if [ -z "$PR_NUM" ]; then
            PR_URL=$(gh pr create \
                --base main \
                --head "$BRANCH_NAME" \
                --title "$COMMIT_MSG" \
                --body "Auto-generated by publish.sh to reconcile main with the deployed segment $SEGMENT artifact. Frontmatter mutations: \`dataCutoff\`, \`weather\` (sometimes \`images\`). The deploy already happened on $(date +%Y-%m-%d); this PR closes the reconciliation gap so a fresh clone builds the same artifact that is in production.") \
                || { echo "ERROR: gh pr create failed. Resolve manually; the deploy already happened."; exit 1; }
            PR_NUM=$(echo "$PR_URL" | grep -oE '[0-9]+$')
        else
            echo "Reusing existing PR #$PR_NUM for branch $BRANCH_NAME."
        fi
        echo "Reconciliation PR: https://github.com/gneeek/tdf26/pull/$PR_NUM"

        # Wait briefly for GitHub to compute mergeability after the push/create.
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            STATE=$(gh pr view "$PR_NUM" --json mergeStateStatus --jq '.mergeStateStatus' 2>/dev/null || echo "UNKNOWN")
            case "$STATE" in
                CLEAN|UNSTABLE|HAS_HOOKS)
                    break
                    ;;
                DIRTY|BEHIND|BLOCKED)
                    echo "ERROR: PR #$PR_NUM is in $STATE state; cannot squash-merge automatically. Resolve manually."
                    exit 1
                    ;;
                *)
                    sleep 3
                    ;;
            esac
        done
        if [ "$STATE" != "CLEAN" ] && [ "$STATE" != "UNSTABLE" ] && [ "$STATE" != "HAS_HOOKS" ]; then
            echo "ERROR: PR #$PR_NUM mergeability did not resolve within 30s (state: $STATE). Resolve manually."
            exit 1
        fi

        # Squash-merge into main; --delete-branch removes the remote feature branch.
        # Pre-check the PR state: branch protection's auto-merge can win the race
        # against this call (per #496, v1.4.17 publish: PR #495 was auto-merged
        # ~seconds after we pushed, before this script's merge call ran). When the
        # PR is already MERGED, the merge call would fail and `set -e` would kill
        # the script before Step 10 (tag/release). Treating already-merged as
        # success makes the publish path idempotent across the auto-merge race.
        PR_STATE=$(gh pr view "$PR_NUM" --json state --jq '.state' 2>/dev/null || echo "UNKNOWN")
        if [ "$PR_STATE" = "MERGED" ]; then
            echo "PR #$PR_NUM was already merged before our merge call (auto-merge race) — treating as success."
        elif ! gh pr merge "$PR_NUM" --squash --delete-branch; then
            # The pre-check above only narrows the window: auto-merge can still win
            # the race BETWEEN that check and this call, in which case `gh pr merge`
            # fails on the --delete-branch step (HTTP 404, branch already gone) even
            # though main is correctly fast-forwarded (#618, fired on seg 15 + 16).
            # Re-query state: if the PR is now MERGED the failure is the benign
            # branch-delete 404 and we proceed to the tag/release step; otherwise
            # it is a real merge failure and we halt as before.
            PR_STATE=$(gh pr view "$PR_NUM" --json state --jq '.state' 2>/dev/null || echo "UNKNOWN")
            if [ "$PR_STATE" = "MERGED" ]; then
                echo "PR #$PR_NUM merged via another path during our merge call; branch-delete likely 404'd. Treating as success."
            else
                echo "ERROR: gh pr merge --squash failed for PR #$PR_NUM (state: $PR_STATE). Resolve manually."
                exit 1
            fi
        fi

        # Pull the merged main back onto the local checkout
        git -C "$PROJECT_DIR" checkout main \
            || { echo "ERROR: git checkout main failed."; exit 1; }
        git -C "$PROJECT_DIR" pull --ff-only origin main \
            || { echo "ERROR: git pull failed; main may have moved. Resolve manually."; exit 1; }
        git -C "$PROJECT_DIR" branch -d "$BRANCH_NAME" 2>/dev/null || true

        echo "Frontmatter reconciled to main via PR #$PR_NUM."
    fi
fi

# Step 10: Tag and create GitHub Release
# Fires after the frontmatter commit so the tag captures main in agreement with
# the deployed artifact. Skipped if any earlier deploy/commit step was skipped,
# since those leave main and production out of sync.
if [ "$SKIP_RELEASE" = true ]; then
    echo "--- Step 10: Release skipped (--skip-release flag) ---"
elif [ "$SKIP_DEPLOY" = true ] || [ "$SKIP_COMMIT" = true ]; then
    echo "--- Step 10: Release skipped (deploy or commit was skipped) ---"
elif [ -z "$DEPLOY_TARGET" ]; then
    echo "--- Step 10: Release skipped (no DEPLOY_TARGET, no deploy happened) ---"
else
    echo "--- Step 10: Creating release tag $RELEASE_TAG ---"
    "$SCRIPT_DIR/create-release.sh" "$RELEASE_TAG" \
        --title "$RELEASE_TAG - Segment $SEGMENT publication" \
        || { echo "ERROR: create-release.sh failed. Deploy and frontmatter commit succeeded; tag/release require manual creation."; exit 1; }
fi

echo ""
echo "=== Done ==="
