# Strand: Dependabot sweep 2026-05-24

Auto-mode dependency-hygiene strand to clear the eight open dependabot PRs accumulated since the last sweep. Authored 2026-05-24 as part of the v1.4.19 close-out parallel slate. Captures `docs/planning/NEXT.md` item 1 of this weekend's sequenced execution.

## 1. Goal

Land all eight open dependabot PRs (or explicitly close any that the strand finds unsafe) before the v1.4.19 planning session Mon/Tue 2026-05-25/26. Zero source changes expected; CI-green is the merge gate. Bundle PR #583 needs a closer review than the singletons because it touches `@nuxt/content` 3.13 → 3.14, which adds a new search composable.

No tracking issue is filed for the sweep itself per v1.4.10 / v1.4.17 precedent — the PRs are their own tracking. Milestone tagging: leave dependabot PRs un-milestoned (they ride their own merge cadence). Runs in **auto-mode** with two checkpoints: (1) #583 bundle review before merge, (2) any PR that breaks CI.

## 2. Filesystem posture

**Own worktree, even though most operations are remote.** The parent `/home/jhs/code/tdf26` checkout is in use by the planning session; sibling strands use their own worktrees. Dep-sweep needs filesystem isolation for any `gh pr checkout` (which switches branch in cwd), `npm install` (which mutates `node_modules`), and `npm run build` (which writes `.nuxt/`, `.data/`).

```
git -C /home/jhs/code/tdf26 worktree add --detach /home/jhs/code/tdf26-deps main
```

A detached worktree is correct here — the strand creates no local feature branch and lands no local commits; every merge goes through `gh pr merge <N>` against the remote. The detached HEAD just gives `gh pr checkout` and `npm install` a safe place to operate.

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- After `gh pr checkout <N>` inside the worktree, branch state is non-stationary; if for any reason a local commit is needed (e.g., resolving a dependabot rebase conflict by hand), confirm `git branch --show-current` per `feedback_shared_tree_branch_verification.md` before commit.
- The worktree's `node_modules`, `.nuxt/`, and `.data/` are independent of the parent and sibling worktrees — no cross-worktree races.

## 3. Source-of-truth posture

- `package.json` and `package-lock.json` (JS dependencies) and `processing/requirements.txt` (Python dependencies) are the source-of-truth for declared versions. Dependabot PRs mutate exactly these files plus the lockfile.
- GitHub Actions CI on each PR is the safety gate. If CI is not green at review time, **do not merge** — investigate the failure first.
- For any major version bump, check the upstream changelog (linked in the PR body) for breaking changes. None of the eight PRs in this sweep are major bumps, but the practice is per `feedback_pre_publish_scrutiny.md` extended to dependency hygiene.

## 4. Target PRs

Reviewed and ordered by risk shape (lowest first):

| # | Update | Notes | Order |
|---|---|---|---|
| #574 | brace-expansion 5.0.5 → 5.0.6 | Patch, transitive, no source impact | 1 |
| #567 | devalue 5.8.0 → 5.8.1 | Patch, Nuxt serialisation | 2 |
| #579 | js-cookie 3.0.5 → 3.0.7 (devDep) | Patch, dev-only | 3 |
| #581 | ruff `>=0.15.12 → >=0.15.14` (processing) | Lint tool, processing-only | 4 |
| #582 | numpy `>=2.4.4 → >=2.4.6` (processing) | Patch, processing-only | 5 |
| #576 | @nuxt/nitro-server 4.4.4 → 4.4.6 | **Pairs with #575 — merge together** | 6 |
| #575 | nuxt 4.4.4 → 4.4.6 | **Pairs with #576 — merge together** | 6 |
| #583 | minor-and-patch group (6 packages) | **See bundle note below** | 7 |

**Known CI state at strand-spawn time (2026-05-24):** PRs #574, #567, #579, #581, #582, #583 are green. **#575 and #576 are red — `npm ci` lockfile drift on `commander` (bucket (b) in §5 step 6).** Likely fix: `@dependabot rebase` on both, rebased one at a time per the cross-PR ordering note. Do not close them.

