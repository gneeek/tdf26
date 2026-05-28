# Strand: publish-day safety fixes (#617 / #618 / #619)

## 1. Goal

Land the three publish-day safety fixes that gate seg 17. Seg 16 shipped a still-draft entry and 404'd in production; the `gh pr merge` step aborted on both seg 15 and seg 16; and `weather.py` rewrote a prior entry's weather. All three must merge to `main` **before seg 17 publishes (Sun 2026-05-31)** so seg 17 runs on a hardened pipeline. This is the v1.4.20 ("Publish-pipeline hardening") gate strand. Auto-mode with conditional checkpoints; this is script work, not content.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/publish-safety /home/jhs/code/tdf26-publish-safety main
```

- Run from outside the repo or with `git -C`; do not nest the worktree.
- Do NOT `ln -s` the `.claude` dir; it comes with the checkout.
- Before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/publish-safety`.
- Fresh worktree has no `node_modules` and no rider-seed data: run `npm ci`, then `cp data/riders/*.example.json` to their non-example names before `npm run build` (per `feedback_ci_seed_ordering.md`).

## 3. Source-of-truth posture

- The behaviour under test lives in `scripts/publish.sh`, `processing/weather.py`, and `scripts/create-release.sh`. Read them directly; do not assume the flow from the planning notes — verify against current source.
- The failure descriptions are in issues #617/#618/#619 and in `project_next_planning_notes.md` under "Items surfaced during seg-16 publish (2026-05-28)" and "seg-15 publish (2026-05-24)". Treat those as the bug reports, not the fix spec — confirm each against the script before patching.
- `weather.py`'s "current" resolver: read how `--entry current` selects the target before changing it. The fix is to honour an explicit `--entry $SEGMENT` from publish.sh, not to change the "current" semantics for standalone use.

## 4. Target issues

Milestone **v1.4.20 - Publish-pipeline hardening**. Order by dependency, not number:

1. **#617** — draft pre-flight abort. Cheapest, highest leverage; do first.
2. **#619** — `weather.py --entry $SEGMENT` from publish.sh. Independent of #617.
3. **#618** — `gh pr merge` idempotency (check `gh pr view --json state` before merge+branch-delete).

One PR may carry all three (they are small and all in `scripts/`/`processing/`), or split if review clarity wants it. Prefer one PR titled for the gate; the three issues close together.

## 5. Workflow per issue

- **#617:** Add a pre-flight near the top of publish.sh's `main()` (matching the fail-fast pattern Retro v1.4.18 promoted) that reads the target entry's frontmatter `draft:` field and aborts with a clear message if it is `true`. Decide with the publisher (checkpoint) whether to *abort* (publisher flips draft by hand, safest) or *auto-flip* (publish.sh sets `draft: false`). Recommend abort for this strand; auto-flip is the larger #322 design.
- **#619:** Make publish.sh pass `--entry $SEGMENT` (the segment it is publishing) to `weather.py` instead of `--entry current`. Confirm weather lands in seg N and that seg N-1's weather block is untouched on disk (`git diff` clean on the prior entry).
- **#618:** Before `gh pr merge --squash`, query `gh pr view <n> --json state`; if `MERGED`, skip the merge and the branch-delete and proceed to the tag/release step. Re-run cleanly against an already-merged PR.

## 6. Verification commands

- `bash -n scripts/publish.sh` — syntax check after edits.
- `npm test` — full suite (expect 204 pass + skips).
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `python3 processing/validate_points.py`
- `npm run build` (after the seed-data step).
- **Red-green for #617:** point publish.sh at an entry with `draft: true` (a scratch fixture or a temporary flag flip, reverted before commit) and confirm the pre-flight aborts; flip to `draft: false` and confirm it proceeds. Do not commit the breakage.
- **Red-green for #618:** simulate the already-merged state (a PR that is MERGED, or a stubbed `gh pr view` returning `MERGED`) and confirm the merge step is skipped without error.
- If #508's shell-test-harness lands first, wire these as harness cases; otherwise document the manual red-green in the PR body.

## 7. Cross-strand sharing notes

- **Owns (write):** `scripts/publish.sh`, `processing/weather.py`, and a possible new test fixture/harness file under `tests/` or `processing/tests/`.
- **Reads:** `content/entries/*.md` (frontmatter only, no edits), `scripts/create-release.sh`, `data/segments.json`.
- **Must NOT touch:** any `content/entries/*.md` body or frontmatter (published entries are fixed per `feedback_content_change_rule.md`); `data/` files; sibling work.
- **Collisions:** this strand should be the **sole writer of `scripts/publish.sh`** for its window. Do not run it alongside a publish cycle. If #508 (shell-test harness) is being worked in parallel, coordinate — both touch the script's testability surface; land #508's harness first if it is close, else this strand ships its own minimal red-green and #508 generalises later.

## 8. Scope discipline

- File new issues for anything outside the three fixes (e.g. the two-pass-publish `--redeploy` path the seg-16 notes flagged — that is a real gap but a separate issue, not this strand).
- The auto-flip-vs-abort choice for #617 is the one material checkpoint; everything else is mechanical. Do not rubber-stamp; do not over-ask.
- Document any publisher override in the PR body.

## 9. Memories that apply

- `feedback_ci_seed_ordering.md` — fresh-worktree seed step before build.
- `feedback_shared_tree_branch_verification.md` — branch check before commit.
- `feedback_strand_worktree_path.md` — explicit-path worktree.
- `feedback_production_preview.md` — use `nuxt generate`, not the SSR runtime, for any build spot-check.
- `feedback_assertion_bug_class.md` — work the diagnostic by hand before writing a red-green check.
- `feedback_content_change_rule.md` — do not touch published entries (relevant to #619's "don't rewrite seg N-1" check).
- `feedback_strand_session_self_cleanup.md` — own the worktree teardown.

## 10. Stop when

- One PR open (or up to three) closing #617, #618, #619; CI green; red-green demonstrated for #617 and #618 (in harness or documented in PR body).
- **Merged before seg 17 publishes (Sun 2026-05-31).** This is the gate — if it cannot land by then, surface that to the publisher immediately so seg 17 ships on the documented manual workaround rather than silently slipping.
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-publish-safety` once merged.
- Final report to publisher: PR link(s), which red-green ran, any new issue filed (e.g. `--redeploy` gap).
- **Retro inputs written to `project_next_planning_notes.md`** under a new `## Items surfaced during publish-safety strand execution (<date>)` header: decision-actionable observations, light-tier pattern observations, numeric stats (files-touched, commits, checkpoints fired, wall-clock).
