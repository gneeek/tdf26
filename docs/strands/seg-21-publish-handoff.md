# Continuation handoff — seg 21 draft + catch-up publish (segs 20-21)

> TRANSIENT working note. Written 2026-06-15 to hand a long session's state to a fresh one. Delete once seg 21 is drafted and both segments are published.

## Where things are
- Branch: `seg-20-21-publish-prep` (off main). Dev server runs at http://localhost:3000 (background `nuxt dev`; restart if down).
- **Seg 20 ("The Empty Highland") is DONE**: full madrid-review draft + hero and contextual inline figures + bottom gallery + the PNR landscape-history video (`RO4GWK_uZw0`, embed carries `cc_load_policy=1&cc_lang_pref=en&hl=en`). Committed in this checkpoint. Still `draft: true`.
- **Seg 21 ("Toward Mont Bessou") is a STUB** (`*Content coming soon.*`) with `dataCutoff: 2026-06-13` pre-set. Needs drafting.
- Rider data: `data/riders/daily-log.json` (gitignored) loaded through **Jun 13** (74 entries); `stats.json` regenerated asOf Jun 13. Original cutoffs kept: seg 20 = Jun 9, seg 21 = Jun 13. PublishDates unchanged (Jun 10 / Jun 14).

## Seg 21 — decisions already made
- **Voice: tls-essay** (essay variant). Load per `/home/jhs/code/skills/simpson-registers/tls/SKILL.md` then `variants/essay.md` + `samples/essay/`. Restraint is the discipline; right for the WWII material.
- **Subject:** Bugeat, the granite / railway / altitude town, with the **6 April 1944 Resistance wound** as the emotional set-piece. Tone sober and memorial.
- **Workflow:** research then discuss then draft. Bring a structure plus editorial calls to the publisher BEFORE drafting (same loop as seg 20).

## Research / source of truth
`content/research/segs-20-22-block-research.md` — read the **Segment 21** section, **open question #10** (anchor allocation), and **data reconciliations #1/#2**: the on-route Bugeat memorial is the *stèle des fusillés de L'Échameil* (pont de Vezou, 1947), NOT the "Stèle des Maquisards / Mont Gargan" (off-corridor); attractions.json is misattributed. Verify content facts against the dossier, not this note. Reserve Mont Bessou (seg 22) and Meymac / Vézère source (segs 23-24).

## Conventions (same as seg 20)
800-1200 words; no em dashes; no exclamations; numbers spelled out; cited footnotes plus `## Sources` (external URLs only); disclosure footer `*Pair-written by Justin Simpson and Claude Opus 4.8. Voice register: tls-essay.*`; images via `::inline-figure` (hero after H1) plus frontmatter `images:` gallery; video via `::video-embed`. Author links: use `Special:Contributions/<user>` (Commons user pages often 404).

## PUBLISH GOTCHA — read before snapshotting
`rider_stats.py` sums EVERY logged day and ignores `--reference-date` for the totals. The daily-log already holds all 7 days (through Jun 13). So:
- An honest **snapshot-20 (Jun 9 cutoff)** must be generated from a log **truncated to Jun 9**, THEN the full log restored for **snapshot-21 (Jun 13)**.
- Publishing seg 20 against the full log would bake Jun 10-13 into its standings. Order: truncate, snapshot 20, restore, snapshot 21.

## Publish (catch-up, content-first)
1. Draft seg 21, pick images, commit content+images (seg 20 already committed).
2. `publish.sh` per segment, honoring the pre-set dataCutoffs. Mind the snapshot gotcha above. Track `snapshot-20` / `snapshot-21` after.
3. Keep publishDates Jun 10 / Jun 14. Resume normal cadence with seg 22 on Jun 17.

## Open flags (carry, do not silently drop)
- Seg 16 (published) uses a dead `User:Avocat_jean` author link: pre-existing attribution-link bug; publisher to decide file-issue vs sweep.
- CLAUDE.md section 3b still describes the old `min(actual, 2)` rider model; real code is rolling carry-over. Doc drift, offered for next-planning notes.
- attractions.json "Stele des Maquisards" misattribution (dossier recon #1/#2): file an issue (problem-only title, `Refs` not `Closes`).
