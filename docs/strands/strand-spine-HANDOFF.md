# Spine strand — session handoff (2026-05-29)

Companion to `docs/strands/strand-spine-322-479-508-326.md` (the brief — read it first).
This note captures the **chat-only decisions and current worktree state** that the brief
does not, so a fresh session can resume without re-deriving anything. Per
`feedback_session_close_decision_persistence.md`: load-bearing decisions made in chat decay
across session boundaries unless written to a tracked file — this is that file.

> **Why a fresh session, not a compact:** the prior session suffered tool-result truncation
> and one outright hallucination (a fabricated "focus on /home/jhs/code/pap" instruction that
> the publisher never gave). That context is degraded; a compact would carry the corruption
> forward. Start clean from disk + GitHub state, which this note + the brief fully describe.

## Verify on resume (do this FIRST — do not trust this note's state blindly)

The note below records state as of 2026-05-29; readback was flaky when it was written. Re-derive before acting:

```
cd /home/jhs/code/tdf26-spine
git branch --show-current          # expect: feature/pipeline-spine
git status --porcelain             # expect the uncommitted #508 set listed below
git fetch origin -q && git log origin/main --oneline -5   # confirm #635 (#479) landed
source ~/.nvm/nvm.sh && nvm use --silent
npm run test:shell                 # expect 5/5 ok (green)
```

If any of these disagree with the note, trust the commands.

## Progress so far

- **#479 — DONE, MERGED.** PR **#635** (`#479: document inline-JSON image-frontmatter
  convention (Phase 2d)`) merged to `main`. Commit on branch: `9912f66`. Doc-only; its content
  is on `main` via squash. Verified against source: `validate_entries.py` accepts both
  frontmatter forms but only inline-JSON yields real per-image fields; YAML block-list is parsed
  crudely (counts `- src:` lines, drops alt/attribution) — that's the seg-9-crash class. Rule now
  documents actual validator behaviour; full YAML support gated on #326.

- **#508 — IMPLEMENTED, GREEN, UNCOMMITTED.** Lives unstaged in the `tdf26-spine` worktree.
  `npm run test:shell` = 5/5 ok. `npm test` (vitest) = 209 passed / 3 skipped (skips pre-existing).
  `bash -n scripts/publish.sh` clean. **Not yet committed or pushed** — that is the next action.

  Uncommitted change set (from `git status --porcelain`):
  ```
   M .github/workflows/ci.yml      # adds "Run shell tests (bats)" step after JS coverage
   M package-lock.json             # bats@^1.13.0
   M package.json                  # devDep bats; new script "test:shell": "bats tests/shell"
   M scripts/publish.sh            # REFACTOR: source-guard + #617/#618 extracted to functions
  ?? scripts/README.md             # new: shell-script testing rule + script index
  ?? tests/shell/                  # test_helper.bash + 3 .bats files
  ```
  Test files: `tests/shell/{test_helper.bash, draft_preflight.bats, merge_idempotent.bats,
  weather_entry_isolation.bats}`.

- **#322 — NOT STARTED.**
- **#326 — NOT STARTED.**

## Decisions made in chat (carry these forward)

1. **#508 harness = bats-core.** Chosen over shunit2 / Python runner / vitest-shell-out because
   the issue names bats. Installed as a devDependency (`bats@^1.13.0`); not a system dep.
   `npm run test:shell` → `bats tests/shell`; CI runs it after `npm ci`.

2. **#508 = keep the pragmatic refactor (publisher decision).** The implementing agent found the
   brief's described gate-fix interfaces (return-3 draft check; `merge-base --is-ancestor` merge;
   `--segments` flag) **do not match shipped code** (b857802 / #629). Actual shipped behaviour:
   - **#617** auto-flips `draft: true` → `draft: false` in place and continues; only aborts (exit 1)
     on a *missing* entry file. No "refusing to publish", no return 3.
   - **#618** idempotency lives in Step 9's `gh pr view ... state==MERGED` re-query, not a
     `merge-base` check.
   - **#619** flag is `--segments-json` (not `--segments`); with no api-key, `weather.py` writes
     **nothing** (no stub). Tests stub `urllib` to exercise the real injection path.

   To make the gates unit-testable, the agent refactored `scripts/publish.sh`: added a source-guard
   (`[ "${BASH_SOURCE[0]}" != "${0}" ] && return 0`), changed `dirname "$0"` →
   `dirname "${BASH_SOURCE[0]}"`, and extracted #617/#618 logic into sourceable functions
   `preflight_draft_check` and `merge_frontmatter_commit` (behaviour preserved). **Publisher chose
   to keep this refactor** (option: "keep the pragmatic refactor, coordinate merge order") rather
   than reverting it or going black-box.

   **Two caveats to record in the #508 PR body:**
   - The `#618` test (`merge_idempotent.bats`) tests a **model function** (`merge_frontmatter_commit`,
     local `merge-base --is-ancestor`), **not the live `gh`-PR path** (which is impractical to
     unit-test without GitHub). The live Step 9 `gh` flow is left byte-for-byte unchanged. This is
     documented in-file; restate it in the PR so a reviewer isn't misled.
   - The `#617` test asserts **auto-flip**, not the brief's "refusing to publish" — because that's
     what shipped. Flag the brief-vs-source divergence (per `feedback_brief_content_is_carryforward.md`).
   - Red-green was demonstrated transiently (mutate → red → restore → green); **no breakage is
     committed**. Confirm `git status` is clean of mutations before committing.

