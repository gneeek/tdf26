# Planning continuation note

> **Singleton convention:** at most one open planning continuation lives at this path. When a planning session closes that this note tracked, rename to a date-stamped archive (e.g. `docs/planning/2026-05-12-archive.md`) or delete. New sessions overwrite or replace this file.

## Status at handoff

The 2026-05-12 planning session closed the evening of 2026-05-12. There is **no open planning continuation** at this moment. This note exists as a forward-looking pointer for the next planning session, not a mid-session handoff.

Next planning trigger is whichever fires first:

- **Retro after `W20-seg12` production deploy** — fires after the seg 12 publication on Wed 2026-05-13 (production-deploy-bounded per Topic 9c). Retro surfaces its own outputs into `project_next_planning_notes.md`; a planning session typically follows.
- **Retro after `W20-seg13`** (Sun 2026-05-17) or **`W21-seg14`** (Wed 2026-05-20) — each is a separate retro window under the production-deploy-bounded rule.
- **Carryforwards reach a threshold** that warrants a session before the next retro fires.
- **Publisher schedules an explicit session.**

## Reading order for the next session

1. **This note**, then archive it the moment a real continuation is needed.
2. **`project_next_planning_notes.md`** in agent memory — short as of 2026-05-12 evening (117 lines after the big sweep). Top section "State at handoff to next planning (2026-05-12 evening)" lists decisions recorded today and new artifacts; "Carryforwards for the next planning session" is the active-thread list.
3. **`docs/planning/v1.4.19-scope.md`** — milestone-scope artifact for the cycle in progress. Retros for `W20-seg12` / `W20-seg13` / `W21-seg14` read this as "what we said we would do."
4. **`docs/planning/MILESTONE-SCOPE-TEMPLATE.md`** — template the v1.4.19 scope used. Next scope file (when v1.4.20 firms up) uses this template too.
5. **`docs/planning/2026-05-12-archive.md`** — historical planning notes content swept out of memory at session close, preserved for retro reference.
6. **`docs/planning/2026-05-07-archive.md`** — older archive from the prior planning session.

## State of work at handoff

### Releases

- **v1.4.18 — closed.** All carryforward issues moved to v1.4.19/v1.4.20/v1.6.0 or fixed inline at session close.
- **v1.4.19** — Reader uplift and segs 14-16 prep. 16 open issues; spans `W20-seg12` (Wed 2026-05-13) through `W21-seg14` (Wed 2026-05-20). Full scope in [v1.4.19-scope.md](v1.4.19-scope.md).
- **v1.4.20 - TBD.** 10 open issues. Theme set at the planning session that closes v1.4.19.
- **v1.5.0 / v1.6.0** — held for July (Tour de France) / Admin Tooling cycle respectively.

### PRs at session close

- [#543](https://github.com/gneeek/tdf26/pull/543) — STRAND-BRIEF-TEMPLATE.md path fix (closes #510). Awaiting merge.
- [#544](https://github.com/gneeek/tdf26/pull/544) — STRAND-BRIEF-TEMPLATE.md §10 Retro inputs sub-bullet. Awaiting merge.

This session's planning artifacts (`docs/planning/v1.4.19-scope.md` + `docs/planning/2026-05-12-archive.md` + updated `docs/planning/NEXT.md`) need a third PR — see the close-out commit checklist below.

### Strand state

| Strand brief | Status |
|---|---|
| `strand-seg-12-drafting.md` | Spawn instructions issued at planning. Publisher to run in fresh Claude Code session. Publication W20-seg12, Wed 2026-05-13. |
| `strand-seg-13-drafting.md` | Spawn Thu 2026-05-14 after seg 12 ships. Publication W20-seg13, Sun 2026-05-17. |
| `strand-498-verify-segs-17-19.md` | Ready to spawn auto-mode, this week. |
| `strand-499-verify-segs-20-22.md` | Ready to spawn auto-mode, this week. |
| `strand-500-verify-segs-23-26.md` | Ready to spawn auto-mode, this week. |
| `strand-voices-design-session.md` | Authored; separate cadence. Spawn when publisher schedules. |
| Older briefs (`strand-d-content-research.md`, `strand-i-verify-segs-14-16.md`, `strand-claude-md-deprecation.md`, `strand-climb-data.md`, `strand-publish-sh-fail-fast.md`, `strand-skill-strand-brief.md`, `strand-publisher-contract.md`, `strand-tour-history-research.md`, `strand-441-codeql-shell-injection.md`, `strand-519-date-based-tags.md`, `strand-522-entrycard-extraction.md`) | Spawned-and-merged historical briefs. Candidate for sweep at next retro per the strand-brief lifecycle convention. |

### Open carryforwards

Active threads (not blocking) per `project_next_planning_notes.md`:

- Recommended-option calibration — monitor for rubber-stamping.
- Tully/Piers explainer pages — unfold#44 blocks tdf26#529.
- Existing milestone names under date-based scheme — future-only; first instance when v1.4.20 firms or v1.4.21 created.
- Voices design session — spawn on its own cadence.
- Strand-as-first-class unfold candidate — re-evaluate after v1.4.19 ships under multi-strand cadence.

No decision-actionable carryforwards at the moment.

## Pointers

- v1.4.19 milestone-scope: `/home/jhs/code/tdf26/docs/planning/v1.4.19-scope.md`
- Milestone-scope template: `/home/jhs/code/tdf26/docs/planning/MILESTONE-SCOPE-TEMPLATE.md`
- Strand briefs: `/home/jhs/code/tdf26/docs/strands/`
- Planning-notes file (durable input/output): `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- 2026-05-12 archive: `/home/jhs/code/tdf26/docs/planning/2026-05-12-archive.md`
- 2026-05-07 archive: `/home/jhs/code/tdf26/docs/planning/2026-05-07-archive.md`
- Roadmap (wiki): https://github.com/gneeek/tdf26/wiki/Roadmap
- Slip-rate tally (wiki): https://github.com/gneeek/tdf26/wiki/Slip-rate-tally
