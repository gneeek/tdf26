# Strand: EntryCard component extraction (#522)

Vue refactor strand. Authored at the 2026-05-07 planning session resume (Topic 13 item 1). Reader-uplift v1.4.19 work.

## 1. Goal

Extract a shared `components/EntryCard.vue` component and consume it from the existing call sites so future card-shaped reader-uplift work doesn't keep duplicating Tailwind class strings. Closes [#522](https://github.com/gneeek/tdf26/issues/522). Milestone: **v1.4.19**. No deadline.

This is a structural refactor, not a feature change. Visual output should be byte-identical (or near-identical) before and after; the diff lives in component organization, not on the rendered page.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-522-entrycard /home/jhs/code/tdf26-522 main
```

- Run from outside the repo (or via `git -C`); see `feedback_strand_worktree_path.md`.
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/issue-522-entrycard` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- Read both call sites before editing. The duplication shape described in §5 is this brief's understanding — verify against current code per `feedback_brief_content_is_carryforward.md`.
- The Tailwind class string is the canonical visual contract; preserve it exactly when extracting.

## 4. Target issues

- [#522](https://github.com/gneeek/tdf26/issues/522) — extract shared EntryCard. Closes after refactor + visual verification + PR merge.

## 5. Workflow

The card markup currently appears in two places that share a near-identical Tailwind class string but differ in inner content (thumbnail vs no thumbnail).

### 5a. Identify the duplication

- **Homepage** — `pages/index.vue` line 26: `<article>` block under "Latest Entries". Includes thumbnail (`<img v-if="entry.images && entry.images.length">`) before the text block. Link is `<NuxtLink :to="..." class="flex gap-4 items-start">`.
- **Archive** — `pages/entries/index.vue` line 11: same `<article>` shape, no thumbnail. Link is `<NuxtLink :to="..." class="block">`.

The shared class string on `<article>`:
```
group bg-white rounded-lg shadow-sm p-4 hover:shadow-md hover:bg-stone-50 hover:border-l-4 hover:border-correze-red cursor-pointer transition-all border-l-4 border-transparent
```

Both render: optional thumbnail, segment+km label, title, optional subtitle, publishDate.

### 5b. Component shape

Create `components/EntryCard.vue` with:

- **Props**: `entry: object` (the Nuxt Content entry doc — at minimum `path`, `_path`, `segment`, `kmStart`, `kmEnd`, `title`, `subtitle?`, `publishDate`, `images?`); `density: 'compact' | 'standard'` defaulting to `'standard'`.
- **Behavior**:
  - When `images?.length` is truthy and `density === 'standard'`, render the thumbnail block + `<NuxtLink class="flex gap-4 items-start">`.
  - When no images or `density === 'compact'`, render the text-only block + `<NuxtLink class="block">`.
  - Identical class string on the outer `<article>` in both modes.
- **Date formatting**: import / receive `formatDate` consistently. Both call sites currently define their own — pick one canonical implementation (probably extract to `composables/useDate.ts` if it doesn't already live there) or accept the formatted string as a prop, whichever is cleaner.

### 5c. Replace the two call sites

- `pages/index.vue`: replace the `<article v-for="entry in entries">` block (lines ~26-50) with `<EntryCard v-for="entry in entries" :key="entry.path || entry._path" :entry="entry" />`. Default density='standard' shows thumbnails.
- `pages/entries/index.vue`: replace the `<article v-for="entry in entries">` block (lines ~11-22) with `<EntryCard v-for="entry in entries" :key="entry.path || entry._path" :entry="entry" />`. Pass `density='compact'` if archive should stay text-only, OR drop the prop and let archive cards gain thumbnails (decide via AskUserQuestion checkpoint — see §8).

### 5d. Visual verification

Per `feedback_production_preview.md`: build production preview before merging visual PRs. Specifically:

- `npm run build` succeeds.
- `npm run preview` (or production-mode dev server) loads `/` and `/entries` without errors.
- Pixel-diff or side-by-side compare the homepage Latest Entries section and the /entries archive page against `main`. Differences should be: zero (if archive stays text-only) or thumbnails appearing in archive (if density default chosen).
- Test responsive breakpoints (sm, md, lg) — the Tailwind classes include responsive modifiers; the extraction should preserve them.

### 5e. Open the PR

- Title: `refactor: extract shared EntryCard component (closes #522)`.
- Body: list the two call sites' before/after, screenshot of the homepage and archive at `main` vs branch, density-prop decision rationale, link to #522.

## 6. Verification

- `npm test` green (existing tests should continue passing — entry shape isn't changing).
- `npm run build` succeeds; `npm run preview` renders both call sites.
- Visual diff captured in PR body.
- No console warnings on the rendered pages.

## 7. Cross-strand sharing notes

- **Owns (write):** new `components/EntryCard.vue`, edits to `pages/index.vue` + `pages/entries/index.vue`. Possibly `composables/useDate.ts` or similar if extraction collapses out a shared formatter.
- **Reads:** both pages above; existing components for naming-convention reference (`components/StageDetails.vue` is a similar reader-facing component).
- **Must NOT touch:** `pages/entries/[...slug].vue` (separate prev/next nav, different visual element); `content/entries/*.md` (no entry frontmatter changes); the seg-11 / publisher-contract / tour-history strands' file regions.
- **Cross-strand collisions:** none expected; the seg 11 drafting strand writes new entry markdown, which renders through these pages but doesn't touch their templates.

## 8. Scope discipline

- One AskUserQuestion checkpoint at §5b/5c: should the archive page gain thumbnails (drop density='compact') or stay text-only (keep the asymmetry)? The original Topic 13 framing offered "leave the asymmetry as a deliberate 'archive is denser' choice" — the publisher decides whether to preserve that or unify.
- Do not add new entry-card features in this strand (e.g., reading time, related entries). Extraction only. Future card-shaped uplift work is the *third caller candidate* the issue references; this strand makes that work cheap, but doesn't include it.
- File new issues for any drift discovered between the two existing call sites that isn't covered by the density prop.
- Do not refactor unrelated components even if they appear similar. If a third call site is discovered (e.g., the prev/next nav at `pages/entries/[...slug].vue` lines 47-61, which is currently just text links), evaluate whether it benefits from the same component — but default is leave it; that nav is structurally different.

## 9. Memories that apply

- `feedback_brief_content_is_carryforward.md` (verify the duplication shape against current code)
- `feedback_production_preview.md` (build production preview before merging)
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`
- `feedback_parallel_source_of_truth_detector.md` (the duplication is itself a parallel-source-of-truth instance at the markup level — extracting it removes the drift surface)

## 10. Stop when

- `components/EntryCard.vue` exists; both call sites consume it.
- Visual diff captured; publisher endorsed the density-prop decision.
- `npm test` green; `npm run build` succeeds.
- PR opened, reviewed, merged.
- **Cleanup (you run this, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-522` once the PR has merged.
- Final report posted to publisher: PR link, visual diff summary, density-prop decision, any follow-up issues filed.
