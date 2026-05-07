# Strand — Tour-history feature research (#502)

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md). Feeds [#502](https://github.com/gneeek/tdf26/issues/502) (umbrella); does not close it.

## 1. Goal

Produce a research dossier for the `/tour-history` feature — phase 1 of the research-then-discuss-then-draft sequence decided at the 2026-05-07 planning. The dossier expands the existing `data/historical-tdf.json` corpus by surfacing new corridor-relevant Tour de France history, regional race history (Tour du Limousin, Paris-Corrèze, L'Agglomérée cyclosportive), photo/video source candidates, and any race-radio / commentary material that survives under licences compatible with this project.

The dossier feeds the design-discussion phase (next planning session: layout, hero image, story arc, prominent-launch timing) and the subsequent draft phase (a sister strand that builds the `/tour-history` route page).

Milestone v1.4.20 (placeholder; reshuffles when the prominent-launch timing pins a specific milestone).

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-502-tour-history-research /home/jhs/code/tdf26-tour-history main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

- **Read `data/historical-tdf.json` directly** as the starting corpus. It currently has 4 segment-group entries (segs [1,2], [10], [14,15,16], [25,26,27] — note the [25,26,27] entry has a known segment-27 bug filed as #503; the dossier should reference #503's resolution, not the buggy data).
- **Read CLAUDE.md "References: Cycling History Along the Route"** for the catalogued URL bibliography. CLAUDE.md is the primary source of pre-vetted URLs for this corpus; the deprecation strand (#491) does NOT touch this section, only the "Known Waypoints and Climbs" tables, so this reference stays canonical.
- **Read CLAUDE.md "References: Creative Commons Image Sources"** for image-source candidates per segment.
- For any factual claim the dossier captures, cite the URL in the dossier's sources section.
- Cross-check segment keying against `data/segments.json` (per `feedback_on_route_checks.md`) — if a Tour stage finished in Tulle, verify which segment Tulle is in **today** rather than transcribing CLAUDE.md.
- Per `feedback_source_of_truth_framing.md`: this dossier itself is hand-curated and will be downstream of `data/historical-tdf.json` in the long run; the dossier should NOT become a parallel source-of-truth. Any addition that lands in `data/historical-tdf.json` does so via a separate strand (filed as a follow-up issue), not via this dossier.

## 4. Target issues

- **Feeds [#502](https://github.com/gneeek/tdf26/issues/502)** — umbrella for the Tour-history feature; this strand does not close it (subsequent draft + launch strands do).
- **References [#503](https://github.com/gneeek/tdf26/issues/503)** — Paris-Corrèze segments-27 drift; flag in dossier; do not fix here.
- **References [#483](https://github.com/gneeek/tdf26/issues/483)** — observability/instrumentation research sprint; the prominent launch is the measurement moment.
- **Files new follow-up issues** for any new factual entries that should land in `data/historical-tdf.json`. Each follow-up describes the data-add as a problem ("X stage's connection to corridor segment Y is currently undocumented in `data/historical-tdf.json`") per `feedback_issues_describe_problems.md`.

## 5. Workflow

1. **Research subagent pass(es).** Spawn one or more general-purpose Agent subagents to research, structured by topic:
   - **Tour de France stages with corridor connections.** Stages that started, finished, or passed within ~30 km of any segment 1-26. Targets: Brive (segs 1-2), Tulle (seg 10), Ussel (seg 26), Limoges/Périgueux (south-west adjacency), Aurillac/Clermont-Ferrand (south-east adjacency, including 2026 Stage 10 Aurillac→Le Lioran the day after Stage 9). Sources: bikeraceinfo.com, procyclingstats, Wikipedia stage pages, ASO archives. Look beyond the entries already in `data/historical-tdf.json`.
   - **Tour du Limousin** — UCI 2.1 stage race since 1968, recently renamed Tour du Limousin-Périgord-Nouvelle-Aquitaine. Notable winners, route history through Corrèze, photographic / archival material.
   - **Paris-Corrèze** — defunct UCI 2.1 race, 2000s. Final-edition results, Corrèze finishes, narrative arc of why it folded. Resolve the segment keying in the existing corpus entry (currently `[25, 26, 27]` — see #503).
   - **L'Agglomérée cyclosportive (Apr 5 2026)** — amateur sportive on 40 km of the Stage 9 route including Suc au May. Most recent edition (just three months ago at planning time). Worth a callout in the dossier as a recent-amateur-event-on-the-actual-route hook.
   - **2025 Tour de France** — most recent edition; check whether any stages had corridor relevance, and if so capture for the dossier.
   - **Famous riders from Corrèze** — riders born in or strongly associated with Corrèze; their Tour records.
   - **Resistance-era racing / post-war narrative** — the 1944 Tulle massacre is in seg 10's content; the post-war Tour's 1947 return and the corridor's role in restoring civic life is potential background colour. Bonus content if it surfaces.
   - **Photo / video sources by event.** For each event in the dossier, name CC-licensed photo candidates (Wikimedia Commons by event/place categories) and video sources (Dailymotion ASO channel, YouTube CC reels, INA archive — note INA has GDPR cookie banner inside iframe per `reference_european_video_embeds.md`; prefer YouTube/Vimeo-hosted versions).
   - **Race-radio / commentary quotes.** These are often hardest to source under CC. Capture promising URLs even if licensing is unclear; flag licensing as an open question per item.
2. **Write the dossier** to `content/research/tour-history-research.md` (create directory if absent — gitignored at `content/research/` likely; check `.gitignore` first and update if necessary). Structure:
   - **Per-event section** for every Tour-history event the dossier surfaces (existing + new). Include: year, stage / race, route or corridor connection, segment keying (verified against `data/segments.json`), summary narrative, source URLs, photo/video candidates with licence notes, any race-radio quote candidates with licence flag.
   - **Regional race section** — Tour du Limousin, Paris-Corrèze, L'Agglomérée. Same per-event shape.
   - **Story arcs** — the dossier's editorial recommendation for narrative threads the eventual `/tour-history` page could organise around (chronological, geographic, rider-centric, race-history-centric, etc.). 2-4 candidate arcs with brief rationale; decision deferred to design phase.
   - **Hero-image candidates** — 3-6 candidate images with licence + attribution + URL, suitable for a feature-route hero. Decision deferred to design phase.
   - **Sources** — every URL the dossier draws on, in one consolidated list (the dossier is the source-of-record for the eventual page's Sources surface).
   - **Carryforwards out of scope** — anything the research surfaces that belongs in `data/historical-tdf.json` as a data-add (file follow-up issues for these), or in a future segment's content draft.
3. **Open a PR** when the dossier is ready. PR body: short summary of what's in the dossier + which arcs the research recommends + links to follow-up issues filed.

## 6. Verification commands

These exist in this repo and should run clean before PR:

- `npm test` — must pass.
- `python3 scripts/validate_entries.py` — defensive (no entry frontmatter touched).
- `npm run build` — defensive.

If the dossier needs a new directory under `content/research/`, confirm `.gitignore` posture: if `content/research/` is gitignored, the dossier still ships in the PR by adding an exception or by moving to `docs/research/` (precedent set by Strand D's seg 11-13 dossier — match whichever location it landed at).

URL fidelity: every URL cited in the dossier should resolve at write time. Use `curl -sI <url>` for fast spot-checks on suspicious links; not every URL needs a full fetch.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `content/research/tour-history-research.md` (or `docs/research/...` if .gitignore forces it; match Strand D's location convention).
- **What this strand reads:**
  - `data/historical-tdf.json` (the starting corpus)
  - `data/segments.json`, `data/town-coords.json` (for segment-keying verification)
  - CLAUDE.md "References: Cycling History Along the Route" + "References: Creative Commons Image Sources"
  - External research sources (Wikipedia, ASO, Tour archives, Wikimedia Commons, etc.)
- **What this strand must NOT touch:**
  - `data/historical-tdf.json` — additions go through follow-up issues + later strand work, not inline.
  - `content/entries/*.md` — published entries are fixed per `feedback_content_change_rule.md`.
  - `data/segments.json`, `data/attractions.json`, etc. — out of scope.
  - CLAUDE.md — narrative project context belongs to other strands (deprecation #491 owns the "Known Waypoints" tables, but the "References" sections stay; do not edit them).
- **Cross-strand collisions:**
  - **CLAUDE.md deprecation strand (#491)** runs concurrently in v1.4.19 and only edits CLAUDE.md "Known Waypoints and Climbs" subsection — does NOT touch the "References: Cycling History Along the Route" section that this strand reads. No collision.
  - **#478 segs 14-16 verification strand** will be adding the 1987 Chaumeil men's + women's TdF entries to `data/historical-tdf.json` keyed to seg 15. Coordination: this dossier should reference 1987 Chaumeil as upcoming-data (cite #478's eventual landing), not insert it.
  - **#503 historical-tdf.json segments-27 fix** is a v1.4.19 sibling — flag the bug in the dossier; do not fix the JSON inline; reference #503's eventual resolution.
  - **Strand D content research (km 70-92)** completed in v1.4.18; check whether Strand D's dossier surfaces any Tour-history items relevant here — cross-link if so.

## 8. Scope discipline

- **No inline edits to `data/historical-tdf.json`.** Every new entry the research finds → file a follow-up issue; the data-add is a separate strand.
- **No prose drafting for the eventual `/tour-history` page.** The dossier is research, not draft. Story arcs are recommendations; final narrative is design-phase + draft-phase work.
- **No retroactive edits to published per-segment HistoricalContext content** (`feedback_content_change_rule.md`). If the research surfaces something that should have been in seg 1 / 2 / 10's HistoricalContext, capture it in the dossier as carryforward; the eventual `/tour-history` page can include it.
- **AskUserQuestion at material disagreements** — likely candidates:
  - Story-arc recommendation: which arc would the publisher rather see drafted?
  - Hero-image candidate: which to feature?
  - Coverage scope: should the dossier include adjacent-but-not-corridor history (Massif Central terrain, Pyrenees-as-foil, etc.) or stay strict-corridor-only?

## 9. Memories that apply

- `feedback_source_of_truth_framing.md` — dossier is hand-curated; do not let it become a parallel source-of-truth for the canonical data
- `feedback_on_route_checks.md` — verify segment keying against polylines, not CLAUDE.md tabular data
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_issues_describe_problems.md` — follow-up issues describe data-gaps as problems, not solutions
- `feedback_content_change_rule.md` — published entries are fixed
- `feedback_sources_section.md` — dossier sources section is the seed for the eventual page's Sources surface
- `feedback_literary_footnotes.md` — if the eventual `/tour-history` page draws on literary references, capture bibliographic context here
- `reference_european_video_embeds.md` — INA / France Télévisions cookie-banner caveat
- `reference_wikimedia_thumb_widths.md` — image-URL gotcha

## 10. Stop when

- Dossier file exists at the target path with all sections populated.
- Sources section is complete (every factual claim in the dossier traces to a URL or named source).
- Carryforwards-out-of-scope section names every data-add follow-up issue filed.
- Story-arc recommendations and hero-image candidates documented for the design phase.
- PR open and tagged on milestone v1.4.20, referencing #502 (does not close it).
- Follow-up issues filed for each `data/historical-tdf.json` data-add the research uncovered.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-tour-history` once the PR has merged.
- Final report posted to publisher: PR link, dossier path, story-arc recommendation count, hero-image candidate count, follow-up issues filed (count + numbers), any open questions surfaced for the design-phase planning conversation.
