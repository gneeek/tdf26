# Strand-brief template

Use this template when authoring a parallel-strand Claude Code session brief for tdf26. Sections appear in the order below; deviations should be deliberate (see "When deviating" at the end).

This template was promoted out of `README.md` at the 2026-05-07 planning session, applying the v1.4.10 retro's "strand-brief template" gap, the Strand C exit feedback edits from PR #485, and the v1.4.18 Strand A source-of-truth finding. See [unfold#40](https://github.com/gneeek/unfold/issues/40) for the cross-project note candidate.

## Sections

### 1. Goal

One paragraph. Name the deliverable, the milestone goal it serves, and any deadline. If the strand is part of a coordinated release with other strands, link to the others here.

### 2. Filesystem posture

Worktree path, branch verification, isolation policy.

- **Use the explicit-path worktree form** (run from outside the repo, or with `git -C`):
  ```
  git -C /home/jhs/code/tdf26 worktree add -b feature/<branch-slug> /home/jhs/code/tdf26-<strand> main
  ```
  Do NOT use `git worktree add tdf26-<strand> main` from inside the repo. That form nests the worktree inside the parent repo and trips "branch already checked out elsewhere." Captured in `feedback_strand_worktree_path.md`.
- **Do NOT add `ln -s ../tdf26/.claude .claude`** — `.claude/` is tracked in git, so the worktree already has it from the checkout. The symlink command errors harmlessly; drop it.
- **Branch verification rule:** before each `git add` / `git commit`, run `git branch --show-current` and confirm it matches the feature branch. Captured in `feedback_shared_tree_branch_verification.md`.

### 3. Source-of-truth posture

What to read directly, what not to transcribe.

- For any factual claim about route geometry, town/attraction position, climb gradient, or segment data: **read `data/segments.json`, `data/town-coords.json`, `data/attractions.json`, `data/points-config.json`, and `data/segments/*.gpx` directly**.
- **Do NOT transcribe CLAUDE.md known-waypoints km positions** or other tabular data — that table has confirmed staleness per [#491](https://github.com/gneeek/tdf26/issues/491). CLAUDE.md narrative project context is fine; CLAUDE.md tabular data is not bedrock.
- Per `feedback_source_of_truth_framing.md`: when a JSON file is hand-curated downstream of another source, trace the provenance before treating it as bedrock.
- Per `feedback_on_route_checks.md`: use the segment GPX polyline, not `segments.json` endpoints, when testing if a coordinate is on the race route.

### 4. Target issues

Issue numbers, ordering rationale, milestone. If the strand opens its own tracking issue, name it here.

### 5. Workflow per issue

Concrete steps. For research strands, this is the research plan. For data strands, this is the audit pass + cross-check. For content strands, this is the draft cadence.

### 6. Verification commands

Only commands that actually exist in `package.json` / the codebase. Examples that exist:

- `npm test`
- `python3 processing/validate_points.py`
- `python3 scripts/validate_entries.py`
- `npm run build`
- `npx nuxt prepare` (in worktrees, if `.nuxt/` not yet generated)

Examples that do **not** exist (do not list them — past briefs got this wrong):

- `npm run typecheck` — does not exist in this repo.

Where applicable, demonstrate red-green: show that the test fires red against the broken state and green against the fix. Don't commit artificial breakage; use temporary file moves or a restored state.

### 7. Cross-strand sharing notes

This is the **load-bearing** section. List, in order:

- **What this strand owns (write):** explicit file paths or globs the strand will modify.
- **What this strand reads:** files the strand consumes but does not modify.
- **What this strand must NOT touch:** files owned by sibling strands or out-of-scope.
- **Cross-strand collisions and rebasing rules:** what to do if a sibling lands first and changes a shared assertion or data file. Forecast the most likely failure mode.

In v1.4.10 and v1.4.18, three-of-three strands honoured each other's file regions because of explicit declarations here. In v1.4.18 the one collision (Strand A's new `sport` category breaking Strand B's emoji-completeness assertion) was forecast in this section and resolved in one line of code with no design conversation.

### 8. Scope discipline

What to file as new issues vs fix inline.

- Default: file new issues for findings outside the strand's owned write-set; do not over-scope.
- Document overrides ("publisher said keep X") in PR body and `WORK-LOG.md` when relevant.
- AskUserQuestion is the soft-veto on stale brief assumptions — use at material disagreement points, not as a rubber stamp on every choice.

### 9. Memories that apply

List `feedback_*.md` and `project_*.md` memories the strand should load. Common ones:

- `feedback_source_of_truth_framing.md`
- `feedback_on_route_checks.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`
- `feedback_content_change_rule.md` (for content strands)
- `feedback_pre_publish_scrutiny.md` (for publication-day strands)
- `feedback_literary_footnotes.md` (for content strands seg 6+)
- `feedback_sources_section.md` (for content strands seg 6+)
- `project_disclosure_practice.md` (for content strands seg 7+)
- Voice memories (`project_meymac_voice.md`, `project_barthes_callback.md`) if relevant to the segment.

### 10. Stop when

Exit criteria specific to the strand's deliverable. Always include the cleanup sub-bullet:

- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-<strand>` once the work has merged or been pulled back into the parent. The strand owns its own worktree teardown; do not leave it for the publisher to discover.
- Other exit criteria specific to the strand's deliverables (PR open, dossier landed, smoke test green, etc.).
- Final report posted to publisher: PR link, deliverable path, any open questions surfaced for downstream strands.

## Lifecycle

Briefs are working artifacts for one release. Once a release ships and its retro is published, briefs that are no longer load-bearing should be removed; any patterns worth keeping go into the wiki, memory, or this template.

## Worked examples

- **v1.4.10:** `strand-a-content.md` (research + 3 drafts), `strand-b-deps.md`, `strand-c-landing.md`
- **v1.4.11:** `strand-a-security.md`, `strand-b-bugclass.md`, `strand-c-sqlite.md`
- **v1.4.18:** `strand-a-verify.md`, `strand-b-assertions.md`, `strand-c-schema.md`
- **v1.4.18+:** `strand-d-content-research.md` (research-only)

## When deviating

Common deliberate deviations:

- **Research-only strands** (e.g., `strand-d-content-research.md`): drop "Workflow per issue" or fold it into Goal + Stop when. Output is a dossier, not commits to multiple file regions.
- **Single-issue strands**: collapse "Target issues" + "Workflow per issue" into one section.
- **Skill / template strands**: replace "Verification commands" with output-correctness checks (does the skill produce the expected shape?).
- **Drafting strands** (one segment per strand, publisher-paced): the cadence is publisher-driven via AskUserQuestion checkpoints; "Workflow" lists the checkpoints, not the prose-writing steps.
