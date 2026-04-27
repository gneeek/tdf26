# Strand C — Publisher experience (stretch): better-sqlite3 rebuild (v1.4.11)

**Start here:** [Roadmap → Next → v1.4.11](https://github.com/gneeek/tdf26/wiki/Roadmap#next)

## Goal

Stop `better-sqlite3`'s `Module did not self-register` error from interrupting publisher and developer workflows. After this strand, fresh clones, Node version changes, and dependency updates should not require a manual `npm rebuild better-sqlite3` recovery step.

Goal 3 (publisher experience). **Stretch tier.** Drops out of scope if strands A and B consume the available window. Three of the four commit-tier items (A's two plus B's two) is the milestone's success bar; this strand makes it five.

## Filesystem posture

**Worktree.** Run in a separate worktree.

```
cd /home/jhs/code
git worktree add tdf26-sqlite main
cd tdf26-sqlite
```

When the strand finishes: `git worktree remove tdf26-sqlite` from the main checkout.

Branch: `feature/issue-425-sqlite-rebuild-automation`. Verify `git branch --show-current` immediately before each `git add` / `git commit`.

## Target issue

- **[#425](https://github.com/gneeek/tdf26/issues/425)** — Automate `better-sqlite3` rebuild on install or dev/publish startup.

## File-region constraint (load-bearing)

**Prefer the `package.json` postinstall route. Avoid touching `scripts/publish.sh` and `scripts/dev.sh`.**

Why: strand B's #426 lands changes in `scripts/publish.sh`. Putting the sqlite rebuild in publish.sh creates a cross-strand collision in the same file. The postinstall hook in `package.json` runs on every `npm ci` / `npm install`, which covers fresh clones and dependency updates — the failure modes named in #425's body. Node version changes are also covered if the publisher re-runs `npm ci` after switching Node (which the existing `feedback_env_check.md` discipline already requires).

Existing `package.json` `postinstall` value: `nuxt prepare`. **Do not clobber it.** Augment as a chained command, e.g.:

```json
"postinstall": "npm rebuild better-sqlite3 && nuxt prepare"
```

Watch for recursion: `npm rebuild better-sqlite3` runs `better-sqlite3`'s own install/postinstall (the rebuild step), not the project-root `postinstall`, so this should be safe. Verify by running `npm ci` in a clean checkout and confirming the rebuild fires once.

If during implementation the postinstall route is genuinely insufficient — e.g. it does not address a failure mode named in #425's body — escalate to the publisher before falling back to a `publish.sh` / `dev.sh` edit. Falling back to `publish.sh` requires rebasing on strand B's #426 branch (or waiting for B's PR to merge to main).

## Workflow

1. Read `#425`'s body in full to confirm the failure modes the issue is targeting.
2. Read the current `package.json` `postinstall` value and confirm it is `nuxt prepare`.
3. Augment `postinstall` to chain `npm rebuild better-sqlite3` before the existing command.
4. Test the failure recovery path: in the worktree, after the change, simulate the failure mode by running `node -e "require('better-sqlite3')"` directly (which is what trips the `Module did not self-register` error), then run `npm ci` and re-test. Confirm the error is gone.
5. Test the no-regression path: run `npm test` and `npm run build` to confirm the augmented postinstall does not break the existing flow.
6. Open PR, assign to milestone v1.4.11.

## Verification commands

The following npm scripts exist in `package.json`:

- `npm ci`, `npm run lint`, `npm test`, `npm run build`, `npm run generate`, `npm run preview`, `postinstall` (chained: `npm rebuild better-sqlite3 && nuxt prepare`).
- There is **no** `npm run typecheck`.

Pre-PR:

- `npm ci` (confirm rebuild fires and existing postinstall behavior preserved)
- `node -e "require('better-sqlite3')"` (smoke test the previously failing import)
- `npm run lint && npm test && npm run build`

For Node-touching Bash, prefix with `source ~/.nvm/nvm.sh && nvm use --silent &&`.

## Cross-strand sharing notes

- Strand A (security) and strand B (#422) do not touch `package.json`. **No overlap.**
- Strand B's #426 touches `scripts/publish.sh`. **This strand stays out of `publish.sh` per the brief above.** That keeps the cross-strand collision profile zero.
- If B's #426 lands first, no rebase needed for this strand. If this strand lands first, B does not need to rebase.

## Scope discipline

- One issue, one PR. Do not start a second.
- File new issues for any other recurring publisher-experience interrupts surfaced while reading #425's context. Do not fix inline.
- If the postinstall route turns into a non-trivial investigation (recursion edge case, npm version-specific behavior), file a follow-up issue and escalate to the publisher rather than silently falling back to publish.sh.

## Memories that apply

- `feedback_bash_nvm_sourcing.md`, `feedback_env_check.md`, `feedback_pr_polling.md`, `feedback_shared_tree_branch_verification.md`.
- `feedback_issues_describe_problems.md`.

## Stop when

- The #425 PR is merged into main.
- A clean `npm ci` in a fresh checkout reproduces the rebuild without manual intervention.
- The previously failing `require('better-sqlite3')` smoke test passes after install.
- Worktree removed.
- Any unrelated issues are filed, not fixed inline.

## Drop-out conditions

This is the stretch item. Drop out without prejudice if any of these fire:

- Strand A or B is still in flight near the segment 9 publish window (Sun 2026-05-03) and finishing this strand would push them.
- The postinstall route turns out to require a non-trivial investigation that would consume the remaining window.
- The publisher needs window for an unrelated urgent item between now and segment 9 publish.

Dropping out means: close the worktree without merging, leave #425 open for a future release, file any partial findings as comments on #425.
