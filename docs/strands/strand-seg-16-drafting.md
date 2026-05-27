# Strand: Seg 16 drafting

Drafting strand for segment 16 of the tdf26 travelogue. Authored 2026-05-24 alongside the seg 15 strand finishing, in advance of the seg 16 publish slot Wed 2026-05-27.

> **Revised 2026-05-27 (planning session).** The original brief named Lestards (thatched-roof church) as seg 16's central anchor and assigned Treignac to seg 17. Both are wrong (see [#596](https://github.com/gneeek/tdf26/issues/596) close-out): Lestards is seg 19, Treignac is seg 18, and seg 16 has no on-route town, climb, or historical-TdF event. The publisher's 2026-05-27 framing decision is **descent-primary with the Vézère watershed as the geographic spine, target ~800 words** (low end of the 800–1200 window), conditional on verifying the watershed claim at draft time. Milestone set to **v1.4.20** (v1.4.19 closed). Sections below reflect the revision.

## 1. Goal

Land a draft of `content/entries/16-descent-from-the-monedieres.md` (currently a stub: `draft: true`, single placeholder line) ready for the publisher's pre-publish review window before the seg 16 publish (Wed 2026-05-27). Segment 16 covers km 106–112 — the descent off the Monédières massif, beginning shortly after the Suc au May summit (seg 15) and running down toward the Madranges approach (seg 17). Milestone: **v1.4.20**.

