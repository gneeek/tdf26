# Strand briefs (v1.4.11)

Three parallel Claude sessions for v1.4.11. Each session reads the [Roadmap](https://github.com/gneeek/tdf26/wiki/Roadmap) for the goals/outcomes view, then reads its brief in this directory for issue-level scope.

- [Strand A — Process: security alerts](strand-a-security.md) (#440 + #442)
- [Strand B — Developer: bug-class cleanup](strand-b-bugclass.md) (#422 + #426)
- [Strand C — Publisher (stretch): better-sqlite3 rebuild](strand-c-sqlite.md) (#425)

## Brief template (applied to all three)

Each brief contains, in this order:

1. **Goal** — one paragraph, plus which milestone goal it serves.
2. **Filesystem posture** — worktree path, branch verification rule (`git branch --show-current` before each `git add` / `git commit`).
3. **Target issues** — issue numbers, ordering rationale.
4. **Workflow per issue** — concrete steps.
5. **Verification commands** — only commands that actually exist in `package.json` / the codebase. No `npm run typecheck` (it does not exist).
6. **Cross-strand sharing notes** — file regions touched, collision avoidance, rebasing rules.
7. **Scope discipline** — what to file as new issues vs fix inline.
8. **Memories that apply** — the relevant feedback / project memory pointers.
9. **Stop when** — exit criteria.

This template is the v1.4.10 retro's "strand-brief template" gap, applied. If a future multi-strand release deviates, the deviation should be deliberate.

## v1.4.10 strand briefs

The v1.4.10 briefs (`strand-a-content.md`, `strand-b-deps.md`, `strand-c-landing.md`) remain in the directory until v1.4.10 tags on Wed 2026-04-29 alongside the segment 8 publish, after which they should be removed per the "working artifacts for one release" rule below.

## Lifecycle

These briefs are working artifacts for one release. Once a release ships and its retro is published, the briefs that are no longer load-bearing should be removed; any patterns worth keeping go into the wiki, memory, or this README's template section.
