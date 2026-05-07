# Strand — CLAUDE.md known-waypoints deprecation (#491)

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md). Closes [#491](https://github.com/gneeek/tdf26/issues/491).

## 1. Goal

Deprecate the `CLAUDE.md` "Known Waypoints and Climbs (for segment assignment)" section — specifically the "Major Towns (approximate km)" and "Categorized Climbs" subsection tables — in favour of `data/*.json` as the source of truth. For each fact in the tables, locate a JSON home or file a follow-up issue to add it; then remove the tables and replace with pointers to the JSON files. CLAUDE.md keeps narrative project context (architecture, tech stack, directory structure, conventions); it loses tabular data that has demonstrated drift.

Milestone v1.4.19. Companion to the climb-data strand (#490 + #492). Cross-link [unfold#40](https://github.com/gneeek/unfold/issues/40) for awareness; do not open unfold work from inside this strand.

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-491-deprecate-known-waypoints /home/jhs/code/tdf26-claude-md main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

This strand's job is to **make** `data/*.json` the single source of truth for route geometry, town positions, and climb data. It reads:

- `data/segments.json` — town/climb assignments per segment
- `data/town-coords.json` — town coordinates
- `data/attractions.json` — attractions, including some cycling-context info
- `data/points-config.json` — climbs, gradients, lengths, ASO categorisation (the climb-data strand may be modifying this concurrently — coordinate)
- `data/historical-tdf.json` — historical Tour stage references
- `data/segments/*.gpx` — polylines

It writes only to `CLAUDE.md`. Any *missing* data discovered (e.g., Ussel not currently tagged as a town in segments.json seg 26 despite being the stage finish) is filed as a new issue per `feedback_issues_describe_problems.md` — this strand does not add data inline.

## 4. Target issues

- **Closes [#491](https://github.com/gneeek/tdf26/issues/491)** — single tracking issue, milestone v1.4.19.
- **Files new follow-up issues** for any datum in the deprecated tables that has no current JSON home. Expected examples (preliminary, verify during audit):
  - Ussel as a town in `data/segments.json` seg 26 (surfaced by #500 issue body)
  - Total-distance reconciliation: 182 km (segments.json) vs 185 km (CLAUDE.md text); decide which is canonical
  - Cycling-context paragraphs per climb (gradient narrative, summit notes) — if any survive the audit as JSON-shape-resistant, document a home (e.g., a new `data/climb-narrative.json` keyed by climb id, or accept they stay in CLAUDE.md as inline narrative).
- **Companion issues** (do NOT touch but be aware of): #490 (Côte des Naves gradient — climb-data strand owns), #492 (Puy de Lachaud non-ASO — climb-data strand owns).

## 5. Workflow

1. **Inventory pass.** Read CLAUDE.md sections "Major Towns (approximate km)" and "Categorized Climbs". For each row, capture: the row's claim, the candidate JSON home, the current value in JSON, drift if any. Build an audit table.
2. **Per-claim resolution.** For each row:
   - **Has JSON home, JSON value matches CLAUDE.md (or is the better value):** mark for table removal.
   - **Has JSON home, JSON value drifts from CLAUDE.md:** mark for table removal; the JSON wins (per the deprecation decision); flag drift in PR body for awareness only.
   - **No JSON home:** file a follow-up issue describing the missing data (problem-shaped per `feedback_issues_describe_problems.md`); mark CLAUDE.md fact for retention until the follow-up resolves, OR remove and let the follow-up restore — decide per fact via AskUserQuestion at material checkpoints.
3. **Edit CLAUDE.md.** Remove the two tables. Replace each subsection with a pointer paragraph:
   - "Major Towns": pointer to `data/segments.json` (towns per segment) + `data/town-coords.json` (coordinates).
   - "Categorized Climbs": pointer to `data/points-config.json` (climb metadata) + brief note that non-ASO regional climbs are documented in points-config schema after #492 lands.
   - Keep any cycling-context paragraphs that pre-date or outlive the tables (verify nothing in the route narrative or development-notes sections references the deleted tables; update cross-references as needed).
4. **Cross-reference sweep.** `grep -rn "Known Waypoints" /home/jhs/code/tdf26/` to find any links to the deprecated tables in wiki, docs, briefs, or memories. Update or remove pointers. Most likely callers: existing strand briefs (e.g., `strand-d-content-research.md`, `strand-i-verify-segs-14-16.md`, `strand-verify-segs-17-19.md`-through-`-23-26.md` if they exist) — these explicitly tell their agents NOT to transcribe CLAUDE.md known-waypoints; that text becomes obsolete once the tables are gone, but keeping it is harmless. Do not modify completed strand briefs from past releases.
5. **Validators.** Run repo validators; confirm nothing depends on the table contents at parse time.
6. **AskUserQuestion checkpoints** — expect 1-3, around:
   - Whether to remove a table entry whose follow-up issue isn't resolved yet (lose the data temporarily vs keep until follow-up lands).
   - Whether to absorb cycling-context paragraphs into JSON or leave them in CLAUDE.md as inline narrative.
   - Total-distance reconciliation (182 vs 185 km).

## 6. Verification commands

- `npm test` — must pass.
- `python3 processing/validate_points.py` — must pass.
- `python3 scripts/validate_entries.py` — must pass.
- `npm run build` — must pass (a CLAUDE.md edit shouldn't break build, but the audit-script + segment-data validations run on build path; defensive).
- After edits: `grep -n "km " CLAUDE.md` confirms no table-shape km references remain in deprecated sections (cycling-history references like "1951 Tour, Stage 11" are fine and should remain).

Demonstrate read-fidelity: render the deprecated section once before edit, once after; confirm the after-version compiles to a coherent narrative without the tables.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `CLAUDE.md` (the deprecation edits)
- **What this strand reads:**
  - `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/points-config.json`, `data/historical-tdf.json`, `data/segments/*.gpx`
  - `docs/strands/*.md` (cross-reference sweep; do not modify completed briefs)
  - Wiki content if the cross-reference sweep surfaces wiki references
- **What this strand must NOT touch:**
  - `data/*.json` files — adding/correcting data is out of scope; file new issues. (The climb-data strand will be touching `data/points-config.json` concurrently for #490/#492; coordinate by not touching that file.)
  - `data/segments/*.gpx` — the master geometry; no edits.
  - Existing strand briefs — they're working artifacts of their own releases.
- **Cross-strand collisions:**
  - **Climb-data strand (#490 + #492)** runs concurrently in v1.4.19 and modifies `data/points-config.json` + schema + tests. This strand only **reads** points-config; no file overlap. If the climb-data strand lands first, this strand's pointer paragraph for "Categorized Climbs" should reference the new ASO flag posture (cite #492's outcome). If this strand lands first, the climb-data strand's PR can update the pointer paragraph as part of its work. Either order is fine; the second strand to land does the small text update.
  - **Verification strands (#498/#499/#500)** read CLAUDE.md narrative for context. They explicitly do not transcribe the deprecated tables — that's already in their briefs. After this strand lands, those briefs' "do not transcribe" caveat becomes redundant but not wrong.

## 8. Scope discipline

- **Do NOT add new data inline.** File follow-up issues for missing-data facts. The data-layer regime says JSON is canonical; adding data is the verification strands' job, not this one's.
- **Do NOT remove project-context narrative.** Tech Stack, Directory Structure, Phase 1/2/3/4 sections, Publication Schedule, Development Notes, References — these stay. Only the two tabular subsections under "Known Waypoints and Climbs" are in scope.
- **Do NOT modify the existing strand briefs** even if their "do not transcribe CLAUDE.md" caveats become stale. They're release-bound working artifacts.
- AskUserQuestion at material disagreements (3 expected per Workflow step 6).

## 9. Memories that apply

- `feedback_source_of_truth_framing.md` — this strand IS the resolution of one source-of-truth-framing case
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_issues_describe_problems.md` — follow-up issues describe problems, not solutions
- `feedback_unfold_tdf26_work_fit.md` — capture observations for unfold but do not open unfold work from inside
- `feedback_explicit_mechanics.md` — when documenting the new pointer paragraphs, prefer explicit human-understandable explanations
- `project_unfold_legible_model.md` — light-tier observations during this strand may go to memory; heavy-tier portable patterns wait for the unfold note

## 10. Stop when

- CLAUDE.md tables removed; pointer paragraphs in place.
- Follow-up issues filed for every missing-data fact (Ussel-as-town, total-distance reconciliation, cycling-context-paragraph homes, others surfaced).
- Cross-reference sweep complete; obsolete pointers updated or accepted as harmless.
- All verification commands green.
- Audit table in PR body listing every deprecated row, its resolution (JSON home / follow-up issue #), and any drift flagged for awareness.
- PR open against milestone v1.4.19 closing #491.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-claude-md` once the PR has merged.
- Final report posted to publisher: PR link, audit-table summary, follow-up issues filed, any open questions surfaced.
