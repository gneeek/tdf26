# Planning continuation note

> **Singleton convention:** at most one open planning continuation lives at this path. When a planning session closes that this note tracked, rename to a date-stamped archive (e.g. `docs/planning/2026-05-07-archive.md`) or delete. New sessions overwrite or replace this file.

## Status at handoff

The 2026-05-07 planning session (morning + afternoon resume) closed the evening of 2026-05-07. There is **no open planning continuation** at this moment. This note exists as a forward-looking pointer for the next planning session, not a mid-session handoff.

Next planning trigger is whichever fires first:

- **Retro v1.4.18 / W19-seg11** — fires after the seg 11 production deploy on Sun 2026-05-10 (production-deploy-bounded per Topic 9c). The retro will surface its own outputs into `project_next_planning_notes.md`; a planning session typically follows.
- **Carryforwards reach a threshold** that warrants a session before the next retro fires.
- **Publisher schedules an explicit session.**

## Reading order for the next session

1. **This note**, then archive it the moment a real continuation is needed.
2. **`project_next_planning_notes.md`** in agent memory — has the running carryforward backlog plus the **"Stats and observations for the next retro (2026-05-07 evening close)"** section that summarises today's outputs. The file also has a final **"Carryforwards for the next planning session"** entry the publisher specifically asked to be raised.
3. **`docs/planning/MILESTONE-SCOPE-TEMPLATE.md`** — pinned 2026-05-07 (Topic 9b). The next planning session writes its first scope file using this template.
4. **`docs/planning/2026-05-07-archive.md`** — the archived continuation note from the 2026-05-07 morning planning, preserved for context.

## State of work

### Releases

- **v1.4.18** — Data-layer stability + seg 11 prep. Expected production deploy: Sun 2026-05-10 with seg 11 publish (tag `W19-seg11`). 9 issues still open in milestone (some may close via the seg 11 publish itself; carryforwards into v1.4.19 expected).
- **v1.4.19** — Reader uplift + segs 14-16 prep. 10 issues open. Includes today's #441 (CodeQL — closed), #503 (historical-tdf seg-27 keying), #517 (UI hardcoded climb data), #518 (summit-km invariant), #522 (EntryCard — closed), #483 (instrumentation), #466 (map render), #492 (closed), #311, #481, #326.
- **v1.4.20 — TBD.** 8 issues open. Verification briefs (#498/#499/#500), tour-history (#502 + #527), test harness (#508), worktree bootstrap (#509), and other v1.4.20-tagged work.

### Strand briefs on `main`

13 in `docs/strands/`. Categorised:

- **Spawned + merged this session (3):** `strand-seg-11-drafting.md`, `strand-tour-history-research.md` (Session 2), `strand-522-entrycard-extraction.md`. Plus `strand-441-codeql-shell-injection.md`, `strand-519-date-based-tags.md` (these may have been spawned by the publisher between briefcommit and execution; PRs #532 / #533 cleared them).
- **Spawned but no PR yet, sibling work landed in #520 (1):** `strand-publisher-contract.md`. Wiki edit may or may not be complete; check `gneeek/tdf26.wiki.git` before re-spawning.
- **Ready to spawn (4):** `strand-seg-12-drafting.md`, `strand-seg-13-drafting.md`, `strand-498-verify-segs-17-19.md`, `strand-499-verify-segs-20-22.md`, `strand-500-verify-segs-23-26.md`.
- **Ready, separate cadence:** `strand-voices-design-session.md`.
- **Pending v1.4.18 retro sweep:** the six v1.4.18+ briefs whose work shipped today and earlier (`strand-d-content-research`, `strand-i-verify-segs-14-16`, `strand-claude-md-deprecation`, `strand-climb-data`, `strand-publish-sh-fail-fast`, `strand-skill-strand-brief`).

### Open questions for the next planning session

Highlights from `project_next_planning_notes.md`'s **Carryforwards for the next planning session** section:

- **Strand-brief template: retro-flavored close-out + stats.** Should §10 mandate retro-relevant observations and numeric stats (tokens used, context-window HWM, AskUserQuestion count, etc.) at session close? Today's strand sessions added observations voluntarily; codifying it would standardise. Decisions needed: which stats are agent-accessible, where they land, optional vs mandatory, whether to add a §11 or fold into §10. Single template edit once decided.

Plus the carryforwards from earlier today that didn't get final closure but are not blocking:

- Existing milestone names under date-based scheme — settled "future-only" but the next milestone created after 2026-05-07 will be the first instance of a non-semver name. Decide its naming form at creation time.
- Voices design session — brief authored, separate cadence; spawn whenever the publisher schedules it.
- Tully/Piers explainer pages — unfold#44 (mechanics-explainer) blocks tdf26#529 (origin-story page). Re-evaluate when unfold#44 lands.

### Carryforwards from the strand-execution sessions

The strand sessions added their own retro-eligible observations to `project_next_planning_notes.md` while running today:

- **Memory examples drift between decision-time and implementation-time** (from the #519 strand): when a memory captures a decision with an example, expect drift if the decision lands later — implementation should reconcile.
- **Multi-axis decision via successive AskUserQuestion rounds** (from the #519 strand): three iterations, each substantive. Worked example for the brief-template's "load-bearing checkpoint" guidance.

Plus whatever the in-flight publisher-contract / tour-history sessions added that the planning session didn't get back to.

## Pointers

- Original 2026-05-07 morning agenda: `/home/jhs/.claude/plans/inherited-enchanting-cascade.md`
- Afternoon-resume plan: `/home/jhs/.claude/plans/rosy-wiggling-crescent.md`
- Strand briefs directory: `/home/jhs/code/tdf26/docs/strands/`
- Milestone-scope template: `/home/jhs/code/tdf26/docs/planning/MILESTONE-SCOPE-TEMPLATE.md`
- Planning-notes file (durable input/output): `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- Archived continuation: `/home/jhs/code/tdf26/docs/planning/2026-05-07-archive.md`
