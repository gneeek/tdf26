# Strand B — Developer experience: per-source-of-truth assertions (v1.4.18)

**Start here:** [Roadmap → Next → v1.4.18](https://github.com/gneeek/tdf26/wiki/Roadmap#next), then [#474](https://github.com/gneeek/tdf26/issues/474).

## Goal

Generalise the #422/#448 worked example: build vitest assertions that fail when hand-maintained lists in code drift from their declaring JSON source. Survey the codebase for parallel-source pairs; write assertions for the ones the publisher confirms.

Goal 4 (developer experience) and goal 5 (process improvement). Commit-tier — foundational for the v1.4.18 data-layer regime.

## Filesystem posture

**Worktree.** Run in a separate worktree.

```
cd /home/jhs/code
git worktree add tdf26-assertions main
cd tdf26-assertions
ln -s ../tdf26/.claude .claude
source ~/.nvm/nvm.sh && nvm use --silent
npm ci
cp ../tdf26/data/riders/daily-log.json data/riders/
cp ../tdf26/data/riders/points.json data/riders/
cp ../tdf26/data/riders/stats.json data/riders/
[ -d ../tdf26/data/riders/snapshots ] && cp -r ../tdf26/data/riders/snapshots data/riders/
npx nuxt prepare
```

When the strand finishes: `git worktree remove tdf26-assertions` from the main checkout.

Branch: `feature/issue-474-source-of-truth-assertions`. Verify `git branch --show-current` immediately before each `git add` / `git commit`.

## Target issue

- **[#474](https://github.com/gneeek/tdf26/issues/474)** — Data drift: hand-maintained lists in code aren't asserted against their declaring source

## Workflow

1. **Read the precedent.** `tests/utils/stage-totals.test.ts` from PR #448 is the worked example. Internalise the shape before scanning.
2. **Survey.** Scan the codebase for parallel-source pairs — hand-maintained lists, sets, enums, or arrays in `utils/`, `components/`, `pages/`, `composables/`, `server/` that name strings declared in `data/*.json`. Use `grep` / `rg` to find candidates: list-literals near data file imports.
   Likely candidates to look for explicitly (not exhaustive):
   - Rider IDs in code vs `data/riders/rider-config.json`
   - Segment names referenced in code vs `data/segments.json`
   - Climb categories in code vs `data/competition/points-config.json`
   - Attraction categories in code vs `data/attractions.json`
3. **Checkpoint with publisher** on which pairs to land in this PR vs defer (see Checkpoints).
4. **For each agreed pair:** write a vitest assertion in `tests/utils/` that derives the expected value from the JSON source and asserts the code-side list matches. Test must fail-red without the assertion, green with it.
5. **Demonstrate red-green** — temporarily mutate the source-of-truth JSON, run the test, confirm fail, revert. Do not commit the mutation.
6. **Open PR**, milestone v1.4.18.

## Checkpoints with publisher (AskUserQuestion)

- **After survey:** present the list of parallel-source pairs found as one AskUserQuestion (multi-select). Format options as: "(N) `<code-location>` shadows `<json-source>`". The publisher picks which to assert in this PR vs defer to follow-up issues.
- **For each ambiguous pair** (where the code-side list might be a deliberate subset/derivation rather than a shadowed copy): AskUserQuestion before writing the assertion. Options: (a) assert exact equality, (b) assert subset, (c) deliberate derivation — document and skip, (d) skip — file follow-up issue.
- **Before opening PR:** AskUserQuestion to confirm test file names and total assertion count.

If the publisher session is unavailable and a checkpoint blocks: stop, write what you've found to a `WORK-LOG.md` in the worktree root, exit cleanly. Do not guess past a checkpoint.

## Verification commands

The following npm scripts exist in `package.json`:
- `npm ci`, `npm run lint`, `npm test`, `npm run build`, `npm run generate`, `npm run preview`. There is **no** `npm run typecheck`.

For this strand:
- `source ~/.nvm/nvm.sh && nvm use --silent && npm test`
- For each new assertion: temporarily mutate the source JSON, run `npm test -- tests/utils/<name>.test.ts`, confirm red, revert.

## Cross-strand sharing notes

- **Strand A** (#477) writes to `data/*.json`. **No write overlap.** Coordinate: if A's data corrections happen before this strand opens PR, the assertion derivations stay fresh against final data. If after, this strand may need a small post-merge tweak (or A may need to update an assertion if a key changes).
- **Strand C** (#475) writes new schemas + validation wiring. **No overlap with `tests/utils/`.** Different validation surfaces; both can coexist (vitest assertions catch cross-file consistency; schemas catch shape).
- **Publish session for seg 10 (parallel today)** writes to `data/riders/*.json`. **No overlap with this strand's writes.** If you assert against `rider-config.json` and the publish session updates it, your assertion holds (rider-config is not changed by publish day).
- This strand owns `tests/utils/` writes for v1.4.18.

## Scope discipline

- One issue, one PR.
- File follow-up issues for parallel-source pairs not landed in this PR.
- **Do not** build the general grep-shaped scanner — per the v1.4.8 retro the per-pair assertion approach explicitly beat the global tool.
- Do not modify `data/*.json` shape — that's strand A's territory and would conflict.

## Memories that apply

- `feedback_shared_tree_branch_verification.md`
- `feedback_multi_strand_session_checkpoints.md`
- `feedback_bash_nvm_sourcing.md`, `feedback_env_check.md`, `feedback_pr_polling.md`, `feedback_issues_describe_problems.md`

## Stop when

- #474 PR is merged into main.
- At least one new assertion landed (matching the assertion shape from PR #448).
- Each new assertion demonstrated red-green against a temporary source mutation that was reverted.
- Worktree removed.
