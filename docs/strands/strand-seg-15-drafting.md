# Strand: Seg 15 drafting

Drafting strand for segment 15 of the tdf26 travelogue. Authored 2026-05-24 alongside the v1.4.19 close-out parallel slate.

## 1. Goal

Land a draft of `content/entries/15-suc-au-may-the-fierce-one.md` (currently a stub: `draft: true`, single placeholder line) ready for the publisher's pre-publish review window before the seg 15 publish. Segment 15 covers km 98–106 — Chaumeil to the Suc au May summit, the **Barthes arc "develops" beat** per `project_barthes_callback.md` (segs 6 plant, 12 tighten, 15 develop). Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/52).

Publish slot: Sun 2026-05-24 per `docs/planning/NEXT.md`. The publisher has flagged "I do not have rider stats yet" as a constraint on publish.sh itself; drafting can proceed in parallel with rider-data collection. Draft must be review-ready well before stats land so the publish window is rider-data-bound, not draft-bound.

This strand runs in **publisher-paced single-strand mode** (per `feedback_multi_strand_session_checkpoints.md`) — checkpoint at editorial micro-decisions. Spawn after the seg 14 publish; voice and beat choices for seg 15 should compose with seg 14's "approach into the massif" texture.

Segment 15 is the **earned summit** — the language the seg 12 and seg 13 drafting strands were told to reserve becomes available here at the summit, not just at the approach (which seg 14 already opened). The seg 14 entry opens the Monédières framing; seg 15 lands the Suc au May summit as the argument's payoff. The crest is here.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-15-draft /home/jhs/code/tdf26-seg-15 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`, and `data/segments/segment-15.gpx` directly. Per #491 / PR #507, do not transcribe CLAUDE.md tabular data. Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`, `feedback_source_of_truth_framing.md`).

Data-layer state for seg 15: segs 14-16 verification closed via #478. `data/segments.json` lists seg 15 as km 98–106, town `Chaumeil`, climb `Suc au May` (summit ~km 105, contested category per #513). Treat the verified data as bedrock; if any verified value seems wrong at draft time, file an issue rather than retrofit prose against unverified intuition.

**Research dossier:** `content/research/segs-14-16-block-research.md` is the dossier for this block. The seg 15 section names: Chaumeil as the canonical Monédières village; Suc au May as the fierce one; the 1987 men's + women's TdF double-finish at Chaumeil (Martial Gayant won the men's; the women's Tour de France Féminin Stage 3 also finished here the same day, Saturday 11 July 1987); the Bourrée des Monédières; Léon Dautrement / the Sainte-Fortunade "morceau de Monédières perdu" quote; the L'Agglomérée cyclosportive's relationship to the Suc au May climb. Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding, not bedrock — verify against the cited source URLs before writing them into prose.

**Sibling-strand interlock:** the #513 Suc au May points-config strand is firing in parallel; the climb's declared category/gradient may change under this draft mid-flight. **Verify the resolved values in `data/competition/points-config.json` immediately before writing any climb-stat sentence**, and avoid quoting the numeric category or gradient in prose unless the publisher signs off — narrate the climb in language that survives a category fix ("the fierce one," "the Barthes payoff," "the highest road-summit before Mont Bessou" all survive; "the HC climb" or "the 7.1% gradient" do not). If the #513 fix changes the category to Cat 2/3/4, the entry's reader-facing PowerStats card will reflect that automatically — the draft should not echo it as prose.

**#564 interlock:** the Chirac burial-location fix lands in parallel. The dossier reaches for Sarran/Chirac as an adjacency thread for the Monédières corridor; **do not repeat the "buried in Sarran" claim** that #564 is removing. The corrected framing (Château de Bity / Bernadette as municipal councillor / Sarran museum) is fair game; the burial line is not.

## 4. Target issues

No tracking issue at brief time. File one at strand start: `Seg 15 drafting strand`, milestone v1.4.19. PR closes whatever issue is opened.

## 5. Workflow per issue

Cadence is publisher-paced via AskUserQuestion checkpoints. List of checkpoints (not prose-writing steps):

