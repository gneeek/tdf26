# Strand: Entry-card thumbnail selection (#535)

Reader-uplift strand to make `EntryCard`'s thumbnail an editorial choice rather than an accident of frontmatter image order. Authored 2026-05-13.

## 1. Goal

Replace `EntryCard.vue`'s "first image in frontmatter" thumbnail mechanism with an editorially-controlled selector, so the homepage card and the archive page card can eventually share a single component without forcing weak thumbnails on entries whose first frontmatter image is a person, a map fragment, or a small detail.

Closes #535. Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/52). Smallest of the v1.4.19 reader-uplift bucket per scope.md rationale ("recommended order: #535 first (smallest, EntryCard already extracted)"). EntryCard already extracted via PR #536 (#522).

Runs in **publisher-paced mode** — the editorial-control mechanism is a design choice (frontmatter field vs heuristic vs manifest, per #535's body), and that choice belongs to the publisher. Fire AskUserQuestion at the design checkpoint before writing code.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/535-entry-card-thumbnails /home/jhs/code/tdf26-card-thumbs main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `components/EntryCard.vue` is the single rendering site post-#522 extraction. The current thumbnail logic is at lines 6–10 (`entry.images[0]`) and the suppression gate is the `density` prop (line 38).
- `density='compact'` is set by the archive page (`/entries`) specifically to suppress thumbnails because of this bug — confirm by reading `pages/entries/index.vue` (or wherever the archive route lives). Once thumbnail selection is editorial, `density='compact'` becomes a pure layout concern.
- The `objectPosition` pass-through (line 10) landed in PR #540 — preserve it; whatever mechanism this strand introduces should compose with `objectPosition`, not replace it.
- Per `feedback_pre_publish_scrutiny.md`: image rights / attribution are checked at publish-time; this strand doesn't change image content or licensing, only which one renders as the thumbnail.

## 4. Target issues

- **Closes #535** — use `Closes #535` in PR body (per `feedback_pr_closure_keywords.md`).
- If the strand surfaces image-licensing-shaped findings (e.g., a thumbnail-selection mechanism would benefit from a per-image card-suitable flag), file a separate issue rather than expanding scope.

## 5. Workflow

Publisher-paced cadence:

1. **Survey current state.** Read `components/EntryCard.vue` (full file, ~50 lines). Read every published entry's frontmatter (`content/entries/0[1-9]-*.md` through `12-*.md`) and note: which entries have `images[0]` that is a strong scannable thumbnail vs which entries have a weak first image. Concrete examples are evidence for the design checkpoint.
2. **Design checkpoint (AskUserQuestion).** Present three options from #535's body — verbatim is fine:
   - **Frontmatter field** (e.g., `thumbnail: /path/to/img.jpg` or `images[N].thumbnail: true`): explicit per-entry choice; needs a fallback to `images[0]` for entries without the field.
   - **Heuristic** (e.g., pick first image with `aspectRatio` close to square, or with `role: landscape`): no frontmatter changes needed, but heuristic correctness is a moving target.
   - **Manifest** (e.g., `data/entry-thumbnails.json` keyed by segment): centralizes thumbnail choice outside entries; useful if thumbnails are curated by someone other than the entry author.
   Plus the implicit fourth: **hybrid** (frontmatter field is canonical; fall back to heuristic; fall back to `images[0]`). The publisher picks; do not start writing until the answer is in. Per `feedback_voice_checkpoint_prep.md` (the same principle applies to design checkpoints): read each option's implementation cost before presenting, so the publisher's choice is between substantive options.
3. **Implement chosen mechanism.**
   - If frontmatter field: pick the canonical field name (`thumbnail`, `cardImage`, `featuredImage` — propose one in the checkpoint), update `EntryCard.vue` to read it, fall back to `images[0]` for entries without it. **Do not retrofit published entries** with the new field (per `feedback_content_change_rule.md`); they continue to use the `images[0]` fallback until forward-only authoring uses the new field. Surface this in the PR body.
   - If heuristic: add a small derivation function; consider where it runs (build-time vs render-time). Document the heuristic rule in a code comment (one line, per the "no comments unless the WHY is non-obvious" rule — heuristic rules ARE non-obvious).
   - If manifest: add `data/entry-thumbnails.json` (consider whether it's checked in vs gitignored; check is correct here — it's curated editorial data); add a loader; document in CLAUDE.md or `data/README.md`.
4. **Update the archive page.** If the design checkpoint produces an editorial-control mechanism strong enough to render thumbnails everywhere, drop `density='compact'` from the archive route — that prop's only purpose was suppressing weak thumbnails. Per #535: "the `density` prop's role shrinks to a layout-only concern, and the archive can drop `density='compact'` without visual regression."
5. **Visual review checkpoint (AskUserQuestion).** Run `npm run dev`, open the homepage and the archive, walk through every published entry's card with the publisher. Publisher confirms each thumbnail meets the bar (or names which entries need authored-in thumbnails as forward-only follow-up).
6. **PR open against `main`.** Title `feat(entry-card): editorial thumbnail selection (closes #535)`. Body lists:
   - Mechanism picked at design checkpoint.
   - Whether the archive's `density='compact'` was dropped.
   - Any entries flagged for future thumbnail authoring.
   - Screenshots of homepage + archive before/after if the change is visible.

## 6. Verification commands

- `npm test` — entry-shape assertions pass.
- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — must pass; if the design checkpoint picks a frontmatter field, the validator should not reject entries without it (the field is optional, falls back to `images[0]`).
- `npm run build` — production build succeeds.
- **Dev preview:** start `npm run dev`, walk through `/` (homepage) and `/entries` (archive). Both card surfaces render thumbnails per the new mechanism. Per `project_dev_server_content_index.md`: if entries don't show after the branch switch, delete `.data/content/contents.sqlite*` and restart dev.
- **Production preview** if the visual change is non-trivial (per `feedback_production_preview.md`): `nuxt generate` + static serve; verify against the SSR dev output.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `components/EntryCard.vue`
  - The chosen mechanism's implementation site (e.g., `data/entry-thumbnails.json` if manifest; a composable if heuristic; a frontmatter validator hint if field).
  - The archive page (`pages/entries/index.vue` or equivalent) only if dropping `density='compact'`.
- **What this strand reads:**
  - `content/entries/*.md` frontmatter (read-only; do not retrofit per `feedback_content_change_rule.md`).
  - The homepage (`pages/index.vue`) for card-usage reference; do not modify unless dropping a `density` prop there.
- **What this strand must NOT touch:**
  - `content/entries/*.md` — even forward-only authoring with the new field should be a separate follow-up (so the EntryCard change is reviewable in isolation; new-field authoring is a content concern).
  - The seg 12 publish branch (`chore/seg-12-pre-publish`) — active in the parent worktree.
  - `processing/validate_entries.py` (MDC validator strand owns it; if a new optional frontmatter field needs validation, file an issue rather than expanding scope).
  - The rider-stats fix strand's `processing/` files.
  - STRAND-BRIEF-TEMPLATE.md untouched.
- **Cross-strand collisions:** none expected. The MDC validator strand reads but doesn't modify entries; the rider-stats fix touches `processing/` only. Concurrent merging is safe.

## 8. Scope discipline

- **Do not retrofit published entries** with a new frontmatter field. Per `feedback_content_change_rule.md`, published entries are fixed; the fallback to `images[0]` keeps them working until forward-only authoring picks up the new field.
- **Do not redesign EntryCard's layout.** The `density` prop's structural role is in scope to drop only if the design checkpoint chose a mechanism strong enough; the visual layout otherwise stays.
- **AskUserQuestion fires at the design checkpoint and the visual review checkpoint.** Implementation steps in between are not checkpointed.
- **If the publisher prefers to defer:** acceptable outcome is "design checkpoint fires, publisher chooses 'not yet, file follow-ups'". Close the strand with the design notes captured in the PR description (or the issue body) as input for future work; do not push a half-implementation.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_content_change_rule.md` (no retroactive edits to published entries)
- `feedback_pre_publish_scrutiny.md` (image rights unchanged here; flagged so the strand doesn't accidentally touch them)
- `feedback_voice_checkpoint_prep.md` (apply same principle to the design checkpoint — read each option's implementation cost before presenting)
- `feedback_issues_describe_problems.md`
- `feedback_pr_closure_keywords.md`
- `feedback_production_preview.md` (use generated static for visual review if the change is non-trivial)
- `project_dev_server_content_index.md` (dev fs-watcher gap after branch switch)
- `feedback_multi_strand_session_checkpoints.md` (publisher-paced this strand)

## 10. Stop when

- PR opened against `main`, `Closes #535` in body.
- Design checkpoint fired and answered; mechanism documented in PR body.
- Visual review checkpoint fired and answered; publisher confirmed homepage + archive thumbnails meet the bar.
- `npm test` + entry validators green; `npm run build` green.
- Dev preview rendered without error; visual evidence (screenshots or "publisher signed off in checkpoint N") in PR body.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-card-thumbs` once the PR has merged.
- Final report posted to publisher: PR link, mechanism picked, archive `density='compact'` disposition, any entries flagged for forward-only thumbnail authoring.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during 535-entry-card-thumbnails strand execution (<date>)`:
  - **Decision-actionable observations:** entries needing forward-only thumbnail authoring, any image-licensing follow-ups, related EntryCard concerns surfaced.
  - **Light-tier pattern observations:** design-checkpoint shape findings, brief-template gaps.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock.
