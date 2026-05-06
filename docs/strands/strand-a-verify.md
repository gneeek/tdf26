# Strand A — Content quality: segs 11-13 data verification (v1.4.18)

**Start here:** [Roadmap → Next → v1.4.18](https://github.com/gneeek/tdf26/wiki/Roadmap#next), then [#477](https://github.com/gneeek/tdf26/issues/477).

## Goal

Complete data verification for segments 11-13 (km 70-92, Naves through Chaumeil) before any seg 11 prose drafting starts. Mirror the seg 9+10 verification (#434 → PR #470) shape: per-claim audit, citations, outcomes documented in the PR body. This is the load-bearing time-sensitive item for v1.4.18 — seg 11 publishes Sun 2026-05-10.

Goal 2 (content quality). Commit-tier.

## Filesystem posture

**Worktree.** Run in a separate worktree. Symlink the agent config from main; copy (do not symlink) the gitignored rider data files because the publish session running in parallel today writes to them.

```
cd /home/jhs/code
git worktree add tdf26-seg11-verify main
cd tdf26-seg11-verify
ln -s ../tdf26/.claude .claude
source ~/.nvm/nvm.sh && nvm use --silent
npm ci
cp ../tdf26/data/riders/daily-log.json data/riders/
cp ../tdf26/data/riders/points.json data/riders/
cp ../tdf26/data/riders/stats.json data/riders/
[ -d ../tdf26/data/riders/snapshots ] && cp -r ../tdf26/data/riders/snapshots data/riders/
npx nuxt prepare
```

When the strand finishes: `git worktree remove tdf26-seg11-verify` from the main checkout.

Branch: `feature/issue-477-segs-11-13-verification`. Verify `git branch --show-current` immediately before each `git add` / `git commit`.

## Target issue

- **[#477](https://github.com/gneeek/tdf26/issues/477)** — Data verification: segments 11-13 (km 70-92, Naves through Chaumeil)

Single issue, single PR.

## Workflow

Per-segment audit for segments 11, 12, 13 (in order):

1. **GPX polyline integrity.** Read `data/segments/segment-NN.gpx`. Confirm continuous polyline, no gaps, total km matches `data/segments.json` `km_start`/`km_end`. Use polyline (not endpoints) for all proximity checks per `feedback_on_route_checks.md`.
2. **km markers.** Confirm segment boundaries match cumulative distance from `data/master.gpx`.
3. **Climb summit positions.** Côte des Naves (~km 76.6 per CLAUDE.md), Puy de Lachaud. Verify summit lat/lng against IGN/OSM; verify km position against the segment polyline.
4. **`segments.json` notable_points/towns/climbs.** Each entry verified against CLAUDE.md canon and IGN/OSM. Each correction documented in PR body.
5. **`data/attractions.json`.** Each attraction in segs 11-13 verified for proximity (use polyline), category accuracy, and `infoUrl` validity.
6. **`data/historical-tdf.json`.** Existing entries verified. **NEW research required** for seg 13: 1987 TdF men's Stage 11 + women's Tour Stage 3, both finished at Chaumeil. Source: `https://cyclingflash.com/location/chaumeil`. Add entries keyed to seg 13 with stage number, date, departure point, winner(s), route distance, jersey context. Cite each fact.
7. **Elevation profile data.** `data/elevation/segment-NN.json` smoothness, gradient calculations match.

**Carryforward content cues** — document explicitly in PR body:
- **Tintignac** (Gallo-Roman sanctuary, Naves commune) → seg 11 regional content NOT a `data/attractions.json` entry. Document this no-add explicitly so future drafters don't re-discover it.
- **Auzelou stadium / Stade Alexandre-Cueille** at lat 45.27801 / lng 1.78261 = km 70.93 in seg 11. Add to `data/attractions.json` with cross-link to seg 10's L'Agglomérée mention. Cross-segment caveat: stadium is correctly seg 11 even though seg 10 prose mentions the area.

## Checkpoints with publisher (AskUserQuestion)

This strand is research- and judgment-heavy. Use `AskUserQuestion` at each of these moments rather than guessing — the publisher would rather decide than have you assume:

- **After initial per-segment research, before drafting any changes:** present the per-segment finding summary as one AskUserQuestion. Options: (a) accept all proposed changes, (b) flag specific items for further research, (c) override specific items.
- **For 1987 Chaumeil research:** when winners + route departures + jersey context are gathered, AskUserQuestion: "What detail level for historical-tdf.json — minimal (winners + dates), medium (+ context), or full (+ narrative)?" Seg 13 prose hasn't been drafted yet, so the data shape should match what seg 13 will pull.
- **If any verification finds material disagreement with current data** (more than minor coordinate corrections — e.g. a town placement off by km, wrong climb category, wrong attraction category): AskUserQuestion before changing. Material changes affect rendering.
- **Auzelou stadium attraction entry:** before adding, AskUserQuestion on category (sport / landmark / other) and `infoUrl` choice (lagglomeree.agglo-tulle.fr official cyclosportive page vs. Wikipedia vs. none).
- **Before opening PR:** AskUserQuestion to confirm the audit-trail PR body covers everything verified (no silent skips), the carryforward cues are documented, milestone v1.4.18 assignment is correct.

If the publisher session is unavailable (away, in another session) and a checkpoint blocks: stop, write what you've found to a `WORK-LOG.md` in the worktree root, exit cleanly. Do not guess past a checkpoint.

## Verification commands

- `source ~/.nvm/nvm.sh && nvm use --silent && npm test && npm run build`
- `npm run preview` after build — confirm the seg 11/12/13 entries (placeholder content, but data renders) display the updated data
- `processing/.venv/bin/python processing/validate_entries.py`
- `processing/.venv/bin/python processing/audit_segment_data.py` — existing audit script; cross-check its output against your manual audit

## Cross-strand sharing notes

- **Strand B** (#474, per-source-of-truth assertions) writes to `tests/utils/`, reads `data/*.json`. **No write overlap.** If B lands first with new assertions, this strand's data corrections must satisfy them — read the assertion test names visible in `tests/utils/` before changing data.
- **Strand C** (#475, JSON Schema validation) writes new `schemas/` directory and validation wiring, reads `data/*.json`. **No write overlap.** If C lands first with strict schemas, this strand's data corrections must validate; if C's schemas reject what should be correct, file a follow-up issue, do not edit C's PR.
- **Publish session for seg 10 (parallel today)** writes to `data/riders/*.json` and the seg 10 entry. **No overlap with this strand.** Do not pull mid-strand if avoidable.
- This strand owns `data/segments.json`, `data/attractions.json`, `data/historical-tdf.json` writes for v1.4.18.

## Scope discipline

- One issue, one PR.
- File new issues for any data-correctness findings outside segs 11-13. Do not fix inline.
- File new issues for process improvements (e.g. "audit_segment_data.py needs a --segment flag"). Do not fix inline.
- Do not modify `processing/` validators or audit scripts to make them more useful — that's #475's territory.

## Memories that apply

- `feedback_on_route_checks.md` (use polyline not endpoints)
- `feedback_pre_publish_scrutiny.md`
- `feedback_content_change_rule.md` (the verification IS the prevention of retroactive edits)
- `feedback_shared_tree_branch_verification.md`
- `feedback_multi_strand_session_checkpoints.md` (this strand's whole structure embodies the checkpoint discipline)
- `feedback_bash_nvm_sourcing.md`, `feedback_env_check.md`, `feedback_pr_polling.md`, `feedback_issues_describe_problems.md`

## Stop when

- #477 PR is merged into main.
- Per-claim audit row format from PR #470 reproduced in PR body.
- Tintignac no-add documented in PR body.
- Auzelou stadium added to `data/attractions.json` (or alternative landing decided with publisher).
- 1987 Chaumeil men's + women's stages added to `data/historical-tdf.json` keyed to seg 13.
- Worktree removed.
