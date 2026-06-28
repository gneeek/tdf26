# Strand: #502 tour-history feature — the /tour-history aggregate route

Feature strand for [#502](https://github.com/gneeek/tdf26/issues/502) (the `/tour-history` aggregate reader surface for Tour de France history along the 2026 Stage 9 corridor), targeted at a pre-stage launch (~July 2, ahead of the actual stage Sun 2026-07-12). **NOT a travelogue entry** — it is data + a route/page. **Fully parallel-safe** with the seg 25/26/27 drafting strands (it touches `data/` + new route files, not `content/entries/`), so it can start now.

## 1. Goal

Deliver #502 Phase 1 (research) and, on publisher go, the page. Per the #502 planning decisions (2026-05-07) the feature is phased **research → design discussion → draft → launch**. Phase 1 (research) is spawnable now and is the core deliverable. Given the project's near-end and the ~July-2 target, the **first checkpoint asks the publisher whether to compress into research+draft in this strand** or stop at a design checkpoint for a planning discussion before the page build.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/502-tour-history /home/jhs/code/tdf26-502 main
```

- Explicit-path worktree; no nesting (`feedback_strand_worktree_path`). Verify branch before each commit (`feedback_shared_tree_branch_verification`).
- Real `npm ci` + seed rider data before any build (`reference_worktree_node_modules_build`, `feedback_ci_seed_ordering`).
- New images under `public/images/` with attribution files.

## 3. Source-of-truth posture

- `content/research/tour-history-research.md` is the **canonical cycling-history dossier** — it owns the Ussel cycling-history corpus (Ussel never a TdF town before 2026; Paris-Corrèze, founded by Laurent Fignon; 2009 Tour du Limousin Limoges→Ussel; GP d'Ussel / Koblet 1955). `docs/reference/cycling-history.md` holds the two items the dossier does not own (La Corrézienne VTT, CycleBlaze journals).
- Re-verify load-bearing facts against source (`feedback_brief_content_is_carryforward`); the dossier and prior planning notes are scaffolding. Disambiguate corridor commune names by dept 19 (`feedback_corridor_commune_name_collisions`).
- `data/historical-tdf.json` groups events by a shared `segments` array with no per-event field (#603 finding) — adding a per-segment event means splitting into its own group, not editing a field.

## 4. Research scope (#502 Phase 1)

Expand `data/historical-tdf.json` (currently ~10 events across 4 segment groups): every Tour stage that started/finished/passed through the km 0-185 corridor; regional race history (Tour du Limousin, Paris-Corrèze, L'Agglomérée, GP d'Ussel); notable rider stories; 2025 Tour content; race-radio quotes. Source CC-licensed photos/videos with attribution.

**Sourcing caveats:** prefer YouTube/Vimeo-hosted over INA/France Télévisions embeds (GDPR cookie-banner-in-iframe, `reference_european_video_embeds`); Wikimedia `/Npx-/` thumb returns 400 when N = original width (`reference_wikimedia_thumb_widths`); French tourisme-office sites (terresdecorreze.com etc.) 403 the fetcher — verify via search snippet, cite the canonical URL (`reference_correze_tourisme_fetch_block`).

## 5. Workflow (publisher checkpoints)

1. **Compress vs phase:** research+draft in this strand vs research-then-design-checkpoint for planning (the phase decision above).
2. **Post-research:** present the expanded corpus + a design proposal (story arc, hero, layout) for go/no-go. Layout/hero/arc were explicitly reserved to a design discussion.
3. **(If building) first-render review.**

## 6. Verification commands

- `npm test` (+ a new data-schema assertion if a new aggregate surface introduces a parallel source of truth — `feedback_parallel_source_of_truth_detector`).
- `python3 processing/validate_points.py` if competition data is touched.
- `npm run build` + `nuxt generate` preview for the route (a non-draft route renders in the static build).

## 7. Cross-strand sharing notes

- **Owns (write):** `data/historical-tdf.json`, `content/research/tour-history-research.md` (research additions), and — if greenlit — the new `/tour-history` route + its components + a homepage card link.
- **Reads:** `tour-history-research.md`, `docs/reference/cycling-history.md`, `data/historical-tdf.json`, `data/segments.json`.
- **Must NOT touch:** `content/entries/*.md` (`feedback_content_change_rule`). A per-segment HistoricalContext cross-link to the route is a **sibling PR**, not part of this strand.
- **Coordination with seg 27 (Ussel finish), confirmed division of labour (dossier open Q #2):** **#502 owns the Ussel cycling history**; **seg 27 owns the place + arrival** and uses only the single 2003-Paris-Corrèze-on-Avenue-Thiers fact inline. Honour the split so neither surface duplicates the other.

## 8. Scope discipline

- #502 is an **umbrella** issue with a separate launch issue downstream — `Refs #502`, do NOT auto-close.
- Append-and-flag for any prose-bearing generated doc; never auto-rewrite hand-authored prose (`feedback_append_flag_generated_docs`).
- File issues for findings outside the write-set.

## 9. Memories that apply

`feedback_brief_content_is_carryforward`, `feedback_source_of_truth_framing`, `feedback_parallel_source_of_truth_detector`, `feedback_content_change_rule`, `feedback_interpolated_pr_pattern`, `feedback_corridor_commune_name_collisions`, `reference_european_video_embeds`, `reference_wikimedia_thumb_widths`, `reference_correze_tourisme_fetch_block`, `feedback_append_flag_generated_docs`, `feedback_ci_seed_ordering`, `feedback_shared_tree_branch_verification`, `feedback_strand_session_self_cleanup`, `reference_worktree_node_modules_build`, `feedback_pr_closure_keywords`.

## 10. Stop when

- Research corpus expanded + verified and (per the phase decision) either a design proposal presented for planning, or the `/tour-history` page built, previewed, and PR open against `main` (`Refs #502`).
- **Cleanup (you run):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-502` once merged.
- Final report: PR link, what was added to `historical-tdf.json`, the compress-vs-phase decision, and confirmation the seg-27 split was honoured.
- **Retro inputs** to `project_next_planning_notes.md` under `## Items surfaced during #502 tour-history strand execution (<date>)`.