**Bundle note on #583:** title says 7 but body lists 6 packages: `@nuxt/content 3.13.0 → 3.14.0`, `better-sqlite3 12.9.0 → 12.10.0`, `marked 18.0.3 → 18.0.4`, `nuxt 4.4.4 → 4.4.6`, `@vitest/coverage-v8 4.1.5 → 4.1.7`, `eslint 10.3.0 → 10.4.0`.

Two things to know about #583:
- **Overlap with #575**: #583 also bumps `nuxt` 4.4.4 → 4.4.6. If #575 merges first, dependabot should auto-rebase #583 to remove the duplicate bump; if #583 merges first, #575 becomes redundant and should be closed. **Recommended path: merge #575 + #576 first (the explicit nuxt pair), then let dependabot rebase #583, then merge #583's remaining packages.**
- **`@nuxt/content` 3.13 → 3.14** is the only feature-bearing change in the sweep — adds a `useSearchCollection` composable (FTS5 full-text search) per the changelog. The minor-version bump shouldn't break anything, but read the [@nuxt/content 3.14 changelog](https://github.com/nuxt/content/blob/main/CHANGELOG.md) for breaking changes before merging.
- **`better-sqlite3` 12.9.0 → 12.10.0**: PR #446 previously added a postinstall rebuild step to retire the Module-did-not-self-register class. Verify that postinstall still runs cleanly under the bumped version — if it doesn't, file a separate issue and hold #583 until resolved.

## 5. Workflow

Auto-mode sequence; AskUserQuestion fires only at the two checkpoints noted.

1. **Fetch each PR's current CI state**:
   ```
   for n in 574 567 579 581 582 576 575 583; do
     gh pr checks $n --required
   done
   ```
   Any PR with red CI does not merge in this pass — investigate per step 6.

