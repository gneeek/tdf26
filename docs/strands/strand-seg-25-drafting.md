# Strand: seg 25 drafting — Meymac, the abbey set-piece, the Côte des Gardes

Publisher-paced single-segment drafting strand (deviation: "Workflow" lists publisher checkpoints, not prose-writing steps; cadence is publisher-driven). Mirrors the seg 15/16/17/18/19 drafting strands. **This is the richest entry of the back half — the Meymac set-piece.**

## 1. Goal

Draft the seg 25 entry (currently the mis-titled stub `content/entries/25-approach-to-ussel.md`) from `content/research/segs-23-27-block-research.md` ("Segment 25" section). Seg 25 is **Meymac + the Côte des Gardes** (`segments.json`: seg 25, km 168-176, `towns:["Meymac"]`, `climbs:["Côte des Gardes"]`). **The stub slug is wrong** (Meymac is seg 25, not "approach to Ussel" — Ussel is seg 27). Rename via `git mv` at the anchor checkpoint to **`25-meymac-and-the-cote-des-gardes`** (dossier-recommended, open Q #1). The publisher will set/confirm the `publishDate` inside this strand (current frontmatter says 2026-06-28, imminent — expect to move it).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-25-draft /home/jhs/code/tdf26-seg-25 main
```

- Explicit-path worktree; no nesting, no `.claude` symlink (`feedback_strand_worktree_path`). `git branch --show-current` → `feature/seg-25-draft` before each commit (`feedback_shared_tree_branch_verification`).
- Rename the stub via `git mv` once the new slug is chosen; don't create a second file.
- Fresh worktree: real `npm ci` + seed rider data (`cp data/riders/*.example.json` to non-example names, `feedback_ci_seed_ordering`) before any build/preview — symlinked `node_modules` breaks `nuxt build` (`reference_worktree_node_modules_build`).
- Single-strand orchestrator session only — **do not spawn sub-agents for the drafting** (seg-13 finding).
- Image frontmatter: inline-JSON, not YAML list (#479 / seg-9 crash history). Hero is an `::inline-figure` after the H1 (not frontmatter); MDC blocks need a closing `::` (`reference_tdf26_entry_visual_components`).

## 3. Source-of-truth posture

- Dossier is scaffolding, not bedrock (`feedback_brief_content_is_carryforward`) — re-verify load-bearing claims against source. Verify on-route anchors against `data/town-coords.json` + the seg-25 GPX, not `segments.json` endpoints (`feedback_on_route_checks`). Disambiguate commune-name searches by dept 19 (`feedback_corridor_commune_name_collisions`).
- **Non-negotiable fact caveats (getting these wrong is a reader-facing error):**
  - **Black Madonna (Vierge noire):** the "brought back from the Crusades / from Egypt" story is **legend only** — the official Palissy notice records no such provenance. Voice it as legend (Saintsbury's cheerful-concession move is ideal). The displayed figure is a recent copy; the ~900-year-old original lives in the mairie safe.
  - **Saint-Léger skull-relic** claim is search-snippet-level — verify against a primary/diocesan source before stating, or omit.
  - **No Meymac-specific cèpe festival exists** ("cèpe country" is fair colour; the named fête is at the village of Corrèze, off-route).
  - **Côte des Gardes:** the stage's last categorised climb, ~2.2 km @ 4.8%, crests ~14 km from the finish. Declared summit km 170.98 sits ~200m past the GPX peak (km 170.766) — write the crest as a race beat, not a km-precise GPS claim. (Data caveat, same class as Naves #490.)
  - **Meymac-1944 execution** (German prisoners, 12 June 1944, the documented sequel to the Tulle hangings of segs 9-10) is **verified** but morally freighted — see checkpoint 3.
- Do NOT transcribe CLAUDE.md tabular data; narrative project context only.

## 4. Anchors available (from the dossier)

The abbey set-piece carries the segment: **Abbaye Saint-André** (founded 1085 by Archambaud III de Comborn; Romanesque clocher-porche; jointly dedicated Saint-André-et-Saint-Léger), the **Black Madonna** (12th c., legend voiced as legend), the **CAC Meymac contemporary-art centre lodged in the abbey** (the genial 1085-meets-cutting-edge collision), and the gloriously improbable **"Meymac-près-Bordeaux"** wine trade (the granite mountain town that was, by reputation, a Bordeaux wine capital — and here the one permitted wine metaphor is *literal*). **Marius Vazeilles** (forester/archaeologist, the block's central figure) and the **abbé d'Aubignac** (theatre theorist, abbey *in commendam* — wants a literary footnote). See dossier lines ~83-117 for the full anchor set and ~197-215 for the voice note.

## 5. Workflow (publisher checkpoints — the cadence)

Fire as AskUserQuestion; iterate in free-form chat between.

1. **Anchor/title:** confirm rename to `25-meymac-and-the-cote-des-gardes` and the lead anchor (abbey + its three improbabilities? the "Meymac-près-Bordeaux" hook? the plateau-edge arrival?).
2. **Voice register:** pre-read the Saintsbury SKILL.md + samples in `/home/jhs/code/skills/registers-framework/saintsbury/` before firing (`feedback_voice_checkpoint_prep`). Recommend **saintsbury period** (reflective mood for abbey/arrival; critical only if judging the art collision); **tls-essay** is the documented fallback. Do not ship saintsbury against a weak anchor (v1.4.5 precedent) — but the anchor is strong here.
3. **Meymac-1944 framing (editorial call before drafting, dossier open Q #3):** developed beat ("victors' justice" register, the documented sequel to Tulle), footnoted aside, or deferred — so it does not overload the abbey set-piece. Do not pre-decide.
4. **Promises-inherited:** what segs 23/24 handed up; and what seg 25 must **plant** for payoff — explicitly the **Ventadour viscount/ducal thread** (paid off at seg 27, Ussel) and the **abbey-architecture motif** (seg 26's Saint-Angel priory echoes it). Coordinate so the echo/payoff are written once.
5. **First-draft review.**
6. **Fact-duplication audit** between revisions and the Sources/disclosure footer.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `npm test`
- `npm run build`; preview the **draft** entry via the dev server (drafts are excluded from `nuxt generate`, `reference_draft_entry_preview`), not the static production preview.
- MDC balance: validator directive check (PR #563) or grep `::name{...}` opens vs closes.
- After drafting, offer 3 clickable Street View viewpoint links, best-bet first (`feedback_streetview_candidates`).

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/25-*.md` only.
- **Reads:** the 23-27 dossier, `segments.json`, `town-coords.json`, seg-25 GPX, `attractions.json`.
- **Must NOT touch:** any other entry (`feedback_content_change_rule`), the seg 26/27 stubs, or `data/`. Out-of-scope edits → sibling PR (`feedback_interpolated_pr_pattern`) or file an issue.
- **Coordination:** seg 25 runs FIRST among the finish-arc segs because it plants the Ventadour thread (→ seg 27) and the abbey-architecture motif (→ seg 26). Fix those choices here.
- **Word count:** target house length (recent entries ~1,200-1,900; seg 22 was 1,875). The CLAUDE.md 800-1,200 floor is **stale** (W22-seg17 retro) — set the real target with the publisher at the anchor checkpoint; given the set-piece, expect the upper end.

## 8. Scope discipline

- File issues for findings outside the entry write-set; don't over-scope.
- Style tics to avoid (cross-entry grep before sign-off): the "the X the Y will not Z" shape (`feedback_will_not_shape`), "polyline" in prose (`feedback_avoid_polyline_in_prose`), em-dashes and exclamation marks (zero — and Saintsbury's nested em-dashes are the single biggest mechanical adjustment; re-route through commas/parentheses), internal-data citations in Sources (`feedback_sources_no_internal`).
- Literary footnotes from seg 6 forward (`feedback_literary_footnotes`) — abbé d'Aubignac wants one; optional `## Sources`, external URLs only (`feedback_sources_section`); per-entry disclosure footer (`project_disclosure_practice`).

## 9. Memories that apply

`project_meymac_voice`, `feedback_content_change_rule`, `feedback_brief_content_is_carryforward`, `feedback_pre_publish_scrutiny`, `feedback_voice_checkpoint_prep`, `feedback_literary_footnotes`, `feedback_sources_section`, `feedback_sources_no_internal`, `project_disclosure_practice`, `feedback_will_not_shape`, `feedback_avoid_polyline_in_prose`, `feedback_interpolated_pr_pattern`, `feedback_on_route_checks`, `feedback_corridor_commune_name_collisions`, `feedback_ci_seed_ordering`, `feedback_shared_tree_branch_verification`, `feedback_strand_session_self_cleanup`, `reference_tdf26_entry_visual_components`, `reference_draft_entry_preview`, `reference_worktree_node_modules_build`, `feedback_streetview_candidates`. (Barthes arc spent at seg 15.)

## 10. Stop when

- Renamed seg 25 entry drafted (house length, target confirmed), validators green, publisher-confirmed dev preview; PR open against `main` (open a seg-25 tracking issue, `Refs #N`).
- Entry left `draft: true` (publisher flips at publish time; publisher sets `publishDate` in-strand).
- **Cleanup (you run):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-seg-25` once merged (`feedback_strand_session_self_cleanup`).
- Final report: PR link, chosen slug, voice register, the 1944 framing decision, the threads planted for segs 26/27.
- **Retro inputs** to `project_next_planning_notes.md` under `## Items surfaced during seg-25-drafting strand execution (<date>)`: decision-actionable observations, light-tier patterns, numeric stats (word count, footnotes, MDC directives, em-dash/exclamation counts, checkpoint cycles, wall-clock).
