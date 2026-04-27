# Strand A — Process: security alerts (v1.4.11)

**Start here:** [Roadmap → Next → v1.4.11](https://github.com/gneeek/tdf26/wiki/Roadmap#next)

## Goal

Close the eight remaining high-severity / hygiene CodeQL alerts opened 2026-04-25. After this strand, the security tab queue drops to one parked low-severity item (#441, deferred per not-internet-exposed context).

Goal 5 (process). Commit-tier: both issues should land. The roadmap success bar (three of four commit-tier items) treats #440 and #442 as two of the four, so this strand is load-bearing for the milestone hitting its bar.

## Filesystem posture

**Worktree.** Run in a separate worktree to keep this strand's branch-switching off any concurrent strand's checkout.

```
cd /home/jhs/code
git worktree add tdf26-security main
cd tdf26-security
```

When the strand finishes: `git worktree remove tdf26-security` from the main checkout.

Within the worktree, branches are per-issue: `feature/issue-440-html-strippers`, `feature/issue-442-deploy-permissions`. Verify `git branch --show-current` immediately before each `git add` / `git commit` (the v1.4.10 retro learning — shared-tree branch state is non-stationary across any sequence of git commands; even in a worktree, do the check, since recovery from a wrong-branch commit costs more than the check).

## Target issues

- **[#440](https://github.com/gneeek/tdf26/issues/440)** — Replace hand-rolled HTML strippers in image attribution rendering. Closes seven CodeQL alerts (#4, #5, #6, #7, #8, #9, #10).
- **[#442](https://github.com/gneeek/tdf26/issues/442)** — Add explicit permissions block to deploy workflow. Closes CodeQL alert #1.

Order: land #442 first (one-line workflow edit, fast win, opens a minute); land #440 second (the real refactor).

## Workflow per issue

### #442 (small)

1. Add a minimal `permissions:` block to `.github/workflows/deploy.yml`. The deploy job does not use `GITHUB_TOKEN` (uses an SSH deploy key); `permissions: contents: read` should be sufficient for `actions/checkout`.
2. Open PR, assign to milestone v1.4.11.
3. After merge, confirm CodeQL alert #1 transitions to `fixed` via `gh api repos/gneeek/tdf26/code-scanning/alerts/1 --jq '.state'`.

### #440 (refactor)

Four files carry the hand-rolled `stripHtml` pattern that CodeQL flags for incomplete-multi-character-sanitization and double-escaping:

| File | Line | CodeQL alerts |
|---|---|---|
| `components/ImageGallery.vue` | 44 | #4, #9 |
| `components/content/InlineFigure.vue` | 47 | #5, #10 |
| `pages/admin/images.vue` | (TBD) | #6, #7 |
| `server/api/wikipedia-images.post.ts` | (TBD) | #8 |

Approach:

1. Read all four sites first to confirm they share a single sanitization shape (Wikipedia attribution metadata cleanup) before deciding the replacement.
2. Replace with a DOM-based sanitizer. Two reasonable options — pick one and apply consistently:
   - `DOMParser` + `textContent` extraction (no new dependency; client-only Vue components).
   - A maintained sanitization library (e.g. `dompurify` or `sanitize-html`) if the textContent route loses needed structure.
   The server route (`wikipedia-images.post.ts`) needs a Node-compatible path; `DOMParser` is browser-only, so the server file likely needs a different approach (e.g. `sanitize-html` or `html-entities` for the specific attribution case). Decide once and document inline.
3. Add or update unit tests covering the attribution shapes that previously broke the hand-rolled regex (entity sequences, nested tags, multi-character constructs). The CodeQL alert descriptions name the failure modes — convert each into a test case.
4. Open PR, assign to milestone v1.4.11.
5. After merge, confirm the seven alerts (#4, #5, #6, #7, #8, #9, #10) transition to `fixed` via `gh api repos/gneeek/tdf26/code-scanning/alerts --jq '[.[] | select(.number | IN(4,5,6,7,8,9,10)) | {number, state}]'`.

## Verification commands

The following npm scripts exist in `package.json` and are real:

- `npm ci` — install
- `npm run lint` (eslint)
- `npm test` (vitest)
- `npm run build`
- `npm run generate`
- `npm run preview`

There is **no** `npm run typecheck` (the v1.4.10 strand-B brief named one and was wrong). Type errors surface during `npm run build` via Nuxt's prepare step.

For a worktree, prefix Node-touching Bash with `source ~/.nvm/nvm.sh && nvm use --silent &&` (per `feedback_bash_nvm_sourcing.md`).

For #440 verification before opening the PR:
- `npm run lint && npm test && npm run build`
- Production preview the rendered attribution in `ImageGallery` and `InlineFigure` on a published entry that exercises Wikimedia attribution (per `feedback_production_preview.md`).

For #442 verification:
- `gh workflow view deploy.yml --repo gneeek/tdf26` and read the merged file.
- The actual deploy job runs on the next publish (Wed 2026-04-29 segment 8 ship); a dry-run is not feasible.

## Cross-strand sharing notes

- Strand B (bug-class) touches `utils/stage-totals.ts`, `components/StageDetails.vue`, `data/competition/points-config.json`, `scripts/publish.sh`. **No file-region overlap with this strand.**
- Strand C (sqlite stretch) touches `package.json` (postinstall augmentation). **No overlap with this strand.**
- This strand's PRs do not need to coordinate with B or C beyond standard rebasing on main.

## Scope discipline

- File new issues for anything that surfaces during the refactor and is not part of closing these alerts. Do not fix inline.
- The CodeQL alerts on `pages/admin/images.vue` (#6, #7) live in admin UI not exposed to the public internet. Still close them — they are in the same class of bug as the public sites and the strand goal is "close the eight alerts," not "close only the public ones."

## Memories that apply

- `feedback_bash_nvm_sourcing.md` — prefix Node-touching Bash with nvm sourcing.
- `feedback_env_check.md` — verify Node version against `.nvmrc` before installing.
- `feedback_pr_polling.md` — verify PR merges via GitHub API.
- `feedback_production_preview.md` — production preview before merging visual PRs.
- `feedback_shared_tree_branch_verification.md` — verify `git branch --show-current` before each `git add` / `git commit`.
- `feedback_issues_describe_problems.md` — issues describe problems; solutions go in PR descriptions.

## Stop when

- Both #440 and #442 PRs are merged into main.
- All eight CodeQL alerts (#1, #4, #5, #6, #7, #8, #9, #10) confirmed transitioned to `fixed`.
- Worktree removed.
- Any unrelated issues surfaced during the refactor are filed, not fixed inline.