2. **Walk PRs 1–5 (low-risk singletons)** in the order in the table above. For each:
   - Confirm CI green.
   - `gh pr diff <N>` — confirm the diff is only `package.json`/`package-lock.json` or `processing/requirements.txt` mutations.
   - `gh pr merge <N> --squash --delete-branch` (or whatever the repo's standard merge mode is — read `.github/dependabot.yml` or recent merged dependabot PRs to confirm).
   - Wait for the previous merge to complete + dependabot to rebase the queue before merging the next, so each PR merges against current `main` and CI re-runs against the latest lockfile state.

3. **Walk the Nuxt pair (#575 + #576)** together:
   - Confirm both green.
   - Merge #576 first (server-side), then #575 (top-level). Dependabot may auto-rebase one against the other; if a conflict surfaces, comment `@dependabot rebase` and wait.
   - After merge, run `npm install && npm run build` locally to confirm the production build succeeds. If it doesn't, revert the Nuxt pair via PR and file an issue.

4. **#583 bundle checkpoint (AskUserQuestion)**:
   - Re-fetch the PR after the Nuxt pair lands; confirm dependabot has dropped the duplicate `nuxt` bump from the bundle.
   - Read the changelog summary for `@nuxt/content` 3.14 (FTS5 search composable — does the project's existing Nuxt Content usage continue to work?).
   - Run `npm install && npm test && npm run build` locally on the rebased branch.
   - Present to publisher: "PR #583 ready to merge: [diff stats], CI green, local build green, @nuxt/content 3.14 added FTS5 search composable (additive — no existing API changes). Merge?" with options Merge / Hold for review / Close.

5. **Verify post-sweep state**:
   - `gh pr list --search "author:app/dependabot" --state open` — should be empty (or only PRs that were explicitly held).
   - `git pull origin main` and confirm clean working tree.
   - `npm test` + `npm run build` + `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` + `python3 processing/validate_points.py` all green.

6. **CI failure path** (most dependabot failures fall in (c) or (d), not (e) — do not jump to closing the PR):

   Fetch the failing log first:
   ```
   gh api repos/gneeek/tdf26/actions/runs/<run-id>/logs > /tmp/log.zip && unzip -o /tmp/log.zip -d /tmp/ci-log
   grep -iE "peer|ERESOLVE|conflict|notarget|invalid|^npm ERR" /tmp/ci-log/*.txt | head -20
   ```

   Triage:

   - **(a) Flaky CI** — failure is not deterministic (timeout, network, unrelated test): re-run via `gh run rerun <run-id>` or comment `@dependabot rebase` to push a fresh commit.

   - **(b) Stale lockfile drift** — the most common dependabot failure on this repo. Symptoms in the log: `npm ci` complains "lock file's X@A does not satisfy X@B" or "Missing X from lock file." Cause: `main` has moved since dependabot opened the PR and the lockfile no longer matches `package.json` or another package's manifest. **Remedy: comment `@dependabot rebase` on the PR.** Wait for dependabot to push a new commit; CI re-runs automatically. If `@dependabot rebase` doesn't resolve it, try `@dependabot recreate` (regenerates the PR from scratch). Only after both fail does this become bucket (d).

   - **(c) Paired-dep cascade** — bumping one package on its own breaks `npm install` because a peer or sibling package needs to be bumped in lockstep (common with `nuxt` + `@nuxt/nitro-server`, or `vue` + `@vue/compiler-*`). Symptoms: ERESOLVE peer-dep error naming both packages. **Remedy: handle the cluster as one merge.** Two options:
     - **Combine locally** — in the dep-sweep worktree: `gh pr checkout <smaller-N>`, then `git fetch origin <other-branch>:<other-branch>`, then `git merge <other-branch>`, run `npm install` to resolve the lockfile, push back. The combined branch's CI runs once; merge resolves both PRs.
     - **Ask dependabot** — comment `@dependabot merge` on the latter after the former lands, or use `@dependabot squash and merge` if the repo allows it. Less reliable than the local combine for paired-dep failures.

   - **(d) Genuine regression** — the bumped package has a real breaking change. Symptoms: test assertions fail, runtime error in the bumped module, build error in code that uses the package's API. **Remedy: file an issue describing the breaking change with a link to the upstream changelog, close the PR with a comment pointing to the issue, configure dependabot ignore for this version range (`.github/dependabot.yml`) so it doesn't auto-recreate.**

   - **(e) Out-of-band failure** — CI infrastructure broken, secret rotated, runner image changed. Symptoms: failure is repo-wide, not PR-specific. **Remedy: not a dep-sweep concern; flag to publisher and hold all merges until repo CI is green again.**

   Order of operations: try (a) re-run / (b) rebase **first** (cheap, often resolves). Only after both fail, move to (c) combine / (d) close / (e) escalate.

   **Cross-PR ordering for shared lockfile drift:** if multiple PRs all fail with bucket (b), rebasing one and merging it will force the others to rebase against the new `main`. Handle one at a time — rebase #N, wait for CI green, merge, then rebase #N+1 against the new main. Parallel rebases of two PRs touching the same lockfile region produce double-rebases.

## 6. Verification commands

- `gh pr list --search "author:app/dependabot" --state open` — empty (or held PRs listed) post-sweep.
- `npm test` — green post-sweep.
- `npm run build` — green post-sweep.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green post-sweep (Python deps changed via #581 / #582).
- `python3 processing/validate_points.py` — green post-sweep.
- **Spot-check** seg 15 entry render in dev to confirm Nuxt Content still works after #583 lands.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `package.json`, `package-lock.json` (via dependabot PR merges only — no manual edits).
  - `processing/requirements.txt` (via dependabot PR merges only).
- **What this strand reads:**
  - `.github/dependabot.yml` for merge-mode convention.
  - Recent merged dependabot PRs for any project-specific merge-script conventions.
- **What this strand must NOT touch:**
  - `content/entries/*` — owned by seg 15 drafting strand.
  - `data/competition/points-config.json` — owned by #513 strand.
  - `data/attractions.json` — owned by #564 strand.
  - `tests/utils/*.test.ts` — owned by #518 strand.
  - `components/EntryCard.vue` — owned by #535 strand (in flight in another session).
  - `processing/validate_entries.py` and friends — not in dependabot's mutation set anyway.
- **Cross-strand collisions and rebasing rules:**
  - **High-likelihood collision: #583 bumps `nuxt`, and so does #575.** Resolved by the merge order in §5 (merge #575+#576 first, let dependabot rebase #583).
  - **Possible collision: #518's new climb-summit-km test uses Vitest, and #583 bumps `@vitest/coverage-v8`.** Low risk (patch-level vitest plugin bump), but if #518 lands first, re-run #518's test under the new vitest to confirm green before merging #583.
  - **No collision expected with #513, #564, seg 15 drafting, or #535** — different files entirely.
  - **Recommended merge order across all parallel strands:**
    1. dependabot singletons (#574, #567, #579, #581, #582) — quick wins.
    2. dependabot Nuxt pair (#575, #576) — clears the way for #583.
    3. #564 Chirac fix (smallest non-dep work).
    4. #513 Suc au May fix.
    5. #518 summit-km assertion.
    6. dependabot bundle (#583) after #583 rebases against post-#575/576 main.
    7. seg 15 drafting (lands when ready, against fully-deps-clean main).
    8. #535 thumbnails (independent file region; lands whenever the in-flight session finishes).

## 8. Scope discipline

- **No manual edits to lockfiles.** All dependency bumps flow through dependabot PRs.
- **Hold rather than merge** any PR with red CI, a flagged major-version bump, or a breaking-change changelog entry. File an issue per held PR explaining the hold; do not let dependabot re-create indefinitely.
- **AskUserQuestion fires at the #583 bundle and any CI failure.** Other singletons are mechanical.
- **No scope expansion.** This strand does not audit `package.json` for unrelated upgrades, does not introduce new dependencies, does not remove unused ones. Those are separate work.

## 9. Memories that apply

- `feedback_strand_worktree_path.md` (no worktree needed; if one is created for local repro, follow the rule).
- `feedback_shared_tree_branch_verification.md` (any local rebase needs branch verification).
- `feedback_pre_publish_scrutiny.md` (extended to dependency hygiene: read changelogs).
- `feedback_ci_seed_ordering.md` (CI seeds rider data after JS tests; dependency bumps shouldn't change this, but verify post-merge CI run if anything in the rider-stats pipeline depends on bumped packages).
- `feedback_bash_nvm_sourcing.md` (any local npm command needs `source ~/.nvm/nvm.sh && nvm use --silent &&` prefix).
- `feedback_pr_closure_keywords.md` (dependabot PRs don't need `Closes` keywords; they reference their own update entries).

## 10. Stop when

- All eight PRs either merged or explicitly held (with an issue filed per held PR).
- `gh pr list --search "author:app/dependabot" --state open` returns empty or only the held set.
- `npm test` + `npm run build` + Python validators all green against post-sweep `main`.
- Seg 15 dev render confirmed working after #583 lands.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-deps` once the sweep is complete. If any `gh pr checkout` left a stranded local tracking branch inside the worktree, it disappears with the worktree.
- Final report posted to publisher: list of merged PRs, list of held PRs with rationale, post-sweep CI state.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during dependabot-sweep strand execution (<date>)`:
  - **Decision-actionable observations:** any held PRs needing follow-up, any breaking-change patterns surfaced in the changelogs, any postinstall regressions (e.g., better-sqlite3).
  - **Light-tier pattern observations:** sweep wall-clock vs the v1.4.10-retro question ("if manual cost stays low, recurring routine is overhead"); update the routine-vs-manual decision input.
  - **Numeric stats:** PRs merged, PRs held, AskUserQuestion checkpoints fired, approximate wall-clock.
