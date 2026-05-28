# Strand: segs 20-22 block research dossier (km 134-154)

Research-only strand (deviation: no "Workflow per issue"; output is a dossier, not commits to multiple file regions). Mirrors `content/research/segs-17-19-block-research.md` (PR #600), `segs-14-16-block-research.md` (PR #559), `segs-11-13-block-research.md` (PR #501).

## 1. Goal

Compile `content/research/segs-20-22-block-research.md`, the narrative-anchor research that feeds the seg 20, 21, 22 drafting strands. Must land **before seg 20 drafts (~publishes 2026-06-10)**. This is the Plateau-de-Millevaches heart + Mont Bessou block — the route's high-altitude traverse. Auto-mode; spawn a research subagent for depth as the 17-19 dossier did (~20-25 min subagent run). No publisher checkpoint expected unless a material framing fork surfaces.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/segs-20-22-research /home/jhs/code/tdf26-segs-20-22 main
```

- Explicit-path worktree; do not nest. No `.claude` symlink. `git branch --show-current` before commit → `feature/segs-20-22-research`.
- Research-only branch: no `node_modules`, no rider seed needed (dossier doesn't touch entries or data files). `validate_entries.py` will run green because nothing under `content/entries/` changes.

## 3. Source-of-truth posture

- **Work from `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-{20,21,22}.gpx` directly.** The verified segment shape for this block:
  - **seg 20** (km 134-140): no towns, no climbs — the open Plateau heart. The "verified empty" beat (per #498/#499 precedent): the Parc itself is the attraction; do not invent landmarks to fill it.
  - **seg 21** (km 140-148): town = **Bugeat**; climb = Mont Bessou (begins). Bugeat town centre is ~24 m off the seg-21 polyline at ~km 144 — Bugeat is properly a seg 21 town (the seg 19 "gateway" title was a threshold-framing, not a literal-location, title).
  - **seg 22** (km 148-154): no towns; climb = **Mont Bessou** (summit). Mont Bessou is the highest point in Corrèze (977 m); its town-coords coord was realigned to points-config km 152.31 under #499/PR #550 — verify it still holds.
- Per `feedback_on_route_checks.md`: test on-route claims against the GPX polyline, not segments.json endpoints. Per `feedback_source_of_truth_framing.md`: trace provenance before treating a hand-curated value as bedrock.
- Do NOT transcribe CLAUDE.md tabular data; narrative context only.

## 4. Research plan

Produce the dossier in the now-stable shape:

1. **Cross-segment threads (top):** the threads that span the block. Strong candidates:
   - **The Plateau de Millevaches proper** — heathland, peat bogs, *"mille sources"* (Celtic/Occitan, not "thousand cows"); Parc naturel régional; one of the least-populated areas of France; 20th-c. conifer afforestation (*fermeture paysagère*).
   - **The geological-transition story deferred from seg 11** (see `project_next_planning_notes.md` forward-looking notes): the genuine lithological/topographic story of the Plateau basement belongs here or at Mont Bessou. Sources already gathered: BRGM Tulle 761 notice, Université de Limoges Bassin de Brive page, Géologie du Limousin FR Wikipédia. **This block is the natural home; develop it.**
   - **The Resistance corridor** — the Bugeat 6 April 1944 atrocity (four L'Echameil inhabitants executed; eleven Jewish residents arrested, ten deported to Auschwitz) and the Bugeat Maquis stèle at km 143.64 (seg 21, already in attractions.json). The seg 18 dossier reserved the Bugeat-specific names for this block — they anchor seg 21.
   - **Mont Bessou as the roof** — highest point in Corrèze, the day's altitude apex, the watershed/source country (the Vézère rises in the Longéroux peatland near here at 887 m).
   - **2024 TdF Stage 11** re-keyed to seg 22 (Mont Bessou as altitude parallel for Puy Mary) under PR #478/#514 — verify the keying and write the beat from the seg 22 side.
2. **Per-segment sections**, each with the six fixed headers: *Geography & geology / Local history & archaeology / Cycling context / Famous local people / Culture / Literary-musical*. Name which anchors belong to which segment (anchor allocation). Flag where a segment is genuinely thin (seg 20 likely is — write the "verified empty / the Plateau is the subject" framing rather than padding).
3. **Data reconciliations:** capture any drift found vs points-config / town-coords / attractions as **recommended issue titles** (problem-only, per `feedback_issues_describe_problems.md`); do not file from the research worktree — planning files them. Cross-check the open summit-km items (#591 Croix de Pey is upstream; Mont Bessou drift was #499/closed — confirm). Note the Tourbière de Longeyroux (km 154.4, keyed seg 23).
4. **Carryforwards:** explicit checklist + verification log so the drafting strands can run short and auto-mode (the 17-19 → drafting handoff worked because of this).
5. **Sources:** external URLs backing factual claims, each flagged if it 503s/404s on spot-check (per `feedback_sources_section.md`). External only — never cite internal JSON (`feedback_sources_no_internal.md`).
6. **Open questions:** unresolved framing forks for the drafters.

## 5. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green (no entry changes).
- Source URL spot-check: confirm each cited URL is reachable; flag failures inline rather than dropping.
- `npm test` is **not** required (dossier-only branch, no JS/data changes — the 17-19 strand skipped it for this reason).

## 6. Cross-strand sharing notes

- **Owns (write):** `content/research/segs-20-22-block-research.md` only.
- **Reads:** all `data/` files, `data/segments/*.gpx`.
- **Must NOT touch:** any `content/entries/*.md`, any `data/` file, sibling research dossiers.
- **Collisions:** none expected — single new file. If the seg 20-22 *data verification* (#499 follow-ups) is still in flight, read its PR for the latest town-coords; otherwise no shared write region.

## 7. Memories that apply

- `feedback_source_of_truth_framing.md`, `feedback_on_route_checks.md`, `feedback_corridor_commune_name_collisions.md` (disambiguate Bugeat / Millevaches communes by dept), `feedback_sources_section.md`, `feedback_sources_no_internal.md`, `feedback_issues_describe_problems.md`, `feedback_strand_worktree_path.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_session_self_cleanup.md`.

## 8. Stop when

- `content/research/segs-20-22-block-research.md` committed; PR open against `main` (title references the block, body lists recommended issue titles, `Refs` not `Closes` if no umbrella issue).
- Source URLs spot-checked; failures flagged inline.
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-segs-20-22` once merged.
- Final report: PR link, dossier path, anchor-allocation summary, recommended issue titles, open questions for the seg 20/21/22 drafters.
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during segs-20-22-content-research strand execution (<date>)`: decision-actionable observations, light-tier pattern observations, numeric stats.
