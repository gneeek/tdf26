# Planning session continuation — 2026-05-07

> **Singleton convention:** this file lives at `docs/planning/NEXT.md`. At most one open planning continuation exists at a time; if a session is in progress, this is where its handoff state lives. When the session it tracks closes, rename to a date-stamped archive (e.g. `docs/planning/2026-05-07-archive.md`) or delete. New planning sessions that need a continuation overwrite or replace this file.

This note hands off mid-session state to a future Claude Code session that will resume the 2026-05-07 planning. Read this first; cross-references point at the durable artifacts (issues, strand briefs, the original agenda).

## How to resume

1. **Read this note** in full.
2. **Read the original agenda** at `/home/jhs/.claude/plans/inherited-enchanting-cascade.md` for the topic-by-topic structure and the per-topic context. Today's session worked through topics 1, 2, 3, 4, 5, 6, 7, 10, 12 in that order. Remaining topics: **8, 9, 11, 13, 14, 15** (in suggested order; the publisher may reshuffle).
3. **Confirm the current strand status with the publisher** before authoring more strand briefs — strand status changes between sessions and the table below is a snapshot.
4. **Use the `/strand-brief` skill** for any new strand briefs. The skill landed in this session and reads `docs/strands/STRAND-BRIEF-TEMPLATE.md` at invocation time.
5. **At session close**, run the "items to record in `project_next_planning_notes.md`" checklist (below).

## Session state at handoff

- **Date:** 2026-05-07.
- **Context:** post Retro v1.4.17 (filed earlier today). Session shapes the back half of v1.4.18 (seg 11 publishes Sun 2026-05-10, deadline now cleared by the publish.sh fail-fast strand) and seeds v1.4.19 / v1.4.20.
- **Workflow in use:** topic-by-topic, no time boxes. Decisions captured via AskUserQuestion. Strand briefs written when work is clear and independent; spawned strands run in parallel during the session.
- **Strands completed in-session (4):** content research km 70-92, CLAUDE.md known-waypoints deprecation, `/strand-brief` skill, publish.sh fail-fast.
- **Strand-brief template** lives at `docs/strands/STRAND-BRIEF-TEMPLATE.md`; the publisher edited it during the session — that edit is intentional, do not revert.

## Decided topics (this session)

