# Strand I — Data verification: segments 14-16 (km 92-112)

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md). Closes [#478](https://github.com/gneeek/tdf26/issues/478).

## 1. Goal

Verify the data layer (route geometry, town/attraction positions, climb data, historical-tdf entries) for segments 14, 15, 16 — covering km 92-112, the Monédières heath through the Suc au May summit. Output is a single PR landing audit-row corrections plus a per-claim audit table in the PR body, mirroring PR #470 (segs 9-10) and PR #489 (segs 11-13).

Verification must land before seg 14 drafting starts. Seg 14 publishes Wed 2026-05-20 per twice-weekly cadence. Milestone v1.4.19.

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-478-segs-14-16-verify /home/jhs/code/tdf26-verify-14-16 main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

- Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/points-config.json`, `data/historical-tdf.json`, `data/segments/segment-14.gpx` / `segment-15.gpx` / `segment-16.gpx` directly.
- **Do NOT use CLAUDE.md's known-waypoints km positions as canon.** That table has confirmed staleness per [#491](https://github.com/gneeek/tdf26/issues/491) — segs 17-26 issue-filing today (2026-05-07) surfaced fresh evidence: Bugeat ~12 km drift, Meymac ~13 km drift, Ussel not tagged, total km 182 vs 185. Treat CLAUDE.md narrative project context as fine; treat its tabular data as drift-prone.
- Use polylines (not segment endpoints) for proximity checks per `feedback_on_route_checks.md`.
- The `validate_points.py` spanning-climb invariant (`Suc au May` and any other multi-segment climb must appear in every segment whose km range overlaps the climb span) is enforced. Run it.

## 4. Target issues

- **Closes [#478](https://github.com/gneeek/tdf26/issues/478)** — single tracking issue, milestone v1.4.19.
- Findings outside the audit's owned write-set (e.g., points-config gradient drift in seg 14-16 corridor) → file new issues, do not fix inline.

## 5. Workflow per issue

The verification follows the audit-script + manual-cross-check pattern (3rd worked instance: PR #470, PR #489, this PR).

1. **Mechanical pass:** run `python3 processing/audit_segment_data.py --segments 14,15,16` (or equivalent flag — verify the script's CLI; if no segment-filter flag exists, run full and grep). Capture output.
2. **Manual elevation-profile pass:** read `data/elevation/segment-14.json` / `segment-15.json` / `segment-16.json`. Cross-check Suc au May summit position (~km 105, elevation 903m, 3.8km at 7.7% per CLAUDE.md content notes — verify against actual elevation data, not the table).
3. **Manual polyline pass:** for every town in `data/segments.json`'s towns list and every attraction in `data/attractions.json` for segs 14-16, confirm position against the segment GPX polyline.
4. **Cross-source check:** `data/historical-tdf.json` for any Suc au May / Monédières TdF history. Verify 2024 Stage 11 Vingegaard/Pogačar adjacency keying (per CLAUDE.md it's segs 14-16 terrain — this is one of the keying claims to confirm).
5. **Build per-claim audit table** in the PR body, same shape as PR #489: claim, source, current value, audit finding, action.
6. **Apply corrections** to the data files; do not change the elevation source data without comment.
7. **Use AskUserQuestion at material disagreements** — the seg 11-13 strand surfaced override calls (Tintignac, 1987 Chaumeil seg keying); expect 1-2 such checkpoints in this strand.

## 6. Verification commands

- `npm test` — must pass.
- `python3 processing/validate_points.py` — must pass; runs the spanning-climb invariant.
- `python3 scripts/validate_entries.py` — defensive (no entry frontmatter touched, but verifies nothing leaked).
- `python3 processing/audit_segment_data.py` — the mechanical pass; output drives the audit table.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `data/segments.json` (segs 14, 15, 16 entries only)
  - `data/attractions.json` (only attraction entries with km in 92-112 range)
  - `data/historical-tdf.json` (additions / corrections for the segs 14-16 corridor — 1987 Chaumeil men's + women's TdF entries keyed to **seg 15** per #478 deferral comment from PR #489)
  - PR body audit table
- **What this strand reads:**
  - All `data/*` for cross-reference
  - `content/research/segs-11-13-block-research.md` if Strand D has landed (for any cross-segment notes flagged for segs 14-16)
  - `data/elevation/segment-14.json` / `15.json` / `16.json`
  - `data/segments/segment-14.gpx` / `15.gpx` / `16.gpx`
  - CLAUDE.md *narrative* sections only (not the known-waypoints table).
- **What this strand must NOT touch:**
  - `data/segments.json` outside segs 14-16 (#491 / #498 / #499 / #500 own those).
  - `data/points-config.json` (per-source assertions are Strand B's territory; if drift surfaces here in seg 14-16 climbs, file a new issue).
  - `content/entries/14-*.md` / `15-*.md` / `16-*.md` (drafting strands own these; do not touch beyond verifying frontmatter is internally consistent).
  - CLAUDE.md (the staleness fix is #491's job).
- **Cross-strand collisions:** Strand D content research touches `content/research/`, no overlap. Strand E/F/G drafting strands haven't been spawned. If any sibling strand modifies `data/historical-tdf.json` mid-flight (unlikely), rebase and resolve by additive merge.

## 8. Scope discipline

- **Findings outside scope go to new issues, not inline fixes.** Examples expected: points-config gradient drift in seg 14-16 climbs (sister to #490); CLAUDE.md known-waypoints km drift confirmation (joins #491); attraction proximity outliers.
- Override decisions (e.g., publisher chooses to keep an attraction the audit would deprecate) get an AskUserQuestion checkpoint with documented reasoning in PR body.
- Do not poach segs 17+ content (Treignac, Plateau de Millevaches, Mont Bessou, Meymac, Ussel) — those belong to #498 / #499 / #500.
- Do not draft prose for any segment in this strand. Prose is the drafting strand's job.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_on_route_checks.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`
- `feedback_content_change_rule.md`
- `feedback_pre_publish_scrutiny.md`
- `project_meymac_voice.md` (seg 24 reservation; not these segs but informs surrounding planning — and #500 flagged that Meymac may actually be in seg 25 not 24, so the voice plan could shift; do not act on that here)
- `project_barthes_callback.md` (seg 6/12/15 arc — seg 15 is the "develops" beat; the verification surfaces but does not consume Sainte-Fortunade / Monédières framing)

## 10. Stop when

- PR open against milestone v1.4.19 closing #478.
- Per-claim audit table in PR body.
- All verification commands green.
- 1987 Chaumeil men's + women's TdF entries added to `data/historical-tdf.json` keyed to **seg 15** (NOT seg 13 — CLAUDE.md staleness corrected at PR #489 time, captured in #478).
- Any new findings filed as separate issues with sister-issue cross-links.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-verify-14-16` once the PR has merged.
- Final report posted to publisher: PR link, audit-table summary, any open questions surfaced for the segs 14-16 drafting strands (which spawn after seg 13 drafting completes).

## Carryforwards reserved for downstream drafting strands

These belong to drafting, not verification — capture in the audit table for awareness but do **not** consume them in this strand:

- **Sainte-Fortunade / Monédières framing** (Léon Dautrement: "un morceau de Monédières perdu dans le bas Limousin"; cherry microclimate near Château de la Morguie ripens 15 days earlier than southern reaches). Drafter chooses placement among segs 14/15/16.
- **Bourrée des Monédières** / *Boreïa de las botelhas* (1950, René Lafeuille) — music thread for seg 14 or 15.
- **Suc au May** as the Monédières summit (~km 105, 903m, 3.8km at 7.7%) — marquee climb of the segment block, content peak for seg 15 prose.
- **2024 Stage 11 Vingegaard/Pogačar** terrain adjacency — verify keying during audit; drafter consumes for the cycling-context section of the relevant entry.
