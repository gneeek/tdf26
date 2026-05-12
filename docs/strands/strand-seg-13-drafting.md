# Strand: Seg 13 drafting

Drafting strand for segment 13 of the tdf26 travelogue. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Land a draft of `content/entries/13-*.md` ready for the publisher's pre-publish review window before the seg 13 publish (Sun 2026-05-17 if the cadence holds). Segment 13 covers km 84–92 (Puy de Lachaud crest into the Chaumeil-approach plateau). Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/19) (subject to renumbering per Topic 9a). Hard deadline: roughly Sat 2026-05-16 evening.

This strand runs in **publisher-paced single-strand mode** (per `feedback_multi_strand_session_checkpoints.md` 2026-05-07 sharpening) — checkpoint at editorial micro-decisions. Spawn after seg 12 has shipped (or has at least been drafted to publisher-review state); voice and beat choices for seg 13 should compose with seg 12.

The dossier flagged seg 13 as the **"between-places" texture beat** — the route is leaving Naves and approaching Chaumeil but neither is the anchor; the prose must work with the absence of a destination. Reserve Monédières framing entirely (seg 14+ territory).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-13-draft /home/jhs/code/tdf26-seg-13 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-13.gpx` directly. Per #491 / PR #507, do not transcribe CLAUDE.md tabular data. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`, `feedback_source_of_truth_framing.md`).

