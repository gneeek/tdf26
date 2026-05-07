# Strand: Verify segs 23-26 (#500)

Data-verification strand. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Audit `data/*.json` against `data/segments/segment-{23,24,25,26}.gpx` and authoritative external sources for the segs 23–26 block (km ~150–185: Meymac, Côte des Gardes, Ussel — the stage-9 finish at Place Voltaire). Closes [#500](https://github.com/gneeek/tdf26/issues/500). Milestone: [v1.4.20](https://github.com/gneeek/tdf26/milestone/20) (subject to renumbering per Topic 9a). Spawn timing: ~6 weeks from 2026-05-07 (publisher discretion). Mirrors PR #470, #489, #514.

**Special checks for this strand:**

- **Mascaron / Saintsbury voice scheduling.** Per `project_meymac_voice.md` and the planning-notes carryforward, Meymac's saintsbury voice may need to shift from seg 24 to seg 25 depending on which segment actually anchors the abbey (Abbaye Saint-André, founded 1085). This audit decides. Update `project_meymac_voice.md` accordingly when the answer lands.
- **`historical-tdf.json` segments [25, 26, 27] grouping.** The route only has 26 segments per `data/segments.json`; the [25, 26, 27] keying in `data/historical-tdf.json` references a non-existent seg 27. Pre-existing finding flagged in PR #514's "out of scope" notes (#503 tracks). This strand should fix or surface as needed.
- **Paris-Corrèze keying.** Per the #502 tour-history strand Session 1 dossier, the existing Paris-Corrèze entry is mis-keyed to segs [25, 26, 27] but every documented year (2005–2012) finished at **Chaumeil (seg 15)** and 2009 specifically went **Tulle (seg 10) → Chaumeil (seg 15)**. The keying needs correction; do this strand or close as fixed elsewhere if the tour-history strand handled it first.
- **Ussel finish geometry.** Place Voltaire is the sprint judge; Avenue Thiers is the run-in. Verify that the polyline passes through both and that town-coords / segments.json reflect the finish accurately.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-500-segs-23-26-verify /home/jhs/code/tdf26-500 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-{23,24,25,26}.gpx` directly. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`). External sources: OSM, Wikipédia, Mérimée, Tourisme Corrèze, Tourisme Egletons, Meymac abbey site, Ussel municipal site, regional press. Per `feedback_brief_content_is_carryforward.md`: facts cited in this brief are scaffolding; verify against authoritative sources.

This strand sits at the end of the route — sources for Ussel and Meymac are richer than for the Plateau de Millevaches block, so the audit table should be denser on attractions, sparser on the "verified empty" pattern.

## 4. Target issues

