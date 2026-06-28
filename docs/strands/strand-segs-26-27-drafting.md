# Strand: segs 26 + 27 drafting — Saint-Angel, then Ussel (the finish)

Publisher-paced drafting strand covering the **last two entries of the project**, drafted **one at a time, in order: seg 26 (Saint-Angel) first, then seg 27 (Ussel, the finish line).** Mirrors the seg 15-19/25 drafting strands; the deviation is that one session carries two sequential entries, each as its own PR. **Seg 27 is the emotional climax of the whole 27-segment blog — it lands the arrival everything has ridden toward.**

This strand runs **after seg 25 and the #502 tour-history special have merged** (it depends on both). Its first job is to review what those two actually shipped.

## 1. Goal

Draft, in sequence:
1. **Seg 26 — Saint-Angel** (stub `content/entries/26-ussel-place-voltaire.md`; the slug is wrong, Ussel is seg 27). `segments.json`: seg 26, km 176-182, `towns:["Saint-Angel"]`, no climbs. Rename via `git mv` to **`26-saint-angel`** (dossier open Q #1). Thin material, one strong anchor; do not pad.
2. **Seg 27 — Ussel, the finish** (stub `content/entries/27-place-voltaire-the-finish-line.md`; slug is correct, **keep** — optionally `27-ussel-the-finish-line`, publisher's weak call). `segments.json`: seg 27, km 182-184.84, `towns:["Ussel"]`, no climbs.

Source: `content/research/segs-23-27-block-research.md` ("Segment 26" ~120-150, "Segment 27" ~154-193) + the per-segment checklist (~237-238) + open questions (~288-299). Publisher sets each `publishDate` in-strand.

## 2. Phase 0 — review what merged for seg 25 and #502 (do this FIRST, before any drafting)

`git fetch` and confirm against **remote/main** (not local alone — `feedback_pr_polling`, multi-session visibility) that seg 25 and #502 are merged. If either is still an open PR, read it from its PR branch and note the dependency. Then extract and write down:

**From the merged seg 25 entry (`content/entries/25-meymac-*.md`):**
- The **final slug and title**, the **voice register** chosen, and the **1944-framing decision** (developed / footnoted / deferred) — seg 26's register choice and tone should be made knowing seg 25's.
- **How the Ventadour thread was planted** — seg 27 must *pay it off* (the dukes leaving the Château de Ventadour for Ussel); quote/anchor to what seg 25 actually said so the payoff is continuous, not a restatement.
- **How the abbey architecture was written** — seg 26's Saint-Michel-des-Anges priory *echoes* Meymac's abbey design; write it as the echo, referencing (not duplicating) seg 25's treatment.
- Any **promises seg 25 made or deferred**, its **disclosure footer** wording, and its **Sources** (for the cross-entry fact-dup audit).
- The seg-25 strand's **retro-input notes** in `project_next_planning_notes.md` (`## Items surfaced during seg-25-drafting...`).

**From the merged #502 tour-history work (`data/historical-tdf.json`, `content/research/tour-history-research.md`, and the `/tour-history` route if built):**
- Exactly **what Ussel cycling-history material #502 now owns** (never-a-TdF-town, Paris-Corrèze, 2009 Limoges→Ussel, GP d'Ussel) — so **seg 27 points to it and does not restate it**. Confirmed division of labour (dossier open Q #2): **#502 owns the cycling history; seg 27 owns the place + arrival** and uses only the single 2003-Paris-Corrèze-on-Avenue-Thiers fact inline.
- Whether the `/tour-history` route exists yet, so seg 27 can decide whether to **link to it** inline.

Carry these findings into the relevant checkpoints below.

## 3. Filesystem posture

Sequential, one entry at a time:

```
# Seg 26 first
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-26-draft /home/jhs/code/tdf26-seg-26 main
#   ...draft, PR, leave draft:true...
# Then seg 27, off the latest main (after seg 26's PR is open/merged)
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-27-draft /home/jhs/code/tdf26-seg-27 main
```

- Explicit-path worktrees; no nesting, no `.claude` symlink (`feedback_strand_worktree_path`). `git branch --show-current` before each commit (`feedback_shared_tree_branch_verification`).
- **Finish seg 26 (draft + PR open) before starting seg 27** — "one at a time."
- `git mv` each stub to its corrected slug; don't create second files.
- Real `npm ci` + seed rider data (`cp data/riders/*.example.json` to non-example names, `feedback_ci_seed_ordering`) per worktree before any build — symlinked `node_modules` breaks `nuxt build` (`reference_worktree_node_modules_build`).
- Single orchestrator session; **no sub-agents for the drafting** (seg-13 finding). Inline-JSON image frontmatter (#479); hero is an `::inline-figure` after the H1; MDC blocks need a closing `::` (`reference_tdf26_entry_visual_components`).

## 4. Anchors + non-negotiable caveats

Re-verify load-bearing claims against source (`feedback_brief_content_is_carryforward`); verify on-route anchors against `data/town-coords.json` + each segment's GPX, not `segments.json` endpoints (`feedback_on_route_checks`); disambiguate commune names by dept 19 (`feedback_corridor_commune_name_collisions`).

**Seg 26 — Saint-Angel (dossier ~120-150):**
- **Anchor:** Prieuré / église **Saint-Michel-des-Anges**, on the **foundational 1840 monuments historiques list** — phrase **"on the 1840 list," NOT "classified by decree in 1840."** The strongest fact: a small depopulated plateau village holds one of France's earliest protected monuments.
- **Charroux foundation charter (~783):** authenticity is **debated** — "a donation recorded in a charter whose authenticity is debated," not flat fact.
- **Geology correction:** there is **no sedimentary "Ussel basin."** Saint-Angel sits on crystalline Hercynian socle — **granite giving way to gneiss/migmatite** within the same basement; village core on a gneiss outcrop. Never write crystalline-to-sedimentary.
- **Abbey-architecture echo** to seg 25 (write as the echo, per Phase 0). **People are genuinely sparse** — say so, do not pad (only Jean-Baptiste Poulbrière is a thin tie). Register: **"Village Étoilé" (dark-sky village)**, silence-and-forest, the last village before the finish. **No literary/musical hook** for Saint-Angel — do not invent one (that material is Ussel's). No climbs; keep cycling light.

**Seg 27 — Ussel, the finish (dossier ~154-193):**
- **Finish geometry (do not paper over):** the GPX parcours ends **~216m west of the Place Voltaire** sprint line. Write the finish on the **verified endpoint (Avenue Thiers, 45.5456/2.30422)** and note the ~216m gap — same finishing straight, a data-trace shortfall, not a different place (#554).
- **Roman eagle (Aigle romaine):** granite, late-2nd/early-3rd c., found **headless**; head added **1804 by the sculptor Pic** for Napoleon's coronation; now on Place Voltaire. The sprint is judged beside an 1,800-year-old re-headed Roman eagle.
- **Ventadour payoff** (closes the seg-25 thread): the duché de Ventadour's three capitals (Égletons, Ussel, Meymac); the dukes left the Château de Ventadour for Ussel (Hôtel ducale des Ventadour, 8 rue des Ventadours).
- **Chirac — do NOT misplace:** Ussel = where Chirac first won **national** office (1967 législatives, 3rd circ. of Corrèze = Ussel constituency). But **buried at Montparnasse, Paris** (not Corrèze); **Musée Jacques-Chirac is at Sarran** (off-route, not Ussel). Do not re-import the #564/#585 burial or #586/#605 museum errors.
- **Watershed:** Ussel drains **Atlantic** via the Diège → Dordogne. Do **not** place a continental divide at Ussel or invoke a Mediterranean basin.
- **uxello- = "the high place"** — the etymological cap on the whole climbing stage. **Accordion thread** from Tulle (segs 9/10) re-surfaces via **René Limouzin** (writer/accordionist, died at Ussel) — a deliberate full-circle callback.
- **Cycling context KEEP LIGHT** — point to #502 (per Phase 0); only the 2003 Paris-Corrèze-on-Avenue-Thiers fact inline. Finish profile: last climb Côte des Gardes ~14 km out, final km ~0.3% (effectively flat), expected reduced-bunch/breakaway finish (verify the final-km figure against the official profile before asserting).

## 5. Workflow (publisher checkpoints — the cadence)

Run **Phase 0 (§2) first.** Then, for **seg 26**, then again for **seg 27**, fire as AskUserQuestion and iterate in free-form chat between:

1. **Anchor/title** (confirm the rename; the lead anchor). For seg 27 this also confirms the **#502 division of labour** and whether to link the `/tour-history` route inline.
2. **Voice register** — pre-read candidate register SKILL.md briefs before firing (`feedback_voice_checkpoint_prep`). Seg 26: continuity with seg 25's register (reinforces the priory↔abbey echo) vs a quiet shift for a deliberately-quiet transitional segment. Seg 27: the finish may want its own register weight; this entry also closes the project's authorial arc, so consider a closing note in the disclosure footer.
3. **Promises-inherited** — seg 26 inherits the abbey-architecture echo and reserves all Ussel material for seg 27; **seg 27 pays off Ventadour (from seg 25) and the accordion (from segs 9/10)** and lands the whole-blog arrival.
4. **First-draft review.**
5. **Fact-duplication audit** between revisions and the Sources/disclosure footer — for seg 27, audit hard against the merged #502 material and against Tulle (segs 9/10) for the accordion.

**Word count:** house length (recent entries ~1,200-1,900). The CLAUDE.md 800-1,200 floor is **stale** (W22-seg17 retro). Set the real target per entry at the anchor checkpoint: **seg 26 likely the shorter end** (thin material), **seg 27 likely the upper end** (the finish/climax).

## 6. Verification commands (per entry)

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `npm test`
- `npm run build`; preview each **draft** entry via the dev server (drafts are excluded from `nuxt generate` — `reference_draft_entry_preview`), not the static production preview.
- MDC balance via the validator directive check (PR #563) or grep `::name{...}` opens vs closes.
- After each draft, offer 3 clickable Street View viewpoint links, best-bet first (`feedback_streetview_candidates`) — the Ussel finishing straight is a natural one for seg 27.

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/26-*.md` and `content/entries/27-*.md` — **one PR per entry** (one-entry-per-PR norm; segs 26 and 27 are separate PRs, `feedback_content_change_rule`).
- **Reads:** the merged seg 25 entry + #502 work (Phase 0), the 23-27 dossier, `segments.json`, `town-coords.json`, segs 26/27 GPX, `attractions.json`, `historical-tdf.json` (read-only — it is #502's to write).
- **Must NOT touch:** any other entry (including seg 25 — `feedback_content_change_rule`), or `data/`. Out-of-scope edits → sibling PR (`feedback_interpolated_pr_pattern`) or file an issue.
- **Dependency:** requires seg 25 + #502 merged (Phase 0). Segs 26 and 27 are otherwise light on each other (different towns) — the shared upstream is seg 25 + #502, not each other.

## 8. Scope discipline

- File issues for findings outside the entry write-set; don't over-scope.
- Style tics to avoid (cross-entry grep before sign-off): the "the X the Y will not Z" shape (`feedback_will_not_shape`), "polyline" in prose (`feedback_avoid_polyline_in_prose`), em-dashes and exclamation marks (zero), internal-data citations in Sources (`feedback_sources_no_internal`), and the "next essay's business" handoff device (overused segs 17-19 — and seg 27 has no next essay, so it must not reach for it).
- Literary footnotes from seg 6 forward (`feedback_literary_footnotes`); optional `## Sources`, external URLs only (`feedback_sources_section`); per-entry disclosure footer (`project_disclosure_practice`).

## 9. Memories that apply

`feedback_content_change_rule`, `feedback_brief_content_is_carryforward`, `feedback_pre_publish_scrutiny`, `feedback_pr_polling`, `feedback_voice_checkpoint_prep`, `feedback_literary_footnotes`, `feedback_sources_section`, `feedback_sources_no_internal`, `project_disclosure_practice`, `feedback_will_not_shape`, `feedback_avoid_polyline_in_prose`, `feedback_interpolated_pr_pattern`, `feedback_on_route_checks`, `feedback_corridor_commune_name_collisions`, `feedback_ci_seed_ordering`, `feedback_shared_tree_branch_verification`, `feedback_strand_session_self_cleanup`, `reference_tdf26_entry_visual_components`, `reference_draft_entry_preview`, `reference_worktree_node_modules_build`, `feedback_streetview_candidates`. (Barthes arc spent at seg 15; Meymac/saintsbury voice was seg 25.)

## 10. Stop when

- **Both** entries drafted (renamed, house length per the confirmed targets), validators green, publisher-confirmed dev previews; **two PRs** open against `main` (open a tracking issue per entry, `Refs #N`), each left `draft: true` (publisher flips at publish; publisher sets `publishDate` in-strand).
- **Cleanup (you run):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-seg-26` and `.../tdf26-seg-27` once each merges (`feedback_strand_session_self_cleanup`).
- Final report: both PR links, chosen slugs, voice registers, confirmation that **(a) the Ventadour payoff and accordion callback landed in seg 27, (b) the abbey-architecture echo landed in seg 26, and (c) the seg-27/#502 split was honoured (no duplicated cycling history).** Note that seg 27 closes the 27-entry project.
- **Retro inputs** to `project_next_planning_notes.md` under `## Items surfaced during seg-26-drafting...` and `## Items surfaced during seg-27-drafting...` (this is the final content strand — flag anything the endgame/wind-down planning should know).
