# Milestone scope template

Use this template when closing a planning session, per the 2026-05-07 Topic 9b decision. Each planning session writes one file per milestone it scopes, at `docs/planning/<milestone>-scope.md`. The retro for the corresponding production deploy reads this file as the "what we said we would do" reference.

The template is intentionally small. Pre-decide the shape; fill in the specifics during the planning session's close.

## Sections

### 1. Title

`<milestone> — <one-line theme>`. Example: `v1.4.19 — Reader uplift and segs 14-16 prep`.

### 2. Milestone link

GitHub milestone URL by number per `feedback_milestone_urls.md` (e.g. `https://github.com/gneeek/tdf26/milestone/19`), not by title-search.

### 3. Planned issues

One-line each. Group by theme if the milestone spans multiple. Example shape:

- **Theme A**
  - #NNN — short title — one-line gloss of why it's in scope
  - #NNN — short title — one-line gloss
- **Theme B**
  - #NNN — short title — one-line gloss

Issue must be filed before scope-pinning (an issue without a number is a planning-conversation item, not a scoped item).

### 4. Expected ship window

Date or date-range when the milestone's production deploy is expected. Per Topic 9c: retros are production-deploy-bounded. The ship window anchors the retro window.

### 5. Success criteria

What "done" looks like for this milestone. Two to four bullets is usually right. Examples:

- All planned issues closed via PR merge.
- Publish.sh runs without halting on any of the three documented failure modes.
- Dev preview renders the new component on every entry page.

### 6. Out of scope (explicit)

What planning explicitly *decided* not to include. Captures intent so the retro doesn't reconstruct it. Examples:

- New entry types (deferred to next milestone).
- Voices project rewire (#364, blocked on Voices design session).

### 7. Rationale notes

Free-form notes on scope decisions that future-you will want to remember. Why a borderline issue was kept in or excluded; what tradeoffs got made; what assumptions the milestone rests on. Brief; this is not a full planning transcript.

### 8. Cross-links to strand briefs

If the milestone is being delivered by named strands, list them with paths:

- `docs/strands/strand-<id>.md` — one-line role
- `docs/strands/strand-<id>.md` — one-line role

## When deviating

Common deliberate deviations:

- **Hotpatch / non-publication production deploy**: §3 may be a single issue; §4 is "as soon as ready"; §6 is small or absent.
- **Process-only milestone** (no code, just retro/wiki/planning work): §3 lists planning-decisions instead of issues; §5 success criteria are about decisions landed, not code shipped.
- **Multi-strand release**: §8 grows; consider a small "strand coordination notes" subsection if cross-strand collisions are forecast.

## Lifecycle

Each milestone-scope file is a one-shot artifact. After the corresponding retro fires, the file becomes historical record. Do not edit it post-retro to reflect what actually happened — that's the retro's job. The scope file stays as the "what we said we would do" snapshot.
