# Strand B — Developer experience: dependency-update queue

**Start here:** [Roadmap → Now → Developer-experience strand](https://github.com/gneeek/tdf26/wiki/Roadmap#now)

## Goal

Clear the open dependency-update queue. Verify each pending update against a real build and a real test run; merge what is safe, close what is not. Nothing else.

## Worktree first

This strand runs in a separate git worktree to keep its branch-switching off the shared checkout. Strands A and C work in `/home/jhs/code/tdf26/`; do not disrupt that working tree.

```
cd /home/jhs/code
git worktree add tdf26-deps main
cd tdf26-deps
```

When the strand finishes: `git worktree remove tdf26-deps` from the main checkout.

## Target PRs

Seven open Dependabot PRs as of 2026-04-27 (refresh with `gh pr list --repo gneeek/tdf26 --author app/dependabot`):

- #418 pytest-cov >=6.0.0 → >=7.1.0
- #417 ruff >=0.11.0 → >=0.15.12
- #416 numpy >=1.26.0 → >=2.4.4
- #415 pytest >=8.0.0 → >=9.0.3
- #414 gpxpy >=1.6.0 → >=1.6.2
- #406 minor-and-patch group across 1 directory with 8 updates (npm)
- #405 postcss 8.5.8 → 8.5.10

All seven were opened in a single wave on 2026-04-24.

## Verify-then-merge loop

Per PR:

1. `gh pr checkout <N>` (inside the worktree).
2. Install for the affected ecosystem:
   - npm PRs (#405, #406): `npm ci`
   - python PRs (#414-#418): use the project's processing tooling (see `processing/pyproject.toml` and `processing/requirements.txt`).
3. Run the relevant test set:
   - npm: `npm run lint && npm run typecheck && npm test && npm run build`
   - python: `cd processing && pytest`
4. If green, merge via `gh pr merge --squash --delete-branch <N>` and assign to milestone v1.4.10.
5. If red: investigate. If the failure is a real breakage with the new version, close the PR with a comment explaining why and the safer pin to keep. Do not merge red PRs.

## Memories that apply

- `feedback_bash_nvm_sourcing.md` — prefix Node-touching Bash with `source ~/.nvm/nvm.sh && nvm use --silent &&`.
- `feedback_env_check.md` — verify Node and Python versions match `.nvmrc` and `pyproject.toml` engines before installing.
- `feedback_pr_polling.md` — verify merges via GitHub API, don't rely solely on what `gh pr merge` prints.

## Scope discipline

If a PR fails for an unrelated reason (flaky test, environment drift), the fix belongs to the strand only if it unblocks merging. Anything that turns into a non-trivial investigation gets filed as a new issue and the PR is left for the next pass. Do not re-scope into an upgrade-and-fix sprint.

## Stop when

- All seven PRs have been resolved (merged or closed with reason).
- Any failures that surfaced during verification are filed as new issues.
- Worktree removed.
