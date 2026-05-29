# Strand: release ceremony automation (#480 / #521 / #339)

The v1.4.20 "ceremony" strand: automate the manual post-deploy run-in steps so a release ships its own Roadmap update, checklist, and tag/release sequence instead of relying on memory and ad-hoc judgement. Runs **after** the publish-safety gate (#617/#618/#619) merges — #480 edits `scripts/publish.sh`'s release-create step, which the gate owns for its window. Lands across the **seg 17–19 publish cycles** (target close ~seg 20, 2026-06-10). Not a publication-day deadline.

## 1. Goal

Land the three release-ceremony issues that take the manual run-in steps off the publisher's plate: automate the wiki Roadmap update at release time (#480), produce a full-lifecycle release checklist with conditional branching (#521), and codify the tag → release → milestone → retro → Roadmap sequence as a `/release` skill or hook (#339). These nest — #480 is a named dependency of #339, and #521's checklist is the human-readable spec the #339 skill mechanises — so they are ordered below and worked in sequence by one strand session. Milestone: **v1.4.20 — Publish-pipeline hardening**. Serves the milestone success criterion "the wiki Roadmap update step is no longer a manual post-deploy chore (#480), or is on a documented path to it."

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/release-ceremony /home/jhs/code/tdf26-ceremony main
```

- Branch off `main` **after the gate strand has merged** (#480 inserts into the same `scripts/publish.sh` region the gate's #618 edits — see §7). Explicit-path worktree; no nesting, no `.claude` symlink.
- Before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/release-ceremony`.
- Fresh worktree: `npm ci` + `cp data/riders/*.example.json` to non-example names before any `npm run build` (per `feedback_ci_seed_ordering.md`).
- **The wiki is a separate git repo** (`git@github.com:gneeek/tdf26.wiki.git`). #480 and #339 both write to it — clone it separately; do not assume it is reachable from this worktree. Confirm push access before relying on automation that pushes to it.

## 3. Source-of-truth posture

- **Read `scripts/publish.sh` and `scripts/create-release.sh` directly** before editing — `create-release.sh` already automates tag-creation and GitHub Release publication (landed under #456, v1.4.12); #480 and #339 extend it, they do not re-implement it. Verify what `create-release.sh` already does so the skill wraps it rather than duplicating it.
- **The reliable tag/release sequence is documented in #339's "sharp edges"**: `git tag -a <name> -m <msg> <sha> && git push origin <name> && gh release create <name> --notes-file <file>` — *not* `gh release create --target <sha>`, which failed with "tag_name is not a valid tag." Use the documented sequence.
- **Verify the current wiki Roadmap page shape** (`## Now` / `## Next` / `## Completed` or current headings) before writing the update automation — #480's scope hint flags the headings as the input contract and says "verify current shape." Per `feedback_roadmap_style.md`, the Roadmap describes goals and outcomes, not issue numbers; the automation must preserve that style.
- Mine the v1.4.5–v1.4.17 release history for #521's checklist branches (the issue names twelve worked examples). Read the actual lifecycles, don't invent the branches.
- Per `feedback_milestone_urls.md`: link milestones by number (`/milestone/<n>`), not title search, anywhere the automation emits a milestone link.

## 4. Target issues

Milestone **v1.4.20**. Order by dependency, not number:

1. **#480** — automate the wiki Roadmap "In flight" / "Completed" update at release time, inserting at the `create-release.sh` release step. The concrete, highest-leverage piece; a named dependency of #339. Do first.
2. **#521** — full-lifecycle release checklist with conditional branching (publication vs non-publication, hotfix, multi-strand vs single-strand). Research-then-draft from the v1.4.5–v1.4.17 history. A markdown artifact (no code) — this is the human-readable spec #339 mechanises. Explicitly out of scope: the planning-session ritual (#481) and the tag/version naming scheme (#519).
3. **#339** — the `/release` skill or hook that executes the seven ceremony steps (tag, push, GitHub release, close milestone, retro wiki stub from the four-section template, Retrospectives index row, Roadmap Completed move). Builds on #480 (Roadmap step) and #521 (the checklist it mechanises). Must stop-on-error with partial state documented for recovery; must handle both the main repo and the wiki repo. Acceptance bar: used for at least one real release before considered proven.

## 5. Workflow per issue

- **#480:** Add a Roadmap-update step to the release path (in `create-release.sh` or as a function publish.sh calls), cloning/pulling the wiki repo, moving the just-shipped release from the in-flight section to Completed with release + retro links, committing and pushing. Preserve the goals-and-outcomes Roadmap style. Dry-run first against a scratch branch of the wiki.
- **#521:** Read each of v1.4.5–v1.4.17's actual lifecycle; identify the branches (release type, strand count, publication vs not); draft the conditional checklist as a committed markdown artifact (location: `docs/planning/` alongside the milestone-scope template, or `docs/RELEASE-CHECKLIST.md` — pick and note). Model the shape on how `/retro` enforces the four-section retro structure.
- **#339:** Implement the skill/hook wrapping `create-release.sh` (#480 included) and walking the #521 checklist. Use the documented tag sequence (not `--target`). Handle the wiki repo as a separate clone/commit/push. Stop-on-error, document partial state. **Prove it on one real release** (a non-publication tag is the safest first target) before closing.

## 6. Verification commands

- `bash -n scripts/publish.sh scripts/create-release.sh` after edits.
- The shell-test harness from #508, **if the spine strand has landed it** — wire #480's Roadmap-update logic as a harness case (dry-run / stubbed wiki push) rather than a manual reproduction. If #508 has not landed, document the manual red-green in the PR body and note the harness backfill as follow-up.
- `npm test`.
- For #339: a `--dry-run` invocation that prints the seven steps without executing, plus one real proven release (record which).
- Red-green for #480: run against a release that already has a Roadmap row (idempotent — no duplicate row) and one that does not (row added).

## 7. Cross-strand sharing notes

**Load-bearing — the ceremony strand contends with the gate and spine strands on `scripts/publish.sh` / `scripts/create-release.sh` and with the spine on the release checklist.**

- **Owns (write):** `scripts/create-release.sh` and the release-step region of `scripts/publish.sh` (#480), the release-checklist markdown artifact (#521), the `/release` skill/hook files + any `.claude/` skill definition (#339), and wiki-repo pages (Roadmap, Retrospectives index, retro stub).
- **Reads:** the v1.4.5–v1.4.17 release history (`gh release list`, retro wiki pages), `docs/planning/v1.4.20-scope.md`, the four-section retro template.
- **Must NOT touch:** `scripts/publish.sh`'s draft pre-flight / merge-idempotency / weather logic (gate owns #617/#618/#619); `processing/*.py` (spine owns the parser work); `content/entries/*.md`; `data/`.
- **Sequencing (hard):**
  - **Start only after the gate (#617/#618/#619) has merged.** #480 edits the `create-release.sh`/publish.sh release region; #618 (idempotent `gh pr merge`) edits the adjacent merge step. Rebase on the gate; do not run concurrently.
  - **Coordinate the release-checklist with the spine strand (#322/#521).** Both #322's process half and #521 want the build-and-preview step. Recommended split: **#322 owns the *verification* step (the automated render-check), #521 owns the *checklist artifact* that references it.** Agree this before either writes it.
  - **#521 is the one piece runnable in parallel with the gate** — it is research + markdown, touches no shared code. Land #480/#339 only after the gate.
- **Forecast failure mode:** most likely collision is #480's publish.sh insertion conflicting with the gate's #618 merge-step edit at the same line region. Mitigation: branch after the gate merges and rebase; keep the Roadmap-update in `create-release.sh` (further from #618's merge edit) rather than inline in publish.sh's main flow where possible.

## 8. Scope discipline

- File new issues for findings outside the three-issue write-set; do not over-scope. Explicitly out of scope per the issues: planning-session ritual (#481), tag/version naming scheme (#519).
- The #322/#521 checklist-ownership split is the one material checkpoint — resolve it with the spine strand or publisher, do not write the build-and-preview step in both places.
- #339's "prove on one real release" bar means this strand may not *close* #339 within the window even if the skill is written — that is acceptable; ship the skill, note the proving run as the close condition, and surface it to the publisher.
- Document any publisher override in the PR body.

## 9. Memories that apply

- `feedback_roadmap_style.md` — Roadmap describes goals/outcomes, not issue numbers; the #480 automation must preserve this.
- `feedback_milestone_urls.md` — link milestones by number, not title search.
- `feedback_release_tagging.md` (project) — tags follow production deployments; the skill must respect the cadence, not tag arbitrarily. (Memory: `project_release_tagging.md`.)
- `feedback_no_regex_in_bash.md` — relevant for any embedded-Python in the shell automation.
- `feedback_ci_seed_ordering.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_worktree_path.md`, `feedback_strand_session_self_cleanup.md`.
- `project_deployment.md` — deploy posture context (SSH to OVH, not rsync) for any deploy-adjacent step.

## 10. Stop when

- PRs open closing #480 and #521; #339 either closed (if a real release proved it in-window) or shipped-and-pending-proof with the proving run named as its close condition. CI green; red-green demonstrated for #480.
- The wiki Roadmap update is no longer a manual post-deploy chore (the milestone success criterion) — or is on a documented automated path via the merged #480.
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-ceremony` once merged. Remove any scratch wiki clone.
- Final report to publisher: PR links, the #322/#521 checklist-ownership resolution, #339's proving status, the verified current Roadmap page shape.
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during release-ceremony strand execution (<date>)`: decision-actionable observations, light-tier pattern observations, numeric stats (files-touched, commits, checkpoints fired, wall-clock).
