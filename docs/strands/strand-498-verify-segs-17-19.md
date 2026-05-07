# Strand: Verify segs 17-19 (#498)

Data-verification strand. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Audit `data/*.json` against `data/segments/segment-{17,18,19}.gpx` and authoritative external sources for the segs 17–19 block (km ~112–128: Treignac, Côte de la Croix de Pey, the Plateau de Millevaches gateway). Closes [#498](https://github.com/gneeek/tdf26/issues/498). Milestone: [v1.4.20](https://github.com/gneeek/tdf26/milestone/20) (subject to renumbering per Topic 9a). Spawn timing: ~3 weeks from 2026-05-07 (publisher discretion). Mirrors PR #470 (segs 9-10), #489 (segs 11-13), #514 (segs 14-16).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-498-segs-17-19-verify /home/jhs/code/tdf26-498 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-{17,18,19}.gpx` directly. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`). External sources: OSM, Wikipédia (FR/EN), Mérimée database, Tourisme Corrèze, regional press archives. Per `feedback_brief_content_is_carryforward.md`: facts cited in this brief are scaffolding; verify against authoritative sources before using.

## 4. Target issues

- [#498](https://github.com/gneeek/tdf26/issues/498) — data verification segs 17-19. Closes when the audit ships and any data corrections land.

## 5. Workflow per issue

Per-claim audit pass (pattern established by PRs #470, #489, #514):

1. **GPX polyline integrity** for segs 17, 18, 19 — `data/segments/segment-NN.gpx` reads cleanly; km markers in `data/segments.json` match GPX cumulative distance.
2. **Town keying** — `Treignac` (currently keyed to seg 18 per existing data; verify against polyline; the medieval bridge / granite town is the seg 18 anchor). Confirm any other towns the route transits or passes near in segs 17-19.
3. **Climb keying** — Côte de la Croix de Pey (7.0 km @ 4.4% per current points-config; verify summit km against GPX local maximum and gradient against per-source detector pattern at `tests/utils/climb-gradient.test.ts`). Any other climbs in segs 17-19 currently in points-config.
4. **`data/attractions.json`** — proximity (≤5 km from polyline), category, source URL, infoUrl. Treignac's medieval bridge is the obvious candidate; the Plateau de Millevaches gateway has fewer landmarks and may surface the "verified empty" finding pattern (per `feedback_pre_publish_scrutiny.md` audit-table format).
5. **`data/historical-tdf.json`** — verify any events keyed to segs 17-19 are correct; surface any corridor-relevant events not yet keyed.
6. **AskUserQuestion at material disagreements** — expect 1-2 such checkpoints (per `feedback_multi_strand_session_checkpoints.md`).
7. **Audit summary** — per-claim table in PR body listing source, current value, audit finding, action.
8. **PR open against `main`** — title `data: seg 17-19 verification (closes #498)`; closes #498.

## 6. Verification commands

```bash
npm test                                                                       # all tests pass
python3 processing/validate_points.py                                          # OK
python3 processing/validate_entries.py --entries-dir content/entries --non-interactive   # OK
python3 processing/audit_segment_data.py --segment 17                          # clean
python3 processing/audit_segment_data.py --segment 18                          # clean
python3 processing/audit_segment_data.py --segment 19                          # clean
npm run build                                                                  # complete
```

Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `data/attractions.json` (additions / corrections for segs 17-19), `data/segments.json` (towns / notable_points for segs 17-19), `data/town-coords.json` (any new towns added), `data/historical-tdf.json` (additions / re-keyings keyed to segs 17-19), `data/town-positions.ts` (mirror of any town additions). PR-body audit summary.
- **What this strand reads:** `data/competition/points-config.json` (read-only; climb metadata is canonical there per #516); `data/segments/segment-{17,18,19}.gpx`; `data/elevation/segment-{17,18,19}.json`; CLAUDE.md narrative project context (not deprecated tabular data).
- **What this strand must NOT touch:** `content/entries/*.md` (separate drafting strands); `data/competition/points-config.json` (only climb-data strands write here); STRAND-BRIEF-TEMPLATE.md.
- **Cross-strand collisions:** none expected. Drafting strands for segs 12-13 work on different file regions; the seg 17 drafting strand (when it spawns) reads this strand's outputs.

## 8. Scope discipline

- Default: file new issues for findings outside the strand's owned write-set (e.g., a points-config drift discovered while reading; a CLAUDE.md narrative inaccuracy).
- AskUserQuestion at material-disagreement points only.
- Document publisher-approved scope overrides in the PR body.
- Use the audit-table distinction between "verified empty" and "unaudited absence" (per the seg 14-16 strand's pattern observation about Plateau de Millevaches sparseness).

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_on_route_checks.md`
- `feedback_multi_strand_session_checkpoints.md`
- `feedback_pre_publish_scrutiny.md` (segs 17-19 publish ~late May / early June 2026)
- `feedback_brief_content_is_carryforward.md`
- `feedback_parallel_source_of_truth_detector.md` (cross-source assertions are the bug-class-fix pattern; flag drift discovered in audit)
- `feedback_assertion_bug_class.md` (any new assertion needs hand-computed diagnostic)

## 10. Stop when

- Per-claim audit table complete in PR body for segs 17, 18, 19.
- Any data corrections landed; any cross-strand follow-ups filed (e.g., points-config drift → file separate issue).
- `npm test` + validators + audit script all clean for segs 17-19.
- PR opened, reviewed, merged.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-498` once the work has merged.
- Final report posted to publisher: PR link, audit table summary, any open questions surfaced for downstream drafting strands (segs 17, 18, 19 drafters will consume).
