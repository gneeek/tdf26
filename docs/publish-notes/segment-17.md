# Segment 17 publish-day notes (publishes Sun 2026-05-31)

Read this during the Sunday final review + rider-distances pass for **The Closing of the Land**. Image long-list added in PR (feature/seg-17-images); these notes explain what to pick and what to fix before `draft: false`.

## Before publish (action items)

- [ ] **Prune the gallery.** 17 images are a *long-list*, not a final gallery. Pick a subset (suggest 3-5). My picks are flagged `recommended: true` and prefixed `[RECOMMENDED]` in their `alt`.
- [ ] **Strip the `[RECOMMENDED]` prefixes** from the `alt` of any image you keep. They are review aids, not publishable caption text. (Also drop the `recommended: true` flag, or leave it; the template ignores it.)
- [ ] **Flip `draft: false`** at publish time (publish.sh / your call), not before.
- [ ] **Rider distances** for the week entered before the stats snapshot runs.
- [ ] **Open question carried from the draft PR (#626):** the disclosure footer says **Claude Opus 4.8** (prior entries said 4.7). Factual (this entry was written on 4.8), but flag if you want consistency with the back-catalogue.

## The three recommended picks

1. **`Le temple protestant de Madranges.jpg`** (Avocat jean, CC BY-SA 4.0) — banner. The lead small-history beat; it *is* the temple the entry opens its history on.
2. **`Madranges, l'église catholique Saint Barthélémy.jpg`** (Avocat jean, CC BY-SA 4.0) — pairs with the temple for the "two faiths, two buildings" beat. Same photographer, so a temple+church diptych is tonally consistent.
3. **`Douglas des farges 1.jpg`** (Amalo, CC BY-SA 3.0) — the conifer/afforestation spine (Douglas fir, the species the entry names).

## Caption-honesty caveats (important)

- **Only the Madranges village images are genuinely on/at the segment**: the temple, the church (both names), `Madranges Monument` (war memorial), `Madranges Puits 1/2` (wells), and `Ruisseau de Boulou` (the stream the entry names). Caption these as Madranges.
- **The Douglas + lande images are elsewhere on the Plateau, not the seg-17 roadside.** Caption them as *illustrative of the plateau landscape*, never as "the road above Madranges" (per `feedback_on_route_checks.md` / `feedback_pre_publish_scrutiny.md`).
- **`Douglas des farges` is a historic c.1850 stand** (forêt domaniale at Les Farges), not the post-war FFN mass-planting the entry's `[^ffn]` footnote describes. It illustrates the *species*, not the *programme*. Keep the caption to "a Douglas-fir stand on the Plateau," not a date claim that would contradict the footnote.
- **The `Bruyère` / `Entre Peret Bel air … La Naucodie` lande shots risk duplicating seg 16's banner** (seg 16 already used a heather image, and its PR deliberately swapped to avoid repeating seg 15). If you use one, keep it out of the lead, or drop it.

## Technical / rights

- All 17 are **CC BY-SA** (4.0 or 3.0); attribution is wired in frontmatter (author, license, licenseUrl, sourceUrl). René Hourdry has a Commons user page (linked); the redlink authors (Avocat jean, Amalo, Fc42, Noeljupiter) are plain-text by name (no user page to link).
- `src` uses **1280px thumbnails**. All originals are wider than 1280, so the `/Npx-/` thumb-width gotcha (`reference_wikimedia_thumb_widths`, HTTP 400 when N == original width) does **not** apply here.
- Madranges is photo-poor on Commons (its category holds 6 files); the temple/church photos were found by title search, not the geosearch. The `suggest_images.py` geosearch for this segment is dominated by **Treignac** — that is **seg 18's** subject, deliberately excluded here.
