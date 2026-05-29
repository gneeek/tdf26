# /release skill — repo mirror

> This is a version-controlled snapshot of the `/release` skill for review.
> The **canonical, installed** copy lives at `~/.claude/skills/release/SKILL.md`
> (user-global, alongside `/retro`, `/strand-brief`, `/tdf26-voice`). Skills in
> this project are installed globally, not loaded from the repo — this file exists
> so the skill is reviewable in a PR and survives in history. If you edit one, edit
> both. Origin: #339.

---

---
name: release
description: Run the tdf26 release ceremony — tag, GitHub Release, milestone close, retro stub, Retrospectives index row, and the Roadmap Completed move — as one stop-on-error sequence over the main repo and the wiki repo. Use when the publisher asks to "cut the release", "run the release ceremony", "tag and release vX", or at milestone close. Supports a dry-run.
---

# tdf26 /release skill

Codifies the post-deploy release ceremony so steps stop being driven by memory and
ad-hoc judgement. Mechanises the lifecycle declared in
[docs/RELEASE-CHECKLIST.md](https://github.com/gneeek/tdf26/blob/main/docs/RELEASE-CHECKLIST.md)
(#521) — read it for the conditional branches; this skill executes the **ceremony**
phase (checklist step 8). It composes existing tools rather than re-implementing them:

- `scripts/create-release.sh` — tag → push → GitHub Release, and (with
  `--update-roadmap`) the Roadmap Completed move (#480). Already robust and dry-runnable.
- the `/retro` skill — writes `Retro-<tag>.md` and adds the `Retrospectives.md`
  index row (ceremony steps 5–6 live there; do not duplicate them here).
- `gh` — milestone close, by number.

## Scope: what this skill does NOT do

- It does **not** deploy. Deploy happens first (`publish.sh` for publications,
  the build+deploy path for chore/intervention releases). This skill runs **after**
  a successful deploy.
- It does **not** write retro content. It invokes `/retro`, which scaffolds the
  four-section structure for humans/agents to fill and sign off.
- It does **not** rewrite the Roadmap `## Now` prose (see step 6).

## Inputs

Establish before running:

1. **Tag** — date-based, year-implicit: `W<NN>-seg<N>` (publication) or `W<NN>.<N>`
   (non-publication). `create-release.sh` validates the form and refuses duplicates.
2. **Target commit** — defaults to `HEAD` of `main`. Confirm `main` is at the
   deployed artifact before tagging.
3. **Release type** — publication / non-publication / chore / hotfix (RELEASE-CHECKLIST §1).
   Determines the tag form and whether this is also a **milestone close**.
4. **Milestone number** — for the `--milestone <n>` link and the close step. Link
   milestones **by number** (`/milestone/<n>`), never title search.
5. **Is this a milestone close?** Milestones are decoupled from tags and span
   several deploys. Close the milestone and do the full Roadmap Completed move
   **only** at milestone close; per-deploy ceremony still tags, releases, and files
   a per-deploy retro.

## The reliable tag sequence

Always `git tag -a <tag> -m <msg> <sha>` → `git push origin <tag>` →
`gh release create <tag> --notes-file <file>`. **Never** `gh release create --target
<sha>` — it fails with "tag_name is not a valid tag." `create-release.sh` already
uses the correct sequence; call it rather than hand-rolling.

## Procedure

Run the steps **in order**. **Stop on the first error**, print what completed and
what did not, and document the partial state for recovery (see "Recovery" below).
Do a dry-run first whenever the release is non-routine.

### Step 0 — preconditions
- Confirm the working repo is clean and `main` is at the intended target commit.
- Confirm wiki push access. **The wiki is a separate repo cloned over HTTPS**
  (`https://github.com/gneeek/tdf26.wiki.git`); the SSH host key is not trusted in
  headless/CI runs, so do not rely on `git@…`. `create-release.sh --update-roadmap`
  clones it for you.

### Steps 1–3 + 6 — tag, push, GitHub Release, Roadmap Completed move
Run, after the deploy, from the repo root:

```
# dry-run first (no tag, no release, no push — prints commands + Roadmap diff):
scripts/create-release.sh <tag> --title "<title>" --update-roadmap --milestone <n> --dry-run

# then for real:
scripts/create-release.sh <tag> --title "<title>" --update-roadmap --milestone <n>
```

- This tags, pushes, creates the Release, and (idempotently) inserts the Completed
  bullet into the wiki Roadmap.
- It prints a **WARNING that the `## Now` block needs a manual trim** — it does not
  rewrite that prose, to preserve the goals-and-outcomes Roadmap voice. Do the trim
  by hand (step 6, below) when this is a milestone close.
- Omit `--update-roadmap` for a mid-milestone deploy where you do not yet want a
  Completed row.

### Step 4 — close the milestone (milestone close only)
```
gh api -X PATCH repos/gneeek/tdf26/milestones/<n> -f state=closed
```
Skip for a mid-milestone production deploy.

### Steps 5 — file the per-deploy retro
Invoke the **`/retro`** skill, scoped to this tag/deploy. It enforces the four
sections (What went well / What was challenging / What we learned / What we lack),
runs the publisher review + Piers/Tully voice pass, and on sign-off commits
`Retro-<tag>.md` and adds the `Retrospectives.md` index row. Add the retro link
back into the GitHub Release notes once the retro page exists.

### Step 6 — trim the Roadmap `## Now` block (milestone close only)
The `--update-roadmap` step added the Completed bullet but deliberately left `## Now`
describing the just-shipped milestone. Edit `## Now` to describe what is **now** in
flight (the next milestone), preserving the goals-and-outcomes prose style. Commit
and push to the wiki.

## Dry-run

`--dry-run` is passed straight through to `create-release.sh` for steps 1–3 + the
Roadmap move (it prints the tag/release commands and the Roadmap diff, changing
nothing). For steps 4–6, "dry-run" means: state the milestone you would close, the
retro page you would create, and the `## Now` edit you would make — do not execute.

## Stop-on-error and recovery

| If this fails | State left behind | Recover by |
|---------------|-------------------|------------|
| tag/push (`create-release.sh`) | no tag, no release | rerun; it refuses to act if the tag already exists |
| GitHub Release | tag pushed, no Release | `gh release create <tag> --notes-file <file>` |
| Roadmap move | release exists; wiki commit local-only or unpushed | the script prints the temp clone path; push it manually |
| milestone close | release + Roadmap done | rerun the `gh api` PATCH |
| retro | everything above done | run `/retro` separately |

Because the release exists once steps 1–3 succeed, **a later step failing never
invalidates the release** — it only leaves a documented follow-up.

## Acceptance / proving

Per #339, the skill is "proven" only after it has driven **one real release**. A
**non-publication tag** (`W<NN>.<N>`) is the safest first proving target. Until a
real release has used it end-to-end, treat #339 as shipped-pending-proof and name
the proving run as its close condition.

## Self-checks before running for real
- Tag matches `W<NN>-seg<N>` or `W<NN>.<N>` and does not already exist.
- `main` is at the deployed commit.
- Milestone number is correct and you have decided whether this is a milestone close.
- You ran the `--dry-run` and the Roadmap diff looks right.
