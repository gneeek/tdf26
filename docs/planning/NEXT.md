# Planning continuation note

> **Singleton convention:** at most one open planning continuation lives at this path. When a planning session closes that this note tracked, rename to a date-stamped archive (e.g. `docs/planning/2026-05-22-archive.md`) or delete. New sessions overwrite or replace this file.

## Status at handoff

[Retro v1.4.19](https://github.com/gneeek/tdf26/wiki/Retro-v1.4.19) fired 2026-05-22, covering `W20-seg12` + `W20-seg13` + `W21-seg14`. The next planning session is expected Mon 2026-05-25 / Tue 2026-05-26 to (a) close v1.4.19 once its minimal-set issues land, (b) set the theme and scope of v1.4.20.

Same-day pre-planning trim (2026-05-22) recorded below: v1.4.19 narrowed to a four-issue minimal close-out set; ten issues reassigned to v1.4.20.

## Pre-planning trim decision (2026-05-22)

Retro v1.4.19 surfaced that the milestone was past its original close-out target (`W21-seg14` = 2026-05-21) with 14 open issues, and that the "Reader uplift" half of the milestone title had no shipped item. The publisher took **Path B**: stretch v1.4.19 to close after seg 15 or seg 16 with a minimal scope, rather than close the milestone now and reassign all 14 (Path A).

### Kept in v1.4.19 (4 issues)

- [#513](https://github.com/gneeek/tdf26/issues/513) — Suc au May points-config drift. Seg 15 is Suc au May; must land before seg 15 publish (Sun 2026-05-24).
- [#564](https://github.com/gneeek/tdf26/issues/564) — Chirac burial location in `data/attractions.json`. Seg 15 dossier reaches for Sarran/Chirac adjacency; small data fix.
- [#535](https://github.com/gneeek/tdf26/issues/535) — Improve entry-card thumbnail selection. Honours the "at least one reader-uplift item ships visibly" criterion in the original scope file; strand brief already written at `docs/strands/strand-535-entry-card-thumbnails.md`.
- [#518](https://github.com/gneeek/tdf26/issues/518) — Climb summit km drift assertion. Five-instance carry (Lachaud, Naves, Mont Bessou, Croix de Pey, Côte des Gardes); Retro v1.4.19 promoted from candidate to must-have.

### Reassigned to v1.4.20 (10 issues)

[#311](https://github.com/gneeek/tdf26/issues/311), [#326](https://github.com/gneeek/tdf26/issues/326), [#466](https://github.com/gneeek/tdf26/issues/466), [#476](https://github.com/gneeek/tdf26/issues/476), [#479](https://github.com/gneeek/tdf26/issues/479), [#481](https://github.com/gneeek/tdf26/issues/481), [#483](https://github.com/gneeek/tdf26/issues/483), [#486](https://github.com/gneeek/tdf26/issues/486), [#487](https://github.com/gneeek/tdf26/issues/487), [#517](https://github.com/gneeek/tdf26/issues/517).

Rationale: none are reader-visible by the seg 15/16 cycle deadline, none are blocking, and the milestone-as-tag honesty cost of carrying them another cycle is lower than the schedule cost of forcing them in now.

### Sequenced execution this weekend (publisher-driven)

1. Dependabot sweep (8 open PRs).
2. Seg 15 draft + publish cycle (publishes Sun 2026-05-24).
3. v1.4.19 planning session at Mon 2026-05-25 / Tue 2026-05-26.

The four kept v1.4.19 issues line up with these phases: #513 and #564 ride the seg 15 cycle; #535 and #518 are planning-session work after.

## Next planning trigger

Mon 2026-05-25 / Tue 2026-05-26 session will:

- Close v1.4.19 once the four kept issues land, or accept further slippage explicitly with a slip-rate-tally row.
- Set the theme and full scope of v1.4.20 against its now-larger 17-issue list.
- Decide whether seg 15 and seg 16 cycles belong to v1.4.19's tail or to v1.4.20's head.

## Reading order for the next session

1. **This note.**
2. **[Retro v1.4.19](https://github.com/gneeek/tdf26/wiki/Retro-v1.4.19)** — its "What we lack" section has eight new carryforward candidates for the v1.4.20 scope.
3. **`project_next_planning_notes.md`** in agent memory.
4. **`docs/planning/v1.4.19-scope.md`** — preserved as point-in-time artifact from 2026-05-12, not rewritten.
5. **`docs/planning/2026-05-12-archive.md`** — prior session archive.

## State of work at handoff

### Releases

- **v1.4.19** — open. 18 issues closed, 4 kept (per above), 10 reassigned. Close-out target shifted from `W21-seg14` to whichever cycle the four kept issues land in.
- **v1.4.20 - TBD** — 17 open issues. Theme set at the planning session that closes v1.4.19.
- **v1.5.0 / v1.6.0** — held for July (Tour de France) / Admin Tooling cycle respectively.

### Production deploys this cycle

- `W20-seg12` (Wed 2026-05-15), `W20-seg13` (Sun 2026-05-17), `W21-seg14` (Thu 2026-05-21) all shipped on-cadence.

### Upcoming cycles

- `W21-seg15`, Sun 2026-05-24 — Suc au May, the Barthes arc "develops" beat per `project_barthes_callback.md`. No drafting brief yet at brief-write time of this note; scaffold via `/strand-brief` before spawn.
- `W22-seg16`, Wed 2026-05-27.

### Open PRs

Fluid as of this note; the dependabot sweep is one of the three priorities above. Refresh `gh pr list` at planning time.

## Open carryforwards

Active threads (not decision-pending; carry forward to next planning unless cleared):

- Recommended-option calibration — monitor for rubber-stamping.
- Tully/Piers explainer pages — unfold#44 blocks tdf26#529.
- Existing milestone names under date-based scheme — future-only; first instance whenever v1.4.21 is created.
- Voices design session — spawn when publisher schedules it.
- Strand-as-first-class unfold candidate — re-evaluate with the v1.4.19 cycle's multi-strand evidence in hand.
- Retro v1.4.19 "What we lack" items (8) — promotion-decision-actionable at next planning. Climb-coord assertion (#518) and tour-history reader surface (#502) are the two carrying >1 retro per the slip-rate tally row at the bottom of the retro page.

## Pointers

- v1.4.19 milestone-scope (point-in-time): `/home/jhs/code/tdf26/docs/planning/v1.4.19-scope.md`
- Milestone-scope template: `/home/jhs/code/tdf26/docs/planning/MILESTONE-SCOPE-TEMPLATE.md`
- Strand briefs: `/home/jhs/code/tdf26/docs/strands/`
- Planning-notes file (durable input/output): `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- 2026-05-12 archive: `/home/jhs/code/tdf26/docs/planning/2026-05-12-archive.md`
- Roadmap (wiki): https://github.com/gneeek/tdf26/wiki/Roadmap
- Retro v1.4.19 (wiki): https://github.com/gneeek/tdf26/wiki/Retro-v1.4.19
- Slip-rate tally (wiki): https://github.com/gneeek/tdf26/wiki/Slip-rate-tally
