# Strand: seg 17 drafting — the Treignac approach via Madranges

Publisher-paced single-segment drafting strand (deviation: "Workflow" lists the publisher checkpoints, not the prose-writing steps; cadence is publisher-driven). Mirrors the seg 13 / seg 15 drafting strands.

## 1. Goal

Draft `content/entries/17-*.md` (currently a 9-word stub) for the **Sun 2026-05-31** publish slot, 800-1,200 words, from `content/research/segs-17-19-block-research.md`. **The stub is mis-titled** `17-treignac-granite-and-water.md` — that title belongs to seg 18 (Treignac proper + the "Granite and Water" frame). Seg 17's verified content is **Madranges + the approach to Treignac across the Vézère gorges** (segments.json: seg 17 km 112-120, `towns: ["Madranges"]`, no climbs). Re-title at the arc/anchor checkpoint to a Madranges/approach anchor; flag that seg 18 likely wants the "Treignac — Granite and Water" frame.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-17-draft /home/jhs/code/tdf26-seg-17 main
```

- Explicit-path worktree; no nesting, no `.claude` symlink. `git branch --show-current` → `feature/seg-17-draft` before each commit.
- Rename the stub via `git mv` once the new slug is chosen (per the seg 12/13 precedent), don't create a second file.
- Fresh worktree: `npm ci` + seed rider data (`cp data/riders/*.example.json` to non-example names, per `feedback_ci_seed_ordering.md`) before any `npm run build` / dev preview.
- **Single-strand, orchestrator-session only — do not spawn sub-agents for the drafting itself.** Per the seg-13 finding, spawned agents don't surface AskUserQuestion cleanly; publisher-paced drafting runs in the orchestrator session so checkpoints fire directly.

## 3. Source-of-truth posture

- **Verify named on-route anchors against `data/town-coords.json` + the seg-17 GPX polyline before writing any prose around them** (the seg-16 strand's hardest-won lesson — a brief that named the wrong segment's anchor would have cost a whole draft). Madranges bourg is ~65 m off the polyline at ~km 113.5; confirm.
- The dossier (`segs-17-19-block-research.md`, "Segment 17" section) is the research bedrock, but per `feedback_brief_content_is_carryforward.md` the dossier is scaffolding — re-verify load-bearing claims (the 1900 Protestant temple date + architect, the watershed hypothesis which the dossier explicitly flags as **unverified by Géoportail**) before they become assertions in published prose.
- Do NOT transcribe CLAUDE.md tabular data. Narrative project context only.

## 4. Anchors available (from the dossier)

- **Madranges Protestant temple** — Protestantism arrived 1898; temple inaugurated **11 March 1900**, architect **Adolphe Augustin Rey** (Paris-trained, social-housing). An isolated upland Corrèze commune turning Protestant in 1898 is the segment's distinctive small-history beat. (Verify date + architect.)
- **Église Saint-Barthélemy** — older Catholic village set-piece.
- **The approach** — the medieval town of Treignac becoming visible across the Vézère gorges; *paysage à l'orée* register, looking onto the town rather than the massif. The dossier names this as the seg 17 frame.
- **Landscape transition** — leucogranite basement continues from the Monédières; the open *lande* gives way to closed conifer plantation (Douglas-fir / sitka — the 20th-c. *fermeture paysagère*).
- **No cycling-history beat** — the corridor's pro-cycling shadow is seg 18 (the 2020 Croix de Pey inversion). Per the dossier: write seg 17 as the approach; do not force a Tour beat.

## 5. Workflow (publisher checkpoints — the cadence)

Fire these as AskUserQuestion in the orchestrator session; iterate between them in free-form chat.

1. **Anchor/title checkpoint (run first, before voice):** confirm the re-title (seg 17 = Madranges/approach, not Treignac) and the anchor selection (Protestant temple as the lead small-history beat? approach-as-frame?). This doubles as the "brief-reset" checkpoint the seg-16 strand showed is the right move when verification changes the framing.
2. **Voice register:** pre-read the candidate register SKILL.md briefs *before* firing (per `feedback_voice_checkpoint_prep.md`). Seg 14-15 ran TLS-essay continuity; seg 17 opens a new sub-arc (post-Suc-au-May, the quiet approach) — present continuity vs a register break as a genuine fork, with one-line trade-offs. Survey, then ask.
3. **Promises-inherited check (Retro v1.4.19 "what we lack" #2):** before drafting, enumerate the forward-looking promises earlier entries made that seg 17 must honour or consciously defer — the seg 16 close handed off the road descending toward the next commune; the Paris-continuation foreshadow planted earlier; the Monédières range is *spent* (seg 13 planted it, seg 15 earned it). Confirm what seg 17 picks up vs leaves for seg 18.
4. **First-draft review.**
5. **Fact-duplication audit pass** (codified from the seg-15 finding) between first-draft revisions and Sources/disclosure — catch prose/footnote/Sources triple-duplication before sign-off.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `npm test`
- `npm run build` then a **`nuxt generate`** preview (not the SSR runtime, per `feedback_production_preview.md`) — note the entry stays `draft: true` through drafting, so confirm rendering on the most-recent *published* entry, or temporarily preview with draft included; do NOT flip `draft: false` in the drafting PR (the publisher flips it at publish time, and #617 is adding the pre-flight).
- MDC balance: if any `::name{...}` directives are used, grep opens vs closes (or rely on the #561/PR #563 validator now in `validate_entries.py`).

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/17-*.md` (the renamed seg 17 entry) only; possibly `data/historical-tdf.json` *only if* a card is added (unlikely — no seg 17 cycling beat).
- **Reads:** the 17-19 dossier, `data/segments.json`, `data/town-coords.json`, seg-17 GPX, `data/attractions.json`.
- **Must NOT touch:** any other `content/entries/*.md` (published entries are fixed, `feedback_content_change_rule.md`); seg 18/19 stubs; `data/` beyond an optional historical-tdf card. Out-of-scope edits authorised mid-strand open as **sibling PRs** off main (`feedback_interpolated_pr_pattern.md`), not mixed into the draft PR.
- **Data corrections in the corridor** (#549 Sprint-Bugeat, #551 Croix de Pey, #602 Pont de la Tourmente, #603 2017 TdL keying) are seg 18/19 concerns — note if seg 17 surfaces anything, file an issue, don't fix inline.

## 8. Scope discipline

- File new issues for findings outside the entry write-set; don't over-scope.
- Style tics to actively avoid (cross-entry pattern grep before sign-off): the **"the X the Y will not Z" shape** (`feedback_will_not_shape.md` — overused seg 6-12), the word **"polyline" in prose** (`feedback_avoid_polyline_in_prose.md` — use "the road" / "the parcours"), em-dashes and exclamation marks (project standard: zero), internal-data citations in Sources (`feedback_sources_no_internal.md` — external URLs only).
- Literary references get proper footnotes (`feedback_literary_footnotes.md`); optional `## Sources` section (`feedback_sources_section.md`); per-entry pair-writing/voice disclosure footer (`project_disclosure_practice.md`).

## 9. Memories that apply

- `feedback_content_change_rule.md`, `feedback_brief_content_is_carryforward.md`, `feedback_pre_publish_scrutiny.md`, `feedback_voice_checkpoint_prep.md`, `feedback_literary_footnotes.md`, `feedback_sources_section.md`, `feedback_sources_no_internal.md`, `project_disclosure_practice.md`, `feedback_will_not_shape.md`, `feedback_avoid_polyline_in_prose.md`, `feedback_interpolated_pr_pattern.md`, `feedback_on_route_checks.md`, `feedback_ci_seed_ordering.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_worktree_path.md`, `feedback_strand_session_self_cleanup.md`. (Barthes arc is spent at seg 15 — no seg 17 obligation. Meymac/saintsbury voice is seg 25, not here.)

## 10. Stop when

- Renamed seg 17 entry drafted (800-1,200 words), validators green, dev preview confirmed by publisher; PR open against `main` closing/`Refs` the seg 17 tracking issue (open one if none exists).
- Entry left `draft: true` (publisher flips at publish time).
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-seg-17` once merged.
- Final report: PR link, the chosen slug, voice register used, promises picked-up vs deferred to seg 18, any issue filed.
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during seg-17-drafting strand execution (<date>)`: decision-actionable observations, light-tier pattern observations, numeric stats (word count, footnotes, MDC directives, em-dash/exclamation counts, checkpoint cycles, wall-clock).
