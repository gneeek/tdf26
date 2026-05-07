# Strand: Voices project design session

Voices-project decision-making session. Authored at the 2026-05-07 tdf26 planning (Topic 13 item 3). Not a tdf26 implementation strand — the deliverable is decisions about the Voices project's shape, not changes to the tdf26 repo.

## 1. Goal

Land decisions on four open Voices-project design questions that have been carrying since 2026-04-18:

1. Should the voices project define an explicit override contract (what's overridable, what isn't)?
2. Is there a portable pattern for "voice + project overlay" that other projects could use?
3. Does the integration mechanism (absolute path in a skill file) need to evolve?
4. Should the voices repo go on GitHub, and if so, public or private?

The session is a design conversation, not an implementation strand. Output: documented decisions on each question, ready to inform the next time tdf26 reaches for a Voices-project resource (saintsbury for seg 24 is the next concrete trigger, per `project_meymac_voice.md`).

## 2. Filesystem posture

This strand does not touch the tdf26 repo's source tree. It records decisions in:

- The Voices project repo (or local checkout, if not yet on GitHub) — wherever the Voices project's design notes / README lives.
- One updating commit on `project_meymac_voice.md` and a follow-up unfold issue if the design conversation surfaces portable patterns.

No tdf26 worktree needed. No branch to verify in tdf26 unless decision (4) lands "yes, go public" and tdf26 picks up a public-link reference.

## 3. Source-of-truth posture

The Voices project's existing skill files and SKILL.md are the bedrock for what currently exists. CLAUDE.md and tdf26 memories describe how tdf26 *uses* voice content, not what the Voices project's interface is. Read both before deciding.

Per `feedback_brief_content_is_carryforward.md`: the four open questions in this brief are themselves carryforwards from the 2026-04-18 design notes. Verify the current state of each question against the actual Voices project before treating "the question" as well-formed.

## 4. Target deliverables

Four decisions, recorded somewhere durable. Suggested location: a `DESIGN.md` or equivalent in the Voices project repo, plus a parallel update to:

- `project_meymac_voice.md` (tdf26 memory) — note the integration mechanism if (3) changes it.
- An unfold issue if (2) yields a portable pattern.
- A tdf26 strand brief follow-up if (4) yields a public-repo URL that voice-using strands should cite.

## 5. Workflow

This strand is publisher-paced single-strand mode (per `feedback_multi_strand_session_checkpoints.md` 2026-05-07 sharpening). The four questions are interdependent; take them in order:

1. **Q4 first (repo public-or-private).** Other three questions partially depend on visibility. Public means the integration mechanism has to work for outsiders; private means it's just a tdf26 dependency.
2. **Q1 (override contract).** What's overridable, what isn't. If voices declares an explicit contract, tdf26 strands can rely on it; if not, every project carrying a voice has to figure out overrides ad-hoc.
3. **Q2 (portable overlay pattern).** Most likely an unfold-shaped question — the pattern, if it exists, is portable across projects that pair voices with project context.
4. **Q3 (integration mechanism).** Currently absolute path in a skill file (per `project_meymac_voice.md`). Decide whether that's stable or needs to evolve. The answer probably comes from Q1 + Q4: if the contract is explicit and the repo is reachable, the path-based mechanism may be fine.

AskUserQuestion checkpoints at each of the four. The publisher decides each.

## 6. Verification

- Each decision is recorded in a place future sessions will find.
- The Voices project README or DESIGN.md reflects the decisions.
- `project_meymac_voice.md` is updated if (3) changes the integration mechanism.
- An unfold issue is filed if (2) yields a portable pattern.

## 7. Cross-strand sharing notes

- **Owns (write):** Voices project repo's design / README artifact; possibly `project_meymac_voice.md`; possibly a new unfold issue.
- **Reads:** existing Voices project skill files and SKILL.md; `project_meymac_voice.md`; the 2026-04-18 design notes (in `project_next_planning_notes.md`).
- **Must NOT touch:** tdf26 source tree.

## 8. Scope discipline

- Four questions only. Do not expand into Voices-project implementation work.
- If a question reveals a deeper open issue (e.g., a missing voice sample, a coupling with tdf26 that needs untangling), file as a separate issue — don't inline.
- Per `feedback_unfold_tdf26_work_fit.md`: anything portable lands as an unfold issue, not Voices-project work or tdf26 work.

## 9. Memories that apply

- `project_meymac_voice.md` (the concrete trigger; saintsbury for seg 24)
- `feedback_unfold_tdf26_work_fit.md` (portable patterns route to unfold)
- `feedback_brief_content_is_carryforward.md` (the four questions are carryforwards; verify state)
- `feedback_explicit_mechanics.md` (when explaining tooling to a future session, prefer explicit human-understandable mechanics)
- `project_disclosure_practice.md` (the voice-register disclosure depends on the integration mechanism)
- `project_unfold_legible_model.md` (two-stage publishing: in-progress vs battle-tested)

## 10. Stop when

- Four decisions recorded.
- `project_meymac_voice.md` updated if relevant.
- Unfold issue filed if a portable pattern surfaced.
- Final report posted to publisher: each decision on one line; pointer to the recording artifact.
- No worktree to clean up.
