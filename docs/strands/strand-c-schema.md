# Strand C — Developer experience: JSON Schema validation for data/*.json (v1.4.18)

**Start here:** [Roadmap → Next → v1.4.18](https://github.com/gneeek/tdf26/wiki/Roadmap#next), then [#475](https://github.com/gneeek/tdf26/issues/475).

## Goal

Author JSON Schema (or equivalent shape contract) for each `data/*.json` file and wire validation into a canonical run path. Catches shape drift — missing required fields, type changes, accidental field renames — that per-source assertions don't see.

Goal 4 (developer experience). Commit-tier — sister to strands A (verification) and B (per-source assertions) in the v1.4.18 data-layer regime.

## Filesystem posture

**Worktree.** Run in a separate worktree.

```
cd /home/jhs/code
git worktree add tdf26-schema main
cd tdf26-schema
ln -s ../tdf26/.claude .claude
source ~/.nvm/nvm.sh && nvm use --silent
npm ci
cp ../tdf26/data/riders/daily-log.json data/riders/
cp ../tdf26/data/riders/points.json data/riders/
cp ../tdf26/data/riders/stats.json data/riders/
[ -d ../tdf26/data/riders/snapshots ] && cp -r ../tdf26/data/riders/snapshots data/riders/
npx nuxt prepare
```

When the strand finishes: `git worktree remove tdf26-schema` from the main checkout.

Branch: `feature/issue-475-json-schema-validation`. Verify `git branch --show-current` immediately before each `git add` / `git commit`.

## Target issue

- **[#475](https://github.com/gneeek/tdf26/issues/475)** — `data/*.json` files have no shape contract enforced at build time

## Workflow

1. **Library survey.** Candidates to evaluate:
   - **AJV** (JS, JSON Schema-native, fastest, schemas are JSON files)
   - **zod** (TypeScript-native, schemas are TS code, can generate JSON Schema)
   - **Python jsonschema** (the data pipeline is already Python; schemas could live in `processing/`)
   - **JSON Schema CLI** + npm script (lightest dependency footprint)
   Consider: runtime cost (build-time only is fine), schema authoring ergonomics, where validation should live (Node test, Node build, Python pipeline, pre-commit), and what already exists in the project's dependency tree.
2. **Checkpoint with publisher** on library + integration point (see Checkpoints).
3. **Author schemas.** One schema per `data/*.json` file. Files in scope (verify against current `ls data/*.json data/**/*.json`):
   - `data/segments.json`
   - `data/attractions.json`
   - `data/historical-tdf.json`
   - `data/competition/points-config.json`
   - `data/riders/rider-config.json`
   - others as discovered
   Start permissive (validate current data). Tighten iteratively only if straightforward.
4. **Wire validation** into the chosen integration point.
5. **Confirm** all current `data/*.json` files validate clean.
6. **Demonstrate the schema catches a shape error** — temporarily mutate one file (rename a required field), run validator, confirm fail, revert.
7. **Open PR**, milestone v1.4.18.

## Checkpoints with publisher (AskUserQuestion)

- **After library survey:** present the shortlist with tradeoffs (JS-side vs Python-side, runtime, ergonomics, dependency weight). AskUserQuestion: "Which library?" with the shortlist as options.
- **After library choice:** AskUserQuestion on integration point. Options: (a) `npm test` step (vitest assertion per file), (b) `npm run build` step (fails build on invalid data), (c) pre-commit hook, (d) standalone `npm run validate-data` invoked by `publish.sh`.
- **For schemas with ambiguous fields** (optional vs required, type strictness, enum values where the current data is permissive): AskUserQuestion before committing the schema. For obvious cases just author and proceed.
- **Before opening PR:** AskUserQuestion to confirm the validation command name (matches project's npm-script naming) and where it gets invoked.

If the publisher session is unavailable and a checkpoint blocks: stop, write what you've found to a `WORK-LOG.md` in the worktree root, exit cleanly. Do not guess past a checkpoint.

## Verification commands

- `source ~/.nvm/nvm.sh && nvm use --silent && npm test && npm run build`
- The new validation command (whatever it ends up named) must run clean against all current `data/*.json`.
- Schema-fail demonstration: temporarily mutate a `data/*.json` (e.g. rename a required field), run validator, confirm fail. Revert before staging.

## Cross-strand sharing notes

- **Strand A** (#477) writes to `data/*.json`. **No write overlap with this strand's files.** If this strand's schemas land first with strict constraints, A's data corrections must validate. To minimise friction: this strand's first-pass schemas should be permissive enough that current data validates without surgery. If A's corrections trip a schema, that's a real signal — coordinate.
- **Strand B** (#474) writes to `tests/utils/`. **No overlap with this strand.** Different validation surfaces; both coexist.
- **Publish session for seg 10 (parallel today)** writes to `data/riders/*.json`. If this strand's schemas cover rider-side files: they must permit the publish-day write shape (ratings updated, dates updated, possibly new entries). Read `processing/rider_stats.py` to understand the publish-time write shape before authoring those schemas. If unsure, defer rider-side schemas to a follow-up issue.
- This strand owns the new `schemas/` directory (or equivalent location) and the validation runner.

## Scope discipline

- One issue, one PR.
- **Do not** refactor `data/*.json` shapes to suit the schema — schema fits the data, not the other way around. File follow-up issues if shape problems surface.
- **Defer** [#476](https://github.com/gneeek/tdf26/issues/476) (segment-pinning audit-trail metadata) — sister issue, but needs its own design conversation.
- Do not touch `processing/validate_entries.py` (existing validator) — out of scope; consolidation is #326.

## Memories that apply

- `feedback_shared_tree_branch_verification.md`
- `feedback_multi_strand_session_checkpoints.md`
- `feedback_bash_nvm_sourcing.md`, `feedback_env_check.md`, `feedback_pr_polling.md`, `feedback_issues_describe_problems.md`

## Stop when

- #475 PR is merged into main.
- All current `data/*.json` files validate against their schemas.
- Validation runs from at least one canonical path (build / test / publish / pre-commit).
- Schema-fail demonstrated (and reverted) for at least one file.
- Worktree removed.