| # | Topic | Outcome |
|---|---|---|
| 1 | Publication: segs 11/12/13 by Sun afternoon | Block-research + 3 publisher-paced drafting strands |
| 2 | Data verification: #478 + segs 17-26 gap | #498/#499/#500 filed (v1.4.20 placeholder); #478 brief written |
| 3 | publish.sh fail-fast | #496 expanded to fail-fast policy per failure mode; brief written; ✅ shipped |
| 4 | CLAUDE.md known-waypoints + data-layer regime expansion | Deprecate path; #490/#491/#492 → v1.4.19; #491 ✅ shipped; #490+#492 brief written |
| 5 | Strand-brief template | Path C (file + skill); template + README + skill ✅ shipped; unfold#40 filed |
| 6 | Tour-history feature scoping | Dedicated `/tour-history` route + homepage card; soft-launch URL early, prominent launch pre-stage; #502 + #503 filed; research strand brief written |
| 7 | Content / voice forward-looking | Auzelou seg 11 (cyclosportive primary), Sainte-Fortunade seg 14 (Monédières establishment), music ledger keep-prose, Mascaron deferred pending #500 |
| 10 | Date-gated experiment evaluations | Block-research + register-shifts both hold light-tier; tracking-issue-per-deploy watch-item closed (unfold#36 comment added) |
| 12 | Testing infrastructure | bats harness #508 filed (v1.4.20); worktree bootstrap #509 filed (v1.4.20); 3 light-tier carryforwards held |

## Strand status at handoff

Status legend: ✅ done · 🚀 spawned (running) · 📝 brief written, ready to spawn · ✏️ writeable, decisions made · 🚧 blocked

| Status | Brief / Strand | Milestone | Notes |
|---|---|---|---|
| ✅ | `strand-d-content-research.md` | v1.4.18 | Block research km 70-92 (segs 11-13) |
| ✅ | `strand-claude-md-deprecation.md` (#491) | v1.4.19 | CLAUDE.md known-waypoints tables → JSON pointers |
| ✅ | `strand-skill-strand-brief.md` (`/strand-brief` skill) | v1.4.18 | Skill is callable in any tdf26 session |
| ✅ | `strand-publish-sh-fail-fast.md` (#496) | v1.4.18 | Three publish.sh fixes shipped; Sun deadline cleared |
| 📝 | `strand-i-verify-segs-14-16.md` (#478) | v1.4.19 | Spawn ~1 week (after seg 13 stabilises) |
| 📝 | `strand-climb-data.md` (#490 + #492) | v1.4.19 | Anytime in v1.4.19 |
| 📝 | `strand-tour-history-research.md` (#502) | v1.4.20 | Research-only; runs for days |
| ✏️ | `strand-verify-segs-17-19.md` (#498) | v1.4.20 | Spawn ~3 weeks; can scaffold via `/strand-brief` |
| ✏️ | `strand-verify-segs-20-22.md` (#499) | v1.4.20 | Spawn ~5 weeks; can scaffold via `/strand-brief` |
| ✏️ | `strand-verify-segs-23-26.md` (#500) | v1.4.20 | Spawn ~6 weeks; can scaffold via `/strand-brief` |
| ✏️ | Seg 11 drafting strand | v1.4.18 | Auzelou framing decided; voice register at draft time |
| 🚧 | Seg 12 drafting strand | v1.4.19 | Voice + seg 11 publication learnings |
| 🚧 | Seg 13 drafting strand | v1.4.19 | Voice |

## Issues filed / updated this session

**Filed (tdf26):**
- [#498](https://github.com/gneeek/tdf26/issues/498) — Data verification segs 17-19 (Treignac, Côte de la Croix de Pey), v1.4.20
- [#499](https://github.com/gneeek/tdf26/issues/499) — Data verification segs 20-22 (Plateau de Millevaches, Mont Bessou), v1.4.20
- [#500](https://github.com/gneeek/tdf26/issues/500) — Data verification segs 23-26 (Meymac, Ussel finish), v1.4.20
- [#502](https://github.com/gneeek/tdf26/issues/502) — Tour-history feature umbrella, v1.4.20
- [#503](https://github.com/gneeek/tdf26/issues/503) — `historical-tdf.json` segment-27 drift, v1.4.19
- [#508](https://github.com/gneeek/tdf26/issues/508) — Shell scripts have no test harness, v1.4.20
- [#509](https://github.com/gneeek/tdf26/issues/509) — Worktree bootstrap fragility, v1.4.20

**Updated (tdf26):**
- [#496](https://github.com/gneeek/tdf26/issues/496) — retitled to fail-fast policy per failure mode; milestone v1.4.18; planning decision recorded as comment
- [#490](https://github.com/gneeek/tdf26/issues/490), [#491](https://github.com/gneeek/tdf26/issues/491), [#492](https://github.com/gneeek/tdf26/issues/492) — moved to v1.4.19; planning-decision comments added

**Filed (unfold):**
- [#40](https://github.com/gneeek/unfold/issues/40) — heavy-tier note candidate: strand-brief template shape

**Comment added (unfold):**
- [#36](https://github.com/gneeek/unfold/issues/36) — tracking-issue-per-deploy worked-example list updated; tdf26 watch-item closed

## Remaining topics — suggested order

| # | Topic | Why this slot now |
|---|---|---|
| 8 | **Publisher / developer-experience contract** | Wiki-edit strand candidate. Becomes urgent when second publisher arrives (per `project_publisher_onboarding.md`); currently implicit because publisher and developer are the same person. Natural home: How-We-Work wiki page alongside late-add/hotpatch policy. |
| 9 | **OODA alignment (versioning + planning-Decide artifact + retro-scope)** | Discussion-heavy; not parallelisable. Three items plausibly resolve as one conversation. Likely interacts with #481 (planning-shape design) and decisions about how this very planning session was run. |
| 11 | **Process / wiki / older retro carryforwards** | Batch-decide. Items: slip-rate tally artifact, How-We-Work → docs/strands link, full-lifecycle release checklist, drafter-as-first-fresh-reader, pre-locked decision tables, pair-writing disclosure forwards-consistency, cultural-threads ledger format (already pinned at Topic 7), verify-then-mutate-with-scope-first rule, class-of-bug residue, end-to-end render verification, parallel-source-of-truth detector, audit completeness. |
| 13 | **Strand C carryforwards + Voices project / unfold pending** | Batch. Items: EntryCard duplication, "One improvement only" rule, Voices project design questions (4 open), content lints, status check on unfold#35/#36. |
| 14 | **Backlog sweep** | Unmilestoned: #309, #339, #364, #387, #441, #473, #482. Decide schedule / defer / close per issue. |
| 15 | **Sweep / clear** | Session close — clear RESOLVED items from `project_next_planning_notes.md`; record new items per the checklist below. |

## Items to record in `project_next_planning_notes.md` at session close

This is the checklist the new session runs at session close. Add as durable lines in the planning-notes file (under appropriate sections).

**Decisions to record:**
- Topic 1: block-research + 3 publisher-paced drafting strands chosen for segs 11-13. Strand D landed.
- Topic 2: segs 14-16 verification (#478) v1.4.19; segs 17-26 split into #498/#499/#500 v1.4.20 placeholder; #478 brief written today.
- Topic 3: publish.sh fail-fast policy per failure mode landed (#496 closed); chore-deploy wrapper deferred (no instance fired this cycle); pre-publish PR pattern still deferred for codification.
- Topic 4: CLAUDE.md known-waypoints deprecate path chosen; #491 landed; #490+#492 paired in v1.4.19 brief written.
- Topic 5: strand-brief template Path C; both file (`docs/strands/STRAND-BRIEF-TEMPLATE.md`) and skill (`/strand-brief`) shipped; unfold#40 filed as heavy-tier candidate.
- Topic 6: Tour-history feature = dedicated `/tour-history` route + homepage card; soft-launch URL early, prominent launch pre-stage; #502 umbrella + #503 data-drift fix filed; research strand brief written.
- Topic 7: Auzelou seg 11 frame = cyclosportive primary; Sainte-Fortunade Monédières framing lands at seg 14 entry with cherry detail; music threads ledger stays as planning-notes prose; Mascaron seg-24-vs-25 deferred pending #500.
- Topic 10: block-research-then-N-drafts holds light-tier; register-shifts holds light-tier; tracking-issue-per-deploy watch-item **closed** (unfold#36 covers it).
- Topic 12: bats harness #508 filed (v1.4.20); worktree bootstrap #509 filed (v1.4.20); 3 light-tier carryforwards continue (external tooling supplies test spec; red-demonstration via physical breakage; v1.4.11 Strand C smoke-vs-deletion).

**Carryforwards to remove from the planning-notes file** (since they're decided):
- Image frontmatter convention (already RESOLVED 2026-05-06; clearable)
- Data-layer stability regime (already RESOLVED 2026-05-06; clearable)
- Late-add + hotpatch policy (already RESOLVED 2026-05-06; clearable)
- All Topic 1-7 + 10 + 12 items above (now decided this session; clearable)
- Tracking-issue-per-deploy watch-item (Topic 10 closed it)
- Date-gated 2026-05-07 evaluations (Topic 10 held both light-tier; new evaluation date depends on segs 11-13 reader signal — re-flag at the next planning if the publisher wants explicit re-evaluation)

**New carryforwards to add:**
- Mascaron / Saintsbury voice may need to shift from seg 24 to seg 25 per `data/segments.json`; awaiting #500 verification.
- Music threads ledger format pinned as planning-notes prose; promotion criteria recorded (ledger > 6 threads / lookup cost bites / rendering surface needs data).
- Sainte-Fortunade Monédières framing lands at seg 14 entry (Dautrement quote + cherry-15-days-earlier microclimate detail together).
- Auzelou seg 11 frame: cyclosportive-departure primary, "99-100 days before stage" as one rhetorical beat, amateur-cycling embedded.
- Six new issues filed today (#498/#499/#500/#502/#503/#508/#509); all v1.4.19 or v1.4.20 placeholder; reshuffle as milestones shape.
- Five strand briefs in `docs/strands/` ready to spawn; four already shipped.

**Memory update items** (potentially):
- `project_meymac_voice.md` may need an edit to reflect "seg 24 OR seg 25 pending #500"; do not change today.
- `project_barthes_callback.md` says seg 6/12/15; verify against current `data/segments.json` if #500 surfaces a similar drift.

## Open carryforwards from the original agenda not yet addressed

These are in the agenda but not yet decided. They live in topics 8, 9, 11, 13, 14, 15. The new session covers them. Highlights:

- **OODA alignment (Topic 9):** versioning scheme, planning-Decide → retro-Observe artifact, retro-scope convention. Three items, likely one conversation. Cross-link [#481](https://github.com/gneeek/tdf26/issues/481).
- **Publisher / developer-experience contract (Topic 8):** how-we-work edit; becomes social fact when second publisher arrives.
- **Backlog sweep (Topic 14):** #309, #339, #364, #387, #441, #473, #482.
- **Strand C carryforwards (Topic 13):** EntryCard duplication, "one improvement only" rule.
- **Voices project (Topic 13):** four open design questions.

## Notes for the new session's first actions

- The `/strand-brief` skill is now available. Use it for #498/#499/#500 brief scaffolding when those are written.
- The strand-brief template at `docs/strands/STRAND-BRIEF-TEMPLATE.md` was edited mid-session by the publisher; the section structure may differ from the version in this note. Read the actual file at invocation time.
- Four strand briefs are uncommitted and live on `main`: `STRAND-BRIEF-TEMPLATE.md`, `README.md` (in docs/strands), four shipped briefs (D, deprecation, skill, publish-sh-fail-fast — these may have been committed by the strands themselves), and the not-yet-spawned briefs (i-verify-14-16, climb-data, tour-history-research). Confirm git state at the start of the new session.
- This continuation note itself is uncommitted. The publisher decides whether to commit + push before the new session, or hand the path to the new session directly.

## Pointers

- Original agenda: `/home/jhs/.claude/plans/inherited-enchanting-cascade.md`
- Strand briefs directory: `/home/jhs/code/tdf26/docs/strands/`
- Planning-notes file (durable input/output): `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/project_next_planning_notes.md`
- Memory index: `/home/jhs/.claude/projects/-home-jhs-code-tdf26/memory/MEMORY.md`
- This continuation note: `/home/jhs/code/tdf26/docs/planning/NEXT.md` (singleton convention — there is at most one open planning continuation under this name; rename to a date-stamped archive when the planning session it tracks closes, or delete if no archive is needed)
