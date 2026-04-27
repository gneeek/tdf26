# Strand B — Developer experience: bug-class cleanup (v1.4.11)

**Start here:** [Roadmap → Next → v1.4.11](https://github.com/gneeek/tdf26/wiki/Roadmap#next)

## Goal

Close two lingering bug-classes by fixing them at the root, each of which has bitten the project once already:

- Parallel-source-of-truth: a hand-maintained list naming strings declared elsewhere drifts. (#369 Côte de Malemort silent-drop incident.)
- Silent-failure: a shell pipeline prints success regardless of exit code. (Seg 7 publish-day false-success deploy print, 2026-04-26.)

Goal 4 (developer experience). Commit-tier: both should land. Together with strand A's two items, these are the four commit-tier items in the milestone's success bar.

## Filesystem posture

**Worktree.** Run in a separate worktree.

```
cd /home/jhs/code
git worktree add tdf26-bugclass main
cd tdf26-bugclass
```

When the strand finishes: `git worktree remove tdf26-bugclass` from the main checkout.

Branches per issue: `feature/issue-422-categorized-climbs-derive`, `feature/issue-426-publish-deploy-exit-code`. Verify `git branch --show-current` immediately before each `git add` / `git commit`.

## Target issues

- **[#422](https://github.com/gneeek/tdf26/issues/422)** — Derive `CATEGORIZED_CLIMBS` from `points-config.json` instead of hand-maintaining it.
- **[#426](https://github.com/gneeek/tdf26/issues/426)** — `publish.sh` deploy step prints 'Deploy complete' even when SSH fails.

Order: independent. Either order works. #426 is smaller; landing it first frees a slot quickly.

## Workflow per issue

### #422 (refactor)

Current state:

- `utils/stage-totals.ts:15` exports `CATEGORIZED_CLIMBS` as a hand-maintained `Set<string>`.
- `data/competition/points-config.json` declares `climbs[].name` and self-describes as "Single source of truth for climb identity, summit segment, and span."
- `components/StageDetails.vue:34,82` consumes `CATEGORIZED_CLIMBS`.
- `utils/stage-totals.ts:64,86` consumes it twice more.

Approach:

1. In `utils/stage-totals.ts`, replace the hand-maintained `Set` with a `Set<string>` derived from `points-config.json`'s `climbs[].name` field. Decide whether to keep the export name (`CATEGORIZED_CLIMBS`) or rename to something derivative (`POINTS_CONFIG_CLIMB_NAMES`). Default: keep the name to minimise churn in consumers.
2. Add a unit test that asserts the derived set matches the points-config climbs and fails if the two drift. (This test, not the hand-maintained list, becomes the parallel-source-of-truth detector for this case.)
3. Confirm `components/StageDetails.vue` continues to render correctly under `npm run build` and a production preview.
4. Open PR, assign to milestone v1.4.11.

Out of scope: building the general parallel-source-of-truth detector noted in `project_next_planning_notes.md`. File a follow-up issue if it surfaces during this work.

### #426 (shell hardening)

Current state:

- `scripts/publish.sh` Step 8 (Deploy) runs an SSH-tar pipeline and unconditionally `echo "Deploy complete."` afterwards.
- The seg 7 publish (2026-04-26) emitted SSH `agent refused operation` warnings; the deploy succeeded (SSH fell back to IdentityFile), but the misleading success message would have masked a real failure.

Approach:

1. Add explicit exit-code handling to the SSH-tar pipeline in Step 8. Options:
   - `set -o pipefail` at the top of the step + check `$?` after the pipeline.
   - Capture the SSH exit code into a variable and gate the success message on it.
   - Run the pipeline under a function that exits non-zero on failure.
   Pick one and document inline why.
2. If the deploy fails, the script should print a clear failure message naming the failed step and exit non-zero so the orchestrating release process notices.
3. Verify by simulating a deploy failure in a local invocation (e.g. point the SSH host at an unreachable target) and confirming the script no longer prints "Deploy complete."
4. Open PR, assign to milestone v1.4.11.

Out of scope: end-to-end render verification (carryforward from v1.4.6+v1.4.7 retro) and other steps in `publish.sh` that may have similar silent-failure patterns. If they surface, file new issues — do not fix inline.

## Verification commands

The following npm scripts exist in `package.json`:

- `npm ci`, `npm run lint`, `npm test`, `npm run build`, `npm run generate`, `npm run preview`.
- There is **no** `npm run typecheck`. Type errors surface during `npm run build`.

Per-issue:

- #422: `npm run lint && npm test && npm run build`. Production preview confirms `StageDetails.vue` renders the climb list.
- #426: `bash -n scripts/publish.sh` (syntax check). Manual simulation of an SSH failure to confirm the failure path.

For Node-touching Bash, prefix with `source ~/.nvm/nvm.sh && nvm use --silent &&`.

## Cross-strand sharing notes

- Strand A (security) touches `components/ImageGallery.vue`, `components/content/InlineFigure.vue`, `pages/admin/images.vue`, `server/api/wikipedia-images.post.ts`, `.github/workflows/deploy.yml`. **No overlap with this strand.**
- Strand C (sqlite stretch) is briefed to prefer the `package.json` postinstall route to avoid touching `scripts/publish.sh`, which is this strand's #426 region. **If C lands first** with a `publish.sh` edit (it shouldn't, per its brief), this strand rebases on C. Default expectation: C does not touch `publish.sh`.
- This strand should land #426 cleanly without coordinating with C. If C surprises, rebase.

## Scope discipline

- Two issues, two PRs. Do not bundle.
- File new issues for class-of-bug instances surfaced during this work (e.g. other parallel-source-of-truth lists, other silent-failure shell pipelines). Do not fix inline.

## Memories that apply

- `feedback_bash_nvm_sourcing.md`, `feedback_env_check.md`, `feedback_pr_polling.md`, `feedback_production_preview.md`, `feedback_shared_tree_branch_verification.md`.
- `feedback_no_regex_in_bash.md` — relevant if any inline Python lands in `publish.sh` shell-embedded contexts.
- `feedback_issues_describe_problems.md`.

## Stop when

- Both #422 and #426 PRs are merged into main.
- The #422 unit test asserts the derived/declared sets match.
- The #426 fix is confirmed by a local failure simulation that does not print "Deploy complete."
- Worktree removed.
- Any class-of-bug residue is filed as new issues, not fixed inline.
