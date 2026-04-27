# Strand C — Reader experience: landing page

**Start here:** [Roadmap → Now → Reader-experience strand](https://github.com/gneeek/tdf26/wiki/Roadmap#now)

## Goal

Improve the experience for readers landing on the homepage. Pick one improvement, ship it, stop. The goal is a noticeably better landing page, not a particular feature.

## Candidate set

These are the open issues in scope for the strand. Pick one and start there; the others can be redirected to a future release.

- **#391** Homepage: add thumbnail image to each entry card.
- **#407** Homepage: let readers reach entries older than the latest 5.
- **#408** Entry page: show simplified rider stats at top, link to full dashboard below. *(In scope here because the publisher grouped it with the landing-page set; entries are the main reader destination after the homepage.)*

## How to choose

The publisher has not pre-selected. The strand decides based on:

- Smallest scope that produces a noticeable reader-experience win.
- Avoid anything that would conflict with strand A's edits to `content/entries/0[8-9]*.md`, `content/entries/10-*.md`. None of the three candidates touch those files.

If you start one and find it bigger than estimated, finish it anyway — do not split mid-flight.

## Scope discipline

- One improvement only. Do not start a second.
- File touches expected: `pages/index.vue`, `components/`, possibly `composables/` or `layouts/default.vue`. If the change reaches into `data/` or `processing/`, the scope has drifted; reset.
- Branch: `feature/issue-N-<short-name>`. Assign the PR to milestone v1.4.10.

## Memories that apply

- `feedback_production_preview.md` — preview a production build before merging visual PRs.
- `feedback_pr_polling.md` — verify PR merges via GitHub API.

## Stop when

- The chosen issue is shipped (PR merged into main).
- A production preview has confirmed the change works.
- The other candidate issues are left untouched for a future release.
