# Strand briefs

Working artifacts for parallel-strand Claude Code sessions on tdf26. Each session reads the [Roadmap](https://github.com/gneeek/tdf26/wiki/Roadmap) for goals/outcomes view, then reads its brief in this directory for issue-level scope.

## Template

New briefs should follow [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md) — the canonical 10-section shape, promoted from this README at the 2026-05-07 planning session.

To scaffold a new brief, invoke the `/strand-brief` skill from the repo root: it reads the template, prompts for the strand identifier, type, target issues, milestone, and worktree posture, and writes a pre-filled brief at `docs/strands/strand-<id>.md`.

## Lifecycle

These briefs are working artifacts for one release. Once a release ships and its retro is published, the briefs that are no longer load-bearing should be removed; any patterns worth keeping go into the wiki, memory, or the template.
