# Strand D — Content research: km 70-92 block (segs 11/12/13)

**Start here:** Roadmap → Now → Content. This brief decided at planning session 2026-05-07 in advance of seg 11 publication on Sun 2026-05-10.

## Goal

Produce a single research dossier across the 22km block from km 70 (post-Tulle, just past the Auzelou stadium) to km 92 (transition toward Chaumeil approach). The dossier is consumed by three downstream draft strands (E/F/G — one per segment, publisher-paced). Research lands first; drafting strands consume it.

This is the second instance of the block-research-then-N-drafts technique (first instance: seg 8/9/10 under v1.4.10 strand-a-content). The technique is currently a light-tier watch-item under date-gated experiment evaluation; today's session counts as the next data point — work cleanly so the evaluation has signal.

## Filesystem posture

- **Worktree path (parent dir):** `git -C /home/jhs/code/tdf26 worktree add -b feature/v1.4.18-content-research /home/jhs/code/tdf26-research main`. Run from `/home/jhs/code` or use the absolute path form. Do NOT use `git worktree add tdf26-research main` from inside the repo (nests inside repo and trips "branch already checked out elsewhere").
- **No `.claude` symlink** — `.claude/` is tracked; the worktree already has it from checkout.
- **Branch verification:** before each `git add`/`git commit`, run `git branch --show-current` and confirm it matches the feature branch (`feedback_shared_tree_branch_verification.md`).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-research` once the dossier has merged or been pulled into the parent.

## The 22km block

| Segment | Km range | Towns (data/segments.json) | Climbs | Known content cues |
|---------|----------|----------------------------|--------|---------------------|
| 11 | 70-78 | (none in segments.json; Tulle outskirts behind, en route to Naves) | Côte des Naves | Stade Alexandre-Cueille / Auzelou stadium at km 70.91 (cyclosportive-departure, amateur-cycling angle, "99-100 days before stage" framing); Tintignac Gallo-Roman sanctuary nearby (Celtic carnyx find, well-documented; in `data/attractions.json` at km 77.66, 656m off route) |
| 12 | 78-84 | Naves | Puy de Lachaud (starts) | Naves itself; Côte des Naves gradient open question (#490) — points-config 5.6% disagrees with CLAUDE.md / ASO / elevation-derived 6.7-6.8% (the drafter should know this is contested but should not resolve it; the resolution is a separate strand) |
| 13 | 84-92 | (none in segments.json; transitional toward Chaumeil approach) | Puy de Lachaud (continues; spans seg 12 + 13 per `validate_points.py` invariant) | Puy de Lachaud is **not** on the official ASO climb list (#492) — open question whether to keep as non-ASO regional climb; the drafter should treat it as present-but-non-Categorised pending the resolution |

The route enters the Monédières range starting around segs 14-16 — **do not** spend Monédières framing in segs 11-13. The Sainte-Fortunade / Léon Dautrement "morceau de Monédières perdu dans le bas Limousin" line is reserved for segs 14/15/16 drafting (per #478 and the planning ledger).

## Workflow

1. **Spawn a single research subagent** (general-purpose Agent) with a self-contained prompt covering all three segments. Target ~5-10 minutes of research, similar shape to the v1.4.10 seg 8/9/10 research call.
2. The research subagent should cover, per segment and across the block:
   - **Geography and geology** — Corrèze plateau leaving the river valley, Naves basin, approach to the Monédières foothills.
   - **Local history** — Naves Roman heritage (the commune name traces to a Roman context); Tintignac as the major archaeological landmark; medieval/early-modern parish notes; Resistance / WWII traces if any.
   - **Cycling context** — Côte des Naves and Puy de Lachaud profiles; any historic Tour de France passages through this corridor (`data/historical-tdf.json` already contains some — research should check for gaps); the L'Agglomérée cyclosportive's relationship to the corridor (its 40km route uses Stage 9 roads including Suc au May further on).
   - **Famous local people** — search broadly for Naves and the surrounding communes.
   - **Culture** — local cuisine, festivals, anything that grounds the route between Tulle (seg 10, just shipped) and Chaumeil (seg 14+, ahead).
   - **Possible literary or musical references** — per the music-thread ledger in `project_next_planning_notes.md`, the Bourrée des Monédières is reserved for segs 14/15. Don't poach it. But check whether smaller local musical traditions exist between Tulle and the Monédières.
3. **Write the dossier** to `content/research/segs-11-13-block-research.md` (create directory if absent — gitignored at `content/research/` if needed; check `.gitignore` first and update if necessary). Structure:
   - Per-segment section (seg 11 / 12 / 13) with the research findings cleanly grouped by topic.
   - A "cross-segment threads" section listing arcs that span the block (e.g., the cyclosportive narrative starting at Auzelou and reflecting on the actual stage 99 days out).
   - A "sources" section listing every URL the dossier draws on (the dossier is the source-of-record for the eventual `## Sources` blocks in each entry — see `feedback_sources_section.md`).
   - A "carryforwards out of scope" section listing anything found that belongs in segs 14+, segs 17+, or in `data/historical-tdf.json` for the Tour-history feature.