3. **#326 scope = all FIVE parsers.** The issue lists four (`validate_entries.py`, `weather.py`,
   `server/api/entries.get.ts`, `server/api/images.post.ts`); the scope doc says "publish.sh is one
   of the four." Source-trace confirms **`publish.sh` also hand-rolls frontmatter** (inline bash +
   Python regex one-liners), so it is functionally a 5th parser. Resolve toward the scope doc:
   consolidate all five. **Flag the issue-vs-scope-doc discrepancy in the #326 PR body**
   (per `feedback_source_of_truth_framing.md`). Note: js `images.post.ts` already uses `js-yaml`,
   not pure regex — confirm its real shape before migrating.

4. **#326 window = attempt all four, split on signal.** Work 479→508→322→326 in sequence. If #326
   starts displacing the other three within the v1.4.20 window (target ~seg 20, 2026-06-10), stop
   and split #326 to a follow-on strand for the next milestone — surface this to the publisher via
   AskUserQuestion **the moment** it looks like displacing, not silently (brief §8).

5. **#322 / #521 checklist ownership — RESOLVED by sequencing.** The ceremony strand already merged
   (`3a1cb3a`, #633) and shipped the #521 lifecycle checklist. So #322 **adds its verification step
   into the existing checklist**; it does NOT author the checklist artifact. No collision; no need to
   re-negotiate.

## Interaction between #508's refactor and #326 (watch this)

Both edit `scripts/publish.sh`. #508 restructures it into sourceable functions; #326 will migrate
its inline frontmatter parsing onto the shared canonical parser. When #326 runs, **rebase on the
merged #508** and re-verify the source-guard + extracted functions survive the parser migration.
The brief's forecast failure mode (#326 silently reverting the gate's `--entry`/weather handling)
still applies — land the #508 weather isolation test before the #326 weather.py migration so the
migration runs against a red-green guard (it now exists: `weather_entry_isolation.bats`).

## Next concrete steps (in order)

1. **Commit + push #508**, open its PR (`Closes #508`), body carrying the three caveats in
   decision #2 and the bats-choice rationale. Confirm CI green (the new bats step + vitest).
2. **#322** — `nuxt generate` render-check in CI asserting each entry page renders (no blank/500),
   static not SSR (`feedback_production_preview.md`); add the verification step into the existing
   #521 checklist; reference #617's draft pre-flight as the first gate, don't re-implement it.
   `Closes #322`.
3. **#326** — shared schema → canonical Python parser (migrate validate_entries.py + weather.py) →
   canonical TS parser (migrate entries.get.ts + images.post.ts) → publish.sh inline parse →
   delete hand-rolls → anti-regression lint/CI guard. Prove byte-identical field extraction on every
   current entry before deleting. Rebase on merged #508. `Closes #326` (or split per decision #4).

## Brief reminders that still bind

- `feedback_shared_tree_branch_verification.md` — `git branch --show-current` = `feature/pipeline-spine`
  before every `git add`/`commit` (multiple worktrees are live: data-route, data-attractions, seg-19).
- `feedback_ci_seed_ordering.md` — worktree already seeded (`cp data/riders/*.example.json`) and
  `npm ci` done this session; re-seed if the worktree is recreated.
- **Must NOT touch:** any `content/entries/*.md` body/frontmatter; `data/` content; publish.sh
  release/merge *logic* (the #508 refactor preserved behaviour — do not change what the merge/release
  steps *do*); the wiki Roadmap step (ceremony owns it).
- One PR per issue (or coherent pair); not one mega-PR.

## Stop-when (from brief §10)

PRs open closing #508, #322, #326 (or #326 split-out with a tracking note); CI green; red-green shown
for #508 and #326. Then: `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-spine`.
Final report to publisher (PR links, #326 disposition, the discrepancy resolution). Retro inputs
appended to `project_next_planning_notes.md` under
`## Items surfaced during pipeline-spine strand execution (<date>)`.
