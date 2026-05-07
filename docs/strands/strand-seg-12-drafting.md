# Strand: Seg 12 drafting

Drafting strand for segment 12 of the tdf26 travelogue. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Land a draft of `content/entries/12-*.md` ready for the publisher's pre-publish review window before the seg 12 publish (Wed 2026-05-13 if the cadence holds). Segment 12 covers km 77–84 (Naves into the Puy de Lachaud approach). Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/19) (subject to renumbering per Topic 9a). Hard deadline: roughly Tue 2026-05-12 evening.

This strand runs in **publisher-paced single-strand mode** (per `feedback_multi_strand_session_checkpoints.md` 2026-05-07 sharpening) — checkpoint at editorial micro-decisions. Spawn only after seg 11 has shipped: voice-register choice and any seg-11-publication learnings should inform seg 12.

This is the **Barthes-arc "tightens" beat** per `project_barthes_callback.md` (seg 6 plants — absence; seg 12 tightens — argument becoming visible; seg 15 develops — argument earned at Suc au May). The forward-looking literary thread opens here, not earlier.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-12-draft /home/jhs/code/tdf26-seg-12 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, and `data/segments/segment-12.gpx` directly for any factual claim about route geometry, town/attraction position, or climb metadata. Do not transcribe CLAUDE.md tabular data (deprecated per #491 / PR #507). Use the GPX polyline (not segment endpoints) for proximity checks (per `feedback_on_route_checks.md`, `feedback_source_of_truth_framing.md`).

`content/research/segs-11-13-block-research.md` (committed via PR #501 with Bol d'Or correction) is the primary content input. Treat as research, not authoritative for facts you'll publish — verify cited sources against URLs given. Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding, not bedrock.

## 4. Target issues

No tracking issue at brief time. If the strand opens its own (e.g., to capture a follow-up surfaced during draft), file at strand start: `Seg 12 drafting strand`, milestone v1.4.19. PR closes whatever issue is opened.

## 5. Workflow per issue

Cadence is publisher-paced via AskUserQuestion checkpoints. List of checkpoints (not prose-writing steps):

1. **Read seg 12 section of dossier** + factor in seg 11 publication learnings (post-mortem of seg 11 ship, anything that surfaced at publish time).
2. **Voice register checkpoint** (AskUserQuestion). Voice picked at draft time; the `tdf26-voice` skill provides options. Do not start drafting until voice is fixed.
3. **Arc agreement checkpoint** — confirm the Barthes seg-12 "tightens" beat stays in scope; confirm the Naves cultural anchors (Tintignac echo if not already spent in seg 11; Koscielny home; Retable de Naves; A89 viaduct framing) the publisher wants foregrounded.
4. **First draft** — write to chosen voice. Keep Naves-as-village-someone-comes-home-to as primary; layer the climb of Côte des Naves (canonical name post-#516; no "s") and the start of the Puy de Lachaud approach. Verify factual claims against the dossier's source URLs.
5. **First draft review** — publisher reads; AskUserQuestion checkpoints fire on factual calls and on any forward-looking thread placement. Note the "between-places" texture of the seg 12-13 transition that the dossier flagged for seg 13 — do not poach.
6. **Revisions** — apply publisher edits.
7. **Sources section + disclosure footer** — `## Sources` per `feedback_sources_section.md`; pair-writing + voice-register footer per `project_disclosure_practice.md`.
8. **PR open against `main`** — title `seg 12 draft: <subtitle>`; body lists voice picked, AskUserQuestion checkpoints fired, any new issues filed.

## 6. Verification commands

- `npm test` — entry-shape assertions pass.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — entry passes shape checks.
- `python3 processing/validate_points.py` — no regression.
- `npm run build` and dev preview at `/entries/seg-12-*`: render renders, ElevationChart shows the climb metadata, image gallery placeholder renders.
- **Pre-publish scrutiny** per `feedback_pre_publish_scrutiny.md`: verify geography, attribution, image rights before publish.sh runs.
- Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `content/entries/12-*.md`. Possibly small additions to `data/historical-tdf.json` if the dossier surfaces a missing event keyed to seg 12, but default is to file an issue per `feedback_issues_describe_problems.md`.
- **What this strand reads:** `content/research/segs-11-13-block-research.md`, `data/segments.json`, `data/historical-tdf.json`, `data/town-coords.json`, `data/competition/points-config.json`, `data/segments/segment-12.gpx`, `data/elevation/segment-12.json`.
- **What this strand must NOT touch:** `content/entries/11-*.md` (seg 11 published before this strand spawns; per `feedback_content_change_rule.md` no retroactive edits). `content/entries/13-*.md` (separate drafting strand). Sainte-Fortunade / Monédières / Léon Dautrement / Bourrée des Monédières — reserved for seg 14+. Suc au May / Mont Bessou / Meymac voices / Saintsbury — out of scope. STRAND-BRIEF-TEMPLATE.md untouched.
- **Cross-strand collisions:** none expected. The seg 13 drafting strand (if running concurrently) writes a different entry file; the dossier sections for segs 12 and 13 are distinct.

## 8. Scope discipline

- Default: file new issues for findings outside the strand's owned write-set (e.g., a dossier claim that fails source verification at draft time, an image needing licensing chase).
- AskUserQuestion at material-disagreement points only; do not rubber-stamp.
- Do not retroactively edit prior entries (per `feedback_content_change_rule.md`).
- Document any publisher-approved scope overrides in the PR body.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_on_route_checks.md`
- `feedback_multi_strand_session_checkpoints.md` (publisher-paced this strand)
- `feedback_content_change_rule.md`
- `feedback_pre_publish_scrutiny.md`
- `feedback_brief_content_is_carryforward.md` (dossier facts are scaffolding)
- `feedback_literary_footnotes.md` (post-seg-6, applies)
- `feedback_sources_section.md` (post-seg-6, applies)
- `project_disclosure_practice.md` (post-seg-7, applies; prose footer per 2026-05-07 decision)
- `project_barthes_callback.md` (this strand owns the "tightens" beat)
- `feedback_content_workflow.md` (research → discuss → draft)

## 10. Stop when

- Draft committed to `feature/seg-12-draft`; PR opened against `main`.
- All AskUserQuestion checkpoints fired and answered; publisher reviewed prose at least once.
- `npm test` + entry validators green.
- Dev preview rendered without error.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-seg-12` once the PR has merged.
- Final report posted to publisher: PR link, voice picked, AskUserQuestion checkpoints fired, any open questions surfaced for downstream strands (seg 13 drafting in particular).