1. **Read the seg 15 data** (segments.json, town-coords.json, GPX polyline, elevation profile, points-config.json — re-read after #513 lands). Read the segs-14-16 dossier and the tour-history dossier for Monédières-corridor entries.
2. **Read seg 14 published entry** (`content/entries/14-into-the-monedieres.md`) to absorb the texture immediately preceding the summit beat. Note the Paris frame seg 14 used and what it set up; seg 15 should resolve or develop, not duplicate.
3. **Voice register checkpoint** (AskUserQuestion). Voice picked at draft time; the `tdf26-voice` skill provides options. Per `feedback_voice_checkpoint_prep.md`: read the candidate register SKILL.md briefs before firing the checkpoint, so the choice is between substantive options the publisher can evaluate. The "summit beat / Barthes payoff" texture may pull voice toward something elevated or argumentative — the publisher decides. Do not start drafting until voice is fixed.
4. **Arc agreement checkpoint** — confirm seg 15 owns the Barthes "develops" landing (per `project_barthes_callback.md`); confirm which of the dossier's reserved anchors (Chaumeil, Suc au May, Bourrée des Monédières, Dautrement quote, 1987 double-finish) lead and which support; confirm whether to plant any Mont Bessou foreshadow (seg 22 owns Bessou as the highest point; do not poach). The Saintsbury voice is reserved for seg 24 per `project_meymac_voice.md`; do not float it here.
5. **First draft** — write to chosen voice. Make Suc au May the summit; Chaumeil as the historic Monédières capital; the Barthes argument earning its development at the road's highest road-summit before Bessou. Verify factual claims against source URLs before they hit prose. Mind the seg 15/16 boundary at km 106 (seg 16 owns the descent off the massif).
6. **First draft review** — publisher reads; AskUserQuestion at factual calls and cross-segment threads. Watch for the "the X the Y will not Z" tic per `feedback_will_not_shape.md`.
7. **Revisions** — apply publisher edits.
8. **Sources section + disclosure footer** — `## Sources` per `feedback_sources_section.md` (external URLs only per `feedback_sources_no_internal.md`); pair-writing + voice-register footer per `project_disclosure_practice.md`.
9. **PR open against `main`** — title `seg 15 draft: <subtitle>`; body lists voice picked, AskUserQuestion checkpoints fired, any new issues filed, interlock confirmation with #513 / #564.

## 6. Verification commands

- `npm test` — entry-shape assertions pass.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — entry passes shape + MDC balance checks (MDC validator landed in PR #563). Use any MDC blocks deliberately.
- `python3 processing/validate_points.py` — no regression.
- `npm run build` and dev preview at `/entries/15-suc-au-may-*`: render renders, ElevationChart shows the segment profile, image gallery placeholder renders. Per `project_dev_server_content_index.md`: if the entry doesn't show in dev after the branch switch, delete `.data/content/contents.sqlite*` and restart dev.
- **Pre-publish scrutiny** per `feedback_pre_publish_scrutiny.md`: verify geography, attribution, image rights before publish.sh runs.
- Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `content/entries/15-suc-au-may-the-fierce-one.md` (overwrite stub).
  - `public/images/segment-15/*` if any publisher-supplied images land in the draft window.
- **What this strand reads:**
  - `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`.
  - `data/segments/segment-15.gpx`, `data/elevation/segment-15.json`.
  - `content/entries/14-into-the-monedieres.md` (texture continuity).
  - `content/research/segs-14-16-block-research.md` (dossier).
  - `content/research/tour-history-research.md` (1987 double-finish, 2024 stage-11 adjacency).
- **What this strand must NOT touch:**
  - Other published entries (per `feedback_content_change_rule.md`).
  - `data/competition/points-config.json` — owned by #513 strand.
  - `data/attractions.json` — owned by #564 strand.
  - `tests/utils/*.test.ts` — owned by #518 strand.
  - `components/EntryCard.vue` — owned by #535 strand.
- **Cross-strand collisions and rebasing rules:**
  - #513 may change Suc au May's category/gradient; if so the entry's PowerStats card auto-updates from points-config, so no rebase is needed unless the draft quoted the numbers. Defence: do not quote numbers in prose.
  - #564 may rewrite the Chirac burial line; the draft should already avoid the burial framing, so no collision expected.
  - #535 may change EntryCard's thumbnail mechanism; the entry's image authoring should pick a strong card-suitable first image regardless (defence in depth).

## 8. Scope discipline

- **Do not modify published entries** (per `feedback_content_change_rule.md`). Corrections from seg 14 forward go into the seg 15 entry's framing.
- **Do not retroactively edit data files** owned by sibling strands; if the draft surfaces a factual problem in `data/*.json`, file an issue and tag it for the right milestone — do not fix inline.
- **AskUserQuestion fires at the voice checkpoint, the arc-agreement checkpoint, the first-draft review, and any factual call the publisher should weigh in on.** Implementation steps in between are not checkpointed.
- **If the publisher prefers to defer:** acceptable outcome is "voice checkpoint fires, publisher chooses 'slip seg 15 to Wed 2026-05-27, push seg 16 to Sun 2026-05-31'". Close the strand with the draft state captured; do not push a forced draft.

## 9. Memories that apply

- `project_barthes_callback.md` (seg 15 is the "develops" beat).
- `project_meymac_voice.md` (Saintsbury reserved for seg 24; do not float here).
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
- Interlock confirmed: #513 resolved (or seg 15 prose carefully avoids climb-stat quotes); #564 resolved (or seg 15 avoids the burial line).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-seg-15` once the PR has merged.
- Final report posted to publisher: PR link, voice picked, checkpoints fired, interlock state with sibling strands.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during seg-15-drafting strand execution (<date>)`:
  - **Decision-actionable observations:** any seg 16 / 17 content threads opened, any data-file follow-ups filed, voice-skill drift surfaced.
  - **Light-tier pattern observations:** Barthes-arc landing experience, dossier-fact verification surprises, voice-checkpoint shape findings.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock.
