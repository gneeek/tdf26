# Strand: Verify segs 20-22 (#499)

Data-verification strand. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Audit `data/*.json` against `data/segments/segment-{20,21,22}.gpx` and authoritative external sources for the segs 20–22 block (km ~128–150: Bugeat, the Plateau de Millevaches heart, Mont Bessou — the highest point in Corrèze at 977m). Closes [#499](https://github.com/gneeek/tdf26/issues/499). Milestone: [v1.4.20](https://github.com/gneeek/tdf26/milestone/20) (subject to renumbering per Topic 9a). Spawn timing: ~5 weeks from 2026-05-07 (publisher discretion). Mirrors PR #470, #489, #514.

Special note: per PR #514, the 2024 Tour de France Stage 11 reference was re-keyed from segs 14-16 to **seg 22** (Mont Bessou as the highest-altitude parallel for that stage's Puy Mary climb). This strand should verify the keying held and the description still reads cleanly post-correction.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-499-segs-20-22-verify /home/jhs/code/tdf26-499 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-{20,21,22}.gpx` directly. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`). External sources: OSM, Wikipédia, Mérimée, Tourisme Corrèze, Parc naturel régional de Millevaches website, regional press. Per `feedback_brief_content_is_carryforward.md`: facts cited in this brief are scaffolding; verify against authoritative sources.

## 4. Target issues

- [#499](https://github.com/gneeek/tdf26/issues/499) — data verification segs 20-22. Closes when the audit ships and any data corrections land.

## 5. Workflow per issue

Per-claim audit pass:

1. **GPX polyline integrity** for segs 20, 21, 22 — files read cleanly; km markers in `data/segments.json` match GPX cumulative distance.
2. **Town keying** — `Bugeat` (currently keyed to seg 21 per existing data; verify against polyline). Confirm other towns transited.
3. **Climb keying** — Mont Bessou (5.0 km @ 2.7% per current points-config post-#516; summit at 977m, the highest point in Corrèze; ASO-categorised per #492 outcome). Verify summit km against GPX local maximum; verify the per-source-of-truth gradient assertion at `tests/utils/climb-gradient.test.ts` still passes.
4. **`data/attractions.json`** — proximity, category, sources. Plateau de Millevaches has sparse classical-attraction density (the Parc itself is the attraction); use the "verified empty" finding pattern where appropriate.
5. **`data/historical-tdf.json`** — verify the 2024 Stage 11 entry (re-keyed to seg 22 by PR #514) still reads cleanly; surface any other corridor-relevant events.
6. **2024 Stage 11 keying check** — the Mont Bessou / Puy Mary parallel is the rationale; confirm the description in `data/historical-tdf.json` still fits and no detail belongs back at segs 14-16.
7. **AskUserQuestion at material disagreements**.
8. **Audit summary** — per-claim table in PR body.
9. **PR open against `main`** — title `data: seg 20-22 verification (closes #499)`; closes #499.

## 6. Verification commands

```bash
npm test                                                                       # all tests pass
python3 processing/validate_points.py                                          # OK
python3 processing/validate_entries.py --entries-dir content/entries --non-interactive   # OK
python3 processing/audit_segment_data.py --segment 20                          # clean
python3 processing/audit_segment_data.py --segment 21                          # clean
python3 processing/audit_segment_data.py --segment 22                          # clean
npm run build                                                                  # complete
```

Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `data/attractions.json` (segs 20-22), `data/segments.json` (towns / notable_points segs 20-22), `data/town-coords.json` (any new towns), `data/historical-tdf.json` (events keyed to segs 20-22), `data/town-positions.ts`. PR-body audit summary.
- **What this strand reads:** `data/competition/points-config.json` (read-only); `data/segments/segment-{20,21,22}.gpx`; `data/elevation/segment-{20,21,22}.json`; CLAUDE.md narrative.
- **What this strand must NOT touch:** `content/entries/*.md`; `data/competition/points-config.json` (only climb-data strands write here); STRAND-BRIEF-TEMPLATE.md; segs 17-19 / 23-26 verification work (separate strands).
- **Cross-strand collisions:** if #498 (segs 17-19) is merged before this spawns, no overlap. If #500 (segs 23-26) is in flight concurrently, neither writes overlapping km ranges; flag in PR body for awareness.

## 8. Scope discipline

- Default: file new issues for findings outside owned write-set.
- AskUserQuestion at material-disagreement points only.
- Document publisher-approved scope overrides in PR body.
- Use the "verified empty" vs "unaudited absence" distinction in audit tables.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_on_route_checks.md`
- `feedback_multi_strand_session_checkpoints.md`
- `feedback_pre_publish_scrutiny.md` (segs 20-22 publish ~mid-June 2026)
- `feedback_brief_content_is_carryforward.md`
- `feedback_parallel_source_of_truth_detector.md`
- `feedback_assertion_bug_class.md`

## 10. Stop when

- Per-claim audit table complete for segs 20, 21, 22.
- Any data corrections landed; cross-strand follow-ups filed.
- `npm test` + validators + audit script all clean for segs 20-22.
- PR opened, reviewed, merged.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-499` once the work has merged.
- Final report posted to publisher: PR link, audit table summary, any open questions surfaced for downstream drafting strands.
