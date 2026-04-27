# Strand A — Content: segments 8/9/10

**Start here:** [Roadmap → Now → Content strand](https://github.com/gneeek/tdf26/wiki/Roadmap#now)

## Goal

Publish segment 8 on Wed 2026-04-29. Produce drafts of segments 9 and 10 inside this strand using shared research across the 20km block (km ~49.7-70). Segments 9 and 10 ship in v1.4.11 and v1.4.12 respectively.

## The 20km block

- **Seg 8 (km 50-56):** Beynat foothills, Côte de Miel climb, Albussac. Templar Commanderie de Puy de Noix is ~4 km off-route, already in `data/attractions.json`.
- **Seg 9 (km 56-64):** Corrèze valley descent. Connective tissue.
- **Seg 10 (km 64-70):** Tulle. Heaviest cultural payload of the block: lace, accordion-making (Maugein already in `data/attractions.json`, see music-thread ledger in `project_next_planning_notes.md`), the WWII massacre of 9 June 1944, Hollande's mayoralty.

Segments 8 and 9 must set up the Tulle arrival. Do not write segment 10's material into the earlier two.

## Workflow

1. Research the full 20km block in one shared pass — history, geology, cycling context, attractions, sources.
2. Bring findings back to the publisher to decide narrative arc and voice register per segment.
3. Spawn three draft subagents — each gets the segment number, the agreed arc, the agreed voice, and the relevant slice of research.
4. Refine seg 8 to publish-ready; commit segs 9 and 10 as first drafts (still `draft: true`).

## Target issues

Open these as the strand's first commits, all on milestone v1.4.10:

- **Segment 8 entry content** — primary deliverable. Placeholder at `content/entries/08-cote-de-miel.md`.
- **Segment 9 entry draft** — drafted in v1.4.10, ships v1.4.11.
- **Segment 10 entry draft** — drafted in v1.4.10, ships v1.4.12.
- **Segment 8 publication** — publish-day tracking issue, matching the pattern set by #423 and #393.

## File regions and branches

- `content/entries/08-cote-de-miel.md`, `09-descent-to-the-correze-valley.md`, `10-tulle-lace-accordions-and-memory.md` (placeholders exist with frontmatter).
- `public/images/segment-08/`, `public/images/segment-09/`, `public/images/segment-10/`.
- `data/attractions.json` only if research surfaces a missing or wrong attraction. Coordinate if any other strand wants this file (none expected).
- Branches: `feature/issue-N-segment-08-content`, etc.

## Memories that apply

- `feedback_literary_footnotes.md`, `feedback_sources_section.md`, `project_disclosure_practice.md`, `feedback_content_change_rule.md`, `feedback_pre_publish_scrutiny.md`, `feedback_on_route_checks.md`.
- Voice references: `project_meymac_voice.md` (seg 24, not these), `project_barthes_callback.md` (segs 6/12/15, not these). Voice for segs 8/9/10 is open and decided with the publisher.
- Music-thread ledger in `project_next_planning_notes.md`.

## Stop when

- Segment 8 is publish-ready (images + attribution, optional `## Sources`, disclosure footer, `draft: false` only after publisher confirms).
- Segments 9 and 10 are first-draft committed (still `draft: true`).
- Any cross-segment concern that surfaces during research is filed as a new issue rather than fixed inline.
