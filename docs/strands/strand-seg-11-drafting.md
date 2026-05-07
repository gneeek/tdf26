# Strand: Seg 11 drafting

Drafting strand for segment 11 of the tdf26 travelogue. Authored at the 2026-05-07 planning session resume.

## 1. Goal

Land a draft of `content/entries/11-*.md` ready for the publisher's pre-publish review window before Sun 2026-05-10 morning. Segment 11 covers km 70–77 (Tulle exit through Côte de Naves, Stade Auzelou departure to Naves approach). Milestone: **v1.4.18**. Hard deadline: Sat 2026-05-09 evening, so the publisher has Sunday morning for pre-publish review and the publish.sh window.

This strand runs in **publisher-paced single-strand mode** — checkpoint via AskUserQuestion at editorial micro-decisions (image picks, prose corrections, frontmatter choices, voice register), per `feedback_multi_strand_session_checkpoints.md` (sharpening 2026-05-07: publisher-paced is the validated counter-instance to the auto-mode rule).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-11-draft /home/jhs/code/tdf26-seg-11 main
```

- Run from outside the repo (or via `git -C`); see `feedback_strand_worktree_path.md`.
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/seg-11-draft` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- For all factual claims about route geometry, Tulle / Naves coordinates, Côte de Naves climb data: read `data/segments.json`, `data/town-coords.json`, `data/competition/points-config.json`, `data/segments/segment-11.gpx` directly.
- Read `data/historical-tdf.json` for any TdF history claims keyed to seg 11 — the segs 11-13 verification (PR #489) and the seg 14-16 verification (PR #514) have populated this file; trust the data layer over CLAUDE.md narrative.
- **Do not transcribe CLAUDE.md known-waypoints km positions** — the table was deprecated in PR #507. CLAUDE.md narrative project context remains useful; CLAUDE.md tabular data is not bedrock.
- The seg 11-13 block research dossier `content/research/segs-11-13-block-research.md` (committed via PR #501, with the Bol d'Or correction landed today) is your primary content source. Treat as research input, not as authoritative for facts you'll publish — verify cited sources against the URLs given.
- Per `feedback_brief_content_is_carryforward.md` (drafted today): facts cited in this brief are scaffolding; verify against authoritative sources before writing them into prose.

## 4. Target deliverable

One markdown entry at `content/entries/11-*.md` (slug TBD; suggest `11-tulle-exit-auzelou` or similar):

- **Frontmatter**: `segment: 11`, `title`, `subtitle`, `publishDate: 2026-05-10`, `kmStart`, `kmEnd`, `gpxFile`, `elevationData`, `images: []` (publisher fills at publish time), `weather: null`, `draft: true`.
- **Body**: ~800–1200 words narrative weaving the eight content topics from CLAUDE.md, with the carryforwards below.
- **Sources section**: `## Sources` per `feedback_sources_section.md`. List external URLs backing factual claims.
- **Disclosure footer**: per `project_disclosure_practice.md` — pair-writing + voice register.

## 5. Workflow

The strand does not re-do block research (Strand D's dossier covers seg 11). It selects beats from the dossier, drafts, and verifies sources.

1. **Read the dossier section for seg 11** in `content/research/segs-11-13-block-research.md`. Note the primary frame (Auzelou cyclosportive departure, 99–100 days before the stage, amateur-cycling embedded), the cultural anchors (Tintignac carnyx archaeology), the climb (Côte de Naves at km 77.45), and reserved-for-later items (Sainte-Fortunade / Monédières / Bourrée — those are seg 14+).
2. **Voice register checkpoint** (AskUserQuestion). The publisher chooses voice at draft time. Sample candidates: `tdf26-voice` skill provides options. Do not start drafting until voice is fixed.
3. **Draft the entry** in the chosen voice. Keep the Auzelou frame primary; embed the L'Agglomérée 2026 cyclosportive (which ran 5 April 2026, two days after seg 1 published) as the connective tissue; surface Tintignac as the cultural depth; treat Côte de Naves as the climbing beat.
4. **Verify factual claims**. Names, dates, distances, attributions — every one cited in the dossier should be re-checked against its source URL before going into prose. Per `feedback_brief_content_is_carryforward.md` — the dossier is research input, not bedrock.
5. **AskUserQuestion checkpoints** (publisher-paced). Trigger at: voice register pick (step 2); image pick (publisher selects after draft lands; the strand does not pick images); any factual call where two reasonable readings exist; any forward-looking thread (the Barthes seg-12 callback per `project_barthes_callback.md` opens at seg 12; do not plant in seg 11).
6. **Sources section** — list the external URLs the prose stands on. Per `feedback_sources_section.md`.
7. **Disclosure footer** — voice register + pair-writing per `project_disclosure_practice.md`.
8. **Open a PR** against `main`. Title: `seg 11 draft: <subtitle>`. Body: voice picked, dossier sources used, AskUserQuestion checkpoints fired, any out-of-scope items filed as new issues.

## 6. Verification

- `npm test` — 186+ tests pass against the new entry (existing assertions guard frontmatter shape).
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — entry passes shape checks.
- `python3 processing/validate_points.py` — no regression.
- Dev preview at `/entries/seg-11-*`: render renders, ElevationChart shows the Naves climb, image gallery placeholder renders without errors.
- **Pre-publish scrutiny window** — per `feedback_pre_publish_scrutiny.md`: verify geography, attribution, image rights before publish.sh runs Sunday morning.

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/11-*.md`. Possibly small additions to `data/historical-tdf.json` if the dossier surfaces a missing event keyed to seg 11 — but default is to file an issue per `feedback_issues_describe_problems.md`.
- **Reads:** `content/research/segs-11-13-block-research.md`, `data/segments.json`, `data/historical-tdf.json`, `data/town-coords.json`, `data/competition/points-config.json`, `data/segments/segment-11.gpx`, `data/elevation/segment-11.json`.
- **Must NOT touch:** any `content/entries/12-*.md` or `content/entries/13-*.md` (separate drafting strands). Sainte-Fortunade / Monédières / Léon Dautrement / Bourrée des Monédières — reserved for seg 14+. Suc au May, Mont Bessou, Meymac voices, Saintsbury — out of scope.
- **Cross-strand collisions:** other strands (`tdf26-tour-history`, `tdf26-publisher-contract`) running in parallel do not modify the same files. No expected collision.

## 8. Scope discipline

- File new issues for: factual gaps surfaced during draft (e.g., a dossier claim that fails source verification), images that need licensing chase, dev-preview render bugs.
- Do **not** retroactively edit prior entries (per `feedback_content_change_rule.md`). Corrections forward.
- Do **not** poach seg 12 / 13 content. The dossier marks these explicitly.
- The Barthes-arc seg-6/12/15 callback: seg 11 is not in that arc — do not plant. Seg 12 is the "tightens" beat (per `project_barthes_callback.md`).
- Literary references after seg 6 use proper footnotes per `feedback_literary_footnotes.md`. Seg 11 is post-6, so apply.

## 9. Memories that apply

- `feedback_content_workflow.md` — research-then-discuss-then-draft (research = dossier; discussion = voice + checkpoint AskUserQuestion calls; draft last)
- `feedback_multi_strand_session_checkpoints.md` (post-2026-05-07 sharpening — this strand is publisher-paced)
- `feedback_brief_content_is_carryforward.md` (verify dossier facts; brief is scaffolding)
- `feedback_source_of_truth_framing.md`
- `feedback_on_route_checks.md`
- `feedback_pre_publish_scrutiny.md`
- `feedback_literary_footnotes.md`
- `feedback_sources_section.md`
- `feedback_content_change_rule.md`
- `project_disclosure_practice.md`
- `project_barthes_callback.md` (don't plant in seg 11)
- `project_meymac_voice.md` (out of scope; awareness only)
- `project_contributor_is_customer.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`

## 10. Stop when

- Draft committed to `feature/seg-11-draft`, PR opened against `main`.
- All AskUserQuestion checkpoints fired and answered; publisher has reviewed prose at least once.
- `npm test` + entry validators green.
- Dev preview rendered without error.
- **Cleanup (you run this, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-seg-11` once the PR has merged. The strand owns its own worktree teardown; do not leave it for the publisher to discover.
- Final report posted to publisher: PR link, voice picked, AskUserQuestion checkpoints fired, any open issues filed.
