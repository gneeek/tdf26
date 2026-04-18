#!/usr/bin/env bash
# PreToolUse guard against destructive git commands when the working tree is
# dirty or has local-only commits. Motivated by the 2026-04-12 lost-commit
# incident (see issue #358, PR #357).
#
# Triggered on: git reset --hard, git clean -f[d], git checkout ., git restore .,
# git push --force/-f, git branch -D.
#
# Checks: (1) git status --porcelain; (2) git log origin/<branch>..HEAD.
# If either produces output, the command is denied with the offending files or
# commits named. Override by appending " # i-know" to the command.
#
# Reads hook JSON on stdin, emits a PreToolUse hookSpecificOutput JSON.
set -u

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')

# Narrow regex: only destructive families. End-of-token anchors avoid matching
# things like "git checkout .venv" or "git clean-room" etc.
if ! printf '%s' "$cmd" | grep -qE '(^|[[:space:];&|])(git reset --hard|git clean +(-[fF][dq]*|--force)|git checkout +\.([[:space:]]|$)|git restore +\.([[:space:]]|$)|git push +([^#]* )?(-f|--force)([[:space:]]|$)|git branch +-D)'; then
  exit 0
fi

# Explicit override
if printf '%s' "$cmd" | grep -qE '#[[:space:]]*i-know'; then
  jq -n '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"allow",permissionDecisionReason:"destructive-git guard: override via i-know marker"}}'
  exit 0
fi

# If we are not inside a git repo, let the command through — git itself will error.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

# Only modified/added/deleted tracked files count — untracked (??) does not, since
# reset --hard, checkout ., restore ., branch -D do not discard untracked files.
dirty=$(git status --porcelain 2>/dev/null | grep -vE '^\?\?' || true)

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
local_commits=""
if [ -n "$branch" ] && git rev-parse --verify --quiet "origin/$branch" >/dev/null 2>&1; then
  local_commits=$(git log "origin/$branch..HEAD" --oneline 2>/dev/null || true)
fi

if [ -z "$dirty" ] && [ -z "$local_commits" ]; then
  exit 0
fi

reason="destructive-git guard triggered on: $cmd"$'\n'
if [ -n "$dirty" ]; then
  reason+=$'\nWorking tree is dirty:\n'"$dirty"
fi
if [ -n "$local_commits" ]; then
  reason+=$'\n\nLocal-only commits on '"$branch (not on origin/$branch):"$'\n'"$local_commits"
fi
reason+=$'\n\nCommit, stash, or push first. To override, append " # i-know" to the command.'

jq -n --arg r "$reason" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
