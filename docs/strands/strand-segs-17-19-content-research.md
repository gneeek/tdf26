# Strand: Content research — km 112-134 block (segs 17/18/19)

Authored 2026-05-24 in advance of seg 17 publication on Sun 2026-05-31. Third instance of the block-research-then-N-drafts technique applied to this corridor (first instance: segs 8-10 at v1.4.10; second: segs 11-13 at PR #501; third: segs 14-16 at PR #559). Mirrors the shape of `segs-14-16-block-research.md`.

## 1. Goal

Produce a single research dossier across the 22km block from km 112 (entry into the Treignac approach, just past the Vézère watershed crossing) to km 134 (entry into Bugeat and the threshold of the Plateau de Millevaches). The dossier is consumed by three downstream drafting strands (one per segment, publisher-paced — seg 17 drafts first; seg 18 and seg 19 follow).

This is the **bridge block** of the route. Seg 17 owns Treignac itself — the "Granite and Water" medieval town. Seg 18 holds the Côte de la Croix de Pey climb (the entry stub names it; but `data/segments.json` shows no climbs in seg 18 and `points-config.json` lists the climb at a contested km — needs reconciliation, see §3). Seg 19 opens the Plateau de Millevaches approach by passing through Lestards (towns array) and ending at the Bugeat threshold.

Milestone: TBD at the Mon/Tue planning session (likely v1.4.20 head). Runs in **auto-mode** per the v1.4.18 retro learning (research suits auto-mode). No publisher pacing; AskUserQuestion fires only on material disagreement (e.g., if the Croix de Pey reconciliation needs publisher arbitration mid-dossier).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/segs-17-19-content-research /home/jhs/code/tdf26-research-17-19 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-research-17-19` once the dossier has merged.

## 3. The 22km block

| Segment | Km range | Towns (segments.json) | Climbs (segments.json) | Known content cues |
|---------|----------|----------------------|------------------------|---------------------|
| 17 | 112-120 | Madranges | (none in-segment) | Approach into Treignac. Madranges as the threshold village. The Vézère valley opens here; Treignac as the "Granite and Water" town (entry stub title) — medieval bridge over the Vézère, granite-village architecture, the Plus Beau Village designation history. Treignac's role as a Resistance centre and as the seat of the Maquis Quercy operations. The "Treignac" name itself is the major content anchor; the village is the centrepiece of this segment. |
| 18 | 120-126 | Treignac | (none in-segment; points-config places Côte de la Croix de Pey climb — needs reconciliation) | Côte de la Croix de Pey is the entry stub's title. `data/competition/points-config.json` lists this climb but `data/segments.json` does not assign it to seg 18's climbs array — verify whether the climb is on-route, in which segment, and whether points-config has the right summit km. Issues #551 (length/gradient drift vs mycols/2020 ASO) and #591 (summit km drift filed by #518 strand) both touch this climb. Treat the data state as fluid mid-strand; reconcile via the data files and file follow-up issues as needed — do not edit data inline. Content-wise: the climb sits in the granite uplands between Treignac and Bugeat; the dossier captures geography/climbing context, the drafter writes against whatever data state lands. |
| 19 | 126-134 | Lestards | (none) | Lestards (the thatched-roof church the seg 16 dossier handed off as borderline) sits firmly in seg 19's towns array — the church is in this segment. The Plateau de Millevaches threshold opens here; the entry stub names "Bugeat - Gateway to Millevaches" but Bugeat itself is at the segment end / seg 20 start. Verify which side of km 134 the Bugeat town centre sits. The "gateway" framing is the dominant cue. |

The route stays in the granite uplands for segs 17-19; do not spend Plateau-de-Millevaches material here (that opens at seg 20, reserved). Mont Bessou (seg 22) and the Meymac arc (segs 23-24) are reserved. The Saintsbury voice candidate (per `project_meymac_voice.md`, but note the memory's seg-number reference may be stale per the v1.4.19 close-out finding) is reserved for the Meymac segment.

## 4. Source-of-truth posture

Read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json`, `data/historical-tdf.json`, `data/segments/segment-17.gpx`, `data/segments/segment-18.gpx`, `data/segments/segment-19.gpx` directly. Per #491 / PR #507, do not transcribe CLAUDE.md tabular data.

**Specific data reconciliation work for this strand:**
- The Côte de la Croix de Pey discrepancy (points-config has it; segments.json doesn't assign it; #551 and #591 are open against the data). Read both files; trace which segment the climb summit km actually falls into using the GPX polyline; report findings in the dossier's "data carryforwards" section. File a new issue if a new drift is surfaced; otherwise note alignment with #551 / #591.
- The Lestards-vs-seg-16-vs-seg-19 question: the seg 16 dossier flagged Lestards as borderline; `data/segments.json` confirms it in seg 19's towns. Confirm via GPX + town-coords which segment the village centre sits in; if it sits in both, name that in the dossier.
- The Bugeat boundary: segments.json shows Bugeat in neither seg 19 nor (likely) seg 20's towns; verify where the village centre is relative to km 134.

Per `feedback_source_of_truth_framing.md`: trace the provenance of each disagreement before treating any file as bedrock. Per `feedback_on_route_checks.md`: use the segment GPX polyline, not segments.json endpoints, when testing if a coordinate is on the race route.

## 5. Workflow

1. **Spawn a single research subagent** (general-purpose Agent) with a self-contained prompt covering all three segments. Target ~5-10 minutes of research, similar shape to PRs #501 and #559 (segs 11-13 and 14-16 dossiers).
2. The research subagent should cover, per segment and across the block:
   - **Geography and geology** — the granite uplands of the Treignac / Bugeat plateau; the Vézère and its valley; the watershed transition between the Monédières (drained south to the Corrèze) and the Plateau de Millevaches (drained north to the Vienne); what changes at the seg 17/18/19 boundaries.
   - **Local history** — Treignac as a Resistance centre (Maquis); the granite-village architectural tradition; the medieval bridge over the Vézère (the Pont de la Vézère); Madranges and Lestards as the small parish villages bracketing the route; any Romanesque or pre-Romanesque ecclesiastical sites.
   - **Cycling context** — Côte de la Croix de Pey profile (reconcile against points-config and elevation data; flag drift for the drafter). The Tour du Limousin's relationship to the Treignac / Bugeat corridor (regional race that runs through these towns). 2024 Stage 11 adjacency if any. The Bugeat-Sornac sport-climbing / cycling-club history if any.
   - **Famous local people** — verify any Treignac / Madranges / Lestards / Bugeat-corridor historical figures (writers, Resistance fighters, mayors, artists). Léon Dautrement was the Monédières anchor; this block needs its own figure(s).
   - **Culture** — local cuisine (Plateau-de-Millevaches gateway means the cuisine begins to shift; capture the boundary). The Lestards thatched-roof church (Église Saint-Symphorien — one of two surviving thatched-roof churches in France) as a major cultural anchor for seg 19. Local festivals.
   - **Possible literary or musical references** — the Maquis Treignac literature; any Limousin-regional writers tied to the corridor; the Vézère as a literary motif (it runs through Lascaux country further downstream — the same river, the same valley).
3. **Write the dossier** to `content/research/segs-17-19-block-research.md`. Structure (mirror PRs #501 and #559):
   - **Per-segment section** (seg 17 / 18 / 19) with research findings grouped by topic.
   - **Cross-segment threads** section listing arcs spanning the block (the granite-uplands → Plateau-threshold arc; the Vézère as the connecting waterway; the Resistance corridor; the Treignac → Bugeat axis as a cultural transition).
   - **Sources** section listing every URL the dossier draws on (the dossier is the source-of-record for each entry's `## Sources` block per `feedback_sources_section.md`; per `feedback_sources_no_internal.md`, list only external URLs).
   - **Carryforwards out of scope** section listing anything found that belongs in segs 20-22 (Plateau de Millevaches body), segs 23-25 (Meymac arc), or `data/historical-tdf.json` for later segments.
   - **Data reconciliations surfaced** section — any drift surfaced between points-config, segments.json, town-coords, and the GPX (the Croix de Pey question, the Lestards question, the Bugeat boundary). One paragraph per finding with a recommended issue title; the drafter or planning session files the issues, not this strand.
4. **Read sources directly, not through CLAUDE.md transcription.** When the dossier cites a km position, town location, or climb gradient, read the data files directly. Per `feedback_source_of_truth_framing.md`, `feedback_brief_content_is_carryforward.md`.
5. **Open a PR** when the dossier is ready. PR body: short summary of what's in the dossier + which segs each section serves. No closing keyword (research dossiers don't close issues; they feed downstream drafting strands).

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green (research dossier doesn't touch entries but the validator should not regress).
- `npm test` — green.
- **Source verification:** for every external URL the dossier cites, confirm it fetches (HEAD or GET successful). If a URL is unreachable, flag in the dossier rather than removing.
- **Dossier completeness check:** before PR open, confirm each segment has at minimum one entry per topic header (geography, history, cycling context, culture, people, references). Empty topics are valid only if explicitly noted "no relevant content found this block; reserve to later block."

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `content/research/segs-17-19-block-research.md` (new file).
- **What this strand reads:**
  - All `data/*.json` files plus the relevant segment GPXs and elevation profiles.
  - The seg 14-16 dossier (for handoffs from the Monédières block, especially the Lestards-borderline note).
  - The tour-history dossier (for Tour de France stages adjacent to the Treignac / Bugeat corridor).
- **What this strand must NOT touch:**
  - Any `data/*.json` file — drift findings get filed as issues, not fixed inline.
  - `content/entries/*` — published entries are fixed; stub entries are owned by their drafting strands.
  - Sibling strand files (seg 15 drafting in flight, seg 16 drafting brief just written, tour-history continuation brief running in parallel — none share file regions with this strand).
- **Cross-strand collisions:**
  - **None expected.** The tour-history continuation strand writes to `data/historical-tdf.json` or to the existing dossier file; this strand writes a new dossier file. Different write sets.
  - If the tour-history continuation strand identifies a 17-19-corridor Tour event mid-research that this strand also surfaces, the dossier captures it under "cycling context" with a cross-reference to the historical-tdf.json entry once it lands. No mergeable conflict.

## 8. Scope discipline

- **Dossier output only.** No entry drafts, no data fixes, no UI changes.
- **Data reconciliations are reported, not fixed.** §5 step 3 captures the recommended issue titles in the dossier's "Data reconciliations" section. The publisher or planning session files the issues.
- **AskUserQuestion fires only at material disagreement.** Routine "is X relevant?" judgement calls are made by the strand and noted in the dossier.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`.
- `feedback_on_route_checks.md`.
- `feedback_brief_content_is_carryforward.md`.
- `feedback_sources_section.md`, `feedback_sources_no_internal.md`.
- `feedback_literary_footnotes.md` (the drafters that consume this dossier need bibliographic detail for any literary anchor — surface it in the dossier).
- `reference_corridor_commune_name_collisions.md` (Treignac, Madranges, Lestards, Bugeat — disambiguate by department or adjacency in any external search).
- `feedback_strand_worktree_path.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_issues_describe_problems.md`.

## 10. Stop when

- PR opened against `main` with the dossier (`content/research/segs-17-19-block-research.md`).
- Per-segment, cross-segment-threads, sources, carryforwards, and data-reconciliations sections all present.
- All external URLs cited in the dossier verified reachable.
- Recommended issue titles for any data reconciliation surfaced are captured in the dossier (drafter / planning session files them; this strand doesn't).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-research-17-19` once the PR has merged.
- Final report posted to publisher: PR link, dossier path, list of data-reconciliations surfaced, recommended downstream drafting cadence.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during segs-17-19-research strand execution (<date>)`:
  - **Decision-actionable observations:** data reconciliations surfaced (recommended issues), any content gaps that need a follow-up research pass, any voice-reservation memory drift surfaced.
  - **Light-tier pattern observations:** dossier-shape findings vs the segs-14-16 and segs-11-13 precedents, source-verification surprises.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired (likely zero), approximate wall-clock.
