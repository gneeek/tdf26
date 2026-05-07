# Strand — `/strand-brief` skill creation

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md).

## 1. Goal

Build a `/strand-brief` skill that generates a strand-brief markdown file populated from `docs/strands/STRAND-BRIEF-TEMPLATE.md`. The skill asks the publisher for strand specifics (id, type, target issues, milestone, sibling strands) and writes the file at `docs/strands/strand-<id>.md` with template sections pre-filled with sensible defaults for the strand's type.

This is the path-C skill half of the strand-brief template work decided at planning. The file template already exists; this strand adds the skill that consumes it.

Milestone: v1.4.18 (decided 2026-05-07; if scope lands cleanly during the session it can ship in the same release as the template file). If it slips, move to v1.4.19.

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/strand-brief-skill /home/jhs/code/tdf26-skill main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

- The template file `docs/strands/STRAND-BRIEF-TEMPLATE.md` is the authoritative section structure. The skill MUST read it at invocation time, not bake the structure into the skill prompt — that way the file remains the single source of truth and edits to the template don't require skill changes.
- Read existing strand briefs (`docs/strands/strand-*.md`) for examples of how each section gets filled. Particularly: `strand-d-content-research.md` (research-only), `strand-a-verify.md` (data verification), `strand-a-content.md` (research+drafts).

## 4. Target issues

File a single tracking issue at start: `Build /strand-brief skill (path C complement to STRAND-BRIEF-TEMPLATE.md)`, milestone v1.4.18. PR closes it.

## 5. Workflow

1. **Decide skill location.** Existing tdf26 skills (`retro`, `tdf26-voice`) live at user-level `/home/jhs/.claude/skills/`. Default to that location: `/home/jhs/.claude/skills/strand-brief/SKILL.md`. If the publisher wants project-level scoping at strand spawn time, route to `/home/jhs/code/tdf26/.claude/skills/strand-brief/SKILL.md` instead.
2. **Skill design.** The skill should:
   - Read `docs/strands/STRAND-BRIEF-TEMPLATE.md` from the working directory.
   - Prompt the publisher (via AskUserQuestion or skill arguments) for:
     - Strand identifier (e.g., `e-seg11-draft`, `i-segs-14-16-verify`).
     - Strand type, picked from: research-only / data-verification / content-draft / code / mixed.
     - Goal (one paragraph, free text).
     - Target issue numbers (comma-separated).
     - Milestone (e.g., `v1.4.18`, `v1.4.19`, `v1.4.20`).
     - Sibling strands running in parallel (for cross-strand sharing notes, free text or skip).
     - Worktree absolute path (default suggested based on identifier: `/home/jhs/code/tdf26-<strand-letter>`).
     - Branch name (default: `feature/<strand-id>`).
   - Generate the brief file at `docs/strands/strand-<id>.md`, pre-filled per strand type:
     - Filesystem posture: standard form with the chosen worktree path + branch.
     - Source-of-truth posture: standard for this repo.
     - Target issues: rendered from the input.
     - Workflow per issue: type-specific stub (research = research-plan stub; data = audit-pass stub; content-draft = draft-cadence stub with publisher checkpoints; code = workflow-per-issue stub).
     - Verification commands: type-specific stub (data → `npm test` + `python3 processing/validate_points.py`; content → `python3 scripts/validate_entries.py`; code → `npm test` + `npm run build`).
     - Cross-strand sharing notes: stub with the load-bearing reminder, populated with sibling-strand info if provided.
     - Scope discipline: standard text.
     - Memories that apply: type-specific defaults.
     - Stop when: standard cleanup sub-bullet + a placeholder for type-specific exit criteria.
3. **Test the skill.** Run it once to generate a sample brief; visually compare against `strand-d-content-research.md` and `strand-a-verify.md` for shape. Iterate until output matches the template structure cleanly.
4. **Document the skill.** Add a short usage example to `docs/strands/README.md` (one line under the Template section pointing at the skill), and to the skill's own description.

## 6. Verification commands

- Skill invocation produces a valid markdown file at the expected path.
- Generated file passes a simple grep for all 10 section headers from the template (`### 1. Goal`, `### 2. Filesystem posture`, etc.).
- Generated file's defaults match the template's recommendations (worktree command form, no `.claude` symlink, cleanup-ownership sub-bullet).
- Existing repo tests still pass: `npm test`, `python3 scripts/validate_entries.py`.

Demonstrate red-green: generate a brief; intentionally remove section 7 from the template; re-generate and confirm the missing section shows in the output (template-driven, not hardcoded). Then restore template.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `/home/jhs/.claude/skills/strand-brief/SKILL.md` (or `.claude/skills/strand-brief/SKILL.md` if project-scoped)
  - Optional small additions to `docs/strands/README.md` (one-line usage example).
- **What this strand reads:**
  - `docs/strands/STRAND-BRIEF-TEMPLATE.md` (template source of truth)
  - `docs/strands/strand-*.md` (existing brief examples)
  - Existing skills under `/home/jhs/.claude/skills/{retro,tdf26-voice}/SKILL.md` for skill-authoring conventions.
- **What this strand must NOT touch:**
  - `docs/strands/STRAND-BRIEF-TEMPLATE.md` (source of truth; do not edit during skill work — if the template needs an edit, file a separate issue and do it as a sibling or follow-up strand).
  - Existing `docs/strands/strand-*.md` working briefs.
- **Cross-strand collisions:** none expected. The publication-cycle strands (D content research, future E/F/G drafting strands, future I segs-14-16 verification strand) are all consumers of the template, not editors.

## 8. Scope discipline

- **Skill should not enforce policy** (e.g., "always use worktree X for letter Y"). It generates the brief; the publisher reviews.
- **Skill should not bake structure into prompt.** Read the template file each invocation.
- **No retroactive update of existing briefs.** They are working artifacts; per `docs/strands/README.md` lifecycle, they're removed when their release ships.
- File new issues for any template improvements surfaced during skill testing rather than edit `STRAND-BRIEF-TEMPLATE.md` from this strand.
- AskUserQuestion checkpoints are appropriate at material-disagreement points only; do not rubber-stamp every section.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md` — template is the source; skill reads it.
- `feedback_strand_worktree_path.md` — explicit-path form is what the skill should suggest by default.
- `feedback_shared_tree_branch_verification.md` — generated brief should include the verification rule.
- `feedback_explicit_mechanics.md` — skill output should be human-readable; no clever abstractions hiding the structure.
- `feedback_unfold_tdf26_work_fit.md` — this strand is tdf26-craft; cross-link the unfold note candidate ([unfold#40](https://github.com/gneeek/unfold/issues/40)) for awareness but don't open new unfold work from inside this strand.

## 10. Stop when

- Skill exists at agreed location and is callable.
- Sample invocation produces a brief that visually matches the template structure.
- Section-presence test passes (all 10 section headers appear in generated output).
- One-line skill usage hint added to `docs/strands/README.md`.
- PR open and tagged on milestone v1.4.18.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-skill` once the work has merged.
- Final report posted to publisher: PR link, sample brief output snippet, any open questions for the publisher to refine the skill's defaults.
