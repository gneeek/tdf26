# Strand: Publisher / developer-experience contract

Wiki-edit strand. Authored at the 2026-05-07 planning session (Topic 8a). Not yet spawned.

## 1. Goal

Land a "Publisher / developer-experience contract" section on the How-We-Work wiki page. The contract has been implicit because the publisher and developer are the same person; it becomes a social fact when a second publisher is active (per `project_publisher_onboarding.md`). The deliverable is wiki text that a new publisher can read once and operate from. Milestone: v1.4.20 placeholder; promote to v1.4.19 if the second publisher's first ship arrives sooner.

## 2. Filesystem posture

This strand does not touch the tdf26 repo's source tree. It edits the GitHub wiki (separate git repo at `gneeek/tdf26.wiki.git`).

- Clone the wiki repo:
  ```
  git clone https://github.com/gneeek/tdf26.wiki.git /home/jhs/code/tdf26-wiki
  ```
- Edit `How-We-Work.md` (or whatever the existing page is named — verify on first checkout).
- No worktree against the main repo is needed.

## 3. Source-of-truth posture

The wiki is the canonical home for process documentation. Cross-link from in-repo docs/strands/README.md or CLAUDE.md only when readers need a process pointer; do not duplicate the contract text.

## 4. Target deliverables

One wiki edit. Optionally one in-repo `docs/strands/README.md` cross-link.

No corresponding GitHub issue at brief time; if scope grows, file an umbrella issue per `feedback_issues_describe_problems.md`.

## 5. Workflow

1. Read the current How-We-Work page; identify the existing structure and where the contract section fits.
2. Draft the contract sections inline (see "Contract content" below).
3. Apply the late-add / hotpatch policy carryforward from Topic 11 if it lands as part of this strand (otherwise leave a placeholder + link).
4. Commit and push to the wiki.
5. Update the planning-notes file's "next planning" carryforward to remove the publisher-contract line once the wiki edit lands.

## 6. Verification

- Open the wiki page in a browser; read the new section as if you were a new publisher onboarding.
- Have the publisher review the draft before final push (this strand should run in publisher-paced single-strand mode — see `feedback_multi_strand_session_checkpoints.md` and Topic 8b sharpening).

## 7. Cross-strand sharing notes

- **Owns (write):** `tdf26.wiki.git`'s How-We-Work page section on the contract.
- **Reads:** `feedback_multi_strand_session_checkpoints.md`, `feedback_carry_debt_reading.md`, `feedback_pre_publish_scrutiny.md`, `feedback_content_change_rule.md`, `project_contributor_is_customer.md`, `project_publisher_onboarding.md`, `feedback_issues_describe_problems.md`, `feedback_roadmap_style.md`.
- **Must not touch:** in-repo files except a possible one-line cross-link in `docs/strands/README.md`.

## 8. Scope discipline

Contract content (what the contract should cover):

1. **Publisher's promises to the developer / agents:** scope decisions made before strand spawn; AskUserQuestion checkpoints answered within the session window; out-of-scope items filed as issues rather than inlined; retro participation.
2. **Developer's / agents' promises to the publisher:** issues describe problems (not solutions); strand briefs declare ownership and read-set; PRs include test plan; visible/blast-radius actions confirmed before execution; pair-writing disclosure on content entries (per `project_disclosure_practice.md`).
3. **Workflow expectations:** publication cadence (twice weekly Sun/Wed mornings per `project_schedule.md`); pre-publish scrutiny window (per `feedback_pre_publish_scrutiny.md`); content-change rule (published entries are fixed; corrections forward, per `feedback_content_change_rule.md`); strand-brief template (per `docs/strands/STRAND-BRIEF-TEMPLATE.md`).
4. **Decision authority:** Tully owns tdf26 tie-breaking; Piers owns unfold tie-breaking (per `feedback_agent_ownership.md`); both voices contribute on every decision.
5. **Late-add / hotpatch policy:** carryforward from Topic 11 (already RESOLVED 2026-05-06 per planning-notes). Lift the existing policy text into the contract and add a one-line cross-reference if the policy lives elsewhere.
6. **Retro / planning rhythm:** retro filed after each tag; planning continuation per `docs/planning/NEXT.md` singleton convention; planning-notes file (`memory/project_next_planning_notes.md`) is the durable input/output.

Out of scope:
- New process invention. The contract is descriptive of current practice, not aspirational.
- Code or data changes.
- Slip-rate tally artifact (Topic 11 sub-item, separate strand candidate).

## 9. Memories that apply

Loaded above (§7). Most load-bearing for content authoring:

- `feedback_multi_strand_session_checkpoints.md` (post-2026-05-07 sharpening; wiki-edit strand should run publisher-paced)
- `project_publisher_onboarding.md` (verify currency before drafting; second-publisher status changes)
- `feedback_explicit_mechanics.md` (unpack vocabulary; human publishers are part of the audience)

## 10. Stop when

- Wiki page edit pushed; URL handed to publisher.
- Planning-notes file's publisher-contract carryforward line removed.
- One GitHub issue filed if scope grew beyond the wiki edit (per `feedback_issues_describe_problems.md`).
- No worktree to clean up (wiki repo lives outside `/home/jhs/code/tdf26-*`).
