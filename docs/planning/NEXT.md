# Planning continuation note

> **Singleton convention:** at most one open planning continuation lives at this path. When a planning session closes that this note tracked, rename to a date-stamped archive (e.g. `docs/planning/2026-06-XX-archive.md`) or delete. New sessions overwrite this file.

> **This note supersedes the 2026-05-28 → seg-18 run-in continuation** (preserved in git history). That note's flagged "run a full planning session once seg 18 ships" action is now done: the **2026-06-28 endgame triage** retired the backlog, wound down the milestones, and put the project into its finish-and-close stretch.

## Status (2026-06-28) — the project is finishing

Segs 1–24 are published (`W26-seg24`, 2026-06-27). The infrastructure chapter closed two retros ago; the project is in **run-mode** and **closes after the real Stage 9 on 2026-07-12**. See the [W23-seg18 retro](https://github.com/gneeek/tdf26/wiki/Retro-W23-seg18-W26-seg24).

**Done since the triage opened (merged to main, fast — parallel sessions):**
- **Seg 25 — Meymac** drafted and merged as `content/entries/25-meymac-and-the-cote-des-gardes.md` (#704/#705); re-slugged off the stub; tracking issue #703 closed.
- **#502 — Tour-history essay** "Poulidor Country" shipped (#702); the umbrella issue #502 stays open.
- **Dependabot** npm group landed via #707; #689 closed (superseded); the `strand-deps-689.md` brief is spent.
- **Strand briefs merged** (#701, #706).

**Remaining content (unblocked, ready to run):**

| Work | Strand brief | Status |
|------|--------------|--------|
| Segs 26 → 27 (Saint-Angel, then the Ussel finish) | `docs/strands/strand-segs-26-27-drafting.md` | **Unblocked** — its Phase-0 prerequisite (merged seg 25 + #502) is satisfied; segs 26/27 are still stubs |

Segs 26 and 27 are the only remaining content. Seg 27 closes the 27-segment arc.

## Decisions made (2026-06-28 endgame triage)

- **Backlog retired.** 17 open issues closed not-planned + `wontfix` (developer-experience, admin tooling, process-mechanism, deferred features, and the data-correctness items judged out of runway). Only #502 carried.
- **Milestones wound down.** v1.4.20 + v1.4.21 closed (drained, moved to the Roadmap "Completed" list). v1.6.0 renamed *"Admin tooling (retired, not shipped)"* and closed. v1.5.0 renamed **"Finish line and project close"** — the only open milestone — holding #502, #703, #708, #709.
- **Endgame issues filed.** [#708](https://github.com/gneeek/tdf26/issues/708) closing retrospective; [#709](https://github.com/gneeek/tdf26/issues/709) archive/handoff of final state; [unfold#46](https://github.com/gneeek/unfold/issues/46) portable-learnings harvest (filed on unfold per the ownership split).
- **Wiki Roadmap updated** to the wind-down shape (Now = finish line → After the stage = project close → Later = retired feature milestones).

## Sequenced execution (what is left)

1. **Finish the content** (this week): seg 25 + #502 + the dependabot bump are done; run the segs 26–27 strand to draft the last two entries.
2. **Land the finish** (through 2026-07-03): seg 27 closes the 27-segment arc; the Tour-history surface goes live for the stage-week reader peak.
3. **Close the project** (after the 2026-07-12 stage): execute the three endgame issues — closing retro (#708), archive/handoff (#709), unfold harvest ([unfold#46](https://github.com/gneeek/unfold/issues/46)).

## Open carryforwards

The carryforward backlog is **cleared** — everything not retired is now one of the four open issues above. The only forward work is finishing the content and executing the three close issues. `project_next_planning_notes.md` (agent memory) holds the per-strand close-out detail and the W23-seg18 retro-handoff block.

## Pointers

- Open milestone: https://github.com/gneeek/tdf26/milestone/26 (Finish line and project close)
- Strand briefs: `docs/strands/` (seg-25, segs-26-27, 502, deps-689)
- Latest retro: https://github.com/gneeek/tdf26/wiki/Retro-W23-seg18-W26-seg24
- Roadmap (wiki): https://github.com/gneeek/tdf26/wiki/Roadmap
- Planning-notes memory: `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- Prior planning archives: `docs/planning/2026-05-28-archive.md` (and 05-12, 05-07)
