# Strand: Tour-history corridor expansion (#527)

Auto-mode data-population strand to expand `data/historical-tdf.json` with the corridor-relevant Tour de France entries the tour-history research dossier (`content/research/tour-history-research.md`) surfaced but did not action. Authored 2026-05-24. Closes the gap between research (done, PR #526) and data-layer realisation (open umbrella issue #527).

## 1. Goal

Land per-segment entries in `data/historical-tdf.json` for the late-route corridor (segs 14-27 priority; backfill earlier segs opportunistically) drawn from the dossier's "Carryforwards out of scope" section and the per-event corpus. Each entry follows the existing `historical-tdf.json` shape (verify against current records) and is keyed to a segment so the entry pages can render it as historical context.

Closes #527. Milestone: TBD at Mon/Tue planning session (likely v1.4.20 head). Runs in **auto-mode** per the v1.4.18 retro learning (data-population suits auto-mode). One AskUserQuestion checkpoint: scope ceiling (how many entries to land in this strand vs hold for a follow-up — see §5 step 4).

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/527-tour-history-corridor /home/jhs/code/tdf26-tour-history-2 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `data/historical-tdf.json` is the canonical reader-facing historical-events index, keyed by segment. **Read the current file end-to-end first** to confirm the entry shape (fields, segment-keying convention, source-URL field, year/race/winner conventions). Do not invent a schema.
- `content/research/tour-history-research.md` is the research dossier. Sections to mine:
  - **Per-event corpus** (lines 25-226) — the raw events. Already includes the 1987 Chaumeil double-finish keyed to seg 15 (per the dossier, this is already in `historical-tdf.json` — confirm). Other events here have been classified by relevance and may not all warrant `historical-tdf.json` entries.
  - **Carryforwards out of scope** (line 575 onward) — the dossier's explicit "this belongs in historical-tdf.json for later segments" section. **This is the strand's primary input.**
  - **Sources** (line 441 onward) — every external URL the dossier verified. Use these as the canonical citations for the json entries this strand adds.
- Per `feedback_source_of_truth_framing.md`: the dossier is a research synthesis, not bedrock. For any event whose claim is non-trivial (winner name, year, route detail), verify against the cited source URL before landing in `historical-tdf.json` — the file becomes reader-visible and an incorrect entry breaks a reader's trust harder than a dossier note does.
- Per `feedback_brief_content_is_carryforward.md`: dossier facts are scaffolding; verify before relying. The dossier's verification log (line 640) records what session 2 verified — entries not in that log are still candidates for re-verification.

## 4. Target issues

**Closes #527** — use `Closes #527` in PR body (per `feedback_pr_closure_keywords.md`).

If a corridor event surfaces during this strand that isn't in the dossier (e.g., a 2026 race result that lands after the dossier shipped), file a separate issue rather than expanding scope. The strand's input is the existing dossier; new research is its own strand.

## 5. Workflow

Single-issue strand; collapse "Target issues" + "Workflow per issue" into one cadence.

1. **Survey current state.** Read `data/historical-tdf.json` end-to-end. Tabulate which segments already have entries, what fields each entry uses, how segments are keyed (by `segment` integer? by km range?), what the source-citation convention is. Note the segs already covered.
2. **Read the dossier's "Carryforwards out of scope" section.** Tabulate each candidate event with: segment(s) it would key to, event detail summary, cited source URL(s), and the dossier's reasoning for parking it.
3. **Cross-reference: dossier carryforwards × existing historical-tdf.json entries.** Identify which carryforwards are already landed (skip), which are missing (candidates for this strand), and which are partially landed (entry exists but missing fields).
4. **Scope-ceiling checkpoint (AskUserQuestion).** Present:
   - **Tight (land 5-10 highest-confidence entries):** lowest risk, fastest merge, easy to land before seg 17 publish. Defers most carryforwards to a follow-up.
   - **Moderate (land all dossier carryforwards that pass single-source verification, ~15-25 entries estimated):** middle ground. May surface new verification needs mid-strand.
   - **Aggressive (land all carryforwards + backfill any thin existing entries):** broadest coverage; longer strand wall-clock; risks over-scoping if a carryforward needs multi-source reconciliation.
   The publisher decides. **Default recommendation: Moderate** — the dossier already filtered to corridor-relevant events; the verification step adds discipline without inflating scope.
5. **Land entries in `historical-tdf.json`.** For each candidate that passes verification:
   - Match the existing entry shape (fields, ordering, conventions).
   - Cite the source URL in whatever the existing `source` / `references` field is.
   - Key to the segment(s) the event corresponds to. If an event spans multiple segments (a stage finish at one town with the breakaway formed in another), follow the existing file's multi-segment convention; if none exists, key to the most-specific segment and note the broader span in a `notes` field if the schema allows.
   - Commit in small batches (5-10 entries per commit) so review can scan the diff sensibly.
6. **Update the dossier's "Verification log"** to reflect what this strand verified. Append a session-3 entry under the existing pattern; do not rewrite session 1 or 2 logs.
7. **Update the dossier's "Carryforwards out of scope" section** to mark each landed entry as `landed in PR #<N>`, so future strands can see what's left.
8. **Spot-check entry rendering.** Pick one or two segments whose entries land in this strand; run `npm run dev` and confirm the entry page renders the new historical-context content (look up where `historical-tdf.json` is read in `pages/entries/[...slug].vue` or its components to confirm rendering site).
9. **PR open against `main`.** Title `feat(historical-tdf): corridor expansion from dossier carryforwards (closes #527)`. Body lists: scope chosen at checkpoint, number of entries landed, segments touched, dossier section updates, verification log appended.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green (historical-tdf.json shape changes shouldn't touch entry validation, but confirm no schema regression if a Python script validates this file).
- `npm test` — green pre- and post-change.
- **JSON validity:** `python3 -c "import json; json.load(open('data/historical-tdf.json'))"` — file parses.
- **Schema consistency:** if a JSON Schema for historical-tdf.json exists (`data/schemas/` per the v1.4.18 schema work), run `jsonschema -i data/historical-tdf.json data/schemas/historical-tdf.schema.json` (or equivalent) — passes.
- `npm run build` — production build succeeds.
- **Reader spot-check** per §5 step 8: dev render of an updated entry page shows the new historical context.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `data/historical-tdf.json` (extend, not restructure).
  - `content/research/tour-history-research.md` (append-only updates to the Verification log and Carryforwards sections; do not rewrite earlier sections).
- **What this strand reads:**
  - The dossier (`content/research/tour-history-research.md`) end-to-end.
  - Current `data/historical-tdf.json` for shape and existing entries.
  - External: source URLs cited in the dossier (Wikipedia, Cyclingnews, ProCyclingStats, ASO archives, etc.).
- **What this strand must NOT touch:**
  - `content/entries/*` — even if an entry's historical-context paragraph would benefit from a new fact, that's a content-change concern owned by the relevant drafting strand.
  - `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/competition/points-config.json` — out of scope.
  - The dossier's per-event corpus, regional-races, riders, wartime sections — read-only here; they are research artifacts.
  - Any sibling strand's files (seg 15 drafting, seg 16 drafting, segs 17-19 research) — all read different files.
- **Cross-strand collisions:**
  - **None expected with seg 15 / seg 16 drafting:** entry pages read `historical-tdf.json` at render time; if this strand lands entries for seg 15 or seg 16 while their drafting strands are open, the entry pages will auto-render the new context on next build — no merge conflict on the markdown.
  - **None expected with segs 17-19 research:** different file. If that strand surfaces new corridor events not in the dossier, those become future-strand input; this strand doesn't try to integrate mid-flight.

## 8. Scope discipline

- **No dossier rewriting.** Append-only updates to Verification log and Carryforwards section. The dossier is a frozen research artifact for the sections it already populates.
- **No new research subagents.** This is a data-population strand; the research has already happened.
- **AskUserQuestion fires once at the scope ceiling.** Per-entry verification is mechanical against cited sources.
- **No backfilling for earlier (already-published) segments unless the dossier explicitly carryforwarded a fact for them.** Per `feedback_content_change_rule.md`, published entries are forward-only; adding historical context to their data file is acceptable (the entry page will render it on next build) but is not the primary goal of this strand.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`.
- `feedback_brief_content_is_carryforward.md` (dossier facts need source verification before landing in reader-visible JSON).
- `feedback_parallel_source_of_truth_detector.md` (if landing entries with year/race/winner data that overlaps with other data files, watch for drift).
- `feedback_strand_worktree_path.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_pr_closure_keywords.md`.
- `feedback_issues_describe_problems.md`.
- `feedback_sources_no_internal.md` (entries cite external URLs, not internal data files).

## 10. Stop when

- PR opened against `main`, `Closes #527` in body.
- Scope-ceiling checkpoint fired and answered; chosen scope + count of landed entries documented in PR body.
- `historical-tdf.json` parses, validates (if schema exists), and renders correctly on spot-checked segments.
- Dossier's Verification log and Carryforwards sections updated.
- `npm test` + `npm run build` green.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-tour-history-2` once the PR has merged.
- Final report posted to publisher: PR link, scope chosen, number of entries landed, segments touched, any new corridor events surfaced that warrant follow-up research.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during tour-history-corridor-expansion strand execution (<date>)`:
  - **Decision-actionable observations:** any historical-tdf.json schema gaps surfaced, any new corridor events found that warrant fresh research, any reader-rendering surprises.
  - **Light-tier pattern observations:** dossier-to-data-file workflow shape (this is the first instance — note what worked and what didn't for the next research-then-realise pair), verification-friction findings.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock, entries landed per hour as a future-planning input.
