# Strand: Date-based release tag migration (#519)

Infrastructure / process strand. Authored at the 2026-05-07 planning session resume (Topic 9a follow-through).

## 1. Goal

Migrate release tags from semver (`v1.4.x`) to date-based on the next production deploy. Closes [#519](https://github.com/gneeek/tdf26/issues/519). No firm milestone — the strand should land before the seg 11 ship Sun 2026-05-10 if format-decision and implementation are quick, otherwise on the Wed 2026-05-13 / next ship after that. Existing `v1.4.x` tags stay as historical record per the planning decision.

This strand is *publisher-paced single-strand mode* — the format decision is the load-bearing AskUserQuestion checkpoint and shouldn't be pre-decided.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-519-date-based-tags /home/jhs/code/tdf26-519 main
```

- Run from outside the repo (or via `git -C`); see `feedback_strand_worktree_path.md`.
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/issue-519-date-based-tags` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `project_release_tagging.md` (memory) is the canonical rule for tagging policy. The 2026-05-07 edit captured the date-based decision; this strand is the implementation.
- `scripts/publish.sh` is the load-bearing code: line ~104 currently validates `^v[0-9]+\.[0-9]+\.[0-9]+$`. The migration changes this regex.
- Per `feedback_brief_content_is_carryforward.md`: the file-line citations and shapes in §5 below are this brief's understanding — verify against current code at strand start.

## 4. Target issues

- [#519](https://github.com/gneeek/tdf26/issues/519) — switch release tags from semver to date-based. Closes after the new format is decided, `publish.sh` migration lands, the next production deploy uses the new format, and the existing tags are confirmed as preserved.

## 5. Workflow

### 5a. Decide the tag format (AskUserQuestion checkpoint — do not pre-decide)

Three plausible candidates; the publisher chooses. Each has tradeoffs:

| Format | Example | Pros | Cons |
|---|---|---|---|
| **ISO week** | `2026-W19` (with `.1`/`.2` if multiple deploys per week) | Aligns with twice-weekly publication cadence; one tag per week is the natural scale; week boundaries match retro windows | Less immediately legible to non-ISO-week audiences; may need leading-zero discipline (`W05` vs `W5`) |
| **Calendar date** | `2026-05-10` (with `.1`/`.2` if multiple deploys same day) | Most legible; sortable lexically; common convention | Two deploys same day need a counter; format is otherwise correct ISO-8601 but git tag chars are fine |
| **Date + sequence** | `2026.05.10.1` | Explicit counter from day 1; sorts cleanly | Verbose; `.` chars in tags may interact awkwardly with some tooling |

Read the publisher's existing memory (`project_release_tagging.md`) before asking — they may already have a leaning. The decision is also tied to the planning-notes carryforward "Date-based milestone naming follow-up" (whether existing v1.4.18/v1.4.19/v1.4.20 milestones get renamed); this strand defers the milestone-rename decision (out of scope).

### 5b. Update the `publish.sh` regex and help text

After the format is decided:

- Edit `scripts/publish.sh` line ~104 (`^v[0-9]+\.[0-9]+\.[0-9]+$` regex) to accept the new format. Decision: replace the regex outright (clean break) or accept *both* old and new during a transition window (defensive). Recommended: clean break — existing tags are historical record, new tags use the new format, no in-flight semver tags need accepting.
- Update the `--help` text (line ~55, line ~63) to show the new format example.
- Update the usage line at the top of the file (line ~6) similarly.
- Smoke: invoke `./scripts/publish.sh --release-tag <bad-format>` and confirm the validation rejects with the new error message.

### 5c. Optional helper: `scripts/next-tag.sh`

If the format chosen has a deterministic "next tag" (e.g. ISO-week or date), a tiny helper script can generate the next valid tag automatically so the publisher doesn't have to type it. Decision via AskUserQuestion at the publisher's option. Default: skip the helper this strand; defer to a follow-up issue if needed.

### 5d. Validate against the seg 11 publish (or next deploy)

The next production deploy will be the first under the new scheme. Verify:

- The new format passes `publish.sh` validation.
- The tag lands on GitHub.
- A GitHub Release renders with the new tag name.
- No tooling that consumes tags breaks — `gh release list`, the deploy workflow (currently doesn't trigger on tags per CI inspection, but verify), any external watchers.

### 5e. Update memory and CLAUDE.md narrative references

- `project_release_tagging.md` — confirm the existing edit's wording matches the format decided in 5a (or amend if it doesn't).
- CLAUDE.md narrative references to versioning are minimal but check; do not edit content/entries (per `feedback_content_change_rule.md`).
- The planning-notes file's "Date-based milestone naming follow-up" carryforward stays open — this strand only addresses tags, not milestones.

### 5f. Open the PR

- Title: `infra: switch release tags from semver to <date-format> (closes #519)`.
- Body: format chosen + rationale, regex before/after, help-text before/after, smoke evidence, link to #519, callout that existing v1.4.x tags are preserved.

## 6. Verification

- `bash -n scripts/publish.sh` — syntax OK.
- `./scripts/publish.sh --help` — help text reflects new format.
- Smoke: `./scripts/publish.sh --release-tag 2026-W19 --skip-release` (or equivalent for chosen format) validates as expected; bad format rejected.
- `npm test` — green (no JS test depends on the tag format).
- The next production deploy uses the new format (this verification spans into the deploy window — schedule the strand merge to leave a buffer before publish.sh runs).

## 7. Cross-strand sharing notes

- **Owns (write):** `scripts/publish.sh`. Possibly `scripts/next-tag.sh` if 5c lands. Possibly small edits to memory/`project_release_tagging.md`. Possibly small CLAUDE.md narrative edits.
- **Reads:** `project_release_tagging.md`, the existing tag list (`git tag`), `.github/workflows/*.yml` to confirm CI doesn't trigger on tag patterns.
- **Must NOT touch:** `content/entries/*` (content-change rule); `data/*` files; the seg-11 / publisher-contract / tour-history / Voices / #441 / #522 strand file regions.
- **Cross-strand collisions with seg-11 drafting (in flight):** seg 11 publishes Sun 2026-05-10. This strand modifies `publish.sh` — the same script that runs the seg 11 publish. Coordination required:
  - **Option A (preferred):** land this strand *before* the publish.sh fail-fast strand finishes consuming attention; the publish.sh changes are isolated to the regex and help text, low risk.
  - **Option B:** land this strand *after* seg 11 publishes (seg 12 ship is Wed 2026-05-13; gives a window).
  - The publisher decides via AskUserQuestion at strand start.

## 8. Scope discipline

- Tag format only. Do not refactor publish.sh structure.
- Do not rename existing milestones (v1.4.18, v1.4.19, v1.4.20) — that's a separate follow-up flagged in planning-notes carryforwards.
- Do not back-tag historical releases. v1.4.x tags stay as historical record.
- Do not update wiki retro pages or other narrative-only references — the new scheme applies forward; old references are part of the project's history.
- File new issues for any related work surfaced (e.g., a `next-tag.sh` helper if deferred; milestone-naming policy decision).

## 9. Memories that apply

- `project_release_tagging.md` (the canonical rule)
- `feedback_brief_content_is_carryforward.md` (verify the file-line citations in §5 against current code)
- `feedback_pre_publish_scrutiny.md` (this strand modifies the publish-day script; the rules apply)
- `feedback_shared_tree_branch_verification.md`
- `feedback_strand_worktree_path.md`
- `feedback_no_regex_in_bash.md` (relevant if the format decision involves a tag-validation regex more complex than the current shape)

## 10. Stop when

- Format decided via AskUserQuestion checkpoint.
- `scripts/publish.sh` regex + help text + usage line updated.
- Smoke confirms validation works for new format and rejects old format.
- PR opened, reviewed, merged.
- The first production deploy under the new scheme lands a date-based tag on GitHub; existing v1.4.x tags confirmed preserved (`git tag` shows both).
- **Cleanup (you run this, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-519` once the PR has merged.
- Final report posted to publisher: PR link, format chosen, smoke evidence, the first new-format tag URL, any follow-ups filed.