- [#500](https://github.com/gneeek/tdf26/issues/500) — data verification segs 23-26. Closes when the audit ships and corrections land.
- [#503](https://github.com/gneeek/tdf26/issues/503) — `historical-tdf.json` segment-27 drift. Likely closes alongside this strand if the segments [25, 26, 27] keying gets fixed here.

## 5. Workflow per issue

Per-claim audit pass:

1. **GPX polyline integrity** for segs 23, 24, 25, 26 — files read cleanly; km markers match GPX cumulative.
2. **Town keying** — `Meymac` (currently seg 24 per existing data; verify polyline; the abbey is the anchor), `Ussel` (segs 25-26; verify finish-line km against the actual stage-9 finish coords; `data/town-coords.json` already has a `note` field for towns whose centre sits off the polyline). Confirm any other transited towns.
3. **Climb keying** — Côte des Gardes (currently seg 24 in points-config: 2.2 km @ 4.3%; verify summit km against GPX). Per `feedback_assertion_bug_class.md`, also sanity-check the gradient assertion at `tests/utils/climb-gradient.test.ts` still passes for this climb.
4. **Meymac abbey segment keying** — does the Abbaye Saint-André sit in seg 23 or seg 24? The medieval town centre vs the route polyline determines voice scheduling per `project_meymac_voice.md`. Decide and update the memory.
5. **`data/attractions.json`** — Meymac abbey, the Centre d'Art Contemporain, Ussel medieval town, Place Voltaire. Verify proximity, category, source URLs.
6. **`data/historical-tdf.json` cleanup** — fix the [25, 26, 27] grouping to reference only existing segments. Re-key or remove the Paris-Corrèze entry per the #502 dossier finding (was finishing at Chaumeil seg 15, not Ussel). Surface any other corridor-relevant events.
7. **AskUserQuestion at material disagreements** — expect 2-3 such checkpoints (this strand has more contested facts than mid-route blocks).
8. **Audit summary** — per-claim table in PR body.
9. **PR open against `main`** — title `data: seg 23-26 verification (closes #500)`; closes #500 (and #503 if folded in).

## 6. Verification commands

```bash
npm test                                                                       # all tests pass
python3 processing/validate_points.py                                          # OK
python3 processing/validate_entries.py --entries-dir content/entries --non-interactive   # OK
python3 processing/audit_segment_data.py --segment 23                          # clean
python3 processing/audit_segment_data.py --segment 24                          # clean
python3 processing/audit_segment_data.py --segment 25                          # clean
python3 processing/audit_segment_data.py --segment 26                          # clean
npm run build                                                                  # complete
```

Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `data/attractions.json` (segs 23-26), `data/segments.json` (towns / notable_points), `data/town-coords.json` (any new towns added), `data/historical-tdf.json` (segs 23-26 events; segments [25, 26, 27] cleanup; Paris-Corrèze re-keying), `data/town-positions.ts`. Possibly `project_meymac_voice.md` (memory edit, depends on seg 24 vs 25 finding). PR-body audit summary.
- **What this strand reads:** `data/competition/points-config.json` (read-only); `data/segments/segment-{23,24,25,26}.gpx`; `data/elevation/segment-{23,24,25,26}.json`; CLAUDE.md narrative; `content/research/tour-history-research.md` (committed via the #502 tour-history strand) for the Paris-Corrèze re-keying context.
- **What this strand must NOT touch:** `content/entries/*.md`; `data/competition/points-config.json` (only climb-data strands write); STRAND-BRIEF-TEMPLATE.md; segs 17-19 / 20-22 verification work.
- **Cross-strand collisions:** if the #502 tour-history strand has already corrected the Paris-Corrèze entry, this strand reads but doesn't re-touch it. Coordinate via PR body / issue comments if both strands are in flight.

## 8. Scope discipline

- Default: file new issues for findings outside owned write-set.
- AskUserQuestion at material-disagreement points only.
- Document publisher-approved scope overrides in PR body.
- The Mascaron / Saintsbury voice question is a memory edit, not a code edit — do not touch any voice-skill files in this strand.
- Use the audit-table distinction between "verified empty" and "unaudited absence."

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_on_route_checks.md`
- `feedback_multi_strand_session_checkpoints.md`
- `feedback_pre_publish_scrutiny.md` (segs 23-26 publish ~late June / early July 2026 — close to the actual stage 9 day)
- `feedback_brief_content_is_carryforward.md`
- `feedback_parallel_source_of_truth_detector.md`
- `feedback_assertion_bug_class.md`
- `project_meymac_voice.md` (this strand decides seg 24 vs seg 25 and updates the memory)

## 10. Stop when

- Per-claim audit table complete for segs 23, 24, 25, 26.
- Mascaron / Saintsbury voice scheduling decided; `project_meymac_voice.md` updated.
- `historical-tdf.json` [25, 26, 27] keying fixed; Paris-Corrèze entry corrected or confirmed correct.
- Any other data corrections landed; cross-strand follow-ups filed.
- `npm test` + validators + audit script all clean for segs 23-26.
- PR opened, reviewed, merged. #500 closes; #503 closes if folded in.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-500` once the work has merged.
- Final report posted to publisher: PR link, audit table summary, voice scheduling outcome, Paris-Corrèze re-keying outcome, any open questions surfaced for downstream drafting strands (Meymac and Ussel drafters will consume).
