# Strand: dependabot #689 — test and merge the npm minor-and-patch group

Maintenance strand: land [PR #689](https://github.com/gneeek/tdf26/pull/689), `build(deps): bump the minor-and-patch group across 1 directory with 11 updates` (npm; `package.json` + `package-lock.json`). Auto-mode, no sub-agents. Mirrors the `deps-640-644` strand. Startable now; orthogonal to the content strands.

## 1. Goal

Get #689 to a clean, verified merge. **Current state (verify it is still true): MERGEABLE = CONFLICTING, MERGESTATE = DIRTY, but CI `test` = SUCCESS.** The conflict is on the lockfile because #700 (`deps: clear Dependabot alerts`, merged 2026-06-27) touched `package-lock.json` after #689 was opened. So the work is: rebase, re-verify, smoke-test the build, merge, confirm.

## 2. Procedure

1. **`git fetch` and re-check live state** (`gh pr view 689 --json mergeable,mergeStateStatus,statusCheckRollup`) — do not trust this brief's snapshot (`feedback_pr_polling`; multi-session visibility).
2. **Rebase, do not hand-resolve.** Comment `@dependabot rebase` on #689 and wait for dependabot to refresh the branch to MERGEABLE/CLEAN with green CI (the `deps-640-644` lesson: same-file lockfile conflicts are dissolved by a rebase, never by manual edits). Re-poll until clean; if rebase stalls, `@dependabot recreate` is the fallback (note: recreate may change the branch name — re-fetch).
3. **Scan the 11 updates for hidden risk.** Read the PR body and the version diffs. The group is configured **minor-and-patch**, so it should carry no majors — but **0.x packages treat a minor as breaking**, so flag any `0.x` minor bump or anything touching the Nuxt/Vite/Nitro build toolchain for the smoke test below. If a true **major** appears (it should not), stop and checkpoint the publisher (the `deps-640-644` Pillow precedent).
4. **Build smoke-test in a scratch worktree** (11 npm bumps at once warrants a real build, not just `npm test` — `nuxt build` is more fragile than the test suite, `reference_worktree_node_modules_build`):
   ```
   git fetch origin
   git -C /home/jhs/code/tdf26 worktree add /home/jhs/code/tdf26-deps689 dependabot/npm_and_yarn/minor-and-patch-f4e34742a4
   ```
   Then in that worktree: real `npm ci`; seed rider data (`cp data/riders/*.example.json` to non-example names, `feedback_ci_seed_ordering`); `npm test`; `npm run build` + `nuxt generate` (must exit 0, routes render). Prefix Node-touching commands with `source ~/.nvm/nvm.sh && nvm use --silent &&` (`feedback_bash_nvm_sourcing`).
5. **Merge on green.** With CI green + clean build smoke and no surprise major, **squash-merge with branch delete**: `gh pr merge 689 --squash --delete-branch` (matches the repo's `... (#NNN)` squash history; dependabot has no human-judgment cost here — the `deps-640-644` precedent merged minors on green CI without a checkpoint).
6. **Verify the merge and post-merge CI.** Confirm `gh pr view 689 --json state` == `MERGED` (`feedback_pr_polling`), then `gh run watch` / `gh run list` on the resulting `main` CI run to confirm it is green.

## 3. Checkpoints

- **None by default** — a minor-and-patch group on green CI + clean build is auto-mergeable (`deps-640-644` precedent).
- **Fire ONE checkpoint only if:** the diff scan turns up a surprise major or a risky `0.x` minor whose consumer the smoke-test can't clear, or the build smoke fails. Then present the offending bump + options (hold that package / merge the rest / proceed) before merging.

## 4. Filesystem / scope

- Scratch worktree only (step 4); **do not** create a branch off main or edit the lockfile yourself — dependabot owns the PR branch. Verify `git branch --show-current` before any incidental commit (`feedback_shared_tree_branch_verification`); this strand should not commit to the repo at all (it merges a PR).
- **Owns:** nothing in-tree — it lands a PR. **Must not touch** `content/`, `data/`, or open a content PR.
- This is the only open dependabot PR at brief-time; if others appear, this strand stays scoped to #689 (one PR), per the publisher's request.

## 5. Memories that apply

`feedback_pr_polling`, `feedback_bash_nvm_sourcing`, `feedback_ci_seed_ordering`, `reference_worktree_node_modules_build`, `feedback_shared_tree_branch_verification`, `feedback_strand_session_self_cleanup`. (Pattern source: the `deps-640-644` close-out in `project_next_planning_notes.md` — `@dependabot rebase` for lockfile conflicts; majors get a checkpoint, minors merge on green; the planning-level question of enabling dependabot auto-merge for patch/minor is **not** this strand's to decide.)

## 6. Stop when

- #689 is `MERGED`, its branch deleted, and the post-merge `main` CI run is green.
- **Cleanup (you run):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-deps689` (`feedback_strand_session_self_cleanup`).
- Final report: confirmation of MERGED + green post-merge CI, the rebase outcome, the 11-update risk scan result (any 0.x/toolchain bumps noted), and whether the build smoke surfaced anything.
- **Retro inputs** to `project_next_planning_notes.md` under `## Items surfaced during deps-689 strand execution (<date>)` — and if the rebase-on-stale-lockfile toil recurs, note it reinforces the still-open planning question of enabling dependabot auto-merge for patch/minor groups.
