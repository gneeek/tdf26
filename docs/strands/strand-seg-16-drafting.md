# Strand: Seg 16 drafting

Drafting strand for segment 16 of the tdf26 travelogue. Authored 2026-05-24 alongside the seg 15 strand finishing, in advance of the seg 16 publish slot Wed 2026-05-27.

## 1. Goal

Land a draft of `content/entries/16-descent-from-the-monedieres.md` (currently a stub: `draft: true`, single placeholder line) ready for the publisher's pre-publish review window before the seg 16 publish (Wed 2026-05-27). Segment 16 covers km 106–112 — the descent off the Monédières massif, beginning shortly after the Suc au May summit (seg 15) and ending before the route enters the Treignac approach (seg 17). Milestone: TBD at the Mon/Tue planning session — file under v1.4.19 tail or v1.4.20 head per that session's decision.

This strand runs in **publisher-paced single-strand mode** (per `feedback_multi_strand_session_checkpoints.md`) — checkpoint at editorial micro-decisions. Spawn after seg 15 has merged so seg 16's opening can pick up the texture seg 15 ended on.

Segment 16 is the **first un-foreshadowed segment after the Barthes "develops" payoff** at seg 15 (per `project_barthes_callback.md`). The literary argument earned its development at the summit; seg 16 is the cool-down — descent, transition, watershed-crossing. The dossier (`content/research/segs-14-16-block-research.md` § Segment 16) names the Lestards thatched-roof church (Église Saint-Symphorien, one of two surviving thatched-roof churches in France) as the main concrete anchor, with the Vézère watershed as the geographic frame.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-16-draft /home/jhs/code/tdf26-seg-16 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`, and `data/segments/segment-16.gpx` directly. Per #491 / PR #507, do not transcribe CLAUDE.md tabular data. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`, `feedback_source_of_truth_framing.md`).

**Data-layer state for seg 16:** segments.json shows km 106–112, `towns=[]`, `climbs=[]` — no town centre, no categorised climb in this 6km stretch. The dossier handles this honestly: the segment passes Lestards near its end (the Lestards commune sits across the seg 16 / seg 17 boundary; the village centre is not on the polyline but is close enough to be a credible anchor per the dossier). Confirm whether Lestards belongs in seg 16's `towns` array via the GPX polyline + town-coords; if it does, file an issue for `segments.json` correction — do not fix inline (per `feedback_content_change_rule.md` for data files: data fixes are their own scope).

**Research dossier:** `content/research/segs-14-16-block-research.md` § Segment 16 (lines 121–152) is the bedrock. It names: descent profile, the Vézère watershed crossing, the Lestards thatched-roof church (Église Saint-Symphorien), historical/cultural anchors. Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding, not bedrock — verify against the cited source URLs before writing them into prose.

**Cross-segment continuity:**
- Seg 15 (already published or in-flight at strand-spawn time) ends at the Suc au May summit area. Seg 16 picks up the road descending. Read seg 15's final paragraphs for texture continuity (per `feedback_will_not_shape.md`: watch for the "the X the Y will not Z" tic).
- Seg 17 owns Treignac itself (km 112–120, town = Treignac). Do not poach Treignac material — leave it for seg 17's drafter. The Treignac approach feeling can be foreshadowed in seg 16's closing if the publisher wants that thread, but the village itself is reserved.

## 4. Target issues

No tracking issue at brief time. File one at strand start: `Seg 16 drafting strand`, milestone TBD (v1.4.19 tail or v1.4.20 head). PR closes whatever issue is opened.

## 5. Workflow per issue

Cadence is publisher-paced via AskUserQuestion checkpoints. List of checkpoints (not prose-writing steps):

1. **Read the seg 16 data** (segments.json, town-coords.json, GPX polyline, elevation profile). Read the segs-14-16 dossier § Segment 16. Read the tour-history dossier for any descent-corridor entries.
2. **Read seg 15 published entry** to absorb the texture immediately preceding the descent. Note the summit beat seg 15 landed on; seg 16 starts the cool-down from there.
3. **Voice register checkpoint** (AskUserQuestion). Voice picked at draft time; the `tdf26-voice` skill provides options. Per `feedback_voice_checkpoint_prep.md`: read the candidate register SKILL.md briefs before firing the checkpoint, so the choice is between substantive options the publisher can evaluate. The "descent / cool-down / watershed-crossing" texture pulls voice differently than seg 15's summit beat — quieter, slower, transitional. The publisher decides. Do not start drafting until voice is fixed.
4. **Arc agreement checkpoint** — confirm seg 16 owns the descent + the Lestards anchor; confirm whether to plant Treignac foreshadow at the closing (seg 17 owns the village). Confirm the Vézère watershed framing belongs here vs in seg 17. The Plateau de Millevaches arc (segs 18-22) is reserved; do not float it.
5. **First draft** — write to chosen voice. Descent + watershed primary; the Lestards thatched-roof church as the concrete cultural anchor; the absence of a categorised climb as a deliberate framing (not a gap). Verify factual claims against source URLs before they hit prose. Mind the seg 16/17 boundary at km 112.
6. **First draft review** — publisher reads; AskUserQuestion at factual calls and cross-segment threads. Watch for the "the X the Y will not Z" tic per `feedback_will_not_shape.md`.
7. **Revisions** — apply publisher edits.
8. **Sources section + disclosure footer** — `## Sources` per `feedback_sources_section.md` (external URLs only per `feedback_sources_no_internal.md`); pair-writing + voice-register footer per `project_disclosure_practice.md`.
9. **PR open against `main`** — title `seg 16 draft: <subtitle>`; body lists voice picked, AskUserQuestion checkpoints fired, any new issues filed.

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
- `project_meymac_voice.md` (Saintsbury reserved for a later Meymac segment — but the memory's seg-number reference needs verification per the v1.4.19 close-out planning surface; do not float Saintsbury here regardless).
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
