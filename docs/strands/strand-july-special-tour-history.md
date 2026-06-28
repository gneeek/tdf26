# July-2 Tour-history special (#502) — design note

> Design-phase record for the standalone Tour-de-France-history essay that publishes 2026-07-02, between seg 26 (07-01) and seg 27 (07-03). Research is complete (`content/research/tour-history-research.md`); this note captures the design decisions that feed the draft. Written 2026-06-16 in a session parallel to the seg-21 draft.

## Status of decisions

| Decision | State | Value |
|---|---|---|
| Arc spine | LOCKED (publisher, 2026-06-16) | "Poulidor country" — figure-led, elegiac, understated |
| Hero image | LOCKED (publisher, 2026-06-16) | Candidate 5 — Raymond Poulidor portrait |
| Voice register | LOCKED (publisher, 2026-06-16) | tls-essay (scholarly/profile sub-mode, first person sparing) |
| Seg-27 division of labour | LOCKED (publisher, 2026-06-16) | Special owns Ussel cycling history; seg 27 owns place + arrival |
| Seg-16 empty `User:` links | LOCKED (publisher, 2026-06-16) | Leave — forward-only convention covers it; no retroactive sweep |

## Arc spine — "Poulidor country" (LOCKED)

Figure-led and tonally honest; least triumphal of the candidates. Beat structure:

1. **OPEN** — the Corrèze never made a champion; its figureheads (Poulidor, Leblanc) are from next door. [cycling-parish register, dossier arc 4]
2. **ANCHOR** — Raymond Poulidor: 14 Tour starts, three times second, five times third, never a day in yellow ("L'Éternel Second"); won the Bol d'Or des Monédières at Chaumeil in 1963, 1966, 1967 — on the actual 2026 Stage 9 road. [dossier arc 1]
3. **ARC** — a place that loves cycling without ever winning it. The Bol d'Or (1952–2002) as connective tissue: Robic, Coppi, Géminiani, Hinault, Fignon, Brun all rode the Chaumeil circuit. The corridor as consumer of the sport's glamour, not producer of champions.
4. **CLOSE** — Ussel-2026: the parish finally gets its day. Ussel has never hosted a Tour de France stage (two independent ledicodutour sources); the 2026 Stage 9 finish on Avenue Thiers / Place Voltaire is genuinely its first. Land on an image, not a triumphal summary — sentimentality risk is highest here.

Supporting material to weave, not foreground: De Carvalho (Ussel-born, four Tour finishes outside the top 45) and Mazeaud as the entire Corrèze pro roster; the 2009 Tour du Limousin Limoges→Ussel as the same-finish-line precedent at smaller scale; the L'Agglomérée amateurs (the road's actual stewards) as a possible one-line sidebar.

## Voice — tls-essay recommended

The elegiac, understated brief wants restraint-as-discipline, which is tls-essay's governing principle; the figure-led framing reads as the variant's licensed *profile* sub-mode (so the "no figures-as-characters" rule relaxes legitimately); the one-lyrical-sentence ration and the no-sentimentality self-check directly guard the Ussel close. Scholarly/profile sub-mode, first person sparing — Poulidor is the lens, not the narrator's autobiography. madrid-review was considered and set aside: warmer and more first-person than restrained elegy wants, and its Madrid/Iberian-sited bilingual machinery is a poor fit for a French Corrèze subject. Continuity note: segs 20–21 are also tls-essay, but this is a standalone feature in the profile sub-mode, distinct from the place-essay segments.

## Hero — Candidate 5 (Poulidor portrait) recommended

The figure-led arc flips the hero from the Chaumeil landscape to the named anchor. Candidate 5: `File:Raymond_Poulidor_-_IMG_1906_(cropped)_(cropped).JPG`, Poudou99 / CC BY-SA 3.0, 3 April 2012 (Brive signing). The dossier flags this as the best fit "if the page leads on arc 4 with Poulidor as the named anchor figure" — exactly the chosen arc. Landscape alternative held in reserve: Candidate 1 (`Le sud des Monédières vers Chaumeil`, Babsy, CC BY-SA 3.0) as a contextual inline figure at the Bol d'Or beat.

## Seg-27 division of labour (confirm)

Per segs-23-27 dossier open-question #2: the July special OWNS Ussel's cycling history (never-a-TdF-town, Paris-Corrèze, 2009 Limoges→Ussel, GP d'Ussel); seg 27 OWNS the place and the arrival (Ventadour, Roman eagle, Chirac's first seat, finish geography, *uxello-* etymology) and points here, using only the single place-specific 2003-Paris-Corrèze-on-Avenue-Thiers fact inline. Confirm so neither surface duplicates the strongest fact in the corpus.

## Mechanics

- ~800–1200 words; publishDate 2026-07-02; standard conventions (no em dashes, no exclamations, numbers spelled out, cited footnotes + external-only `## Sources`, disclosure footer naming the chosen register).
- File/route shape (non-numbered special entry vs. dedicated `/tour-history` page) deferred to draft phase. The 2026-05-07 scoping favoured a `/tour-history` route + homepage card; NEXT.md simplified to "standalone July-2 essay entry." Decide at draft.
- Data-layer note (not blocking): `data/historical-tdf.json` keys Paris-Corrèze to [25,26,27]; the dossier recommends re-key to [15] (#503). Tracked under #503/#527; the essay should not assume the current keying.
- Source of truth: `content/research/tour-history-research.md` (story-arcs §, hero-candidates §, per-event corpus). Verify facts against the dossier, not this note.

## Issues filed alongside this design work (2026-06-16)

- #674 — data/attractions.json "Stele des Maquisards" misattributed (seg 21 / Bugeat).
- #675 — CLAUDE.md §3 rider-stats spec drift (capping model + startDate).
- Seg-16 empty Commons author link: not filed; awaiting publisher call on retroactive sweep vs. forward-only convention.
