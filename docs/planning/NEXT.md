# Planning continuation note

> **Singleton convention:** at most one open planning continuation lives at this path. When a planning session closes that this note tracked, rename to a date-stamped archive (e.g. `docs/planning/2026-06-XX-archive.md`) or delete. New sessions overwrite this file.

> **NEXT ACTION (flagged 2026-06-03): run a full planning session once segment 18 ships today.** The 2026-06-03 session was scoped to the seg-18 publication process *only* (publisher's call — publish day, fresh rider stats in hand). Much of v1.4.20 has drained since the 2026-05-28 handoff (gate fixes, spine #508/#322/#479, geometry-drift, data corrections, release ceremony, segs 17/18/19 drafted), and the carryforward list in `project_next_planning_notes.md` has grown well past the ~15-item trigger noted below — so the planning session is due. Read those close-outs as the primary input.

## Status at handoff (2026-05-28 planning session close)

Segs 1–16 are published (seg 16 shipped 2026-05-28). **v1.4.19 is closed** (drained, 23 issues). **v1.4.20 is themed: "Publish-pipeline hardening"** and trimmed to a 10-issue set. The next planning session has no fixed trigger — it fires when v1.4.20 drains, or sooner if the carryforward list (below) grows past ~15 items.

## Decisions made this session

- **v1.4.20 spine = publish-pipeline hardening.** Chosen over data-to-display reconciliation because seg 16 404'd in production; an unsafe publish.sh is the top reader-reliability risk with 11 segments left. Scope file: `docs/planning/v1.4.20-scope.md`.
- **Three publish-day fixes are a hard gate before seg 17 (Sun 2026-05-31):** #617 (draft pre-flight), #618 (gh-merge idempotency), #619 (weather --entry). Weekend strand brief written: `docs/strands/strand-publish-safety-617-618-619.md`. **Publisher to spawn it this weekend.**
- **#502 tour-history → v1.5.0, shape = standalone July-2 essay entry.** Publishes between seg 26 (07-01) and seg 27 (07-03, already moved via #616). Design now, schedule into the July milestone. Seg 16's closing line already foreshadows it date-free.
- **Data-to-display reconciliation is the candidate spine for the *next* milestone.** Cluster seeded in backlog: #517, #588, #486, #476, #487. Climb data fixes don't reach readers because StageDetails.vue/ElevationChart.vue hardcode parallel values.

## Content production line (the critical path — binding constraint on the run-in)

The entries are the deliverable; this line gates the schedule, the pipeline milestone runs alongside it.

**Drafting:** segs 1–16 published. **Segs 17–27 are all stubs** (`draft: true`, title-only) — 11 entries to write, twice-weekly, with no schedule slack:

| Seg | Publish | Research ready? |
|-----|---------|-----------------|
| 17 | 2026-05-31 | ✅ 17-19 dossier |
| 18 | 2026-06-03 | ✅ 17-19 dossier |
| 19 | 2026-06-07 | ✅ 17-19 dossier |
| 20 | 2026-06-10 | ❌ **needs 20-22 dossier** |
| 21 | 2026-06-14 | ❌ needs 20-22 dossier |
| 22 | 2026-06-17 | ❌ needs 20-22 dossier |
| 23 | 2026-06-21 | ❌ **needs 23-27 dossier** |
| 24 | 2026-06-24 | ❌ needs 23-27 dossier |
| 25 | 2026-06-28 | ❌ needs 23-27 dossier — **Meymac, saintsbury voice reservation** (`project_meymac_voice.md`) |
| 26 | 2026-07-01 | ❌ needs 23-27 dossier |
| — July special | 2026-07-02 | ✅ `tour-history-research.md` |
| 27 | 2026-07-03 | ❌ needs 23-27 dossier — Ussel finish line |

**Research gaps to spawn (block-research-then-N-drafts shape, the stable dossier pattern):**
- **Segs 20–22 dossier** — must land before seg 20 drafts (~2026-06-10). Spawn ~first week of June.
- **Segs 23–27 dossier** — must land before seg 23 drafts (~2026-06-21). Larger block (finish-line stretch); settle the seg-25 Meymac voice at the same time.

**Committed strands this cycle.** Three briefs are written and scheduled to run within the v1.4.20 cycle — they are this-cycle work, not deferred:
- `docs/strands/strand-seg-17-drafting.md` — run now, for the 2026-05-31 slot.
- `docs/strands/strand-segs-20-22-content-research.md` — run before seg 20 (~06-10).
- `docs/strands/strand-segs-23-27-content-research.md` — run before seg 23 (~06-21).

## Sequenced execution

1. **This weekend:** spawn the publish-safety strand; merge #617/#618/#619 before seg 17.
2. **Seg 17 cycle (Sun 2026-05-31):** draft + publish on the hardened pipeline. Brief ready: `docs/strands/strand-seg-17-drafting.md` (note: seg 17 = **Madranges + the Treignac approach**; the stub is mis-titled "treignac-granite-and-water" — that's seg 18 — re-title at the anchor checkpoint).
3. **Segs 17–19 drafting cadence:** publisher-paced, one strand per segment; handle dossier-flagged data corrections (#549, #551, #602, #603) inline. Briefs for segs 18/19 to scaffold from the same 17-19 dossier.
4. **Spawn the 20–22 research dossier** before seg 20 (~06-10): `docs/strands/strand-segs-20-22-content-research.md`. **Spawn the 23–27 dossier** before seg 23 (~06-21): `docs/strands/strand-segs-23-27-content-research.md` (settles the seg-25 Meymac voice + corrects the segs 24/25/26 stub-title drift).
5. **July-2 tour-history essay (#502):** design now, draft from `tour-history-research.md` ahead of 07-02.
6. **Pipeline spine + ceremony (#322/#479/#508/#326/#480/#521/#339):** across the seg 17–20 cycles, alongside (not gating) drafting.

## Open carryforwards (not decision-pending; carry unless cleared)

- **Data-to-display reconciliation cluster** (#517/#588/#486/#476/#487) — next-milestone candidate spine.
- **Summit-km data backlog** (#589/#590/#591) — opportunistic; clears the #518 assertion skip-list. Not milestone-gated.
- **Off-theme backlog** (#483 instrumentation, #481 planning shape, #466 map perf, #409 rider-stats, #509 worktree bootstrap) — reassess next planning.
- **Tour-history July-2 essay design** — v1.5.0; decide drafting cadence and voice closer to July.
- **Recommended-option calibration** — monitor for rubber-stamping. (Note: this session hit one option-set-too-binary signal on the pipeline-timing question; re-fired cleanly.)
- **Tully/Piers explainer pages** — unfold#44 blocks tdf26#529.
- **Voices design session** — `docs/strands/strand-voices-design-session.md`; spawn when scheduled.
- **Strand-as-first-class unfold candidate** — re-evaluate after the v1.4.20 multi-strand cycle.
- **Doc drift:** `data/riders/rider-config.json` `startDate` is `2026-04-01`; CLAUDE.md says `2026-04-02`. Reconcile (file a small issue or fix in a data-hygiene pass). Walker arithmetic in the seg-16 notes assumes 04-01.

## Reading order for the next session

1. This note.
2. `project_next_planning_notes.md` (agent memory) — strand close-out inputs since this session.
3. `docs/planning/v1.4.20-scope.md` — what we said we would do.
4. The next Retro's "What we lack" section.
5. `docs/planning/2026-05-28-archive.md` — this session's archived inputs.

## Pointers

- v1.4.20 scope: `docs/planning/v1.4.20-scope.md`
- Milestone-scope template: `docs/planning/MILESTONE-SCOPE-TEMPLATE.md`
- Strand briefs: `docs/strands/`
- Planning-notes memory: `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- v1.4.20 milestone: https://github.com/gneeek/tdf26/milestone/53
- Roadmap (wiki): https://github.com/gneeek/tdf26/wiki/Roadmap
- Slip-rate tally (wiki): https://github.com/gneeek/tdf26/wiki/Slip-rate-tally
