# Strand briefs

Working artifacts for parallel-strand Claude Code sessions on tdf26. Each session reads the [Roadmap](https://github.com/gneeek/tdf26/wiki/Roadmap) for goals/outcomes view, then reads its brief in this directory for issue-level scope.

The brief format operationalises promises in the [publisher / developer-experience contract](https://github.com/gneeek/tdf26/wiki/How-We-Work#publisher--developer-experience-contract): each brief declares scope, ownership and read-set, target deliverables, and stop conditions, so concurrent work is safe and reviewable.

## Template

New briefs should follow [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md) — the canonical 10-section shape, promoted from this README at the 2026-05-07 planning session.

To scaffold a new brief, invoke the `/strand-brief` skill from the repo root: it reads the template, prompts for the strand identifier, type, target issues, milestone, and worktree posture, and writes a pre-filled brief at `docs/strands/strand-<id>.md`.

## Lifecycle

These briefs are working artifacts for one release. Once a release ships and its retro is published, the briefs that are no longer load-bearing should be removed; any patterns worth keeping go into the wiki, memory, or the template.