This strand runs in **publisher-paced single-strand mode** (per `feedback_multi_strand_session_checkpoints.md`) — checkpoint at editorial micro-decisions. Seg 15 has merged (PR #608, published 2026-05-24), so seg 16's opening can pick up the texture seg 15 ended on.

Segment 16 is the **first un-foreshadowed segment after the Barthes "develops" payoff** at seg 15 (per `project_barthes_callback.md`). The literary argument earned its development at the summit; seg 16 is the cool-down — descent, transition, watershed-crossing. **The honest framing is descent-without-climb-without-village as a deliberate beat, not a gap.** The day's spine is the descent profile (max -8.6%, average -4.4%, 261 m of elevation loss over 6 km) plus the Vézère-catchment crossing as the geographic frame, with the Monédières sucs (Puy de la Monédière, Puy de la Jarrige, Puy Messou) receding to the east. Target **~800 words**.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-16-draft /home/jhs/code/tdf26-seg-16 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`, and `data/segments/segment-16.gpx` directly. Per #491 / PR #507, do not transcribe CLAUDE.md tabular data. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`, `feedback_source_of_truth_framing.md`).

**Data-layer state for seg 16:** segments.json shows km 106–112, `towns=[]`, `climbs=[]` — no on-route town centre, no categorised climb in this 6 km stretch, and no historical-TdF event keyed to it. This is correct, not a data gap. The one attraction near the segment (Suc au May table d'orientation, km 105.48, 442 m off polyline) is really a seg 15 anchor — **do not lean on it.** Do not add anything to `data/segments.json`; if drift is surfaced, file an issue (per `feedback_content_change_rule.md` for data files).

**Corrected corridor mental model** (verified against `data/town-coords.json`, updated under PR #498 — the original brief had this wrong):
- **seg 16 (km 106–112):** pure descent. No on-route town, climb, or historical event.
- **seg 17 (km 112–120):** Madranges (65 m off polyline) — seg 17's only on-route town.
- **seg 18 (km 120–128):** Treignac (22 m off polyline at km ~122).
- **seg 19 (km 128–136):** Lestards (12 m off polyline at km 130.39) — the thatched-roof church belongs to **seg 19**, not seg 16. Reserved for seg 19's drafter.

**Vézère watershed — verify before any prose makes a hydrography claim.** The dossier's working hypothesis is that the route crosses into the Vézère catchment at or near the Suc au May summit, making the seg 16 descent the entry into the Vézère basin. This is the chosen geographic spine, but it is **unverified**. Confirm against Sandre (sandre.eaufrance.fr) and/or Géoportail before writing it as fact. **If it does not verify, fall back to the tight descent beat** (descent profile + Monédières receding east) and drop the watershed framing rather than hedge it into the prose.

**Research dossier:** `content/research/segs-14-16-block-research.md` § Segment 16 is the bedrock for descent profile and cultural-corridor context. Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding, not bedrock — verify against the cited source URLs before writing them into prose. Note the dossier hedged on Lestards' segment assignment (it was right to); the original brief converted the hedge into stated fact, which is the error #596 caught.

**Available non-poaching threads** (with Lestards removed): the descent profile itself; the Monédières sucs receding east; the Vézère-watershed crossing (if verified); the 2020 TdF Stage 12 Hirschi solo (climbed the opposite direction, but this descent line was his solo-pressing corridor — a reverse-direction callback); and a light forward foreshadow toward Madranges (seg 17). The Plateau de Millevaches arc (segs 18–22) is reserved — do not float it.

**Cross-segment continuity:**
- Seg 15 ends at the Suc au May summit area. Seg 16 picks up the road descending. Read seg 15's final paragraphs for texture continuity (per `feedback_will_not_shape.md`: watch for the "the X the Y will not Z" tic, and per `feedback_avoid_polyline_in_prose.md`: say "the road" / "the parcours", never "polyline").
- **Treignac is reserved for seg 18, not seg 16.** A light approach-foreshadow toward Madranges (seg 17) is acceptable at the close; named villages downstream are reserved for their own drafters.

## 4. Target issues

Tracking issue already exists: [#596](https://github.com/gneeek/tdf26/issues/596) (`Seg 16 drafting strand`), milestone **v1.4.20**. It holds the held-strand close-out comment with the corrected framing. PR body: `Closes #596` (per `feedback_pr_closure_keywords.md`).

## 5. Workflow per issue

Cadence is publisher-paced via AskUserQuestion checkpoints. List of checkpoints (not prose-writing steps):

1. **Read the seg 16 data** (segments.json, town-coords.json, GPX polyline, elevation profile). Read the segs-14-16 dossier § Segment 16. Read the tour-history dossier for any descent-corridor entries.
2. **Read seg 15 published entry** to absorb the texture immediately preceding the descent. Note the summit beat seg 15 landed on; seg 16 starts the cool-down from there.
3. **Voice register checkpoint** (AskUserQuestion). Voice picked at draft time; the `tdf26-voice` skill provides options. Per `feedback_voice_checkpoint_prep.md`: read the candidate register SKILL.md briefs before firing the checkpoint, so the choice is between substantive options the publisher can evaluate. The "descent / cool-down / watershed-crossing" texture pulls voice differently than seg 15's summit beat — quieter, slower, transitional. Seg 15 was tls-essay continuity; a register that suits a short exhale may differ. The publisher decides. Do not start drafting until voice is fixed.
4. **Verify the Vézère watershed claim** (Sandre / Géoportail) before the arc checkpoint, so the arc conversation knows whether the spine holds. If it does not verify, the arc collapses to the tight descent beat.
5. **Arc agreement checkpoint** — confirm seg 16 is descent-primary with the Vézère watershed as the geographic spine (or the tight beat if the watershed didn't verify); confirm the ~800-word target; confirm a light Madranges (seg 17) approach-foreshadow at the close is wanted. Treignac (seg 18), Lestards (seg 19), and the Plateau arc (segs 18–22) are all reserved — do not float them.
6. **First draft** — write to chosen voice, target ~800 words. Descent profile as the spine; Vézère-catchment crossing as the geographic frame (only if verified); the absence of a categorised climb as a deliberate cool-down beat, not a gap. Verify factual claims against source URLs before they hit prose. Mind the seg 16/17 boundary at km 112.
7. **First draft review** — publisher reads; AskUserQuestion at factual calls and cross-segment threads. Watch for the "the X the Y will not Z" tic per `feedback_will_not_shape.md`.
8. **Revisions** — apply publisher edits.
9. **Sources section + disclosure footer** — `## Sources` per `feedback_sources_section.md` (external URLs only per `feedback_sources_no_internal.md`); pair-writing + voice-register footer per `project_disclosure_practice.md`.
10. **PR open against `main`** — title `seg 16 draft: <subtitle>`; body lists voice picked, AskUserQuestion checkpoints fired, any new issues filed; `Closes #596`.

## 6. Verification commands

- `npm test` — entry-shape assertions pass.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — entry passes shape + MDC balance checks. Use any MDC blocks deliberately.
- `python3 processing/validate_points.py` — no regression.
- `npm run build` and dev preview at `/entries/16-descent-*`: render renders, ElevationChart shows the segment profile, image gallery placeholder renders. Per `project_dev_server_content_index.md`: if the entry doesn't show in dev after the branch switch, delete `.data/content/contents.sqlite*` and restart dev.
- **Pre-publish scrutiny** per `feedback_pre_publish_scrutiny.md`: verify geography, attribution, image rights before publish.sh runs.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `content/entries/16-descent-from-the-monedieres.md` (overwrite stub).
  - `public/images/segment-16/*` if any publisher-supplied images land in the draft window.
- **What this strand reads:**
  - `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`.
  - `data/segments/segment-16.gpx`, `data/elevation/segment-16.json`.
  - `content/entries/15-suc-au-may-the-fierce-one.md` (texture continuity, once merged).
  - `content/research/segs-14-16-block-research.md` § Segment 16.
  - `content/research/tour-history-research.md` for any descent-corridor entries.
- **What this strand must NOT touch:**
  - Other published entries (per `feedback_content_change_rule.md`).
  - `data/segments.json` even if Lestards' inclusion in seg 16's towns array looks wrong — file an issue.
  - Any file owned by a sibling strand (none active at strand-spawn time; sibling research strand for segs 17-19 reads its own files).

## 8. Scope discipline

- **Do not modify published entries** (per `feedback_content_change_rule.md`). Corrections from seg 15 forward go into the seg 16 entry's framing.
- **Do not retroactively edit data files** even if drift is surfaced; file an issue and tag it.
- **AskUserQuestion fires at the voice checkpoint, the arc-agreement checkpoint, the first-draft review, and any factual call the publisher should weigh in on.** Implementation steps in between are not checkpointed.
- **If the publisher prefers to defer:** acceptable outcome is "voice checkpoint fires, publisher chooses 'slip seg 16 to Sun 2026-05-31, push seg 17 to Wed 2026-06-03'". Close the strand with the draft state captured; do not push a forced draft.

## 9. Memories that apply

- `project_barthes_callback.md` (seg 16 is the cool-down after the seg 15 payoff).
- `project_meymac_voice.md` (Saintsbury reserved for seg 25 / Meymac abbey, retargeted from seg 24 during the seg 23-27 verification strand; do not float Saintsbury here).
- `feedback_avoid_polyline_in_prose.md` (say "the road" / "the parcours", never "polyline" in prose).
- `feedback_content_change_rule.md`.
- `feedback_pre_publish_scrutiny.md`.
- `feedback_literary_footnotes.md`.
- `feedback_sources_section.md`, `feedback_sources_no_internal.md`.
- `project_disclosure_practice.md`.
- `feedback_will_not_shape.md`.
- `feedback_brief_content_is_carryforward.md`.
- `feedback_voice_checkpoint_prep.md`.
- `feedback_multi_strand_session_checkpoints.md` (publisher-paced).
- `feedback_source_of_truth_framing.md`.
- `feedback_on_route_checks.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_strand_worktree_path.md`.
- `project_dev_server_content_index.md`.

## 10. Stop when

- PR opened against `main`, `Closes #<tracking>` in body.
- Voice + arc checkpoints fired and answered; choices documented in PR body.
- First-draft review checkpoint fired; publisher signed off on the draft (or named the slip).
- `## Sources` section present (or omitted with rationale).
- Disclosure footer present.
- `npm test` + entry validators green; `npm run build` green.
- Dev preview rendered without error.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-seg-16` once the PR has merged.
- Final report posted to publisher: PR link, voice picked, checkpoints fired, any data-layer follow-ups filed.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during seg-16-drafting strand execution (<date>)`:
  - **Decision-actionable observations:** any seg 17 / 18 content threads opened, any data-file follow-ups filed, Lestards-in-segments.json finding.
  - **Light-tier pattern observations:** Barthes cool-down beat shape, descent-without-climb framing.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock.
