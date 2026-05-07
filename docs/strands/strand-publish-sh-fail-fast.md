# Strand — `publish.sh` fail-fast policy per failure mode (#496)

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md). Closes [#496](https://github.com/gneeek/tdf26/issues/496) (scope-expanded at planning).

## 1. Goal

Apply three fixes to `scripts/publish.sh` so that the seg 11 publish on Sun 2026-05-10 does not recur the three failure modes that fired during the v1.4.17 publish on Wed 2026-05-06. Fixes ship in one PR with the policy framing documented at top-of-file: **first-fire is a feature; recurrence is a bug; surface vs. autonomous-recovery is decided per failure mode.**

**Hard deadline:** PR must merge before Sun 2026-05-10 afternoon. Seg 11 publish window. Milestone v1.4.18.

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-496-publish-sh-fail-fast /home/jhs/code/tdf26-publish-sh main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

Source-of-truth posture is light for this strand because the work is code-only (no segment data or content involved). Read:

- `scripts/publish.sh` — the production publish path; treat with care
- `scripts/create-release.sh` — sibling tag/release script (for understanding the post-merge step)
- The v1.4.17 publish-day log if it's preserved in the WORK-LOG or wiki — for failure-mode evidence (timestamps, exact error strings)
- Any shell utilities `publish.sh` sources

Per `feedback_no_regex_in_bash.md`: regex backreferences in bash-embedded Python produce control chars; if a fix needs string manipulation, prefer pure bash or a small Python script over shell-piped `sed`/`awk`/`python -c` with backreferences.

## 4. Target issues

- **Closes [#496](https://github.com/gneeek/tdf26/issues/496)** — scope expanded at planning to fail-fast policy per failure mode; covers all three failure modes from this cycle.
- No new follow-up issues expected (the chore-deploy script wrapper carryforward stays deferred per planning decision; do not bundle it).

## 5. Workflow

### Fix 1: Idempotent `gh pr merge --squash`

**Failure:** during v1.4.17 publish, PR #495 was auto-merged at 22:10:04Z (seconds after the script pushed the branch); script's `gh pr merge --squash` then failed because the PR was no longer in a mergeable state, and `set -e` killed Step 10 before tag/release could run.

**Fix:**
- Locate the `gh pr merge --squash` call in `scripts/publish.sh` (Step 9).
- Wrap the call so that "already merged" is treated as success. Two reasonable approaches:
  - Pre-check: `gh pr view <PR_NUMBER> --json state` and only call `gh pr merge --squash` if state is `OPEN`.
  - Post-check: call `gh pr merge --squash`, capture exit code; on non-zero, re-check state via `gh pr view`; if `MERGED`, return 0; otherwise propagate the error.
- Pre-check is cheaper (one extra API call only when relevant); post-check handles a wider race window. Either works for this fix; pre-check probably wins.
- Print a clear message ("PR #N was already merged before our merge call — treating as success.") so future debug logs make the path obvious.

### Fix 2: `dataCutoff` non-interactive fallback

**Failure:** Step 3's `read -rp "Enter dataCutoff: " DATA_CUTOFF` returned non-zero with no TTY (background invocation); `set -e` killed the script before the fallback `DATA_CUTOFF=$(date +%Y-%m-%d)` could fire.

**Fix:**
- Locate the `read -rp` line (Step 3).
- Replace the conditional so that read failure (no TTY OR empty input) falls through to the fallback. Two patterns:
  - `read -rp "..." DATA_CUTOFF || true` followed by `DATA_CUTOFF=${DATA_CUTOFF:-$(date +%Y-%m-%d)}` — single-line idiom.
  - Test for TTY first: `if [ -t 0 ]; then read -rp "..." DATA_CUTOFF; fi` then `DATA_CUTOFF=${DATA_CUTOFF:-$(date +%Y-%m-%d)}` — avoids the `|| true` swallow.
- Pattern 2 is cleaner because it explicitly says "interactive only if TTY"; pattern 1 is one fewer line.

### Fix 3: SSH agent stutter

**Failure:** benign — `sign_and_send_pubkey: signing failed for ED25519 ...: agent refused operation` printed before `Deploy complete.` on the next line. Deploy succeeded; the noise was misleading in publish-day logs.

**Fix:**
- Locate the `rsync` / `ssh` call(s) in Step 8.
- Either:
  - `|| true` on the offending command (simplest; risk: also swallows real failures unless we're careful) — only acceptable if the deploy itself has its own success-confirmation that runs after.
  - Pipe stderr through a filter to drop the known benign line: `2> >(grep -v 'agent refused operation' >&2)`. More precise; preserves real errors.
- Filter is preferred. Document in code comment why this stderr filter exists, citing the v1.4.17 publish.

### Top-of-file policy comment

After the three fixes, add a short comment block at the top of `scripts/publish.sh` capturing the policy:

```
# publish.sh fail-fast policy
# - First-time failure modes surface and halt the script (set -e by default).
# - Recurrence-class failures become autonomous-recovery: the script handles them
#   without halting because publisher investigation is complete.
# - Specific recurrence-handled cases (per #496):
#   1. PR auto-merged before script's own merge call.
#   2. read -rp with no TTY for dataCutoff.
#   3. SSH agent benign-noise stutter on deploy.
# - When a new failure mode fires for the first time, halt and surface; promote to
#   autonomous-recovery in the next planning if it recurs.
```

### Test pass

For each fix, demonstrate red-green where possible:

- **Fix 1:** simulate "already merged" by manually merging a test PR before invoking the merge call. Confirm script returns 0 and continues to Step 10.
- **Fix 2:** invoke publish.sh in a non-interactive shell (`bash -c './scripts/publish.sh ...'` or via cron / nohup). Confirm fallback fires.
- **Fix 3:** harder to reproduce the agent stutter on demand; instead confirm filter doesn't swallow real SSH errors by deliberately breaking the rsync target.

Do not commit artificial breakage. Document the test method in PR body so the publisher can re-verify.

## 6. Verification commands

- `npm test` — must pass (publish.sh isn't covered by JS tests, but defensive).
- `bash -n scripts/publish.sh` — syntax check; must pass.
- `shellcheck scripts/publish.sh` — if shellcheck is installed; lint warnings should not regress vs main. Not a hard requirement.
- **Dry-run test:** `./scripts/publish.sh --help` (or whatever flag exists for help / dry-run) should still work and print expected text.
- **Three fix demonstrations** as outlined in Workflow step "Test pass" — manual but documented in PR body.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `scripts/publish.sh`
- **What this strand reads:**
  - `scripts/create-release.sh` (for context on what comes after the merge step)
  - Any shell utilities sourced from publish.sh (e.g., common helpers if any)
  - The v1.4.17 publish-day log / WORK-LOG.md / wiki Retro v1.4.17 page for failure-mode evidence
- **What this strand must NOT touch:**
  - `scripts/create-release.sh` — separate sibling script; chore-deploy wrapper deferred per planning.
  - `processing/*.py` — out of scope.
  - `data/*.json`, `content/entries/*.md` — out of scope.
- **Cross-strand collisions:**
  - **No concurrent strands touch `scripts/publish.sh`.** The CLAUDE.md deprecation, climb-data, segs-14-16 verification, and skill-creation strands all stay clear of `scripts/`.
  - **Seg 11 publish on Sun depends on this strand merging first.** If this strand slips past Sun morning, the seg 11 publish either re-fires the three failures or has to be done with manual workarounds (the same workarounds that worked for v1.4.17). Plan: PR open by Fri evening, merged by Sat afternoon at latest.

## 8. Scope discipline

- **Three fixes only.** Do not refactor publish.sh structure; do not introduce new features (chore-deploy wrapper deferred).
- **Do not bundle in unrelated cleanup.** If shellcheck flags pre-existing issues outside the three fixes, leave them; file a follow-up issue.
- **AskUserQuestion at material disagreements** — likely candidates:
  - Pattern 1 vs pattern 2 for the dataCutoff fix (the brief recommends pattern 2; if implementation reveals a wrinkle, surface).
  - Pre-check vs post-check for the auto-merge race (brief recommends pre-check; surface if the gh CLI behaves unexpectedly).
  - Stderr filter shape for the SSH stutter (brief recommends grep-based filter; surface if it hides real errors).

## 9. Memories that apply

- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_no_regex_in_bash.md` — relevant if any fix considers shell-piped Python with regex backreferences (avoid)
- `project_publisher_onboarding.md` — the publish.sh fix is publisher-experience; the second publisher arriving after April 14 should not be the one to discover these failure modes
- `feedback_pre_publish_scrutiny.md` — the publish-window context that the policy framing reflects

## 10. Stop when

- Three fixes landed in `scripts/publish.sh`.
- Top-of-file policy comment captures the framing.
- Each fix demonstrated to behave correctly (test method documented in PR body).
- Verification commands green.
- PR open against milestone v1.4.18 closing #496.
- **PR merged before Sun 2026-05-10 afternoon.** This is a hard deadline; the strand is not "done" until merged in time for seg 11 publish.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-publish-sh` once the PR has merged.
- Final report posted to publisher: PR link, three-fix demonstration summary, any open questions surfaced for the seg 11 publish window.

## 11. Notes for next retro (post-execution, 2026-05-07)

PR opened as #512. Worktree removed before merge per publisher request; recreate with the explicit-path form from §2 if review feedback lands.

### What went well
- Brief was specific enough to execute end-to-end without surfacing material disagreements. The three "pattern A vs pattern B" decisions in §8 all resolved to the brief's recommendation.
- Filter-precision smoke for Fix 3 (synthesize a stderr stream containing the benign line + two real-error lines, pipe through `grep -v <signature> >&2`, confirm only benign was dropped) caught the question "does this swallow real errors" cheaply, without needing the actual race condition.
- Red-green smoke for Fix 2 (`bash -c '...' < /dev/null` with and without the TTY gate) gave a clean before/after exit code in two runs.
- Worktree explicit-path form from `feedback_strand_worktree_path.md` worked first try.

### What was challenging / surprising
- **Brief drift from code.** §5 Fix 3 said "locate the rsync / ssh call(s) in Step 8"; actual code is `tar | ssh`, no rsync. Filter still applies, but the placement (inside `if ! ( set -o pipefail; … )`) was non-trivial. Worth noting for future briefs that the source-of-truth scan should sample the actual file before committing to terminology.
- **Self-induced GPG snag.** I added `-c commit.gpgsign=true` to the commit invocation unprompted; local config doesn't enforce signing, and the forced sign tripped on a missing secret key. Removing the flag resolved it. Lesson: do not add git flags that aren't in the brief or current config.
- **git config / memory mismatch.** Local `user.email` is `gneeek@gmail.com`; auto-memory says `gneeek@proton.me`. The commit went through with the gmail address. Worth a one-line confirm at next planning: is the gmail address intentional for tdf26 commits?
- **Worktree needs its own `npm install`.** Not surprising, but adds ~30s to first-test for any fresh worktree. If multi-strand worktree work continues, a shared `node_modules` symlink or pnpm-style store would shave that.

### What we learned
- **Anchor stderr filters on the full benign signature, not the trailing fragment.** `'sign_and_send_pubkey: signing failed.*agent refused operation'` is small enough to be cheap and specific enough that "agent refused operation" appearing in some other context (real auth failure, key revocation) won't be silently swallowed. Template for future filters in publish.sh.
- **`if [ -t 0 ]; then read; fi` beats `read … || true`.** Both work, but the explicit TTY check reads at-a-glance as "interactive only," whereas `|| true` reads as "swallow any failure" — same behavior, worse intent signal. Apply to any future non-interactive-aware prompts.
- **Pre-check is the right shape for race-class fixes.** One extra API call only when the race could matter; no swallowed errors. Better than retry-on-failure in a place where the expected outcome is success.

### What we lack
- **No CI coverage for publish.sh.** Three of these fixes (the `gh pr` race, the no-TTY read, the ssh stderr stutter) cannot be exercised in a JS/Vitest run. Fix 1 in particular gets its first live verification on the seg 11 publish 2026-05-10 — that's a production-only test. A thin smoke harness (mock `gh`, mock `ssh`, drive publish.sh through its decision branches with set fixtures) would shorten the loop on future publish.sh fixes. Candidate carry-debt item.
- **shellcheck not installed locally.** Brief listed it as soft requirement; couldn't run. Next planning could decide whether it goes in the dev-env bootstrap.
- **The auto-merge race fix cannot be unit-tested without faking `gh`.** This is a sub-case of the publish.sh-CI gap above; calling it out separately because it's the one that bit us in v1.4.17 and the next time it bites it will reveal a different fault we don't currently have coverage for.
