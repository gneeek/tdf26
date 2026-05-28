# Strand: segs 23-27 block research dossier (km 154-184.8) — the finish stretch

Research-only strand (deviation: no "Workflow per issue"; output is a dossier). Mirrors the prior block dossiers. **Larger block (5 segments)** than the usual 3 — budget a longer subagent run, or split the subagent pass (23-25 / 26-27) if depth demands; the output is still one dossier file.

## 1. Goal

Compile `content/research/segs-23-27-block-research.md`, feeding the seg 23, 24, 25, 26, 27 drafting strands — the Meymac-to-Ussel finish stretch. Must land **before seg 23 drafts (~publishes 2026-06-21)**. Two things make this block special: (a) **seg 25 (Meymac) carries a voice reservation** — `project_meymac_voice.md` reserves the saintsbury register for the abbey segment, retargeted seg 24→25 under #500; settle the voice question here so samples can be developed before drafting; (b) **seg 27 is the finish line** (Ussel, Place Voltaire) and shares context with the **July-2 tour-history special** (#502) — coordinate so the two don't duplicate the Ussel/finish material. Auto-mode; spawn a research subagent for depth.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/segs-23-27-research /home/jhs/code/tdf26-segs-23-27 main
```

- Explicit-path worktree; no nesting, no `.claude` symlink. `git branch --show-current` before commit.
- Research-only branch: no `node_modules` / rider-seed needed.

## 3. Source-of-truth posture

- **Work from `data/segments.json` directly. The stub entry titles are mis-anchored for this block** (the 26→27 segment re-split shifted content; stubs were named under the old scheme). Verified shape:
  - **seg 23** (km 154-162): no towns, no climbs — descent off Mont Bessou toward Meymac. (Stub "23-descent-to-meymac" is roughly right.)
  - **seg 24** (km 162-168): no towns, no climbs — approach/descent. (Stub "24-meymac-and-the-cote-des-gardes" is **wrong** — Meymac + Côte des Gardes are seg 25.)
  - **seg 25** (km 168-176): town = **Meymac**; climb = **Côte des Gardes**. (Stub "25-approach-to-ussel" is **wrong**.) Benedictine Abbaye Saint-André (founded 1085); Centre d'Art Contemporain in the abbey. **Saintsbury voice reservation applies here.**
  - **seg 26** (km 176-182): town = **Saint-Angel**. (Stub "26-ussel-place-voltaire" is **wrong** — Ussel is seg 27.) Saint-Angel village + priory (added under #500); a Monument Historique priory.
  - **seg 27** (km 182-184.8): town = **Ussel**, the finish. Avenue Thiers finish; sprint judged at Place Voltaire. **Note #554: the GPX polyline ends ~216 m short of Place Voltaire** — the finish-line geometry has a known gap; write the finish on the verified endpoint, flag the discrepancy.
- **Recommend the drafting strands re-title segs 24, 25, 26** at their arc-agreement checkpoints; the dossier should propose corrected anchor-aligned slugs. Do not rename the stub files from this research strand (no entry edits).
- Per `feedback_corridor_commune_name_collisions.md`: disambiguate Meymac / Saint-Angel / Ussel against same-named communes (dept 19 + adjacency). Per `feedback_on_route_checks.md` and `feedback_source_of_truth_framing.md`.
- The #500 verification strand already audited this block's data (filed #553/#554/#555, landed 9 fixes). Read its PR (#556) and the `tour-history-research.md` dossier so the research builds on verified ground, not re-discovers it.

## 4. Research plan

Dossier in the stable shape:

1. **Cross-segment threads (top):** strong candidates —
   - **The descent off the roof** — segs 23-24 are the long descent from Mont Bessou toward the Ussel basin; the Plateau gives way to the Limousin/Auvergne transition.
   - **Meymac and the Benedictine foundation** — Abbaye Saint-André (1085), the Centre d'Art Contemporain, the medieval town. The set-piece of the block.
   - **The Limousin→Auvergne gateway** — Ussel as the historical threshold between the Limousin lowlands and the Auvergne highlands.
   - **Jacques Chirac and Corrèze politics** — Chirac began his political career as an Ussel municipal councillor (note: the Chirac *burial* is Montparnasse per #564/#585, and the Musée Chirac at Sarran opened 15 Dec 2000 per #586/#605 — do not re-import the corrected errors). The Musée du président Jacques-Chirac is at Sarran (off-route, near seg 14 country).
   - **The finish line itself** — Avenue Thiers, Place Voltaire sprint-judge line; coordinate with the **July-2 tour-history special** so the historic-finishes material (Paris-Corrèze stages finishing in Ussel; Ussel never a TdF stage town) lives in the right surface.
2. **Per-segment sections**, six fixed headers each. Be explicit where a segment is thin (segs 23, 24 likely are — descent corridors). Propose anchor allocation **and corrected slugs** for segs 24/25/26.
3. **Voice note for seg 25:** present the saintsbury-register case (per `project_meymac_voice.md`) with enough sample texture that the publisher can confirm or diverge at the seg 25 voice checkpoint. This is the one place the research strand should do voice-prep, because the reservation predates drafting.
4. **Data reconciliations:** recommended issue titles (problem-only) for any new drift; confirm the #500-era fixes held.
5. **Carryforwards:** checklist + verification log for the five drafting strands.
6. **Sources:** external only, spot-checked, failures flagged.
7. **Open questions:** framing forks, especially the seg 27 / July-special division of labour.

## 5. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green (no entry changes).
- Source URL spot-check; flag failures inline.
- `npm test` not required (dossier-only).

## 6. Cross-strand sharing notes

- **Owns (write):** `content/research/segs-23-27-block-research.md` only.
- **Reads:** all `data/` files, `data/segments/*.gpx`, `content/research/tour-history-research.md`, PR #556.
- **Must NOT touch:** any `content/entries/*.md` (including renaming the mis-titled stubs — that's the drafters' job), any `data/` file, the July-special entry, sibling dossiers.
- **Collisions:** none on write (single new file). Coordination, not collision, with the July-2 special (#502) over Ussel/finish material — the dossier's open-questions section names the division.

## 7. Memories that apply

- `project_meymac_voice.md` (the seg 25 reservation — load this), `feedback_corridor_commune_name_collisions.md`, `feedback_source_of_truth_framing.md`, `feedback_on_route_checks.md`, `feedback_sources_section.md`, `feedback_sources_no_internal.md`, `feedback_issues_describe_problems.md`, `feedback_strand_worktree_path.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_session_self_cleanup.md`.

## 8. Stop when

- `content/research/segs-23-27-block-research.md` committed; PR open against `main` (`Refs #502` for the finish/July coordination; body lists recommended issue titles + proposed corrected slugs for segs 24/25/26 + the seg 25 voice recommendation).
- Source URLs spot-checked.
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-segs-23-27` once merged.
- Final report: PR link, dossier path, anchor allocation + slug corrections, seg 25 voice recommendation, July-special coordination note, open questions.
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during segs-23-27-content-research strand execution (<date>)`: decision-actionable observations (esp. the slug corrections + voice call), light-tier pattern observations, numeric stats.
