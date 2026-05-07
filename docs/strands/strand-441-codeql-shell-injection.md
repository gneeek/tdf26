# Strand: CodeQL shell-injection fix (#441)

Security fix strand. Authored at the 2026-05-07 planning session resume (Topic 14 backlog sweep).

## 1. Goal

Clear the three open CodeQL shell-command-injection alerts on admin server APIs by switching from shell-mode `execSync` to argument-array form (`execFileSync` or `execSync` with array args). Closes [#441](https://github.com/gneeek/tdf26/issues/441). Milestone: **v1.4.19**. No deadline; fits as a small strand or single PR.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-441-shell-injection-fix /home/jhs/code/tdf26-441 main
```

- Run from outside the repo (or via `git -C`); see `feedback_strand_worktree_path.md`.
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/issue-441-shell-injection-fix` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- The three CodeQL alert pages are the canonical fix references. Read them first:
  - [#11 — server/api/images-suggest.post.ts](https://github.com/gneeek/tdf26/security/code-scanning/11)
  - [#12 — server/api/publish.post.ts](https://github.com/gneeek/tdf26/security/code-scanning/12)
  - [#13 — server/api/riders.post.ts](https://github.com/gneeek/tdf26/security/code-scanning/13)
- Read each affected file before editing. Per `feedback_brief_content_is_carryforward.md`: the shapes described in §5 below are this brief's understanding — verify against current code before treating them as bedrock.

## 4. Target issues

- [#441](https://github.com/gneeek/tdf26/issues/441) — admin server APIs build shell commands from environment paths. Closes after the three alerts clear and the PR merges.

## 5. Workflow

The three sites have similar shape but each needs its own treatment. Read all three first, then refactor in any order. The pattern: replace `execSync(<single-string>, { shell: ... })` with `execFileSync(<file>, <args-array>, <options>)` so no shell is invoked.

### 5a. `server/api/publish.post.ts` (line 15)

Currently a `run(label, cmd)` helper that calls `execSync(cmd, { cwd, timeout, encoding, shell: '/bin/bash' })`. Three call sites: rider-stats, weather (env-derived `apiKey` interpolated), and any others present at execution time. Refactor:

- Change `run` signature to `run(label: string, file: string, args: string[])`.
- Body uses `execFileSync(file, args, { cwd: projectDir, timeout: 60000, encoding: 'utf8' })` — drop the `shell:` option.
- Update each call site to pass the venv Python path as `file` and the script + args as the array. Example: `run('Rider Stats', venvPython, ['processing/rider_stats.py', '--daily-log', '...', '--rider-config', '...', '--output', '...'])`.
- The weather case interpolates `apiKey` — make sure it's a separate array element, not concatenated into a flag string.

### 5b. `server/api/images-suggest.post.ts` (line 18)

Currently `execSync(\`${venvPython} ${script} --segments-json ... --segment ${segment}\`, { timeout, encoding })` — segment comes from the request body. Refactor:

- `execFileSync(venvPython, [script, '--segments-json', segmentsJson, '--output-dir', outputDir, '--segment', String(segment)], { timeout: 30000, encoding: 'utf8' })`.
- `String(segment)` is the right coercion — segment may be `0` or a number, and the array form forwards the literal string to argv. Reject non-numeric values earlier in the handler if not already done.

### 5c. `server/api/riders.post.ts` (line 9)

Currently builds `[venvPython, scriptPath, ...args]` then JSON.stringify-joins them and passes as a single string to `execSync(cmd, { stdio })`. The JSON.stringify dance was a partial mitigation; the array-form fix supersedes it. Refactor:

- Drop the `cmd = [...].map(...).join(' ')` line.
- `execFileSync(venvPython, [scriptPath, ...args], { stdio: ['ignore', 'pipe', 'pipe'] })`.

### 5d. After all three are refactored

- Run `npm test` — 186+ tests pass against the refactor (these endpoints aren't covered by JS unit tests; defensive).
- Run a manual smoke for each admin endpoint locally (`npm run dev`, hit `/admin/...`, confirm same behavior). Record the smoke evidence in the PR test plan.
- Open PR against `main`. Title: `fix(security): switch admin execSync calls to arg-array form (closes #441)`. Body: list each file's before/after pattern, link the three CodeQL alerts, state that no behavior change is intended.
- After merge, watch the CodeQL re-scan — all three alerts should clear automatically. If any remains open, investigate whether a residual shell-mode call slipped through.

## 6. Verification

- `npm test` green (186+ tests).
- `npx nuxt prepare` (in worktree) to ensure no type errors.
- Manual smoke per §5d.
- CodeQL alerts #11, #12, #13 clear after PR merge. (CodeQL runs on PR-open and on push-to-main; results visible at `gh api repos/gneeek/tdf26/code-scanning/alerts`.)

## 7. Cross-strand sharing notes

- **Owns (write):** `server/api/images-suggest.post.ts`, `server/api/publish.post.ts`, `server/api/riders.post.ts`. Possibly a small shared helper if the three refactors collapse cleanly into one — but default is keep the refactors local; do not create a `runPythonScript` utility unless it falls out naturally.
- **Reads:** the three files above; `processing/.venv/bin/python` path conventions; the CodeQL alert pages.
- **Must NOT touch:** `scripts/publish.sh` (separate territory; the seg 11 ship Sun 2026-05-10 must not be disturbed); content/entries; data files; the seg-11 / publisher-contract / tour-history strands' file regions.
- **Cross-strand collisions:** none expected. Admin endpoints are isolated from the parallel work.

## 8. Scope discipline

- Three alerts only. Do not refactor admin endpoints beyond the shell-mode fix.
- File new issues for any other security findings encountered (e.g., other `execSync` calls or `eval`-shaped patterns) per `feedback_issues_describe_problems.md`.
- Do not introduce a new helper module just to share the `execFileSync` invocation — that's premature abstraction; three local refactors is fine.
- If the smoke test surfaces a behavior change (e.g., env-var interpolation broke because of a quoting subtlety), pause and AskUserQuestion before adjusting.

## 9. Memories that apply

- `feedback_brief_content_is_carryforward.md` (verify the shapes described in §5 against current code)
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`
- `feedback_assertion_bug_class.md` (consider whether to add a lint or test that catches future shell-mode regressions — out of scope for this strand but worth filing as a follow-up if the publisher endorses it)
- `feedback_pre_publish_scrutiny.md` (security-adjacent work in publish-day territory; treat carefully)

## 10. Stop when

- Three CodeQL alerts cleared on a fresh scan against `main`.
- `npm test` green.
- Manual smoke green for each of the three admin endpoints.
- PR opened, reviewed, merged.
- **Cleanup (you run this, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-441` once the PR has merged. The strand owns its own worktree teardown.
- Final report posted to publisher: PR link, before/after pattern per file, smoke evidence, any follow-up issues filed.
