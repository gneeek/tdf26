# Strand: publish.sh redeploy / deploy-only recovery path (#630)

> **Status: PARKED — #630 closed won't-fix on 2026-05-30 (deferred, not rejected).**
> Operator-only benefit and speculative: no publish has yet needed a second pass, so the
> flag would pre-pay a debt not yet incurred. Removed from v1.4.20 (returned it to 10 issues).
> **Reopen trigger:** an actual publish that needs a second pass (a finalize PR merges after
> the initial run and the deployed artifact must be rebuilt + re-uploaded). Cheaper interim
> option if discoverability bites first: option (b), a sub-runbook in the recovery playbook —
> not the flag. This brief is the ready-to-pick-up design; the rest below assumes execution.

Single-issue implementation strand (deviation: "Target issues" + "Workflow per issue" are collapsed into §4–5). Adds the missing second-pass recovery path to `scripts/publish.sh` so an operator can rebuild-and-re-upload the current `main` artifact without re-running the stats/points/snapshot/weather/frontmatter/release pipeline.

## 1. Goal

`publish.sh` has no way to redeploy. When a publish needs a second pass — e.g. a finalize PR merges after the initial run and the deployed artifact must be rebuilt and re-uploaded — the operator hand-copies the Step 7 (`nuxt generate`) + Step 8 (tar-pipe-over-ssh) commands out of the script. There is no `--redeploy` / `--deploy-only` flag that runs only build + deploy against current `main`, skipping Steps 1–6 (stats, points, snapshot, weather, narrative, image validation) and Steps 9–10 (frontmatter reconciliation, tag/release). This strand adds that path. Milestone: **v1.4.20 — Publish-pipeline hardening**; it is the publish.sh-robustness theme the gate fixes (#617/#618/#619, merged) were a down-payment on. Not a publication-day gate. **Note for planning:** #630 was filed 2026-05-29, after the 2026-05-28 session fixed v1.4.20's trimmed 10-issue set, so the milestone now carries 11 issues — reconcile whether #630 is genuinely this-cycle or bumps to the next when this lands.

## 2. Filesystem posture

- Explicit-path worktree, run from outside the repo:
  ```
  git -C /home/jhs/code/tdf26 worktree add -b feature/publish-redeploy-630 /home/jhs/code/tdf26-redeploy main
  ```
  The gate (#617/#618/#619) is already merged to `main`, so branching off `main` is clean. Do **not** use the nesting in-repo form; do **not** add a `.claude` symlink (`feedback_strand_worktree_path.md`).
- **Branch verification:** before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/publish-redeploy-630` (`feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `scripts/publish.sh` is the single artifact this strand edits; read it end-to-end first. The step structure is: Pre-flight (#617 draft check) → Steps 1–6 (data/weather/narrative/images) → Step 7 (`nuxt generate`) → Step 8 (deploy) → Step 9 (frontmatter PR reconcile) → Step 10 (tag/release). The arg-parsing block is the `for arg in "$@"` loop near the top; flags currently are `--segment`, `--release-tag`, `--skip-deploy`, `--skip-weather`, `--skip-commit`, `--skip-release`, `-h/--help`.
- The redeploy path's contract is "rebuild and re-upload **current `main`** verbatim" — it must **not** mutate `data/riders/*`, entry frontmatter, git history, or tags. The whole point is that `main` is already correct; redeploy only re-materialises the artifact.

## 4. Target issue & design decision

**#630** — add a redeploy / deploy-only path. The issue offers two shapes:
- (a) a `--redeploy` flag that runs only Step 7 + Step 8 against current `main`, or
- (b) a documented sub-runbook in the publish.sh recovery mini-playbook.

**Early checkpoint (AskUserQuestion):** confirm flag-vs-runbook before implementing. **Recommend (a) the flag** — it is the durable fix and removes the hand-copy error surface; a runbook leaves the operator hand-copying. (b) is a stopgap, not a deliverable worth a strand. If the publisher picks (b), this strand collapses to a docs change and should say so. The rest of this brief assumes (a).

## 5. Workflow

1. **Add the flag.** Introduce `REDEPLOY=false` alongside the other `SKIP_*` vars; add a `--redeploy` case (consider `--deploy-only` as an accepted alias) to the arg-parsing loop and a line to `--help`. Update the `# Usage:` header comment.
2. **Gate the pipeline.** When `REDEPLOY=true`, skip Steps 1–6 and Steps 9–10, running only Step 7 (`nuxt generate`) and Step 8 (deploy). Prefer an explicit early branch or per-step guards over abusing the existing `--skip-*` flags — the reader should see "redeploy mode runs build+deploy only" plainly, not infer it from a stack of skips.
3. **Keep the pre-flight (recommended), confirm at the checkpoint.** The #617 draft pre-flight is cheap insurance against re-publishing a draft; recommend running it in redeploy mode too so `--redeploy` can never push a `draft: true` target. Flag this as a sub-decision if the publisher wants redeploy to be a pure no-questions re-upload.
4. **Guard the obvious misuse.** `--redeploy` requires `DEPLOY_TARGET`; with `--skip-deploy` it is a no-op — error clearly rather than silently doing nothing. `--redeploy` with `--release-tag` is contradictory (redeploy does not tag) — reject or ignore with a clear message.
5. **Idempotent + re-runnable.** Two consecutive `--redeploy` runs must both succeed and leave `git status` clean (no data/frontmatter mutations, no commits, no tags).

## 6. Verification commands

There is **no shell-test harness yet** (that is the open #508, owned by the spine strand) — so demonstrate behaviour with runnable checks, not a unit test:

- **Step-skip proof (runnable):** run `./scripts/publish.sh --redeploy` with `DEPLOY_TARGET` **unset**. Expected: Step 7 `nuxt generate` runs; Step 8 prints "No DEPLOY_TARGET set, skipping deploy"; Steps 1–6 and 9–10 do not run (confirm via the `=== Step N ===` echo markers absent). Then `git status --porcelain` must be empty — no `data/riders/*` or frontmatter mutation.
- **`npx nuxt generate`** completes clean (Step 7 path; seed gitignored rider data first per `feedback_ci_seed_ordering.md`).
- **`npm test`** stays green (no JS changed; run as a regression guard).
- **`shellcheck scripts/publish.sh`** if available in the environment — keep the script lint-clean.
- **Re-runnability:** invoke `--redeploy` twice; both exit 0 and leave `git status` clean.
- Do **not** run a real deploy against the production VM (`feedback_pre_publish_scrutiny.md`); the `DEPLOY_TARGET`-unset run proves the control flow without touching production.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `scripts/publish.sh` (the arg-parsing block + a redeploy branch around Steps 7–8) and its `# Usage:` / `--help` text. If the checkpoint picks the runbook shape, `scripts/README.md` instead.
- **What this strand reads:** nothing it modifies elsewhere.
- **What this strand must NOT touch:** `data/*`, `content/entries/*`, `processing/*`. The redeploy path must be inert on all of them.
- **Collision with the unrun spine and ceremony strands — this is the load-bearing note.** Three strands edit `scripts/publish.sh`:
  - **Spine (`strand-spine-322-479-508-326.md`, unrun):** #508 adds the shell-test harness; #322 adds a pre-publish render-check. **`--redeploy` is a natural #508 test target.** Recommend this strand lands **before** the spine strand so #508 backfills regression coverage for `--redeploy` (skip-the-pipeline, idempotency, `DEPLOY_TARGET`-unset). If spine lands first, rebase on it and add the redeploy regression test into its harness rather than inventing a parallel one.
  - **Ceremony (`strand-ceremony-480-521-339.md`, unrun):** #480 edits the Step 10 release-create region — a different part of the file from this strand's arg-parser + Steps 7–8 branch, so low collision. If ceremony lands first, rebase; the regions should not overlap.
  - **Rule:** whoever lands second on `publish.sh` rebases, never runs concurrently. Forecast the most likely conflict: the arg-parsing `for arg in "$@"` loop, which every publish.sh strand extends. Keep the `--redeploy` case addition minimal and localized so a rebase is a clean three-way merge of independent `case` arms.

## 8. Scope discipline

- File a new issue for anything beyond the redeploy path (e.g. if reading publish.sh surfaces an unrelated Step 8 fragility) — do not fold it in.
- Record the flag-vs-runbook decision and the pre-flight-in-redeploy sub-decision in the PR body (`feedback_issues_describe_problems.md`).
- `Closes #630` in the PR (this is the implementing PR, not a brief-commit, so a closing keyword is correct — contrast `feedback_pr_closure_keywords.md`).

## 9. Memories that apply

- `feedback_strand_worktree_path.md`, `feedback_shared_tree_branch_verification.md`.
- `feedback_ci_seed_ordering.md` — seed rider data before any build.
- `feedback_pre_publish_scrutiny.md` — do not deploy to production from a test run.
- `feedback_issues_describe_problems.md`, `feedback_pr_closure_keywords.md`.
- `feedback_no_regex_in_bash.md` — if any embedded Python is touched (unlikely here).

## 10. Stop when

- PR open `Closes #630` with the `--redeploy` flag (or, if the checkpoint chose it, the runbook); the `DEPLOY_TARGET`-unset step-skip proof shown in the PR body; `nuxt generate` clean; `npm test` green; `shellcheck` clean (if available); two-run idempotency demonstrated with a clean `git status`.
- The flag-vs-runbook and pre-flight-in-redeploy decisions recorded in the PR body.
- Final report to publisher: PR link, the decisions made, and an explicit note to the spine strand that `--redeploy` wants #508 regression coverage. Reconcile the v1.4.20 issue-count (now 11) at the report.
- **Retro inputs written to `project_next_planning_notes.md` at close** under a new section header (e.g. `## Items surfaced during redeploy-630 execution (<date>)`): decision-actionable observations (incl. the v1.4.20 scope reconciliation and the spine-coverage handoff), light-tier pattern observations, and numeric stats (`git diff --stat`, commits, AskUserQuestion checkpoints fired, approx wall-clock).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-redeploy` once the PR has merged.
