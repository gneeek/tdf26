---
title: Tour-history feature research dossier
strand: docs/strands/strand-tour-history-research.md
issue: 502
status: research-collection-complete-awaiting-synthesis
session: 1 of 2 (planned)
---

# Tour-history feature research dossier

Research dossier for the `/tour-history` feature page (umbrella issue #502). This dossier feeds the design-discussion phase (next planning session: layout, hero image, story arc, prominent-launch timing) and the subsequent draft phase (a sister strand that builds the `/tour-history` route page).

## Progress

- **Session 1 (this commit)**: research collection complete. Five parallel general-purpose subagents executed against the brief's topic list; their structured findings are dropped verbatim below under section headings A–E, each marked `<!-- STATUS: raw notes from subagent X, awaiting synthesis -->`. The dossier is **NOT** synthesized yet; Session 2 owns synthesis, story-arc recommendation prose, hero-image candidate curation, follow-up-issue filing, and PR.
- **Session 2 (planned)**: synthesis. Cross-check segment keying for each event against `data/segments.json` polyline geometry per `feedback_on_route_checks.md` — the raw notes use approximate keying based on town/km. Consolidate per-event sections, write story-arc recommendations, curate hero-image shortlist, write consolidated Sources, file follow-up issues (especially the #503 keying fix recommendation in section C), open PR on milestone v1.4.20.
- **URL spot-check status**: subagents reported real, resolvable URLs. Curated batch of high-leverage URLs spot-checked at end of Session 1; results recorded in §URL spot-check below. Full URL census deferred to Session 2.
- **Coverage scope decision deferred**: per planning-session call, both strict-corridor and adjacent-region findings are captured; adjacent items are tagged "optional context (design-phase decision)" by their source subagent. The publisher decides at the design-phase planning conversation.

## Section A — Corridor Tour de France stages

<!-- STATUS: raw notes from subagent A, awaiting synthesis. Segment keying is approximate (by town); Session 2 must verify against polylines. -->

### A. Confirmed corpus coverage (already in `data/historical-tdf.json`)
- 1951 Stage 11: Brive → Agen (Koblet 135 km solo)
- 1976 Stage 20: Tulle → Puy-de-Dôme (Zoetemelk wins, Van Impe in yellow)
- 1996 Stage 14: Besse-en-Chandesse → Tulle (Abdoujaparov, Bastille Day, Riis)
- 1996 Stage 15: Brive-la-Gaillarde → Villeneuve-sur-Lot (Podenzana)
- 2012 Stage 18: Blagnac → Brive (Cavendish in rainbow, Wiggins yellow)
- 2024 Stage 11: Évaux-les-Bains → Le Lioran
- 2026 Stage 10: Aurillac → Le Lioran (day-after-Stage-9)
- (filed under sister strand #478 / off-limits): 1987 Chaumeil men's & women's stages

### A. New corridor TdF events found (men's)

**1951 — Stage 10: Clermont-Ferrand → Brive**
- Corridor connection: Brive finish (segs 1-2). Pairs with Stage 11 Brive → Agen (Koblet) — they're a day-pair, this is the "arrival" half already absent from corpus.
- Adjacent context only: no
- Bernardo Ruiz (Spain) won the stage; Roger Lévêque held yellow. The only year Brive hosted both a finish and a start in successive days; this is the day Koblet drank Champagne the night before launching his solo from Brive.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf1951.html
- Photo candidates: very limited — Wikimedia has Category:Hugo Koblet (CC BY-SA when present); period press photos likely still in copyright unless via Dutch Nationaal Archief (some CC0).
- Video candidates: none surfaced for 1951 stage 10 specifically.
- Race-radio / commentary: none surfaced; pre-radio era for English-language coverage.

**1964 — Stage 19: Bordeaux → Brive (and Stage 20: Brive → Puy-de-Dôme)**
- Corridor connection: Brive finish + start (segs 1-2)
- Adjacent context only: no
- Stage 19 won by Edouard Sels (Belgium); Anquetil in yellow. Stage 20 won by Julio Jiménez (climber); Anquetil held yellow into Puy-de-Dôme — this is the Tour where the famous Anquetil-Poulidor shoulder-to-shoulder duel happened on Puy-de-Dôme the same day, departing Brive that morning. Significant narrative anchor: Brive was the stage town that launched one of the most-photographed moments in Tour history.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf1964.html
- Photo candidates: Wikimedia Category:Jacques Anquetil, Category:Raymond Poulidor — Puy-de-Dôme 1964 duel is one of the most reproduced cycling photos but the canonical image is by Presse Sports (not free); look for Dutch Nationaal Archief CC0 alternates.
- Video: INA archive hosts the 1964 Puy-de-Dôme duel footage — flag GDPR-iframe issue per project memory; YouTube re-uploads exist but check rights.

**1969 — Stage 19: Libourne → Brive (and Stage 20: Brive → Puy-de-Dôme)**
- Corridor connection: Brive finish + start (segs 1-2)
- Adjacent context only: no
- Stage 19: Barry Hoban (GB) won; Merckx in yellow. Stage 20: Pierre Matignon (France) won — Matignon was lanterne rouge, attacked from a small group and held off the field for an emotional French win on Puy-de-Dôme; one of the most romantic underdog wins in Tour history. Brive was the launch pad.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf1969.html
- Photo candidates: Wikimedia Category:Eddy Merckx 1969 (CC BY-SA where present); Category:Barry Hoban (limited).
- Video: ASO/INA archive only; nothing CC surfaced.

**1973 — Stage 17: Sainte-Foy-la-Grande → Brive-la-Gaillarde (and Stage 18: Brive → Puy-de-Dôme)**
- Corridor connection: Brive finish + start (segs 1-2)
- Adjacent context only: no
- Stage 17 won by Claude Tollet (France); Ocaña in yellow. Stage 18: Ocaña won the next morning's stage himself out of Brive en route to overall victory — Ocaña dominating the Massif Central transition stages in his only Tour win.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf1973.html
- Photo candidates: Wikimedia Category:Luis Ocaña (limited CC; some Dutch Nationaal Archief images CC0).
- Video: none CC surfaced.

**1976 — Stage 19: Sainte-Foy-la-Grande → Tulle** (Tulle hosted TWO finishes in 1976, not just the start of stage 20)
- Corridor connection: Tulle finish (seg 10)
- Adjacent context only: no
- Hubert Mathis (France) won by 7 seconds from a 9-man breakaway (Paolini 2nd); Van Impe in yellow. 1975 winner Bernard Thévenet abandoned during this stage. Tulle hosted back-to-back days: arrival on stage 19, departure on stage 20 to Puy-de-Dôme. The stage-19 arrival is missing from corpus and is the "Tulle as finish" answer to the verification question.
- Sources: https://www.ledicodutour.com/villes_etapes/villes_t/tulle.htm ; https://www.bikeraceinfo.com/tdf/tdf1976.html ; http://www.memoire-du-cyclisme.eu/eta_tdf_1970_1979/tdf1976_19.php ; https://en.wikipedia.org/wiki/1976_Tour_de_France
- Photo candidates: Wikimedia Category:Hubert Mathis (very limited); Category:Lucien Van Impe yellow jersey.
- Video: none surfaced.

**1987 — Stage 12: Brive-la-Gaillarde → Bordeaux, 228 km**
- Corridor connection: Brive start (segs 1-2). Note: Strand I owns 1987 Chaumeil; this is a different 1987 stage and is in scope.
- Adjacent context only: no
- Davis Phinney (USA, 7-Eleven) won the sprint — significant: rare US sprint win in the 80s; Martial Gayant in yellow. The previous stage was the famous Chaumeil stage finish (Strand I), so this is the morning-after departure — narrative pair with Strand I's content.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf1987.html
- Photo candidates: Wikimedia Category:Davis Phinney (limited).
- Video: none surfaced CC.

**1998 — Stage 6: La Châtre → Brive-la-Gaillarde, 204.5 km** and **Stage 7 ITT: Meyrignac-l'Église → Corrèze, 58 km** and **Stage 8: Brive → Montauban, 190.5 km**
- Corridor connection: TRIPLE corridor day. Stage 6 Brive arrival (segs 1-2); stage 7 was an ITT entirely WITHIN Corrèze department, Meyrignac-l'Église to the town of Corrèze (~12 km NE of Tulle, on the seg-12/13 corridor); stage 8 Brive departure.
- Adjacent context only: no
- Stage 6: Mario Cipollini (Italy) sprint win, his second consecutive stage win; Stuart O'Grady in yellow. Stage 7 ITT: Jan Ullrich won (1h15:25) and took yellow — this is the morning the Festina doping scandal broke; Festina was expelled before the stage start. Stage 8: Jacky Durand (France) won; Laurent Desbiens in yellow. The 1998 Tour spent ~3 days entirely in/around the Stage-9-2026 corridor.
- Sources: https://www.bikeraceinfo.com/tdf/tdf1998.html ; https://en.wikipedia.org/wiki/1998_Tour_de_France,_Prologue_to_Stage_11 ; https://www.procyclingstats.com/race/tour-de-france/1998/stage-7
- Photo candidates: Wikimedia Category:1998 Tour de France (limited); Category:Jan Ullrich (CC BY-SA in places); Category:Mario Cipollini.
- Video: search "Festina 1998" YouTube — multiple uploads, copyright varies.

**2001 — Stage 16: Castelsarrasin → Sarran (Corrèze), 227.5 km** and **Stage 17: Brive → Montluçon, 194 km**
- Corridor connection: Sarran finish (~25 km NE of Tulle, ~10 km from Chaumeil seg 15) + Brive start (segs 1-2). Pair of consecutive corridor days.
- Adjacent context only: no
- Stage 16: Jens Voigt (Germany) took his first Tour stage win at Sarran from a breakaway with Nicki Sørensen; Lance Armstrong in yellow (later annulled). Sarran was selected because Jacques Chirac, who was President at the time, has his country residence at Château de Bity in Sarran — this was a presidential-courtesy stage town. Stage 17: Serge Baguet (Belgium) won.
- Sources: https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html ; https://www.bikeraceinfo.com/tdf/tdf2001.html ; https://www.procyclingstats.com/race/tour-de-france/2001/stage-16/
- Photo candidates: Wikimedia Category:Jens Voigt (CC BY-SA available); Category:Sarran.
- Video: YouTube has the stage 16 highlights upload (linked in search). Embeddable: yes via YouTube.

**2016 — Stage 5: Limoges → Le Lioran, 216 km**
- Corridor connection: Limoges start (~80 km NW of Brive — adjacent context, the route went south-east through the Massif Central paralleling the Corrèze northern edge). Verified by ledicodutour Corrèze department page that this is a tracked corridor stage.
- Adjacent context only: yes (skirts the corridor north of the Stage-9-2026 line)
- Greg Van Avermaet (BMC) attacked from break, soloed in for stage win and yellow jersey; held it for several days before losing it to Sagan. One of the iconic mid-2010s breakaway moments. Final climbs: Pas de Peyrol (Puy Mary), Col de Néronne — Cantal terrain immediately south of corridor.
- Sources: https://en.wikipedia.org/wiki/2016_Tour_de_France ; https://www.cyclingstage.com/tour-de-france-2016-route/stage-5-tdf-2016/
- Photo candidates: Wikimedia Category:Greg Van Avermaet (CC BY-SA); Category:2016 Tour de France stage 5.
- Video: ASO Dailymotion archive likely has stage highlights; YouTube has multiple re-uploads (rights vary).

**2020 — Stage 12: Chauvigny → Sarran (Corrèze), 218 km**
- Corridor connection: Sarran finish (~25 km from Tulle, edge of corridor). Stage explicitly named "Sarran Corrèze" by ASO.
- Adjacent context only: no
- Marc Hirschi (Switzerland, Sunweb) soloed to his first pro win after attacking late on the Suc au May approach side; Pierre Rolland 2nd, Søren Kragh Andersen 3rd; Roglič in yellow. Hirschi's breakthrough; first Swiss stage win since Cancellara. Notable: this stage actually crossed parts of the 2026 Stage 9 route — Suc au May is referenced in stage previews for its similar profile.
- Sources: https://www.procyclingstats.com/race/tour-de-france/2020/stage-12 ; https://bikeraceinfo.com/tdf/2020-TDF-daily/tdf2020-stage-12.html ; https://www.cyclingnews.com/races/tour-de-france-2020/stage-12/results/
- Photo candidates: Wikimedia Category:Marc Hirschi (CC BY-SA); Category:2020 Tour de France.
- Video: https://www.dailymotion.com/video/x7zl61i (ASO/Dailymotion), embeddable: yes/likely; https://www.youtube.com/watch?v=WAcJxi8tEdA (last km), embeddable: yes.
- Race-radio / commentary: none surfaced free; ASO archive only.

**2023 — Stage 8: Libourne → Limoges, 200.7 km** and **Stage 9: Saint-Léonard-de-Noblat → Puy de Dôme, 182.4 km**
- Corridor connection: Stage 8 Limoges finish (adjacent context — finish ~80 km NW of Brive); stage 9 Saint-Léonard-de-Noblat start (~70 km NW of Brive, also Limousin-adjacent). The route did NOT pass through the 2026 Stage 9 corridor proper but is the most recent men's TdF crossing of the broader Limousin region.
- Adjacent context only: yes
- Stage 8: Mads Pedersen sprint win, Vingegaard in yellow. Stage 9: Michael Woods (Canada, Israel-Premier Tech) caught Matteo Jorgenson on the Puy de Dôme summit ascent; first Puy-de-Dôme finish since 1988. Major narrative anchor for Massif Central return.
- Sources: https://www.cyclingstage.com/tour-de-france-2023-route/stage-8-tdf-2023/ ; https://www.procyclingstats.com/race/tour-de-france/2023/stage-8
- Photo candidates: Wikimedia Category:Michael Woods cyclist; Category:Mads Pedersen.
- Video: ASO Dailymotion archive; YouTube highlights.

**2025 — Stage 10: Ennezat → Le Mont-Dore Puy de Sancy, 163 km**
- Corridor connection: Adjacent context only — Auvergne-side Massif Central; ~110 km east of Ussel. The route did not enter Corrèze department.
- Adjacent context only: yes
- Simon Yates won (Visma) on Bastille Day — most cat-2 climbs (seven) ever in a single TdF stage; Ben Healy took yellow with bold ride, becoming first Irish leader since Stephen Roche; Pogačar nearly cracked Vingegaard. Massif Central narrative anchor for 2025 (the year's most decisive Massif Central day, equivalent in role to what Stage 9-2026 will be).
- Sources: https://www.procyclingstats.com/race/tour-de-france/2025/stage-10/result/ ; https://lanternerouge.com/2025/07/14/pogacar-nearly-drops-vingegaard-before-the-big-mountains-tour-de-france-2025-stage-10/ ; https://www.auvergnevolcansancy.com/en/tour-de-france-2025-ennezat-le-mont-dore-puy-de-sancy/
- Photo candidates: Wikimedia Category:2025 Tour de France (likely populated with CC BY-SA images already).
- Video: ASO Dailymotion + multiple YouTube uploads of Healy yellow celebration.

### A. New corridor TdF Femmes events found

**2023 Femmes — Stage 2: Clermont-Ferrand → Mauriac, 151.7 km**
- Corridor connection: Route passed through Bort-les-Orgues (Corrèze, ~30 km NE of Ussel, ~25 km from Meymac) at km ~100 — confirmed corridor adjacency. Mauriac finish is in Cantal but immediately east of Corrèze border.
- Adjacent context only: borderline — the race entered Corrèze briefly via Bort-les-Orgues; otherwise Cantal terrain. Mark "borderline yes" — only TdF Femmes edition that has touched Corrèze corridor through 2025.
- Liane Lippert (Movistar) won the uphill sprint on Côte de Trébiac; Lotte Kopecky retained yellow after a six-KOM hilly day (Mont-Dore, La Stèle, Plaines, Boissières, Merlhac, Trébiac). 2023 was the first TdF Femmes Grand Départ from Clermont-Ferrand and the only one to brush the corridor.
- Sources: https://www.cyclingstage.com/tour-de-france-femmes-2023/stage-2-tdf-2023-women/ ; https://www.procyclingstats.com/race/tour-de-france-femmes/2023/stage-2
- Photo candidates: Wikimedia Category:2023 Tour de France Femmes (CC BY-SA images including stage-2 photos); Category:Liane Lippert.
- Video: ASO/Dailymotion has highlights; YouTube: search "Tour de France Femmes 2023 stage 2 highlights" — multiple embeddable uploads. Embeddable: likely yes.
- Race-radio: none surfaced free.

**2022 Femmes, 2024 Femmes, 2025 Femmes** — no corridor relevance found. 2022 was Paris→Vosges→Planche des Belles Filles (no Massif Central). 2024 went Netherlands→south-eastern France→Alpe d'Huez (no Limousin/Corrèze). 2025 went Brittany→Massif Central via Clermont-Ferrand→Ambert (Stage 6) but no Corrèze touchpoint — closest was Guéret (Creuse, Stage 5 finish), ~120 km north of corridor.

### A. 2025 Tour de France corridor check

The 2025 Tour de France men's race had **no direct corridor relevance**. Stage 10 (Ennezat → Le Mont-Dore Puy de Sancy, 163 km) is the closest, but stayed entirely in Puy-de-Dôme department on the eastern Auvergne side of the Massif Central — closest point ~110 km east of Ussel. Stage 11 onwards moved south to Pyrenees. No Corrèze, no Limousin, no Brive/Tulle/Ussel/Limoges. **The 2025 men's Tour did not enter the Stage-9-2026 corridor.**

### A. Verify-or-refute claims

- **"Ussel has never previously been a Tour stage town":** **CONFIRMED** by two independent sources: (a) ledicodutour.com Corrèze department page lists Ussel under "Eight Stage Towns" but with NO entry pre-2026 (page tracks 1947–2026); (b) ledicodutour.com main statistics page (`/statistiques/villes_etapes.html`) does not contain Ussel in the host-city statistics table at all, indicating zero pre-2026 stages. Ussel hosted the Tour du Limousin 11 times (Moncoutié 2001, Castaing 1985, Chalmel 1980) and the Grand Prix d'Ussel (Molinéris 1953, Koblet 1955) but never the Tour de France. The 2026 Stage 9 finish at Avenue Thiers / Place Voltaire is genuinely Ussel's first appearance as a Tour stage town. Source: https://www.ledicodutour.com/departements/departements_c/correze.html ; https://www.ledicodutour.com/statistiques/villes_etapes.html
- **Brive's 1969 stage was Hoban (per CLAUDE.md "Barry Hoban won a stage in Brive-La-Gaillarde in 1969"):** CONFIRMED — Stage 19 Libourne→Brive, Hoban won the sprint. Source: ledicodutour Brive page.
- **Brive's 2008 Cipollini reference (per CLAUDE.md "Mario Cipollini winning there in 2008"):** **REFUTED** — Cipollini did NOT win in Brive in 2008 (Cipollini retired in 2005). The CLAUDE.md reference appears to confuse 1998 (Cipollini won Stage 6 La Châtre→Brive) with 2008. Recommend correcting to 1998. (Note: subagent reports CLAUDE.md mentions a 2008 Cipollini Brive win — verify in CLAUDE.md whether this claim actually appears or if the subagent was confused; spot-check during synthesis.)

### A. Open questions

- ledicodutour.com has a dedicated page per stage town but the Ussel page (`/villes_etapes/villes_u/ussel.htm`) returned 404. The statistics page absence is strong evidence of no prior stages, but a dedicated source listing pre-2026 Ussel-as-stage-town would strengthen the assertion. Tried: https://www.ledicodutour.com/villes_etapes/villes_u/ussel.htm (404) — did not exhaust the URL pattern variations.
- Couldn't confirm whether 2024 Stage 11 (Évaux-les-Bains → Le Lioran) actually crossed Corrèze department — the route map suggests it stayed in Creuse/Cantal, but verification was not completed.
- 2001 Stage 16 Castelsarrasin→Sarran route detail: did the parcours actually pass through Tulle? Sarran is on the Plateau de Millevaches edge but Castelsarrasin→Sarran via Tulle would be the natural routing. Did not verify.

## Section B — Tour du Limousin

<!-- STATUS: raw notes from subagent B, awaiting synthesis. -->

### B. Tour du Limousin — race history

The Tour du Limousin was founded in 1968 as an amateur stage race for the Limousin region (the historical three-department area: Haute-Vienne, Corrèze, Creuse). It ran as an amateur race from 1968 through 1974, becoming professional in 1975. Since 2005 it has held UCI 2.1 status on the UCI Europe Tour, briefly upgraded to 2.HC for 2011–2012 before being downgraded back to 2.1 in 2013. The race has run 58 editions through 2025 and traditionally takes place over four days in mid-to-late August. The final stage has finished in Limoges every year since 1980.

The race has been rebranded twice in recent memory. In 2018 it became "Tour du Limousin-Nouvelle-Aquitaine" to reflect the 2016 administrative dissolution of the historical Limousin région into the larger Nouvelle-Aquitaine region (a name change driven by financial-partner pressure). In 2021 it was rebranded again to "Tour du Limousin-Périgord-Nouvelle-Aquitaine" to acknowledge the regular inclusion of a Dordogne (Périgord) stage on the route.

The narrative arc that matters for the corridor: Bernard Hinault, riding for Gitane in his first professional season, won in 1976 and 1977 — those back-to-back Limousin wins were the launching pad for his five Tour de France titles. Hinault has on the record described the race as formative. ICI Limousin published an interview headlined "Le Tour du Limousin, ça représente beaucoup."

Sources:
- https://en.wikipedia.org/wiki/Tour_du_Limousin
- https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine
- https://fr.wikipedia.org/wiki/Tour_du_Limousin_1976
- https://www.procyclingstats.com/race/tour-du-limousin
- https://tourdulimousin.com/
- https://www.ici.fr/emissions/ici-limousin-sport/bernard-hinault-quintuple-vainqueur-du-tour-de-france-le-tour-du-limousin-ca-represente-beaucoup-5013613

### B. Tour du Limousin — corridor stage history

**1979 — Stage 5: Tulle → Tulle (165 km, final stage)**
- Corridor connection: Tulle (km 65, seg 10), full stage circuit in Corrèze
- Source: https://www.procyclingstats.com/race/tour-du-limousin/1979/gc

**1987 — Stage 4: Tulle → Limoges (final stage)**
- Corridor connection: Tulle (km 65, seg 10) start
- Winner: Kim Andersen (Denmark). Charly Mottet won the GC.
- Source: https://www.procyclingstats.com/race/tour-du-limousin/1987/gc/result/result

**1997 — Stage 2: Le Moutier-d'Ahun → Tulle**
- Corridor connection: Tulle (km 65, seg 10) finish
- Winner: Frédéric Guesdon (France) ahead of Emmanuel Magnien and Arvis Piziks
- Source: https://www.procyclingstats.com/race/tour-du-limousin/1997/stage-2/result/result

**2009 — Stage 1: Limoges → Ussel (159.6 km)**
- Corridor connection: **Ussel (km 182, seg 27) — same finish town as 2026 TdF Stage 9**
- Winner: Borut Božič (Vacansoleil) took the opening jersey. Mathieu Perget won the GC.
- Source: https://fr.wikipedia.org/wiki/Tour_du_Limousin_2009 ; https://www.cyclingnews.com/races/42nd-tour-du-limousin-2-1/stage-1/results/

**2023 — Stage 3: Sarran → Bort-les-Orgues (195.5 km)**
- Corridor connection: Sarran is just NE of the route (~10 km from Chaumeil/seg 15); the stage crossed the eastern Corrèze plateau adjacent to segs 15–25. Romain Grégoire (Groupama-FDJ, age 20) won the stage and the GC.
- Source: https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine_2023 ; https://www.directvelo.com/actualite/99818/

**2024 — Stage 3: La Rivière de Mansac → Argentat-sur-Dordogne (Xaintrie Val'Dordogne)**
- Corridor connection: La Rivière de Mansac is in the Agglomération du Bassin de Brive, ~15 km west of Brive-la-Gaillarde (segs 1–2). Second time Mansac had hosted. Argentat sits SE of the 2026 corridor.
- Winner: Jefferson Cepeda (Caja Rural-Seguros RGA), solo from 10 km out, ahead of Orluis Aular and Clément Venturini. Alex Baudin won the GC.
- Sources: https://tourdulimousin.com/les-etapes-2024/ ; https://www.brive-tourisme.com/en/blog-en/the-tour-of-limousin/ ; https://www.procyclingstats.com/race/tour-du-limousin/2024/stage-3 ; https://www.directvelo.com/actualite/115025/tour-du-limousin-et-3-jefferson-cepeda-1er

**2025 — Stage 3: Saint-Jal → Masseret (182.7 km)**
- Corridor connection: Saint-Jal sits ~12 km north of Tulle, on the plateau between Naves (seg 12) and Chaumeil (seg 15). Masseret is just over the Haute-Vienne border.
- Winner: Paul Lapeira (Decathlon AG2R La Mondiale), summit-style finish. Ewen Costiou retained yellow and won the GC.
- Sources: https://www.cyclingnews.com/races/tour-du-limousin-perigord-nouvelle-aquitaine-2025/stage-3/results/ ; https://france3-regions.franceinfo.fr/nouvelle-aquitaine/correze/brive/tour-du-limousin-2025-suivez-en-direct-l-arrivee-de-la-troisieme-etape-en-correze-3178875.html ; https://decathlonag2rlamondialeteam.com/en/paul-lapeira-remporte-la-3e-etape-du-tour-du-limousin/

Note on Brive-la-Gaillarde proper: subagent could not confirm Brive itself as a Tour du Limousin start/finish town in any specific year. The Brive Basin agglomeration has been represented twice via La Rivière de Mansac (most recently 2024). Donzenac (just N of Brive) and Malemort have appeared as stage towns according to Brive Tourisme, but specific years not pinned.

### B. Tour du Limousin — notable winners

Tour de France GC winners and major figures who won the Tour du Limousin:
- **Bernard Hinault** (FRA, 1976, 1977) — five-time TdF winner. Only TdF GC winner in the Limousin's roll of honour. Wins came as a 21-/22-year-old neo-pro.
- **Marc Madiot** (FRA, 1981) — two-time Paris-Roubaix winner; longtime Groupama-FDJ DS.
- **Charly Mottet** (FRA, 1987, 1993) — multiple-time Critérium du Dauphiné winner, Tour podium contender (4th in 1991).
- **Andrei Tchmil** (UKR/MDA/BEL, 1995) — Monument winner (Paris-Roubaix 1994, Milan-San Remo 1999, Tour des Flandres 2000).
- **Laurent Brochard** (FRA, 1996) — 1997 World Road Race Champion.
- **Stéphane Heulot** (FRA, 1999) — held the TdF yellow jersey in 1996.
- **Pierrick Fédrigo** (FRA, 2004, 2007) — co-record holder for most Limousin wins (2). Four TdF stage wins; born in Marmande (Lot-et-Garonne, just over the regional line).
- **Sébastien Hinault** (FRA, 2008) — Bernard's nephew; long Crédit Agricole/AG2R career. Family continuity story.
- **Sonny Colbrelli** (ITA, 2015) — 2021 Paris-Roubaix winner, 2021 European RR champion.
- **Warren Barguil** (FRA, 2021) — TdF KOM jersey + 2 stage wins 2017; Brittany-born, long association with Arkéa.
- **Romain Grégoire** (FRA, 2023) — youngest GC winner in recent history at 20; tipped as a Groupama-FDJ leader.

Other multiple winners: **Patrice Halgand** (2000, 2002), **François Dubreuil** (1971, 1973). Pierrick Fédrigo and Halgand are the most-recent two-time winners; nobody has won three.

**Corrèze riders winning:** No GC winner of the Tour du Limousin has been identified as a Corrèze native in this research. (Unresolved — see open questions.)

Sources:
- https://en.wikipedia.org/wiki/Tour_du_Limousin
- https://www.procyclingstats.com/rider/pierrick-fedrigo

### B. Tour du Limousin — photo / video candidates

**Wikimedia Commons:**
- `Category:Tour du Limousin` — main category, sparse. Confirmed file: "Tour de Limousin 1984.jpg" — license appears CC. URL: https://commons.wikimedia.org/wiki/Category:Tour_du_Limousin
- Subcategories exist for editions 2009, 2010, 2011, 2012, 2014, 2016, 2017, 2020 (each contains race photos under typical CC BY-SA licenses — verify per file).
- `Category:Tour du Limousin maps` — 4 route maps 2009–2012. URL: https://commons.wikimedia.org/wiki/Category:Tour_du_Limousin_maps
- Embeddable: yes (via standard Wikimedia thumb URLs; mind the thumb-width gotcha noted in project memory).

**YouTube — race-related channels:**
- Official channel: https://www.youtube.com/user/TourDuLimousin — Tour du Limousin's own uploads (older content; activity has moved). Embeddable: yes per YouTube standard embed; redistribution per YouTube TOS, not necessarily CC.
- Older highlights playlist: https://www.youtube.com/playlist?list=PL7CF7BC2A560171BF — embeddable: yes.
- 2024-edition live channel: https://www.youtube.com/channel/UCjqlevAuEKcvkln6yABY40w — embeddable: yes (live archives).
- 2023 edition channel: https://www.youtube.com/channel/UC2JxJZhvr8R9_Rn1cCdt_8g — embeddable: yes.
- Warren Barguil 2021 winner interview: https://www.youtube.com/watch?v=jdYIrvDoHaQ — embeddable: yes.
- France 3 Nouvelle-Aquitaine 2025 stage 3 replay: https://france3-regions.franceinfo.fr/nouvelle-aquitaine/correze/brive/tour-du-limousin-2025-suivez-en-direct-l-arrivee-de-la-troisieme-etape-en-correze-3178875.html — embeddable: unknown (France Télévisions player typically shows GDPR banner per project memory `reference_european_video_embeds`; prefer not to embed inline).

**Stage-archive sources for stills/results:**
- https://www.cyclingnews.com/races/tour-du-limousin-2009/stages/ (and analogous URLs by year)
- https://www.directvelo.com/epreuve/37958/tour-du-limousin-2023
- https://www.velowire.com/article/183/en/exclusive--the-stages-of-the-tour-du-limousin-2009-in-google-maps-google-earth-and-the-participating-teams.html
- BikeRaceInfo per-edition pages (e.g., https://bikeraceinfo.com/stageraces/limousin/2025-limousin-tour.html) — domain hit ECONNREFUSED once during research; treat as flaky.

### B. Tour du Limousin — narrative hooks

1. **"The Tour de France's regional cousin."** Most years Stage 9's actual roads are quiet farm lanes and granite plateau D-roads that the world doesn't see. The Tour du Limousin is what shows them off the other 51 weeks. Hinault literally launched his career on these roads (1976, 1977) before he ever won a TdF. Frame the race as the corridor's "home circuit" and the 2026 Stage 9 as the moment its biggest cousin finally drops by.

2. **"Ussel has seen this finish before."** In 2009 the Tour du Limousin opened with Limoges → Ussel, 159.6 km. Borut Božič (Vacansoleil), an obscure Slovenian sprinter, took the opening jersey. Seventeen years later the same finish town hosts the 2026 TdF Stage 9. Use the 2009 finish as the "previous reading" of the script — different scale, same town, same long approach from the west.

3. **"What 'home' looks like on the palmarès."** Sébastien Hinault winning in 2008 — Bernard's nephew, on the same race his uncle launched a career on. Pierrick Fédrigo (Marmande, just over the line) winning twice. Romain Grégoire winning at 20 in 2023. The race as a place where French regional cycling reproduces itself, in contrast to the TdF's globalised pageant.

### B. Open questions

- **Brive-la-Gaillarde proper as ville-étape**: The Agglomération du Bassin de Brive has hosted via La Rivière de Mansac (2009, 2024) and Donzenac/Malemort are referenced in passing, but Brive *itself* hosting a start or finish was not confirmed. Worth a direct check of the official archives at https://tourdulimousin.com/parcours/ or a list at the Brive Tourisme site.
- **Corrèze native winners**: Nothing in the 1968–2025 list of GC winners surfaced as Corrèze-born during this research. Worth a targeted check on Charly Mottet's birthplace (he is from Drôme, ruling him out) and the early-1970s amateur-era winners.
- **Tulle hosting in the 1970s/early 1980s**: The 1979 Tulle–Tulle stage suggests the départemental capital was a regular fixture in the early years. Full archive reconstruction would need a year-by-year sweep of ProCyclingStats stage URLs (`/race/tour-du-limousin/<year>/`).
- **License flag for Wikimedia Commons race photos**: subagent confirmed the categories exist but did not click through to verify per-file license metadata. Standard practice (assume CC BY-SA, verify before publish) applies.
- **2026 edition route**: Announced as 18–21 August 2026 on the official Facebook; full parcours not yet published as of this research. Worth re-checking closer to the publish date in case the 2026 Limousin parcours overlaps the Stage 9 corridor and creates a same-year tie-in.

## Section C — Paris-Corrèze + L'Agglomérée

<!-- STATUS: raw notes from subagent C, awaiting synthesis. CONTAINS A KEY RECOMMENDATION FOR ISSUE #503 (Paris-Corrèze segment keying) — see C/Paris-Corrèze section below. -->

### C. Paris-Corrèze — race overview

Paris-Corrèze was a French professional stage race that ran annually from 2001 to 2012, created by 1983/1984 Tour de France winner Laurent Fignon together with Corrézien motorsport champion Max Mamers, with backing from the Conseil général de la Corrèze. The race held UCI category 2.4 in 2001, was promoted to 2.3 in 2002, and ran as UCI Europe Tour 2.1 from 2005 onwards. Its inaugural edition was held in late September 2001; from 2005 it moved to early August and was reduced from three stages to two.

Geographically it was a Parisian-basin-to-Massif-Central rouleur's race: the early stages started in the Loir-et-Cher / Indre / Cher (Contres, Saint-Amand-Montrond, Ormes, Vigeois as departure or transition towns), and the race always concluded in Corrèze. From the 2005 edition onward, the final stage closed with five laps of the historic **Bol d'Or des Monédières circuit at Chaumeil** — explicitly preserving the legacy of the post-Tour criterium (1952–2002) that Robic, Coppi, Anquetil, Hinault, Fignon, and Virenque had ridden. This made Chaumeil (segment 15 in our scheme) the spiritual home of the race, not Ussel.

The race did not run in 2013 due to insufficient budget and has not been organised since. Twelve editions were completed, with winners including Thor Hushovd (2001), Baden Cooke (2002), Cédric Vasseur (2003), Philippe Gilbert (2004), Frédéric Finot (2005), Didier Rous (2006), Edvald Boasson Hagen (2007 — won both stages and the GC at age 20), Lloyd Mondory taking a stage in 2008 (overall to Miyataka Shimizu), Francisco Ventoso (2009), Mickaël Buffaz (2010), Samuel Dumoulin (2011), and Egoitz García (2012).

**Sources:**
- https://en.wikipedia.org/wiki/Paris%E2%80%93Corr%C3%A8ze
- https://fr.wikipedia.org/wiki/Paris-Corr%C3%A8ze
- https://en.wikipedia.org/wiki/Bol_d%27Or_des_Mon%C3%A9di%C3%A8res

### C. Paris-Corrèze — editions and corridor finishes

Stage-level routing data is sparse for the early editions; the strongest evidence is for 2007–2012, all of which finished at Chaumeil (Bol d'Or circuit). Per Wikipedia and the Bol d'Or article, **all post-2005 editions** finished at Chaumeil.

**2007 — Stage 2: Vigeois → Chaumeil (159.4 km, 9 Aug 2007)**
- Winner: Edvald Boasson Hagen (Maxbo Bianchi); also won Stage 1 and overall
- Finish: Chaumeil → **segment 15** (Bol d'Or circuit)
- Source: https://autobus.cyclingnews.com/road.php?id=road%2F2007%2Faug07%2Fcorreze07%2Fcorreze072

**2008 — Stage 2: Brive-la-Gaillarde → Chaumeil (161.7 km, 7 Aug 2008)**
- Stage winner: Lloyd Mondory (Ag2r); overall to Miyataka Shimizu
- Departure Brive (segs 1–2), finish Chaumeil → **segment 15**
- Source: https://cqranking.com/men/asp/gen/race.asp?raceid=8246

**2009 — Stage 2: Tulle → Chaumeil (147.6 km, 6 Aug 2009)**
- Stage winner: Wesley Sulzberger; overall to Francisco Ventoso
- Stage 1 was Saint-Amand-Montrond → Besse (outside Corrèze)
- Departure **Tulle (segment 10)**, finish **Chaumeil (segment 15)**. Strongest corridor overlap of any edition.
- Source: https://www.cyclingnews.com/races/9th-paris-correze-2-1/race-history/

**2010 — Stage 1: Contres → Saint-Léonard-de-Noblat (4 Aug 2010); Stage 2 → Chaumeil**
- Stage 1 winner & overall: Mickaël Buffaz (Cofidis)
- Stage 2 finish: Chaumeil → **segment 15**
- Source: https://www.cyclingnews.com/races/10th-paris-correze-2-1/stage-1/results/

**2011 — Stage 2: Objat → Chaumeil (178.7 km)**
- Overall: Samuel Dumoulin
- Departure Objat (Corrèze, ~15 km west of segment 1, off-route), finish Chaumeil → **segment 15**
- Source: https://www.procyclingstats.com/race/paris-correze/2011 (search-surfaced; PCS returns 403 to WebFetch but the page exists)

**2012 — Stage 2: Objat → Chaumeil (170.2 km)**
- Overall: Egoitz García
- Finish Chaumeil → **segment 15**
- Source: https://www.procyclingstats.com/race/paris-correze/2012/stage-2 (403 to WebFetch)

For 2001–2006 stage-by-stage routes, authoritative finish-town data was not found within budget. The Bol d'Or article asserts the Chaumeil finish from 2005 onward; pre-2005 editions plausibly finished elsewhere in Corrèze but cannot be pinned to corridor towns from open sources.

### C. Paris-Corrèze — issue #503 resolution suggestion

The existing `data/historical-tdf.json` keys Paris-Corrèze to segments `[25, 26, 27]` (Meymac/Ussel). Based on the evidence above, **this keying is wrong**: Paris-Corrèze never (in the documented 2005–2012 era) finished in Ussel or Meymac. The race's finish-line identity is **Chaumeil** on the Bol d'Or des Monédières circuit, which is segment 15 in our scheme — and 2009 specifically departed from **Tulle (seg 10)** and finished at **Chaumeil (seg 15)**, putting it directly on the corridor.

**Recommendation for whichever future strand picks up #503:** re-key Paris-Corrèze to `[15]` as the canonical home, and consider adding per-edition entries that surface 2008 (Brive departure, segs 1–2) and 2009 (Tulle → Chaumeil, segs 10 → 15) as corridor highlights. The pre-2005 editions are documented poorly enough that finish locations should not be asserted without a primary source. This is a recommendation only; no JSON edit is being proposed in this dossier.

### C. Paris-Corrèze — photo / video candidates

- **Wikimedia Commons** — `Category:Paris–Corrèze` exists but is sparse. The category page is reachable from both Wikipedia language editions; spot search needed before use. License: CC BY-SA where present.
- **autobus.cyclingnews.com** — 2007 archive page contains race photography by Cyclingnews staff; **all rights reserved**, not redistributable. Use for fact-checking only.
- **CQ Ranking** (`cqranking.com/men/asp/gen/race.asp?raceid=8246`) — text results only, no usable images.
- **velo19.com / velo19.fr** — local Corrèze cycling enthusiast site; presently down (`ECONNREFUSED` during research). May host historical Bol d'Or / Paris-Corrèze photography but licensing is unclear and would need direct contact.
- **Bol d'Or des Monédières (Wikipedia EN/FR)** — articles include archive photos; check Commons category `Bol d'Or des Monédières` for any CC content.

No CC-licensed video of Paris-Corrèze surfaced. INA archives (`ina.fr`) likely hold France 3 Limousin coverage but per memory `reference_european_video_embeds.md` these embed with GDPR cookie-banner overlays — flag, do not embed.

### C. L'Agglomérée 2026 edition

L'Agglomérée 2026 was held **Saturday 4 – Sunday 5 April 2026** in the Tulle agglomeration. The cyclosportive epreuves ran on Sunday morning, starting 09:15. Two cyclo timed distances were on offer — **85 km and 105 km** — alongside three cyclotourisme distances (65, 85, 105 km), a Verticale (1.1 km / 152 m D+) on the Saturday, an Agglo Nature trail (12 / 23 km), VTT, and hiking. Online registrations closed 4 April 17:00; no race-day entries were accepted. **40 km of every cyclo course were laid on the actual 2026 Tour de France Stage 9 route**, including the Suc au May climb. The Tulle agglo official communiqué (post-event) reports ~**1,800 participants and 350 volunteers** across all disciplines and characterises the edition as a successful "moment fédérateur." Per-distance podium table for the 2026 edition was not found: the official results portal at `lagglomeree.agglo-tulle.fr` was returning HTTP 500 during research (one month after the event), and no La Montagne or Le Populaire piece surfaced via search. The 2025 edition (6 April 2025, 110 km) was won by Robin Bourdier in 02:47:38, ahead of Alexis Delrieu (02:50:01) and Guel Faure (02:50:10); women's overall: Annerose Alicot 03:12:08; 235 finishers. This is the closest documented baseline for what 2026 results will look like once the portal is back.

**Sources:**
- https://lagglomeree.agglo-tulle.fr/ (200; results portal currently down at deeper URLs)
- https://www.tulleagglo.fr/actualites/lagglomeree-revient-les-4-5-avril-2026/
- https://www.velo-ouest.com/saison-2025/resultats-2025/cyclosportive-l-agglomeree.html (2025 results)

### C. L'Agglomérée — narrative hook

The hook is exact and modest: the same week the tdf26 blog began publishing (week of 5 April 2026), roughly **1,800 amateurs** rode 40 km of the same Stage 9 tarmac that the WorldTour peloton will use on **12 July 2026** — including the Suc au May climb that anchors segments 14–15 of the travelogue. They got there first by ninety-eight days. That is the structural callout for `/tour-history`: pros are not the only ones whose route this is. The local cycling community has been riding it as a stewardship event since 2023, and Tulle Cyclisme Compétition (the organising club) has been the keeper of the road in a way the ASO is not.

A second, lighter beat for the page: 2026 is also the year the cyclosportive's route effectively *becomes* the Tour route, where in prior editions it merely overlapped. The reverse direction is also telling — the riders climbing Suc au May in April were carrying race numbers attached with the same kind of safety pins the pros use, three months earlier and with weather the pros may not face.

### C. L'Agglomérée — photo / video / press coverage

- **`lagglomeree.agglo-tulle.fr/lagglomeree-2024-en-images/`** — official 2024 image gallery exists (HTTP 500 during research; URL is canonical and likely intermittent). License: not stated → assume **all rights reserved** per French default. Do not republish without written permission from Tulle agglo.
- **Tulle agglo Facebook** (`facebook.com/agglotulle`) and **L'Agglomérée Facebook** (`facebook.com/p/LAgglomérée-100091265376901`) — primary social-media coverage of the 2026 edition. Photos posted there are © event organiser; embed via FB iframe is permissible but redistribution is not.
- **SPORTMAG** (`sportmag.fr/le-sport-a-toutes-les-sauces-avec-lagglomeree/`) — French sports magazine feature; rights reserved.
- **gotrail.run, runtrail.run, werun.world** — race-calendar listings, no original imagery worth using.
- **OK-Time** (`ok-time.fr/evenement/agglomeree-2026-cyclo-dimanche/`) — timing partner, text results only. The deeper 130km-named URL surfaced in search returned 404; the canonical 2026-cyclo-dimanche slug is correct.
- **Wikimedia Commons** — no `Category:L'Agglomérée` exists at time of research. **Gap: nothing CC-licensed is available.** If imagery is wanted for the page, the publisher should ask Tulle Cyclisme Compétition or Tulle agglo communications for a written release on a small selection.

**Tulle Cyclisme Compétition (T2C)** — the organising club is also active in regional road-race results year-round (DirectVelo profile: `directvelo.com/equipe/2271/tulle-cyclisme-competition`). It is one of three co-organisers alongside Cercle Laïque Tulliste Vélo and Club Rando Cyclo Chamboulive. Worth a single sentence in any /tour-history copy as the local cycling stewardship line.

### C. Open questions

1. **2001–2006 Paris-Corrèze stage finish towns** — could not pin down. The Bol d'Or article asserts Chaumeil from 2005 only; 2001–2004 finish locations remain unverified. Worth a focused L'Équipe / La Montagne archive trip if anyone wants to tighten the keying for those years.
2. **2026 L'Agglomérée per-category podiums** — the official results portal was 500-erroring during research; rerun this when the site is back. Likely fine on a retry in a few days.
3. **Did 2026 L'Agglomérée 85 km AND 105 km both touch Stage 9?** — the official copy says "40 km of the Tour de France route" without specifying per-distance; safe to assume both share the Suc au May spine but verify if making a strong claim.
4. **CC-licensed imagery** — none surfaced for either race within the time budget. Wikimedia Commons categories are either thin (Paris-Corrèze) or non-existent (L'Agglomérée). Either commission permission or accept the page goes text-only.
5. **`Bol d'Or des Monédières` Wikimedia category** — flagged but not opened in this pass; may yield CC images that double as Paris-Corrèze coverage given the shared finish.

## Section D — Famous Corrèze riders

<!-- STATUS: raw notes from subagent D, awaiting synthesis. The honest finding is that Corrèze has produced no Tour winner / stage winner / maillot jaune. -->

### D. Pro cyclists from Corrèze

**Alain De Carvalho (1953–)** — Ussel, climber-domestique
- Birthplace: Ussel, Corrèze
- Pro career: 1977–1982 (Flandria-Velda 1977; Fiat 1978–79; Puch-Sem-Campagnolo 1980; Puch-Wolber 1981; Wolber-Spidel 1982)
- Tour de France: 4 starts. 1978 — 48th GC; 1979 — 55th; 1980 — DNF stage 12; 1981 — 53rd. No stage wins, no jersey days.
- Hook: The only Tour de France finisher born in the Corrèze corridor that this stage actually traverses. After his career he opened a bike shop in Pompadour and revived the Grand Prix de Pompadour as the junior/U23 Trophée Alain De Carvalho — a living link between the département's professional past and its current talent pipeline.
- Wikimedia Commons photo: NONE FOUND (Commons search "Alain De Carvalho cyclist" returned zero results — license flag: no usable photo)
- Sources: https://en.wikipedia.org/wiki/Alain_De_Carvalho, https://fr.wikipedia.org/wiki/Alain_De_Carvalho, https://veloquercy.over-blog.com/2026/02/le-trophee-alain-de-carvalho-a-pompadour.html

**Claude Mazeaud (1937–)** — Vignols, sprinter / road
- Birthplace: Vignols, Corrèze (rural commune between Pompadour and Objat)
- Pro career: 1962–1964 (Mercier-BP-Hutchinson 1962–63; Margnat-Paloma-Dunlop 1964); independent before and after
- Tour de France record: Never started a Tour. Best result outside the Tour: 1961 Champion de France des Indépendants; 1966 Grand Prix de Plouay (his self-described biggest win, riding as an independent).
- Hook: A Corrèze farm boy who reached pro level (Mercier, the Poulidor team) but never got on a Tour roster — the more typical fate of pre-corporate-era riders from a non-cycling département.
- Wikimedia Commons photo: NONE FOUND (Commons search returned zero results; FR-Wikipedia article explicitly invites a free-license image)
- Sources: https://fr.wikipedia.org/wiki/Claude_Mazeaud, https://www.memovelo.com/claude-mazeaud, https://www.cyclisme-en-limousin.fr/coureur.php?id_coureur=8708

### D. Riders strongly associated with Corrèze (not born there)

**Raymond Poulidor (1936–2019)** — Haute-Vienne / Creuse-border, GC contender; the regional figurehead
- Birthplace: Masbaraud-Mérignat, **Creuse** (adjacent department; just east of Limoges, near Haute-Vienne line)
- Pro career: 1960–1977 (Mercier-BP all 18 seasons)
- Tour de France record: 14 starts, 12 finishes; 3× 2nd (1964, 1965, 1974); 5× 3rd (1962, 1966, 1969, 1972, 1976); 7 stage wins; **never wore yellow** — "L'Éternel Second"
- Corrèze connection: Won the Bol d'Or des Monédières at Chaumeil in 1963, 1966, 1967 (3rd in 1960). The Monédières crit was the regional cycling festival of the corridor, on the actual Stage 9 route (Chaumeil sits in the segment 13/14 area). Poulidor mentored Luc Leblanc into turning pro.
- Hook: For viewers and old-timers the entire Limousin corridor IS Poulidor country, even if his birthplace is a département north. The Stage 9 announcer will say his name.
- Wikimedia Commons: Category:Raymond Poulidor — multiple CC BY-SA portraits and race photos. Verify per file.
- Sources: https://en.wikipedia.org/wiki/Raymond_Poulidor, https://en.wikipedia.org/wiki/Bol_d%27Or_des_Mon%C3%A9di%C3%A8res

**Albert Bourlon (1916–2013)** — held the Corrèze pro-race torch
- Birthplace: Sancergues, Cher (NOT Corrèze)
- Tour de France: 1947 — set the still-standing Tour record for longest solo breakaway (253 km, Carcassonne–Luchon, ~8h10m at 31 km/h average)
- Corrèze link: Won the inaugural Grand Prix de Pompadour (Corrèze) in 1949
- Hook: The Tour's longest-ever solo break was won by a man whose first post-record victory came on Corrèze roads. Useful for an "endurance through obscurity" framing.
- Wikimedia Commons: Limited — check Category:Albert Bourlon
- Sources: https://en.wikipedia.org/wiki/Albert_Bourlon, https://www.velo18.net/bourlon.html

**Frédéric Brun (1957–2025)** — Dordogne-born but a Bol d'Or des Monédières specialist
- Birthplace: Ribérac, Dordogne (adjacent department)
- Pro career: 1979–1991, including teammate of Bernaudeau, Duclos-Lassalle, Mottet, Claveyrolat
- Tour de France: 9 starts
- Corrèze connection: Won the Bol d'Or des Monédières at Chaumeil in 1988, multiple podiums 1984–1986
- Wikimedia Commons: NONE FOUND in initial search
- Sources: https://fr.wikipedia.org/wiki/Fr%C3%A9d%C3%A9ric_Brun_(cyclisme,_1957)

### D. Adjacent-department riders (optional context — design-phase decision)

**Luc Leblanc (1966–)** — Haute-Vienne (Limoges); world champion, optional context — adjacent department
- Birthplace: Limoges, Haute-Vienne (adjacent)
- Pro career: 1987–1998
- Tour de France: 1991 wore yellow briefly (3 days, after stage 7); 1994 stage 12 winner at Hautacam, beating Indurain in fog; 1994 final GC 4th. World Road Champion 1994.
- Corrèze tie: Won the Tour de la Corrèze 1986 as an amateur; mentored by Poulidor.
- Note: 2025 Tour renamed the Hautacam climb "montée Luc Leblanc" — fresh news hook for 2026.
- Wikimedia Commons: Category:Luc Leblanc — multiple race photos, CC BY-SA
- Sources: https://en.wikipedia.org/wiki/Luc_Leblanc

**Antonin Magne (1904–1983)** — Cantal (Ytrac); 2× Tour winner, optional context — adjacent department
- Birthplace: Ytrac, Cantal (adjacent)
- Tour de France: 1931 winner, 1934 winner (1934: led from stage 2, won 2 stages including Tour's first individual TT); 1936 2nd
- Corrèze tie: Won the Tour de la Corrèze 1929 (his brother Pierre Magne won the same edition's earlier classification); Souvenir Antonin Magne held annually in the Aurillac/Limousin corridor.
- Wikimedia Commons: Category:Antonin Magne — period press photos, mostly PD-old or CC where digitised by Bibliothèque nationale; verify per file.
- Sources: https://en.wikipedia.org/wiki/Antonin_Magne

**Marc Durant (1955–)** — Creuse; Tour-veteran domestique, optional context — adjacent department
- Birthplace: Saint-Sulpice-le-Guérétois, Creuse (adjacent)
- Pro career: 1979–1987
- Tour de France: 5 starts (1981–1985); best GC 30th in 1983
- Hook: Limousin's other regular Tour finisher of the 1980s.
- Sources: https://en.wikipedia.org/wiki/Marc_Durant

### D. Narrative arcs

**Rider-of-the-soil is thin.** The Corrèze has produced no Tour winner, no stage winner, no maillot jaune. The honest narrative is scarcity: Alain De Carvalho (Ussel, 1978–81, four finishes outside the top 45) is the lone Corrèze-born finisher of the modern era; Claude Mazeaud (Vignols, Mercier, 1962–64) reached a yellow-jersey team but never started a Tour. The Stage 9 corridor is cycling-aware (Tulle Cyclisme Compétition, the L'Agglomérée sportive, Bol d'Or des Monédières at Chaumeil) but is a *consumer* of Tour-de-France glamour, not a producer of champions. That makes the natural framing for /tour-history "the Corrèze as cycling parish, not cycling powerhouse" — Pompadour shop, Monédières crit, Tulle club kids — and lean on Poulidor (adjacent Creuse) as the regional figurehead the public actually associates with these roads.

**Climbing-vs-sprinting tendency.** What few pros the corridor produces are climbers/baroudeurs (Brun, De Carvalho), not sprinters. This matches the Massif Central terrain and predicts the kind of breakaway artist who will animate Stage 9 itself: long-range, tactical, not a Cavendish-style finish. A piece on "Massif Central rider DNA" could pair Brun's nine Tours and Bol d'Or wins with Leblanc's 1994 Hautacam ride as templates.

**Tour-veterans-from-the-corridor.** A four-name spine — De Carvalho, Mazeaud, Brun, Leblanc — covers 1962 to 1998 and lets the page tell a 36-year story without overreaching. Poulidor anchors the 1960s, Leblanc anchors the 1990s, De Carvalho fills the gap. The Bol d'Or des Monédières at Chaumeil (1952–2002) is the perfect connective tissue: Robic, Coppi, Géminiani, Poulidor, Hinault, Fignon, Brun, Claveyrolat all rode this circuit on the actual Stage 9 route.

### D. Open questions

1. Are there contemporary (2010s–2020s) Corrèze-born WorldTour riders? Initial searches turned up Tulle Cyclisme Compétition development riders and the Team Corrèze-Suchet-Nouvelle-Aquitaine continental project, but no current WorldTour pro with a Corrèze birthplace. Worth a targeted ProCyclingStats query if access can be arranged (PCS returned 403 to WebFetch).
2. Wikimedia Commons gap: De Carvalho and Mazeaud have no Commons photos. The /tour-history page may need to commission/source photos from local cycling clubs (UC Briviste, Tulle Cyclisme) under explicit license, or rely on text-only profiles for these two.
3. Pierre Magne (Antonin's brother) — won Tour de la Corrèze 1929 and was a Tour-de-France-era pro; birthplace not confirmed Corrèze (likely Cantal like Antonin). Worth a 5-minute follow-up.
4. The 1987 Chaumeil men's and women's Tour stages are owned by sister strand #478 — see #478. Not researched here.
5. Any Tulle massacre / Resistance cyclist link (per CLAUDE.md cultural context)? Not surfaced; possibly an editorial blank.

## Section E — Resistance-era and post-war context (bonus)

<!-- STATUS: raw notes from subagent E, awaiting synthesis. Recommendation: use sparingly per subagent E's editorial judgment. -->

### E. 1947 Tour de France & corridor

The 1947 Tour de France (25 June – 20 July, 21 stages, 4,642 km) was the first post-war edition after a seven-year hiatus. Its route ran clockwise along the periphery: Paris → Lille → Brussels → Luxembourg → Strasbourg → Besançon → Lyon → Grenoble → Briançon → Digne → Nice → Marseille → Montpellier → Carcassonne → Luchon → Pau → Bordeaux → Les Sables-d'Olonne → Vannes → Saint-Brieuc → Caen → Paris. **The route did not touch the Stage 9 2026 corridor at all** — it bypassed central France entirely, avoiding Limoges, Brive, Tulle, Ussel, and Clermont-Ferrand. The Bordeaux→Les Sables-d'Olonne stage (16) hugged the Atlantic, and Lyon→Grenoble (6) ran east of the Massif. ([Wikipedia 1947 TdF](https://en.wikipedia.org/wiki/1947_Tour_de_France))

The symbolic load was real but not corridor-specific. The 1947 edition prioritised reconciliation: it crossed into Belgium and Luxembourg "in the hopes of bringing together a few countries ravaged by the war"; the German team was excluded; the Italian team comprised Franco-Italians since the Franco-Italian peace treaty was not yet ratified. *L'Auto*, the pre-war organiser, had been shut down by de Gaulle for collaboration; the relaunched Tour was run by *L'Équipe* / *Le Parisien Libéré*. Jean Robic's win on the final stage — overhauling Pierre Brambilla on the road to Paris without ever wearing the yellow jersey before the finish — became a foundational post-war national fable. ([War History Online](https://www.warhistoryonline.com/war-articles/tour-de-france.html), [Origins OSU](https://origins.osu.edu/milestones/tour-de-france-and-yellow-jersey))

For the dossier: the 1947 Tour's bypass of the corridor is itself the interesting fact. The first post-war Tour did *not* visit the Tulle/Oradour memorial geography. That absence is not necessarily deliberate avoidance — the route is plausibly explained by traditional perimeter routing — but it is worth noting that the corridor had to wait for the Tour to come.

### E. Resistance-era racing in central France

The **Circuit de France 1942** (28 September – 4 October, 1,650 km, 6 stages) is the central data point and it *did* clip the corridor. The route ran Paris → Le Mans → Poitiers → Limoges → Clermont-Ferrand → Saint-Étienne → Lyon → Dijon → Paris. The Limoges→Clermont-Ferrand stage (163 km) crossed the northern Limousin, though it did not pass through Tulle or Brive (Limoges to Clermont via Aubusson/Ussel-direction is geographically possible but unconfirmed for this race; published sources only cite stage termini). The race was organised by Jean Leulliot of the collaborationist *La France Socialiste* with German and Vichy backing after Jacques Goddet, the *L'Auto* Tour director, refused to restart the Tour itself. 69 starters, only 29 finishers; Belgian François Neuville won the zebra-striped leader's jersey. The Vichy regime banned similar stage races by decree in 1943. ([Wikipedia FR Circuit de France](https://fr.wikipedia.org/wiki/Circuit_de_France), [franceinfo](https://www.franceinfo.fr/tour-de-france/hommes/cyclisme-en-1942-sous-l-occupation-le-circuit-de-france-a-la-place-du-tour-de-france-pour-servir-la-propagande-de-vichy_5906849.html))

Goddet's counter-move was the **Grand Prix du Tour de France** (1943, 1944) — a season-long aggregate competition tallying results from the *single-day* races still permitted. Jo Goutorbe (1943) was awarded a yellow jersey at season's end; the 1944 edition, leading Maurice Desimpelaere, was interrupted by the Normandy landings. Goddet's design was, in effect, a workaround: keep cycling alive and a yellow jersey awarded without organising a stage race that would serve Vichy/German propaganda. ([Wikipedia FR Grand Prix du Tour de France](https://fr.wikipedia.org/wiki/Grand_Prix_du_Tour_de_France))

Émile Idée, a French rider in the 1942 Circuit, reportedly faced Gestapo coercion to participate. ([Wikipedia Tour de France during WWII](https://en.wikipedia.org/wiki/Tour_de_France_during_World_War_II))

### E. Tulle massacre & cycling

**No documented direct connection.** The Wikipedia Tulle massacre article contains zero references to cycling, the Tour, or any sporting commemoration; only "Rue du 9-Juin-1944" is named as memorial geography. ([Wikipedia Tulle massacre](https://en.wikipedia.org/wiki/Tulle_massacre))

The **1996 Bastille Day Tulle finish** (Stage 14, Besse → Tulle, 186.5 km, 14 July 1996, won by Djamoulidine Abdoujaparov) is not framed as commemorative in any source surfaced. The Wikipedia stage page and bikeraceinfo cover it as a flat sprint stage with no mention of memorial framing. François Hollande was indeed mayor of Tulle 2001–2008, *after* this stage; in 1996 he was deputy for Corrèze but not yet mayor, so the often-asserted "Hollande hosted the Tour" reading is anachronistic for 1996. The Bastille Day calendar coincidence is real, but published sources treat it as a routine summer-stage finish, not a Resistance-era memorial. ([Wikipedia 1996 stages 11–21](https://en.wikipedia.org/wiki/1996_Tour_de_France,_Stage_11_to_Stage_21))

For the dossier: be careful here. Reading the 1996 finish as commemorative is interpretation, not history. If the eventual page wants to make that move, it should flag it as the writer's reading, not as documented intent.

### E. Post-war (1947–1965) corridor stages

No specific Tour stage 1947–1965 with corridor relevance was confirmed beyond the 1951 Brive→Agen stage already in the corpus. Stage-by-stage Limousin coverage in this period is not surfaced by general searches — it would require dedicated archive work at letour.fr or in national-team-era stage atlases. The general pattern: the Tour from 1947 through the 1960s used national/regional teams (1930–1961), then trade teams (1962+); it ran through the periphery of France with the Massif Central traversed by Auvergne stages (Clermont-Ferrand, Saint-Étienne, Aurillac) more than by Limousin/Corrèze stages. ([Tour de France records and statistics](https://en.wikipedia.org/wiki/Tour_de_France_records_and_statistics))

### E. Massif Central in the Tour mythology

In the Tour's geographic imagination, the **Massif Central is a secondary climbing theatre to the Alps and the Pyrenees**, not their equal. The Alps and Pyrenees deliver the spectacular Grand Tour decisive stages (Galibier, Tourmalet, Izoard); the Massif Central delivers a different register — historically the **Puy-de-Dôme** (13 appearances 1952–1988), a steep volcanic plug that produced the 1964 Anquetil-Poulidor shoulder-to-shoulder duel and Coppi's 1952 stage win, but rarely a GC-decisive day. The cultural framing in cycling media is closer to "iconic but eccentric" than to "the holy mountains." ([road.cc Puy de Dôme returns](https://road.cc/content/feature/iconic-puy-de-dome-returns-tour-after-35-years-302331), [Cyclist Anquetil-Poulidor](https://www.cyclist.co.uk/in-depth/tour-de-france-history-anquetil-and-poulidor-go-head-to-head))

For Limousin/Corrèze specifically — the western Massif Central — there is no comparable mythological franchise. Christopher Thompson's *The Tour de France: A Cultural History* (UC Press, 2006) treats the Tour as a stage for working out French national identity (rural-vs-urban, masculinity, modernization, war memory) but specific Massif-Central framing was not confirmed without book access. ([Thompson book on JSTOR](https://www.jstor.org/stable/jj.18736045)) The Massif Central's cycling identity in popular sources reads more as **"empty country, hard wind, no glory"** than as the soul-of-French-cycling — Bobet, Vietto, Poulidor are all storied climbers but their mythologies attach to Pyrenean stages (Bobet's Izoard) and Alpine drama, not to Limousin terrain.

### E. Recommendation

**Use sparingly.** Two pieces are worth including on a /tour-history page:

1. **The 1942 Circuit de France** as a one-paragraph counterweight to the post-war Tour — the corridor (Limoges) was raced under occupation for Vichy propaganda before it was raced as part of the legitimate Tour. That juxtaposition is genuinely interesting and historically robust.
2. **The 1947 Tour's bypass of the corridor** as a one-line observation — the first post-war Tour, despite its reconciliation themes, did not visit the Limousin/Corrèze. The corridor waited.

**Do not include** speculative readings of the 1996 Tulle stage as commemorative. There is no source to support that and the dossier's pre-publish-scrutiny norms argue against it.

The Massif Central mythology material is too thin for a section of its own; could be a single sentence inside the broader page.

### E. Open questions

- Did any Tour stage 1947–1965 actually finish or pass through Tulle, Brive, or Ussel? Letour.fr archive query needed; not surfaced by general search.
- What was the exact intermediate route of the 1942 Circuit de France Limoges→Clermont-Ferrand stage? Did it pass through any Corrèze towns? The published sources only give stage termini.
- Did Goddet's 1943–1944 *Grand Prix du Tour de France* aggregate any single-day races run in central France? Worth checking the constituent races if the angle ever becomes more important.
- Christopher Thompson's book likely has the strongest scholarly framing for the Tour's relationship to Resistance memory, but specific Tulle/corridor passages were not verified without book access.

## Story arcs (Session 2 deliverable — placeholder)

<!-- STATUS: not started. Session 2 must synthesize 2-4 candidate arcs from the above material with brief rationale; decision deferred to design phase. -->

Candidate arcs surfaced inline by subagents A–E (not yet consolidated):
- **The corridor's home circuit** (subagent B narrative hook 1) — Tour du Limousin as the corridor's regular cycling life; Stage 9 2026 as the arrival of the bigger cousin.
- **Ussel's first Tour** (subagent A verification + subagent B's 2009 Limoges→Ussel finish) — the verified historical claim that Ussel has never been a Tour stage town, paired with the 2009 Tour du Limousin same-finish-line precedent.
- **Cycling parish, not cycling powerhouse** (subagent D narrative arc 1) — the Corrèze as consumer of Tour glamour, not producer of champions; honest accounting from De Carvalho through to Poulidor (adjacent) as figurehead.
- **Bol d'Or des Monédières as connective tissue** (across A, C, D) — Robic, Coppi, Géminiani, Poulidor, Hinault, Fignon, Brun, Claveyrolat all on the actual Stage 9 corridor at Chaumeil 1952–2002, then Paris-Corrèze 2005–2012; the Stage 9 finish at Chaumeil-area as the latest in a 70-year tradition.
- **The amateur came first** (subagent C narrative hook) — L'Agglomérée 4–5 April 2026, ~1,800 amateurs riding 40 km of Stage 9 ninety-eight days before the pros; cycling stewardship at the local-club scale.
- **Wartime-and-after framing** (subagent E recommendation) — 1942 Circuit de France clipped Limoges under occupation; 1947 first post-war Tour bypassed the corridor; the corridor had to wait for the Tour to come back.

## Hero-image candidates (Session 2 deliverable — placeholder)

<!-- STATUS: not started. Session 2 must curate a 3-6-image shortlist with license + attribution + URL from the photo candidates surfaced in sections A–E above. Per `feedback_pre_publish_scrutiny.md`, license verification per file is required before any image lands in the eventual page. -->

Photo-candidate sources surfaced inline:
- Wikimedia Commons categories per event/rider (CC BY-SA where present, verify per file)
- Bol d'Or des Monédières Wikimedia category (flagged but not opened by subagent C)
- Dutch Nationaal Archief CC0 alternates for 1960s-era material (Anquetil, Poulidor, Merckx, Ocaña)
- Tulle Cyclisme Compétition / Tulle agglo (would require explicit licensing for L'Agglomérée material)

## Sources (Session 2 deliverable — placeholder)

<!-- STATUS: not started. Session 2 must consolidate every URL cited in sections A–E into a single deduped Sources list. The dossier's Sources section is the seed for the eventual page's Sources surface (per `feedback_sources_section.md`). -->

URLs are inline above. Session 2 should produce a single deduped list grouped by topic for the page's Sources surface.

## Carryforwards out of scope (Session 2 deliverable — placeholder)

<!-- STATUS: not started. Session 2 must file follow-up issues per `feedback_issues_describe_problems.md` for each `data/historical-tdf.json` data-add the research uncovered, and capture any other carryforwards. -->

Items the research surfaced that should NOT land in this dossier but should be filed elsewhere:

**Follow-up issues to file (Session 2 task):**
- 1951 Stage 10 Clermont-Ferrand → Brive (men's TdF; segs 1-2; pairs with already-corpus 1951 Stage 11)
- 1964 Stages 19/20 Brive arrival + departure (men's TdF; segs 1-2; Anquetil-Poulidor Puy-de-Dôme launch pad)
- 1969 Stages 19/20 Brive arrival + departure (men's TdF; segs 1-2; Hoban + Matignon underdog Puy-de-Dôme)
- 1973 Stages 17/18 Brive arrival + departure (men's TdF; segs 1-2; Ocaña era)
- 1976 Stage 19 Sainte-Foy-la-Grande → Tulle (men's TdF; seg 10; pairs with already-corpus 1976 Stage 20)
- 1987 Stage 12 Brive → Bordeaux (men's TdF; segs 1-2; Davis Phinney; pairs with #478's Chaumeil work)
- 1998 Stages 6/7/8 (men's TdF; multi-corridor; Festina/Ullrich/Cipollini)
- 2001 Stage 16 Castelsarrasin → Sarran (men's TdF; segs 12-15 area; Voigt; Chirac courtesy)
- 2016 Stage 5 Limoges → Le Lioran (men's TdF; adjacent context only; Van Avermaet)
- 2020 Stage 12 Chauvigny → Sarran (men's TdF; segs 12-15 area; Hirschi breakthrough)
- 2023 Stage 8 Libourne → Limoges + Stage 9 Saint-Léonard-de-Noblat → Puy de Dôme (men's TdF; adjacent context only)
- 2025 Stage 10 Ennezat → Le Mont-Dore (men's TdF; adjacent context only; Healy yellow)
- 2023 Femmes Stage 2 Clermont-Ferrand → Mauriac (women's TdF; borderline corridor via Bort-les-Orgues)
- Tour du Limousin corridor stages 1979 / 1987 / 1997 / 2009 / 2023 / 2024 / 2025 (regional race; multiple segs; particularly 2009 Limoges → Ussel which shares finish with 2026 TdF Stage 9)
- Paris-Corrèze 2007–2012 corridor finishes at Chaumeil (regional race; seg 15)

**#503 issue resolution recommendation:** the existing Paris-Corrèze entry in `data/historical-tdf.json` keys to `[25, 26, 27]`; recommendation is to re-key to `[15]` (Chaumeil). Session 2 should reference #503 in PR description and note this recommendation; the actual JSON edit belongs to a future strand.

**CLAUDE.md correction — RESOLVED at end of Session 1:** subagent A reported CLAUDE.md mentions a 2008 Cipollini Brive win. End-of-Session-1 grep of `/home/jhs/code/tdf26/CLAUDE.md` for "cipollini" / "2008.*brive" / "brive.*2008" returned **zero matches**. The claim is not in CLAUDE.md; subagent A was reacting to a misread. Thread closed; **Session 2 should not file a CLAUDE.md correction** for this. (Pattern noted in retro carryforwards: subagent verify-or-refute claims about specific repo file contents need source-grep verification before being treated as actionable.)

**Research follow-ups (not data-adds):**
- ledicodutour.com Ussel page (404) — alternate URL pattern not exhausted
- 2024 TdF Stage 11 — confirm whether route actually crossed Corrèze department
- 2001 TdF Stage 16 routing through Tulle — not verified
- 2001-2006 Paris-Corrèze finish-town data — not surfaced; archive trip needed
- 2026 L'Agglomérée per-distance podiums — official portal was 500-erroring; retry
- Tour du Limousin: Brive proper as ville-étape (vs agglomeration suburbs) — not confirmed
- Wikimedia license verification per file across all surfaced categories — Session 2 spot-check on hero-image candidates only, full verification at draft time

## URL spot-check (Session 1 outcome)

<!-- STATUS: complete for curated 30-URL high-leverage batch. Full URL census deferred to Session 2 synthesis. -->

Curated batch of 30 high-leverage URLs spot-checked at end of Session 1 via `curl -sIL -A "Mozilla/5.0" --max-time 12`. Results:

- **26 / 30 returned HTTP 200** — all Wikipedia EN/FR, all Wikimedia Commons, all `ledicodutour.com`, the L'Agglomérée portal, the Tulle agglo official, ICI Limousin (Hinault interview), France 3 Nouvelle-Aquitaine 2025 stage replay, Cyclingnews Paris-Corrèze archive, Dailymotion (Hirschi 2020), YouTube (Barguil 2021).
- **4 / 30 returned ERR (DNS resolution failure)** — all four `bikeraceinfo.com` URLs (`tdf1951.html`, `tdf1976.html`, `tdf1998.html`, `tdf2001.html`). The subagents successfully fetched bikeraceinfo URLs during research via their tool environment (WebFetch resolves where the parent shell does not), so these URLs are believed valid and were the source for several specific facts. Session 2 should re-attempt via WebFetch / WebSearch and treat bikeraceinfo as flaky-but-real; if still unreachable at synthesis time, swap to alternative sources where available (ProCyclingStats stage URLs, Wikipedia stage pages).

Full URL census (Session 2 task): the `## Sources` section consolidation must verify each URL once before PR.

## Synthesis tasks for Session 2

### Environment

- **Worktree path:** `/home/jhs/code/tdf26-tour-history` (created Session 1 via `git -C /home/jhs/code/tdf26 worktree add -b feature/issue-502-tour-history-research /home/jhs/code/tdf26-tour-history main`).
- **Branch:** `feature/issue-502-tour-history-research` (pushed; tracks `origin/feature/issue-502-tour-history-research`).
- **Verify branch via `git branch --show-current` immediately before each `git add`/`git commit`** per `feedback_shared_tree_branch_verification.md`.
- **Strand D's PR may or may not have merged by Session 2 start.** If Strand D merged first, `content/research/` already exists on `main` — no semantic conflict; Session 2's PR adds a sibling file. If Strand D has not merged, this strand's PR creates the directory; both PRs creating the same directory is harmless. No coordination needed beyond awareness.

### Concrete handoff list

1. **Read this dossier in full** plus the strand brief at `docs/strands/strand-tour-history-research.md` (especially §3, §5.2, §8).
2. **Cross-check segment keying** for every event in sections A, B, C against `data/segments.json` polyline geometry (per `feedback_on_route_checks.md`). The raw notes use approximate town-based keying; some are off-route adjacent and need explicit polyline-distance verification. Particularly verify: 2001 Stage 16 routing through Tulle (raw notes uncertain), 2024 Stage 11 Corrèze touchpoint (raw notes uncertain), 2023 Femmes Stage 2 Bort-les-Orgues passage (raw notes "borderline").
3. **Consolidate per-event sections** — combine duplicates (e.g., 1976 Stage 19 + Stage 20 should be one Tulle entry; 1964/1969/1973 Brive double-headers can be one entry each), harmonize description style, deduplicate sources.
4. **Write the Story arcs section** — pick 2-4 candidates from the inline hooks above, with brief rationale per arc. Final selection deferred to design-phase planning conversation; Session 2 produces the menu, not the choice.
5. **Curate Hero-image candidates section** — 3-6 specific image candidates with file URL, license, attribution, segment relevance. Spot-check license per file. The Bol d'Or des Monédières Wikimedia category was flagged but not opened by subagent C; check it for hero candidates.
6. **Write consolidated Sources section** — single deduped URL list, grouped by topic. Re-test bikeraceinfo.com URLs via WebFetch (subagents reached them; parent-shell DNS failed in Session 1 spot-check).
7. **Write Carryforwards out of scope** — finalize the data-add follow-up issue list (~16 items pre-listed in the carryforwards section) and file the issues. The Cipollini-2008 CLAUDE.md correction thread is **CLOSED** (verified at end of Session 1, claim not present; do not file).
8. **#503 keying recommendation** — Session 2 should add a comment to issue #503 noting that this dossier surfaced strong evidence the existing `[25, 26, 27]` Paris-Corrèze keying is wrong and recommending re-keying to `[15]` (Chaumeil/Bol d'Or). The actual JSON edit belongs to whichever strand resolves #503; this dossier produces the recommendation only. PR body should reference #503.
9. **Story-arc / hero-image decisions are NOT inline** — per planning-session call, both go to design-phase planning. Session 2 surfaces the menu, the publisher chooses at the design conversation. AskUserQuestion only if a true mid-synthesis material disagreement surfaces (rare — be selective).
10. **Run verification commands** — `npm test`, `python3 scripts/validate_entries.py`, `npm run build`.
11. **Open PR** on milestone v1.4.20, references #502 (does not close), references #503, references #478. PR body: short summary + arcs surfaced + hero-image candidate count + follow-up-issues filed (count + numbers).
12. **Final report to publisher** per brief §10.

### Items worth surfacing for the publisher's attention before Session 2 acts

These were captured in Session 1's final report and are restated here so Session 2 doesn't have to fish them out of conversation history:

1. **#503 keying fix is non-trivial.** Strong evidence that Paris-Corrèze should re-key to `[15]` (Chaumeil), not `[25, 26, 27]`. Session 2 plan: file as a comment on #503 (not a new issue), reference in PR description; the actual JSON edit belongs to a separate strand.

2. **CLAUDE.md Cipollini-2008 correction thread is CLOSED.** End-of-Session-1 grep confirmed CLAUDE.md does not contain the claim subagent A flagged. Session 2 does NOT file a CLAUDE.md correction.

3. **Coverage scope tag was honored.** Adjacent items (2016, 2023, 2025 men's TdF stages; 2023 Femmes; the Antonin Magne / Luc Leblanc rider entries) are tagged `optional context — design-phase decision`. Publisher chooses inclusion at the design-phase planning conversation.

4. **One open question worth a publisher-level call:** subagent E recommends *against* writing the 1996 Bastille Day Tulle stage as a Tulle-massacre commemoration since no source supports the framing. Worth a publisher decision on whether the eventual page makes that interpretive move at all.

5. **~16 data-add follow-up issues** to be filed. Session 2 may want to ask the publisher whether to bundle as one umbrella issue ("`historical-tdf.json` corridor expansion") or file individually per `feedback_issues_describe_problems.md`. The brief says "file new follow-up issues for any new factual entries" (plural); default is individual issues, but the volume may justify consolidation.