`content/research/segs-11-13-block-research.md` (committed via PR #501) is the primary content input. Seg 13's section in the dossier flags the "between-places" texture, granitic plateau geology, and the carryforward-gating that keeps Monédières framing reserved. Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding — verify cited sources before writing them into prose.

Note the seg-13/14 boundary: per the seg 14-16 verification (PR #514), Chaumeil sits in seg 15 (km 100.30) and the seg 14/15 line is at km 99.4. Seg 13 ends roughly at km 92, so Chaumeil is not even in seg 14 — it's two segments away. Drafters who reach for a Chaumeil callback in seg 13 should resist; the texture beat works precisely because the destination is still distant.

## 4. Target issues

No tracking issue at brief time. If the strand opens its own, file at strand start: `Seg 13 drafting strand`, milestone v1.4.19. PR closes whatever issue is opened.

## 5. Workflow per issue

Cadence is publisher-paced via AskUserQuestion checkpoints. List of checkpoints (not prose-writing steps):

1. **Read seg 13 section of dossier** + factor in seg 11 + seg 12 publication learnings.
2. **Voice register checkpoint** (AskUserQuestion). Voice picked at draft time. The "between-places" texture may pull voice toward something more reflective / less landmark-driven; the publisher decides.
3. **Arc agreement checkpoint** — confirm the texture-beat framing; confirm whether to plant any Monédières-as-visible-feature foreshadow (the mountains come into view from the upper Puy de Lachaud plateau, but framing is reserved per the dossier's carryforward).
4. **First draft** — write to chosen voice. Keep "between-places" primary; granitic plateau geology as cultural anchor; the climb of Puy de Lachaud (non-categorised, regional, per #492 outcome) as the climbing beat. Verify factual claims against the dossier's source URLs.
5. **First draft review** — publisher reads; AskUserQuestion at factual calls and any cross-segment thread.
6. **Revisions** — apply publisher edits.
7. **Sources section + disclosure footer** — `## Sources` per `feedback_sources_section.md`; pair-writing + voice-register footer per `project_disclosure_practice.md`.
8. **PR open against `main`** — title `seg 13 draft: <subtitle>`; body lists voice picked, checkpoints fired, any new issues filed.

## 6. Verification commands

- `npm test` — entry-shape assertions pass.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — entry passes shape checks.
- `python3 processing/validate_points.py` — no regression.
- `npm run build` and dev preview at `/entries/seg-13-*`: render renders, ElevationChart shows the Puy de Lachaud climb, image gallery placeholder renders.
- **Pre-publish scrutiny** per `feedback_pre_publish_scrutiny.md`.
- Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `content/entries/13-*.md`. Possibly small additions to `data/historical-tdf.json` if the dossier surfaces a missing event keyed to seg 13, but default is to file an issue.
- **What this strand reads:** `content/research/segs-11-13-block-research.md`, `data/segments.json`, `data/historical-tdf.json`, `data/town-coords.json`, `data/competition/points-config.json`, `data/segments/segment-13.gpx`, `data/elevation/segment-13.json`.
- **What this strand must NOT touch:** `content/entries/11-*.md` and `content/entries/12-*.md` (already published or drafted; per `feedback_content_change_rule.md`). Monédières framing in any form (Sainte-Fortunade, Léon Dautrement quote, Bourrée des Monédières, Suc au May) — reserved for seg 14+. Mont Bessou, Meymac, Saintsbury — out of scope. STRAND-BRIEF-TEMPLATE.md untouched.
- **Cross-strand collisions:** none expected with peer drafting strands; the verification strands (#498/#499/#500) operate later in the timeline.

## 8. Scope discipline

- Default: file new issues for findings outside the strand's owned write-set.
- AskUserQuestion at material-disagreement points only; do not rubber-stamp.
- Do not retroactively edit prior entries.
- Document any publisher-approved scope overrides in the PR body.
- Resist the pull toward the destination. Seg 13 is structurally about absence; let the prose work without anchoring on Chaumeil or the Monédières peaks.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_on_route_checks.md`
- `feedback_multi_strand_session_checkpoints.md` (publisher-paced this strand)
- `feedback_content_change_rule.md`
- `feedback_pre_publish_scrutiny.md`
- `feedback_brief_content_is_carryforward.md`
- `feedback_literary_footnotes.md` (post-seg-6)
- `feedback_sources_section.md` (post-seg-6)
- `project_disclosure_practice.md` (post-seg-7)
- `project_barthes_callback.md` (seg 13 not in arc; awareness only — do not plant)
- `feedback_content_workflow.md`

## 10. Stop when

- Draft committed to `feature/seg-13-draft`; PR opened against `main`.
- All AskUserQuestion checkpoints fired and answered; publisher reviewed prose at least once.
- `npm test` + entry validators green.
- Dev preview rendered without error.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-seg-13` once the PR has merged.
- Final report posted to publisher: PR link, voice picked, AskUserQuestion checkpoints fired, any open questions surfaced for downstream strands (the Monédières opens at seg 14 — note any framing the publisher pre-decided here that's relevant for the seg 14 drafting brief later).

## 11. Notes from seg 12 close (2026-05-12, post-PR #548)

Compose-with-seg-12 details captured at seg 12 PR open, per `feedback_session_close_decision_persistence.md`.

- **Voice continuity.** Seg 12 used `madrid-review` (warmer, place-essay register; seg 11 was tls-essay). Seg 13's "between-places" texture is fair game for a third register or a return to tls-essay; not pre-decided.
- **Bowl frame closed at end of seg 12.** Seg 12 established the four-river basin between the Côte de Naves and the Puy de Lachaud as its load-bearing landscape metaphor and closed the metaphor in its final paragraph. Seg 13 has clean room for a different frame on the climb itself; reaching back for "the bowl" would feel borrowed.
- **Backward-glance hooks available.** Seg 12 left the seg-11 carnyces "in their cases on the Place de l'Église in Tintignac" as a reference point. Seg 13 may reach back further or stay forward-facing; nothing pre-committed.
- **Puy de Lachaud crest is yours.** Seg 12 stops at the climb's foot (km ~83.94); the climb summits in seg 13 at km 87.54. Seg 12's last paragraph leaves riders descending toward the Vimbelle and starting "the climb the polka-dot board will not count" — that's the handoff line. Side note from seg 12 verification: the climb is correctly named **Côte de Naves** (no s) per #515; **Puy de Lachaud** is the named hill the route crosses, not a categorised climb. Don't confuse the two.
- **Monédières-coming-into-view is yours.** Seg 12 deferred per dossier; seg 13 can plant the visibility beat without coordinating back.
- **Literary-footnote precedent at seg 12.** Seg 12 added a fresh expanded footnote (Berque + Donadieu + Hippolyte/Bossis/Burel ONCFS-Rennes I bocage study) tightening the Barthes seg-6 plant. Seg 13 is **not in the Barthes arc** per `project_barthes_callback.md` (the next arc beat is seg 15); awareness only.
- **MDC validator still not built.** Retro v1.4.18 decision-actionable item is open; manual `::name{...}` ↔ `::` grep is the stopgap. Seg 12 used 2 directives, balanced 2/2; one minute of work.
- **#547 (`data/attractions.json` divergence at Saint-Augustin retable) filed during seg 12 verification.** Affects seg 14, not seg 13, but if seg 13 reaches into attractions.json for any feature, treat the file as carryforward-suspect per `feedback_brief_content_is_carryforward.md`.
- **Title-rename precedent.** Seg 12 renamed the placeholder file slug (`12-puy-de-lachaud.md` → `12-naves-coming-home.md`) via `git mv` after the arc-agreement checkpoint settled the title direction. The placeholder slug for seg 13 is `13-chaumeil-and-the-puy-de-lachaud.md`; per the dossier, Chaumeil sits in seg 15 and the texture beat resists destination-anchoring. Expect the slug-rename question at seg 13's arc checkpoint.
