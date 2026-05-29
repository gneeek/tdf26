# Strand: seg 18 drafting — Treignac, the Vézère bridges, the Croix de Pey base

Publisher-paced single-segment drafting strand (deviation: "Workflow" lists the publisher checkpoints, not the prose-writing steps; cadence is publisher-driven). Mirrors the seg 15 / seg 16 / seg 17 drafting strands.

## 1. Goal

Draft `content/entries/18-*.md` (currently the stub `18-cote-de-la-croix-de-pey.md`) for the **Wed 2026-06-03** publish slot, 800–1,200 words, from `content/research/segs-17-19-block-research.md` ("Segment 18" section). Seg 18 is the day's pivot: the route enters **Treignac** (km 121.73), crosses the **Vézère on the medieval bridge** (km 121.99), passes **Église Notre-Dame-des-Bans** (km 122.06), and the **Côte de la Croix de Pey** *begins* here at the bridge (segments.json: seg 18 km 120–126, `towns: ["Treignac"]`, `climbs: ["Côte de la Croix de Pey"]`). **Title decision is a checkpoint:** the seg-17 strand handed off the "Treignac — Granite and Water" frame to this segment (the local *paire de matériaux* touristic catchphrase; granite for the village stones, water for the Vézère gorge). The stub slug `18-cote-de-la-croix-de-pey` foregrounds the climb, but the climb *crests* in seg 19 — seg 18 is the town + bridges + climb-base. Recommend retitling to a Treignac/granite-and-water anchor and leaving the Croix-de-Pey crest beat to seg 19; confirm at the anchor checkpoint.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-18-draft /home/jhs/code/tdf26-seg-18 main
```

- Explicit-path worktree; no nesting, no `.claude` symlink. `git branch --show-current` → `feature/seg-18-draft` before each commit.
- Rename the stub via `git mv` once the new slug is chosen (per the seg 12/13/17 precedent), don't create a second file.
- Fresh worktree: `npm ci` + seed rider data (`cp data/riders/*.example.json` to non-example names, per `feedback_ci_seed_ordering.md`) before any `npm run build` / dev preview.
- **Single-strand, orchestrator-session only — do not spawn sub-agents for the drafting itself** (per the seg-13 finding, spawned agents don't surface AskUserQuestion cleanly; publisher-paced drafting runs in the orchestrator session).
- **Image frontmatter: use the inline-JSON form, not the YAML list** (the form #479 documents; the YAML list is what crashed publish.sh on seg 9). If #479 has landed, follow the CLAUDE.md note; if not, inline JSON regardless.

## 3. Source-of-truth posture

- **Verify named on-route anchors against `data/town-coords.json` + the seg-18 GPX polyline before writing prose around them.** The dossier gives off-polyline distances (Treignac entry 134 m, medieval bridge 81 m, Notre-Dame-des-Bans 68 m, **Pont de la Tourmente 319 m**) — confirm against the polyline.
- The dossier is research bedrock, but per `feedback_brief_content_is_carryforward.md` it is scaffolding — re-verify load-bearing claims before they become published assertions. The dossier itself flags several:
  - **"Pont de la Tourmente" is unverified as a documented Treignac bridge.** Treignac's three documented bridges are the **Vieux Pont / Pont Médiéval (1285, MH Mérimée PA00099910)**, the **Pont Finot (1822–24)**, and the **Pont Bargy (1840)**. **Do NOT write "Pont Médiéval and Pont de la Tourmente" as the same bridge — they are not — and do not use "Pont de la Tourmente" as a primary name until ground-truthed.** File an issue if `data/attractions.json` references it (per the dossier's #145 recommendation).
  - **Treignac is NOT a Plus Beau Village** — it held the label 1989, **lost it in 2008**, and now holds **Petite Cité de Caractère®**. Write it as the latter.
- Do NOT transcribe CLAUDE.md tabular data. Narrative project context only.

## 4. Anchors available (from the dossier)

- **The bridges + granite-and-water frame.** Vieux Pont (1285, three-span Gothic, local granite, MH-listed, ~600 years the only crossing); the Vézère gorge and dam-fed rapids (Saut du Loup just downstream); the village's granite-and-half-timbered character (Porte Chabirande, Maison des Gardes balcony). The inherited frame from seg 17.
- **The Hundred Years' War sack (verified).** Rodrigue de Villandrando (*L'Écorcheur*) sacked Treignac in **1438** to recover 1,000 écus owed by Jean de Comborn; the Halle was rebuilt 1484. The Comborn viscounty explains the walls, three charters (1205/1284/1438), and a market hall worth pillaging.
- **The clocher tors.** Chapelle Notre-Dame-de-la-Paix, built **1626** *outside* the walls (inter-confessional tension, post-Wars-of-Religion settlement, not post-Edict-of-Nantes); twisted bell tower, hexagonal base / octagonal twisted spire rotated 1/16 turn, "only example in France … deliberately treated fantastically," one of ~100 in Europe.
- **Cycling: the 2020 Stage 12 directional inversion** — the seg 18 cycling anchor. 2020 *descended* Croix de Pey into Treignac (Hirschi made the decisive front group there); 2026 *climbs* it out. This climb out of Treignac is now the first hard test of the day's back half (Suc au May already done seg 15, Mont Bessou ahead seg 22). On the contested climb numbers (#551) and summit-km drift (#591): **write the climb on its road shape and its 2020 inversion frame, not on a categorisation figure** — three sources disagree (2020 ASO roadbook 3.8 km @ 6.1% is the tightest; points-config 7.0 km @ 4.4%; mycols 6.4 km @ 5.1%) and the 2026 ASO category is not yet published. The crest is a seg 19 beat; seg 18 owns the *base*.
- **Famous local people (strong here).** **Charles Lachaud (1817–1882)** — Treignac-born, the Second Empire's most famous trial lawyer (defended Marie Lafarge, Maréchal Bazaine, Courbet, Troppmann); the segment's strongest local-person anchor. **Marc Sangnier (1873–1950)** — Lachaud's grandson, founder of *Le Sillon* and the French youth-hostel movement, buried in the Treignac cemetery (Place Marc Sangnier fronts Notre-Dame-des-Bans; the family house is now the Musée des Arts et Traditions Populaires). **Edmond Tapissier (1861–1943)** — painter who designed Gobelins tapestries on Limousin trades, died in Treignac; optional.
- **Kayak heritage.** Treignac hosted the **first canoë-kayak descente World Championships in 1959** (the founding of the discipline as a world-championship sport); returned 2000 and 2022. A verified water lineage on the same gorge the riders' bridge crosses — pairs with the "water" half of granite-and-water. (Pentecost 2026 = 24 May, the local kayakers' dress rehearsal, one week before seg 17 published.)

## 5. Workflow (publisher checkpoints — the cadence)

Fire these as AskUserQuestion in the orchestrator session; iterate in free-form chat between them.

1. **Anchor/title checkpoint (run first, before voice):** confirm the retitle (Treignac / granite-and-water vs the stub's Croix-de-Pey framing) and the lead anchor (the bridges? Lachaud? the 2020 inversion?). Confirm seg 18 owns the climb *base* and hands the *crest* to seg 19.
2. **Voice register:** pre-read candidate register SKILL.md briefs *before* firing (per `feedback_voice_checkpoint_prep.md`). Seg 17 chose a register for the post-Suc-au-May approach sub-arc — present continuity-with-seg-17 vs a break as a genuine fork, with one-line trade-offs.
3. **Promises-inherited check:** enumerate forward-looking promises seg 17 made that seg 18 must honour or defer (the approach-to-Treignac handoff from seg 17; the granite-and-water frame seg 17 flagged as seg 18's; the climb-crest deferred to seg 19). Confirm pick-up vs hand-on.
4. **First-draft review.**
5. **Fact-duplication audit pass** (seg-15 finding) between draft revisions and Sources/disclosure — catch prose/footnote/Sources triple-duplication before sign-off.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `npm test`
- `npm run build` then a `nuxt generate` preview (not the SSR runtime, per `feedback_production_preview.md`); entry stays `draft: true` through drafting — do NOT flip `draft: false` in the drafting PR (the publisher flips at publish time; #617's pre-flight enforces it).
- MDC balance: if any `::name{...}` directives are used, rely on the validator's directive check (PR #563) or grep opens vs closes.

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/18-*.md` (the renamed seg 18 entry) only; possibly `data/historical-tdf.json` *only if* the 2020 Stage 12 / 2017 Tour du Limousin card needs a seg-18 key added (the dossier flags both as candidate additions — verify they aren't already keyed; if adding, that is a sibling PR, not mixed into the draft).
- **Reads:** the 17-19 dossier, `data/segments.json`, `data/town-coords.json`, seg-18 GPX, `data/attractions.json`.
- **Must NOT touch:** any other `content/entries/*.md` (published entries are fixed, `feedback_content_change_rule.md`); the seg 17 entry (published by the time this runs) or the seg 19 stub; `data/` beyond an optional historical-tdf card. Out-of-scope edits open as **sibling PRs** off main (`feedback_interpolated_pr_pattern.md`), not in the draft PR.
- **Data corrections in the corridor:** #551 (Croix de Pey numbers) and #591 (summit km) — **do not fix inline**; write the entry per the dossier's "road shape, not the figure" recommendation and leave the data issues open. #602 (Pont de la Tourmente) and the Treignac-PBVF correction — file/confirm as data issues, don't fix in the draft.
- **Parallel-safety:** orthogonal to the pipeline strands (touches `content/`, not `scripts/`); safe to run alongside the gate/spine/ceremony. Safe alongside seg 19 drafting (different entry file) — but the two share the climb: agree the **base (seg 18) vs crest (seg 19)** split at the seg 18 anchor checkpoint so the climb isn't written twice.

## 8. Scope discipline

- File new issues for findings outside the entry write-set; don't over-scope.
- Style tics to actively avoid (cross-entry grep before sign-off): the **"the X the Y will not Z" shape** (`feedback_will_not_shape.md`), the word **"polyline" in prose** (`feedback_avoid_polyline_in_prose.md` — use "the road" / "the parcours"), em-dashes and exclamation marks (project standard: zero), internal-data citations in Sources (`feedback_sources_no_internal.md` — external URLs only).
- Literary references get proper footnotes (`feedback_literary_footnotes.md`); optional `## Sources` (`feedback_sources_section.md`); per-entry pair-writing/voice disclosure footer (`project_disclosure_practice.md`).

## 9. Memories that apply

- `feedback_content_change_rule.md`, `feedback_brief_content_is_carryforward.md`, `feedback_pre_publish_scrutiny.md`, `feedback_voice_checkpoint_prep.md`, `feedback_literary_footnotes.md`, `feedback_sources_section.md`, `feedback_sources_no_internal.md`, `project_disclosure_practice.md`, `feedback_will_not_shape.md`, `feedback_avoid_polyline_in_prose.md`, `feedback_interpolated_pr_pattern.md`, `feedback_on_route_checks.md`, `feedback_corridor_commune_name_collisions.md`, `feedback_ci_seed_ordering.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_session_self_cleanup.md`. (Barthes arc spent at seg 15 — no obligation. Meymac/saintsbury voice is seg 25, not here.)

## 10. Stop when

- Renamed seg 18 entry drafted (800–1,200 words), validators green, dev preview confirmed by publisher; PR open against `main` (open a seg-18 tracking issue if none exists; `Refs #N`).
- Entry left `draft: true` (publisher flips at publish time).
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-seg-18` once merged.
- Final report: PR link, chosen slug, voice register, the base/crest split agreed with seg 19, promises picked-up vs deferred, any issue filed (esp. Pont de la Tourmente / PBVF).
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during seg-18-drafting strand execution (<date>)`: decision-actionable observations, light-tier pattern observations, numeric stats (word count, footnotes, MDC directives, em-dash/exclamation counts, checkpoint cycles, wall-clock).