4. **Read sources directly, not through CLAUDE.md transcription.** When the dossier cites a km position, town location, or climb gradient, read `data/segments.json`, `data/town-coords.json`, `data/points-config.json`, and the segment polylines — not CLAUDE.md (per `feedback_source_of_truth_framing.md` and the v1.4.18 Strand A finding).
5. **Open a PR** when the dossier is ready. PR body: short summary of what's in the dossier + which segs each section serves. Link to the issue if one is filed (file one if the publisher hasn't already — title `Block research dossier for segs 11-13 (km 70-92)`).

## Target issues

File a single tracking issue at start: `Block research dossier for segs 11-13 (km 70-92)`, milestone v1.4.18. PR closes it.

## Verification commands

These exist in this repo and should run clean before PR:

- `npm test` — must pass.
- `node scripts/validate_entries.py` — must pass (no new entry frontmatter touched, but defensive).
- `python3 processing/validate_points.py` — must pass (no points-config touched, but defensive against any drift).

If the dossier needs a new directory under `content/research/`, confirm `.gitignore` posture: if `content/research/` is gitignored, the dossier still ships in the PR by adding an exception or by moving to `docs/research/`. Decide at PR time.

## Cross-strand sharing notes

- **What this strand owns (write):** `content/research/segs-11-13-block-research.md` (or `docs/research/...` if .gitignore forces it).
- **What this strand reads:** `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/points-config.json`, `data/historical-tdf.json`, `data/segments/segment-11.gpx` / `segment-12.gpx` / `segment-13.gpx`.
- **What this strand must NOT touch:** `content/entries/*.md` (drafting strands E/F/G own these). `data/*.json` (any data corrections discovered are filed as new issues, not fixed inline).
- **Cross-strand collisions:** none expected. The downstream draft strands (E/F/G) have not been spawned yet; they spawn after this dossier lands.

## Scope discipline

- **Do not draft prose for any segment in this strand.** Output is a research dossier, not narrative.
- **Do not fix data inline.** If research surfaces a contradiction between an attraction location and the route, file a new issue. Examples already known: #490 (Côte des Naves gradient), #492 (Puy de Lachaud non-ASO).
- **Do not poach segs 14+ content.** Sainte-Fortunade / Monédières framing, Bourrée des Monédières, 1987 Chaumeil double-finish, Mont Bessou — all reserved.
- **Do not transcribe CLAUDE.md.** Read `data/*` directly. CLAUDE.md known-waypoints km ranges are stale (per #491).

## Memories that apply

- `feedback_source_of_truth_framing.md` — read polylines + JSON, not CLAUDE.md
- `feedback_on_route_checks.md` — use segment GPX polyline, not segments.json endpoints, when testing if a coord is on the race route
- `feedback_sources_section.md` — the dossier's sources section is the seed for each entry's `## Sources`
- `feedback_literary_footnotes.md` — if literary references surface, capture bibliographic context (forward-only from seg 6)
- `feedback_content_change_rule.md` — published entries are fixed; the dossier should not propose retroactive edits to segs 1-10
- `feedback_pre_publish_scrutiny.md` — verify geography, attribution, image rights before publish; the dossier flags anything dubious so seg 11 drafting catches it
- `project_disclosure_practice.md` — drafts (downstream) carry pair-writing footers
- `project_barthes_callback.md` — seg 12 is the "tightens" beat (argument becoming visible) of the seg 6/12/15 arc; the dossier should surface anything in seg 12's research that feeds this beat without spending it
- `project_meymac_voice.md` — seg 24 reserved for Saintsbury voice; do not poach Mascaron, abbey, etc.

## Stop when

- Dossier file exists at the target path.
- Sources section is complete (every factual claim in the dossier traces to a URL or named source).
- Carryforwards-out-of-scope section names anything the research found that belongs to segs 14+ or 17+ or to `data/historical-tdf.json`.
- PR open and tagged on milestone v1.4.18.
- Worktree removed (run cleanup yourself, do not hand off).
- Final report posted to publisher: dossier path, PR link, any open questions surfaced for downstream draft strands.
