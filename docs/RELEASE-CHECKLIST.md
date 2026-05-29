# Release checklist

The full lifecycle of a tdf26 release, with the conditional branches that real
releases have taken. This is the human-readable spec that the `/release` skill
(#339) mechanises for the ceremony steps, and the single artifact a fresh agent
session can follow to know "what should happen for this release."

It **operationalises** the process declared on the wiki — it does not restate it.
Where the wiki is authoritative, this file links to it rather than copying:

- [How We Work](https://github.com/gneeek/tdf26/wiki/How-We-Work) — goals, PR
  workflow, late-add/hotpatch policy, conventions (the source of truth).
- [Roadmap](https://github.com/gneeek/tdf26/wiki/Roadmap) — Now / Completed.
- [Retrospectives](https://github.com/gneeek/tdf26/wiki/Retrospectives) — the
  four-section retro index; enforced by the `/retro` skill.

Out of scope (covered elsewhere, do not duplicate here): the planning-session
entry/exit ritual (#481) and the tag/version naming scheme (#519, the date-based
`W<NN>` migration — already documented on the Roadmap's "Naming note").

---

## 1. Pick the release type

The release type sets which branches apply. Determine it **before** scoping.

| Type | When | Tag | Deploy path | Held to "publish better"? |
|------|------|-----|-------------|---------------------------|
| **Publication** | Anchored by a segment going live | `W<NN>-seg<N>` | `scripts/publish.sh` (full path) | Yes — content + ≥1 reader + ≥1 dev improvement |
| **Non-publication / intervention** | Single-goal, urgency-driven, between publishes | `W<NN>.<N>` | `scripts/create-release.sh` after deploy | No — scoped to the urgent issue |
| **Chore / same-day interleaved** | Small follow-on shipped hours after a publication | `W<NN>.<N>` | `scripts/create-release.sh` | No |
| **Hotfix / post-publish patch** | A fix after the publication tag is already live | `W<NN>.<N>` (own tag) | `scripts/create-release.sh` | No |

Worked examples: publication — `W19-seg11`…`W22-seg16`, v1.4.5/6/9/10/14/17.
Intervention — v1.4.7 (protect incoming publisher), v1.4.11 (security), v1.4.12
(ceremony foundation + publish fix). Chore/same-day — v1.4.15, v1.4.16 (both
shipped within hours of v1.4.14, each as its own tag). Hotfix — v1.4.18's
post-publish cycle (rider-stats bug, EntryCard objectPosition).

**Milestone vs tag (since 2026-05-07):** milestones are issue-bags decoupled from
tags. One milestone can span several production deploys (e.g. v1.4.20 spans
seg 17–20), and **each production deploy gets its own retro**. The Roadmap
"Completed" move and the milestone close happen at **milestone close**, not on
every deploy within it.

---

## 2. Plan (the planning session decides; retro only reflects)

- [ ] Define **1–3 goals** as sentences, mapped to the five project goals. Not issue titles.
- [ ] Every cycle includes some continuous improvement (DX or process). **Order DX issues first** so tooling is available for the rest.
- [ ] Only add issues that serve a goal; new discoveries become issues for a future release.
- [ ] Write the goals to the Roadmap **`## Now`** section as outcomes, not issue numbers (`feedback_roadmap_style`).
- [ ] Confirm the milestone exists and is the issue-bag for this cycle; link it **by number** (`/milestone/<n>`, `feedback_milestone_urls`).

## 3. Brief — **multi-strand releases only**

Skip for single-strand. Multi-strand examples: v1.4.10 / v1.4.17 (3 strands),
v1.4.19 (8-strand blitz).

- [ ] Scaffold a brief per strand from [docs/strands/STRAND-BRIEF-TEMPLATE.md](strands/STRAND-BRIEF-TEMPLATE.md) (or the `/strand-brief` skill).
- [ ] Each brief declares: filesystem posture, source-of-truth posture, target issues, workflow, verification, **cross-strand sharing notes (owns / reads / must-not-touch)**, and stop conditions.
- [ ] Resolve hard sequencing between strands (e.g. "start only after the gate has merged") and shared-file ownership in the briefs, not at runtime.

## 4. Execute (one issue at a time)

- [ ] One issue per PR — separate PR for each issue (per How We Work). A coherent nested pair may share one PR; say so in the PR body.
- [ ] Add acceptance criteria as a checkbox list on the issue; comment the planned approach.
- [ ] If `test-first` label: write failing tests first.
- [ ] Feature branch off `main`; explicit-path worktree for strand work. **Before every `git add`/`commit`, confirm `git branch --show-current`** (`feedback_shared_tree_branch_verification`).
- [ ] Fresh worktree: `npm ci`, then `cp data/riders/*.example.json` to non-example names before any build (`feedback_ci_seed_ordering`).
- [ ] PR body carries a **test plan** (acceptance criteria + how to verify); the publisher should not re-derive it.
- [ ] Use closure keywords (`Closes #N`) only when the PR actually closes the issue; brief/scaffold-only PRs use `Refs #N` (`feedback_pr_closure_keywords`).

## 5. Review, verify, merge

- [ ] CI green. `npm test`; `bash -n` for any touched shell script; the shell-test harness once #508 lands.
- [ ] **Rendered-page verification** (the build-and-preview step). The *automated* render-check (CI generates the site and asserts each entry page renders, no blank/500) is owned by **#322**. Until #322 lands, do this manually: `npm run build` + a `nuxt generate` static preview — **not** the SSR runtime (`feedback_production_preview`). *(Ownership split with #322: #322 implements the verification step; this checklist only references it.)*
- [ ] Visible / blast-radius actions (push, deploy, force) confirmed with the publisher unless pre-authorised for a defined scope.
- [ ] Merge to `main` via PR (squash). Verify the merge via the GitHub API before post-merge steps (`feedback_pr_polling`). Never push directly to `main`.

## 6. Pre-publish scrutiny — **publication releases only**

The window between "entry merged to `main`" and "`publish.sh` has deployed".
After deploy, the content-change rule freezes prose and images.

- [ ] Verify geography, attribution, image rights, and image-caption faithfulness (`feedback_pre_publish_scrutiny`). Raise concerns rather than proceeding silently.
- [ ] Confirm the entry is **not** still `draft: true` (publish.sh's draft pre-flight, #617, halts on this — treat a halt as the contract working).
- [ ] Pair-writing disclosure footer present on the entry (seg 7 onward).

### Late-add / hotpatch during the window

- **Pre-tag (publish.sh in flight):** only site-wide, **≤10-line**, orthogonal changes with publisher sign-off. No entry-body / rendering-path changes for the shipping entry. (See How We Work → Late-add policy.)
- **Post-tag (already deployed):** any further change ships as **its own tag** — there is no amend-the-tag path. Test: "would this look incoherent in the deployed release notes if folded in?" → yes means a new tag (the chore-release pattern, v1.4.15/16).

## 7. Deploy + tag

- **Publication:** run `scripts/publish.sh --segment N --release-tag W<NN>-seg<N>`.
  It handles stats, points, snapshots, weather, image validation, build, deploy,
  the frontmatter-PR merge, and Step 10 (tag + GitHub Release via `create-release.sh`).
- **Non-publication / chore / hotfix:** deploy, then `scripts/create-release.sh W<NN>.<N> [--title ...]`.
- [ ] Tag sequence is `git tag -a` → `git push origin <tag>` → `gh release create <tag> --notes-file …` (what `create-release.sh` already does). **Never** `gh release create --target <sha>` — it fails with "tag_name is not a valid tag."
- [ ] Deploy is SSH to the OVH VM, not rsync (`project_deployment`).

## 8. Ceremony (the seven steps `/release` mechanises)

Driven by `/release` (#339); run at **milestone close** (the Roadmap/milestone
steps), per production deploy for the retro. Each step stops on error with partial
state documented for recovery. The skill handles both the main repo and the
**wiki repo (separate clone, HTTPS — the SSH host key is not trusted in headless
runs)**.

1. [ ] Annotated tag at the target commit.
2. [ ] Push the tag to origin.
3. [ ] Create the GitHub Release with notes (steps 1–3 = `create-release.sh`).
4. [ ] Close the milestone (linked by number).
5. [ ] Create the retro wiki page from the four-section template (`Retro-<tag>.md`).
6. [ ] Add a row to `Retrospectives.md` (`| Release | Date | Theme | Page |`).
7. [ ] **Roadmap Completed move** — `create-release.sh --update-roadmap --milestone <n>`
       appends the Completed bullet (idempotent) and warns that the `## Now`
       block needs a **manual trim** (it does not rewrite the prose). #480.

## 9. Retro (reflect — file after each production deploy)

- [ ] Run the `/retro` skill: exactly four sections — **What went well / What was
      challenging / What we learned / What we lack** — in order, with those exact
      headings. `What we lack` is the systematically-dropped section; enforce it.
- [ ] Publisher reviews the draft (input point 1), then a Piers/Tully voice pass, then publisher sign-off (input point 2) before committing to the wiki.
- [ ] Retro **reflects**; decisions belong to the next planning session. Findings exit to issues, memory entries, or planning-notes flags — not same-session implementation.
- [ ] Update the slip-rate tally if a publication slipped.

## 10. Close out

- [ ] Close each issue with a comment (closure keywords auto-close on merge).
- [ ] Delete merged feature branches (local + remote); strand sessions remove their own worktree (`feedback_strand_session_self_cleanup`).
- [ ] Confirm the Roadmap `## Now` block now describes what is *actually* in flight (the manual trim from step 8.7).
- [ ] Carry unresolved items into `project_next_planning_notes.md`.

---

## What is automated vs human

| Step | Owner |
|------|-------|
| 1–6 (type, plan, brief, execute, review, scrutiny) | Human / agent judgement |
| 7 deploy | `publish.sh` / `create-release.sh` |
| 8 ceremony (tag, push, release, milestone, retro stub, index row, Roadmap move) | `/release` skill (#339), wrapping `create-release.sh` (incl. #480) |
| 9 retro content | `/retro` skill scaffolds; humans write and sign off |

The render-check verification (step 5) is implemented by **#322**; this checklist
references it, by the agreed ownership split between the spine and ceremony strands.
