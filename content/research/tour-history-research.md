---
title: Tour-history feature research dossier
strand: docs/strands/strand-tour-history-research.md
issue: 502
status: synthesized-pending-PR
session: 2 of 2 (final)
---

# Tour-history feature research dossier

This dossier feeds the design-discussion phase of the `/tour-history` feature (umbrella issue [#502](https://github.com/gneeek/tdf26/issues/502)). It surfaces the corridor-relevant Tour de France stages, regional races, riders, photo / video candidates, and historical framing that a future design-phase planning conversation will draw on to decide layout, story arc, hero image, and prominent-launch timing for the page. The subsequent draft strand will write the page itself; this strand stops at PR open.

The dossier is hand-curated and is **not** a parallel source-of-truth for `data/historical-tdf.json`. Per `feedback_source_of_truth_framing.md`, every data-add the research uncovered is captured in the §Carryforwards section below and rolled up into a single umbrella tracker issue; the actual `historical-tdf.json` edits belong to a future strand.

## Progress

- **Session 1** (commits 7895c9c + d6bd583): five parallel research subagents produced raw notes across sections A–E (corridor TdF stages, Tour du Limousin, Paris-Corrèze + L'Agglomérée, Corrèze riders, Resistance / post-war context).
- **Session 2** (this synthesis): polyline-keying verified for off-corridor candidates; raw notes consolidated into per-event corpus; story arcs surfaced; hero-image candidates curated with verified licenses; sources deduped; umbrella-issue body drafted; #503 keying recommendation drafted.
- **Next**: design-phase planning (story-arc selection, hero-image pick, prominent-launch timing) → draft strand → launch strand. Each is a separate future strand; this one ends at PR open.

## Per-event corpus

Each entry below uses the schema from the strand brief §5.2: corridor connection (segment key + polyline-distance for off-corridor cases), narrative, sources. Entries are ordered chronologically. Adjacent items carry the italic flag `*Adjacent context — design-phase decision flag.*` per the publisher decision applied 2026-05-07; the design phase decides whether each adjacent item earns coverage on the eventual page.

### Tour de France men's

#### 1942 — Circuit de France, Stage 3: Limoges → Clermont-Ferrand (163 km)

*Adjacent context — design-phase decision flag.*

- **Corridor connection**: Adjacent only. The 1942 Circuit was not a Tour de France edition and the Limoges → Clermont-Ferrand stage's intermediate routing through Corrèze towns is not in published sources, only stage termini.
- **Narrative**: Vichy-era propaganda race, organised by Jean Leulliot of the collaborationist *La France Socialiste* with German backing after Jacques Goddet of *L'Auto* refused to restart the Tour. Six stages, 1,650 km Paris→Le Mans→Poitiers→Limoges→Clermont→Saint-Étienne→Lyon→Dijon→Paris. 69 starters, 29 finishers; François Neuville (Belgium) won the zebra-striped leader's jersey. Vichy banned similar stage races by decree in 1943. The corridor's nearest brush with stage-race cycling during the occupation, and a counterweight to the post-war Tour's silence on this geography.
- **Sources**:
  - https://fr.wikipedia.org/wiki/Circuit_de_France
  - https://www.franceinfo.fr/tour-de-france/hommes/cyclisme-en-1942-sous-l-occupation-le-circuit-de-france-a-la-place-du-tour-de-france-pour-servir-la-propagande-de-vichy_5906849.html

#### 1947 — Tour de France route bypass

*Adjacent context — design-phase decision flag.*

- **Corridor connection**: The first post-war Tour did not visit the corridor at all. Route ran the periphery: Paris → Lille → Brussels → Luxembourg → Strasbourg → Besançon → Lyon → Grenoble → Briançon → Digne → Nice → Marseille → Montpellier → Carcassonne → Luchon → Pau → Bordeaux → Les Sables-d'Olonne → Vannes → Saint-Brieuc → Caen → Paris.
- **Narrative**: The post-war Tour reopened with reconciliation themes (Belgium and Luxembourg in the route, German team excluded) but did not visit the Limousin / Corrèze. The corridor waited. Jean Robic's last-day overhaul of Pierre Brambilla, never having worn yellow before the finish line, became a foundational post-war Tour fable — but not on these roads.
- **Sources**:
  - https://en.wikipedia.org/wiki/1947_Tour_de_France

#### 1951 — Brive two-day visit (Stages 10 and 11)

- **Corridor connection**: seg 1 (km 0-8). Stage 10 finished in Brive, Stage 11 departed from Brive.
- **Narrative**: Stage 10 (Clermont-Ferrand → Brive) was won by Bernardo Ruiz of Spain; Roger Lévêque held yellow. The morning after, Stage 11 (Brive → Agen, 177 km) was the day Hugo Koblet launched a 135 km solo breakaway, holding off Coppi, Bobet, Bartali, Magni, Géminiani, and Robic. One of the greatest solo rides in Tour history, and the only year Brive hosted both a finish and a successive-day start. The two-day visit reads as a single narrative beat: arrival, rest night, legend.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1951.html (parent-shell DNS + WebFetch resolver both fail; subagent A fetched successfully via different path; treat as flaky-but-real)
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html
  - https://en.wikipedia.org/wiki/1951_Tour_de_France

#### 1964 — Brive double-header (Stages 19 and 20)

- **Corridor connection**: seg 1 (km 0-8). Stage 19 finished in Brive, Stage 20 departed.
- **Narrative**: Stage 19 (Bordeaux → Brive) won by Edouard Sels (Belgium); Anquetil in yellow. Stage 20 (Brive → Puy-de-Dôme) won by Julio Jiménez; Anquetil held yellow into the Puy-de-Dôme — the day of the famous Anquetil-Poulidor shoulder-to-shoulder duel on the volcanic plug. Brive was the launch pad for one of the most-photographed moments in Tour history.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1964.html (flaky; see 1951 note)
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html

#### 1969 — Brive double-header (Stages 19 and 20)

- **Corridor connection**: seg 1 (km 0-8). Stage 19 finished in Brive, Stage 20 departed.
- **Narrative**: Stage 19 (Libourne → Brive) won by Barry Hoban (GB); Merckx in yellow. Stage 20 (Brive → Puy-de-Dôme) won by Pierre Matignon — Matignon was lanterne rouge of the race, and his attack from a small group held off the field for an emotional French underdog win on the Puy-de-Dôme. Brive was the launch pad for one of the most romantic stage wins in Tour history.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1969.html
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html

#### 1973 — Brive double-header (Stages 17 and 18)

- **Corridor connection**: seg 1 (km 0-8). Stage 17 finished in Brive, Stage 18 departed.
- **Narrative**: Stage 17 (Sainte-Foy-la-Grande → Brive) won by Claude Tollet (France); Ocaña in yellow. Stage 18 (Brive → Puy-de-Dôme) won by Ocaña himself, dominating the Massif Central transition stages en route to his only Tour win. The third Brive double-header in nine years.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1973.html
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html

#### 1976 — Tulle two-day visit (Stages 19 and 20)

- **Corridor connection**: seg 10 (km 64-70). Stage 19 finished in Tulle, Stage 20 departed.
- **Narrative**: Stage 19 (Sainte-Foy-la-Grande → Tulle) won by Hubert Mathis (France) by 7 seconds from a 9-man breakaway, with Paolini second. Van Impe held yellow. The 1975 winner Bernard Thévenet abandoned during this stage. Stage 20 (Tulle → Puy-de-Dôme) won by Joop Zoetemelk; Van Impe in yellow into the volcano. Tulle hosted back-to-back days — the only time the départemental capital has been a sustained Tour fixture.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1976.html
  - https://www.ledicodutour.com/villes_etapes/villes_t/tulle.htm
  - http://www.memoire-du-cyclisme.eu/eta_tdf_1970_1979/tdf1976_19.php
  - https://en.wikipedia.org/wiki/1976_Tour_de_France

#### 1987 — Stage 12: Brive-la-Gaillarde → Bordeaux (228 km)

- **Corridor connection**: seg 1 (km 0-8). Brive start.
- **Narrative**: Davis Phinney (USA, 7-Eleven) won the sprint — a rare US sprint win in the 1980s; Martial Gayant in yellow. The previous day's stage was the 1987 Chaumeil men's finish (owned by sister strand #478, segs 14-16); this is the morning-after departure. Read as a narrative pair with the Chaumeil work: the corridor finished the day at Chaumeil, slept in Brive, departed for Bordeaux.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1987.html
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html

#### 1996 — Stage 14 Bastille Day Tulle finish (Besse-en-Chandesse → Tulle, 186.5 km)

- **Corridor connection**: seg 10 (km 64-70). Tulle finish.
- **Narrative**: Already in `data/historical-tdf.json`. Won by Djamoulidine Abdoujaparov in a sprint; Bjarne Riis in yellow. 14 July 1996. **Per publisher decision 2026-05-07: do not write this as a Tulle-massacre commemoration.** No source surfaced supports the framing. François Hollande was deputy for Corrèze in 1996 but did not become mayor of Tulle until 2001 — the often-asserted "Hollande hosted the Tour" reading is anachronistic for this stage. Treat as a routine Bastille Day sprint finish.
- **Sources**:
  - https://en.wikipedia.org/wiki/1996_Tour_de_France,_Stage_11_to_Stage_21

#### 1996 — Stage 15: Brive-la-Gaillarde → Villeneuve-sur-Lot

- **Corridor connection**: seg 1 (km 0-8). Brive start.
- **Narrative**: Already in `data/historical-tdf.json`. Won by Massimiliano Podenzana. Pairs with the Stage 14 Tulle finish — the 1996 Tour spent two consecutive days in the corridor.
- **Sources**:
  - https://en.wikipedia.org/wiki/1996_Tour_de_France,_Stage_11_to_Stage_21

#### 1998 — Three-day Corrèze residency (Stages 6, 7 ITT, 8)

- **Corridor connection**: seg 1 (Brive: stages 6 finish + 8 start) + Tulle-area mid-corridor (stage 7 ITT Meyrignac-l'Église → Corrèze town, ~12 km NE of Tulle, on the seg 12-13 corridor).
- **Narrative**: A triple-corridor day. Stage 6 (La Châtre → Brive, 204.5 km) was a Mario Cipollini sprint win, his second consecutive of the race; Stuart O'Grady in yellow. Stage 7 ITT (Meyrignac-l'Église → Corrèze, 58 km) was won by Jan Ullrich in 1h15:25, taking yellow — and this was the morning the Festina doping scandal broke; Festina was expelled before the stage start. Stage 8 (Brive → Montauban, 190.5 km) won by Jacky Durand (France); Laurent Desbiens in yellow. The 1998 Tour spent ~3 days entirely in or around the 2026 Stage 9 corridor; the corridor was the geographic stage on which the Festina story broke.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf1998.html
  - https://en.wikipedia.org/wiki/1998_Tour_de_France,_Prologue_to_Stage_11
  - https://www.procyclingstats.com/race/tour-de-france/1998/stage-7

#### 2001 — Stage 16: Castelsarrasin → Sarran (227.5 km) and Stage 17: Brive → Montluçon (194 km)

*Adjacent context — design-phase decision flag.* (Sarran is 9.98 km north of the polyline at km 98.65; Stage 17 Brive start is on-corridor.)

- **Corridor connection**: Sarran finish is **adjacent only** — closest seg is 15 at km 98.65, but Sarran is 9.98 km from the polyline (verified Phase 2 below). Stage 17 Brive start is seg 1 (km 0-8).
- **Narrative**: Stage 16 was Jens Voigt's (Germany) first Tour stage win, from a breakaway with Nicki Sørensen; Lance Armstrong in yellow (results later annulled for doping). Sarran was selected because Jacques Chirac, sitting President at the time, has his country residence at Château de Bity in Sarran — a presidential-courtesy stage town. Stage 17 (Brive → Montluçon) was won by Serge Baguet (Belgium). Whether Stage 16's parcours actually passed through Tulle is not verified in raw notes.
- **Sources**:
  - https://www.bikeraceinfo.com/tdf/tdf2001.html
  - https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html
  - https://www.procyclingstats.com/race/tour-de-france/2001/stage-16/

#### 2012 — Stage 18: Blagnac → Brive (222.5 km)

- **Corridor connection**: seg 1 (km 0-8). Brive finish.
- **Narrative**: Already in `data/historical-tdf.json`. Mark Cavendish won the sprint in the rainbow jersey; Bradley Wiggins in yellow. The most-recent Brive stage finish.
- **Sources**:
  - https://www.procyclingstats.com/race/tour-de-france/2012/stage-18

#### 2016 — Stage 5: Limoges → Le Lioran (216 km)

*Adjacent context — design-phase decision flag.*

- **Corridor connection**: Adjacent only. Limoges start is ~80 km NW of Brive; the route went south-east through the Massif Central paralleling the Corrèze northern edge. Final climbs (Pas de Peyrol, Col de Néronne) are Cantal terrain immediately south of the corridor.
- **Narrative**: Greg Van Avermaet (BMC) attacked from a break, soloed in for the stage win and the yellow jersey, holding it for several days before Sagan took it. One of the iconic mid-2010s breakaway moments and a structural template for what a Stage 9-style break could deliver in 2026.
- **Sources**:
  - https://en.wikipedia.org/wiki/2016_Tour_de_France
  - https://www.cyclingstage.com/tour-de-france-2016-route/stage-5-tdf-2016/

#### 2020 — Stage 12: Chauvigny → Sarran (218 km)

*Adjacent context — design-phase decision flag.* (Same Sarran-distance issue as 2001 Stage 16.)

- **Corridor connection**: Adjacent only — Sarran is 9.98 km from the polyline (closest seg 15). Marc Hirschi's solo attack came on the Suc au May approach — the same climb that anchors segs 14-15 of the 2026 corridor.
- **Narrative**: Marc Hirschi (Switzerland, Sunweb) soloed to his first pro win after attacking late on the Suc au May approach; Pierre Rolland 2nd, Søren Kragh Andersen 3rd; Roglič in yellow. Hirschi's breakthrough; first Swiss stage win since Cancellara. The stage previewed the kind of late-attack the 2026 Stage 9 corridor invites — same climbs, same closing geography.
- **Sources**:
  - https://www.procyclingstats.com/race/tour-de-france/2020/stage-12
  - https://bikeraceinfo.com/tdf/2020-TDF-daily/tdf2020-stage-12.html
  - https://www.cyclingnews.com/races/tour-de-france-2020/stage-12/results/
  - https://www.dailymotion.com/video/x7zl61i (ASO highlights, embeddable)
  - https://www.youtube.com/watch?v=WAcJxi8tEdA (last km, embeddable)

#### 2023 — Stage 8 (Libourne → Limoges) and Stage 9 (Saint-Léonard-de-Noblat → Puy de Dôme)

*Adjacent context — design-phase decision flag.*

- **Corridor connection**: Adjacent only. Stage 8 Limoges finish is ~80 km NW of Brive; Stage 9 Saint-Léonard-de-Noblat start is ~70 km NW. Neither stage entered Corrèze proper.
- **Narrative**: Stage 8: Mads Pedersen sprint win, Vingegaard in yellow. Stage 9: Michael Woods (Canada, Israel-Premier Tech) caught Matteo Jorgenson on the Puy de Dôme summit — first Puy-de-Dôme finish since 1988, the major Massif Central narrative anchor of recent years. The most recent men's TdF crossing of the broader Limousin region before 2026.
- **Sources**:
  - https://www.cyclingstage.com/tour-de-france-2023-route/stage-8-tdf-2023/
  - https://www.procyclingstats.com/race/tour-de-france/2023/stage-8

#### 2024 — Stage 11: Évaux-les-Bains → Le Lioran (211 km)

- **Corridor connection**: Already in `data/historical-tdf.json`. Whether the route actually crossed Corrèze department is not verified in raw notes — it stayed in Creuse / Cantal per the route map. Treat the corpus entry as adjacent-context.
- **Narrative**: 4,350 m climbing, Vingegaard-Pogačar duel terrain. Same Massif Central register as the 2026 Stage 9 — the closest recent comparator.
- **Sources**:
  - https://www.dailymotion.com/video/x90ywby (ASO highlights)

#### 2025 — Stage 10: Ennezat → Le Mont-Dore Puy de Sancy (163 km)

*Adjacent context — design-phase decision flag.* (Le Mont-Dore is 40.79 km from the polyline; deep adjacent — see Phase 2 verification below.)

- **Corridor connection**: Adjacent only. Auvergne-side Massif Central; ~110 km east of Ussel; route did not enter Corrèze.
- **Narrative**: Simon Yates won (Visma) on Bastille Day — a stage with seven cat-2 climbs, the most ever in a single TdF stage. Ben Healy took yellow with a bold ride, becoming the first Irish leader since Stephen Roche; Pogačar nearly cracked Vingegaard. The Massif Central narrative anchor of 2025, equivalent in role to what Stage 9-2026 will be for its year.
- **Sources**:
  - https://www.procyclingstats.com/race/tour-de-france/2025/stage-10/result/
  - https://lanternerouge.com/2025/07/14/pogacar-nearly-drops-vingegaard-before-the-big-mountains-tour-de-france-2025-stage-10/
  - https://www.auvergnevolcansancy.com/en/tour-de-france-2025-ennezat-le-mont-dore-puy-de-sancy/

#### 2026 — Stage 10: Aurillac → Le Lioran

- **Corridor connection**: Already in `data/historical-tdf.json`. Day-after-Stage-9 Cantal stage on the same Massif Central terrain as the 2024 Stage 11 finale (where Vingegaard beat Pogačar in a photo finish).
- **Narrative**: Provides immediate continuity with Stage 9: the peloton arrives in Ussel, sleeps, and races south-east into the Cantal volcanoes the next day. The Corrèze stays in the camera frame.
- **Sources**: route announcement at letour.fr 2025-10.

### Tour de France Femmes

#### 2023 Femmes — Stage 2: Clermont-Ferrand → Mauriac (151.7 km)

*Adjacent context — design-phase decision flag.* (Bort-les-Orgues is 20.93 km from the polyline; adjacent — see Phase 2 verification below.)

- **Corridor connection**: Adjacent only. Race passed near Bort-les-Orgues (Corrèze) at km ~100 of the stage but Bort is 20.93 km from the Stage 9-2026 polyline. Mauriac finish is in Cantal.
- **Narrative**: Liane Lippert (Movistar) won the uphill sprint on Côte de Trébiac; Lotte Kopecky retained yellow after a six-KOM hilly day. 2023 was the first TdF Femmes Grand Départ from Clermont-Ferrand and the only Femmes edition through 2025 to brush corridor geography. 2022, 2024, and 2025 Femmes routes had no corridor relevance (Brittany, Netherlands, eastern France).
- **Sources**:
  - https://www.cyclingstage.com/tour-de-france-femmes-2023/stage-2-tdf-2023-women/
  - https://www.procyclingstats.com/race/tour-de-france-femmes/2023/stage-2

### Verified historical claim

#### Ussel has never been a Tour de France stage town

Two independent ledicodutour.com pages confirm this:
- The Corrèze department page lists Ussel under "Eight Stage Towns" but with **no entry pre-2026** (the page tracks 1947-2026).
- The main statistics page (`/statistiques/villes_etapes.html`) does not contain Ussel in the host-city statistics table at all.

Ussel hosted the Tour du Limousin 11 times (Moncoutié 2001, Castaing 1985, Chalmel 1980) and the Grand Prix d'Ussel (Molinéris 1953, Koblet 1955) but never the Tour de France itself. **The 2026 Stage 9 finish on Avenue Thiers / Place Voltaire is genuinely Ussel's first Tour stage.** This is the single strongest fact in the corpus for narrative purposes.

The dedicated Ussel page at `/villes_etapes/villes_u/ussel.htm` returns 404; the URL pattern was not exhausted. The statistics-page absence is strong enough on its own.

- **Sources**:
  - https://www.ledicodutour.com/departements/departements_c/correze.html
  - https://www.ledicodutour.com/statistiques/villes_etapes.html

## Regional races

### Tour du Limousin

The Tour du Limousin was founded in 1968 as an amateur stage race for the Limousin region (Haute-Vienne, Corrèze, Creuse). Amateur 1968-1974, professional from 1975, UCI 2.1 from 2005 (briefly 2.HC 2011-2012). Renamed to Tour du Limousin-Nouvelle-Aquitaine in 2018, then Tour du Limousin-Périgord-Nouvelle-Aquitaine in 2021 to acknowledge a regular Dordogne stage. Has run 58 editions through 2025; final stage finishes in Limoges every year since 1980. The 2026 edition is announced for 18-21 August 2026; full parcours not yet published.

**Bernard Hinault won in 1976 and 1977** — back-to-back wins as a 21- and 22-year-old neo-pro on Gitane, before any of his five Tours. Hinault has on the record described the race as formative ("Le Tour du Limousin, ça représente beaucoup," ICI Limousin).

**Other notable winners**: Marc Madiot (1981), Charly Mottet (1987, 1993), Andrei Tchmil (1995), Laurent Brochard (1996), Stéphane Heulot (1999), Pierrick Fédrigo (2004, 2007), Sébastien Hinault (2008 — Bernard's nephew), Sonny Colbrelli (2015), Warren Barguil (2021), Romain Grégoire (2023, GC at age 20). No GC winner identified as Corrèze-born.

#### Tour du Limousin corridor stages

- **1979 Stage 5**: Tulle → Tulle (165 km, final stage). seg 10. Full Corrèze circuit.
- **1987 Stage 4**: Tulle → Limoges (final stage). seg 10 start. Won by Kim Andersen; Charly Mottet won the GC.
- **1997 Stage 2**: Le Moutier-d'Ahun → Tulle. seg 10 finish. Won by Frédéric Guesdon ahead of Magnien and Piziks.
- **2009 Stage 1**: Limoges → Ussel (159.6 km). **seg 27 (Ussel finish — same finish town as 2026 TdF Stage 9).** Borut Božič (Vacansoleil) took the opening jersey; Mathieu Perget won the GC. The 2009 Limoges → Ussel routing is the closest precedent for the 2026 TdF Stage 9 finish line.
- **2023 Stage 3**: Sarran → Bort-les-Orgues (195.5 km). *Adjacent — Sarran 9.98 km from polyline, Bort-les-Orgues 20.93 km from polyline.* Romain Grégoire won the stage and the GC.
- **2024 Stage 3**: La Rivière de Mansac → Argentat-sur-Dordogne. La Rivière de Mansac is in the Brive agglomeration ~15 km west of Brive (segs 1-2 vicinity). Won by Jefferson Cepeda solo from 10 km out; Alex Baudin won the GC.
- **2025 Stage 3**: Saint-Jal → Masseret (182.7 km). Saint-Jal is ~12 km north of Tulle, on the plateau between segs 12 and 15. Won by Paul Lapeira; Ewen Costiou won the GC.

The Tour du Limousin is the corridor's "regular cycling life" — most years the only professional race on these roads. Brive itself has not been confirmed as a Tour du Limousin start / finish town; the Brive agglomeration has hosted via La Rivière de Mansac (2009, 2024) and Donzenac / Malemort are referenced in passing.

- **Sources**:
  - https://en.wikipedia.org/wiki/Tour_du_Limousin
  - https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine
  - https://www.procyclingstats.com/race/tour-du-limousin
  - https://tourdulimousin.com/
  - https://www.ici.fr/emissions/ici-limousin-sport/bernard-hinault-quintuple-vainqueur-du-tour-de-france-le-tour-du-limousin-ca-represente-beaucoup-5013613
  - https://fr.wikipedia.org/wiki/Tour_du_Limousin_2009
  - https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine_2023
  - https://www.cyclingnews.com/races/tour-du-limousin-perigord-nouvelle-aquitaine-2025/stage-3/results/

### Paris-Corrèze

Paris-Corrèze ran annually 2001-2012, created by 1983/1984 Tour de France winner **Laurent Fignon** with Corrézien motorsport champion Max Mamers and the Conseil général de la Corrèze. UCI 2.4 in 2001, 2.3 in 2002, UCI Europe Tour 2.1 from 2005. Inaugural edition late September 2001; from 2005 moved to early August and reduced from three stages to two. The race did not run in 2013 due to insufficient budget and has not been organised since.

From the 2005 edition onward, the final stage closed with five laps of the historic **Bol d'Or des Monédières circuit at Chaumeil** — explicitly preserving the legacy of the post-Tour criterium (1952-2002) that Robic, Coppi, Anquetil, Hinault, Fignon, and Virenque had ridden. **Chaumeil — segment 15 in our scheme — was the spiritual home of the race**, not Ussel.

#### Paris-Corrèze editions with confirmed corridor finishes (post-2005)

- **2007 Stage 2**: Vigeois → Chaumeil (159.4 km). Edvald Boasson Hagen (Maxbo Bianchi) won the stage and the GC at age 20, also winning Stage 1.
- **2008 Stage 2**: Brive → Chaumeil (161.7 km). Brive start (segs 1-2), Chaumeil finish (seg 15). Stage won by Lloyd Mondory (AG2R); GC to Miyataka Shimizu.
- **2009 Stage 2**: Tulle → Chaumeil (147.6 km). Tulle start (seg 10), Chaumeil finish (seg 15). **Strongest corridor overlap of any edition** — entire stage on the corridor. Stage won by Wesley Sulzberger; GC to Francisco Ventoso.
- **2010 Stage 2**: closing at Chaumeil (seg 15). GC to Mickaël Buffaz.
- **2011 Stage 2**: Objat → Chaumeil (178.7 km, seg 15). Objat is just west of Brive (off-route). GC to Samuel Dumoulin.
- **2012 Stage 2**: Objat → Chaumeil (170.2 km, seg 15). Final edition. GC to Egoitz García.

For 2001-2006 stage routes, authoritative finish-town data was not surfaced; the Bol d'Or article asserts the Chaumeil finish from 2005 onward. Pre-2005 finish locations remain unverified.

#### #503 keying recommendation

Phase 2 verification (computed Session 2): Chaumeil at (45.4555541, 1.8808583) lies **35 m from the Stage 9 polyline at km 100.30** — comfortably inside seg 15 (km 98-106 per `data/segments.json`).

The existing `data/historical-tdf.json` keys Paris-Corrèze to `[25, 26, 27]`. Segs 25-27 are the Ussel approach + finish (~80 km from Chaumeil) — the keying is wrong both by polyline position and by the documented finish-town record. **Recommendation: re-key to `[15]`.** The JSON edit belongs to whichever strand resolves [#503](https://github.com/gneeek/tdf26/issues/503); this dossier produces the recommendation only. The full draft comment is in §Carryforwards below.

- **Sources**:
  - https://en.wikipedia.org/wiki/Paris%E2%80%93Corr%C3%A8ze
  - https://fr.wikipedia.org/wiki/Paris-Corr%C3%A8ze
  - https://en.wikipedia.org/wiki/Bol_d%27Or_des_Mon%C3%A9di%C3%A8res
  - https://autobus.cyclingnews.com/road.php?id=road%2F2007%2Faug07%2Fcorreze07%2Fcorreze072 (2007 archive)
  - https://cqranking.com/men/asp/gen/race.asp?raceid=8246 (2008 results)
  - https://www.cyclingnews.com/races/9th-paris-correze-2-1/race-history/ (2009)
  - https://www.cyclingnews.com/races/10th-paris-correze-2-1/stage-1/results/ (2010)

### L'Agglomérée 2026

L'Agglomérée 2026 was held **Saturday 4 - Sunday 5 April 2026** in the Tulle agglomeration. The cyclosportive ran Sunday morning, starting 09:15. Two cyclo timed distances (85 km and 105 km) plus three cyclotourisme distances (65 / 85 / 105 km), a Verticale (1.1 km / 152 m D+) on Saturday, an Agglo Nature trail (12 / 23 km), VTT, and hiking. **40 km of every cyclo course were on the actual 2026 Tour de France Stage 9 route, including the Suc au May climb.** Tulle agglo's post-event communiqué reports ~1,800 participants and 350 volunteers.

Per-distance podium data for the 2026 edition was not surfaced — the official results portal at `lagglomeree.agglo-tulle.fr` was 500-erroring during research (one month after the event). 2025 edition baseline (6 April 2025, 110 km): Robin Bourdier won in 02:47:38, Alexis Delrieu (02:50:01), Guel Faure (02:50:10); women's overall Annerose Alicot 03:12:08; 235 finishers.

The hook for /tour-history is exact: **the same week the tdf26 blog began publishing (week of 5 April 2026), roughly 1,800 amateurs rode 40 km of the same Stage 9 tarmac the WorldTour peloton will use 12 July 2026 — including the Suc au May climb that anchors segments 14-15 of the travelogue. They got there 99 days first.** The local cycling community has been riding the corridor as a stewardship event since 2023; Tulle Cyclisme Compétition (organising club, alongside Cercle Laïque Tulliste Vélo and Club Rando Cyclo Chamboulive) keeps the road in a way the ASO does not.

CC-licensed imagery for L'Agglomérée: **none surfaced.** No Wikimedia Commons category exists. If imagery is wanted on the eventual page, the publisher should ask Tulle Cyclisme Compétition or Tulle agglo communications for written release on a small selection.

- **Sources**:
  - https://lagglomeree.agglo-tulle.fr/
  - https://www.tulleagglo.fr/actualites/lagglomeree-revient-les-4-5-avril-2026/
  - https://www.velo-ouest.com/saison-2025/resultats-2025/cyclosportive-l-agglomeree.html (2025 results)
  - https://www.directvelo.com/equipe/2271/tulle-cyclisme-competition

## Famous Corrèze riders

The honest finding: **the Corrèze has produced no Tour de France winner, no stage winner, no maillot jaune.** Tulle Cyclisme Compétition, the L'Agglomérée sportive, and the Bol d'Or des Monédières at Chaumeil make the corridor cycling-aware, but as a *consumer* of Tour-de-France glamour, not a producer of champions. The natural framing is "cycling parish, not cycling powerhouse."

#### Alain De Carvalho (1953-)

- **Birthplace**: Ussel, Corrèze.
- **Career**: Professional 1977-1982 (Flandria-Velda 1977; Fiat 1978-79; Puch-Sem-Campagnolo 1980; Puch-Wolber 1981; Wolber-Spidel 1982).
- **Tour de France**: 4 starts. 1978 — 48th GC; 1979 — 55th; 1980 DNF stage 12; 1981 — 53rd. No stage wins, no jersey days.
- **Hook**: The only Tour de France finisher born in the corridor that the 2026 Stage 9 actually traverses. Post-career he opened a bike shop in Pompadour and revived the Grand Prix de Pompadour as the Trophée Alain De Carvalho — the living link between the département's pro past and current talent pipeline.
- **Image**: Wikimedia Commons returns no results for "Alain De Carvalho cyclist." If the eventual page wants imagery, source from local cycling clubs under explicit licence.
- **Sources**: https://en.wikipedia.org/wiki/Alain_De_Carvalho ; https://fr.wikipedia.org/wiki/Alain_De_Carvalho

#### Claude Mazeaud (1937-)

- **Birthplace**: Vignols, Corrèze (rural commune between Pompadour and Objat).
- **Career**: Professional 1962-1964 (Mercier-BP-Hutchinson 1962-63 — the Poulidor team; Margnat-Paloma-Dunlop 1964); independent before and after.
- **Tour de France**: Never started. Best result: 1961 Champion de France des Indépendants; 1966 Grand Prix de Plouay (his self-described biggest win, riding as an independent).
- **Hook**: Reached pro level on the same team as Poulidor but never made a Tour roster — the more typical fate of pre-corporate-era riders from a non-cycling département.
- **Image**: Wikimedia returns nothing; FR-Wikipedia article explicitly invites a free-licence image.
- **Sources**: https://fr.wikipedia.org/wiki/Claude_Mazeaud ; https://www.memovelo.com/claude-mazeaud

#### Riders strongly associated with the corridor (not Corrèze-born)

**Raymond Poulidor (1936-2019)** — born Masbaraud-Mérignat in adjacent Creuse but the regional figurehead. 14 Tour starts, 12 finishes; 3× 2nd, 5× 3rd; 7 stage wins; **never wore yellow** ("L'Éternel Second"). Won the Bol d'Or des Monédières at Chaumeil in 1963, 1966, 1967. For Stage 9 commentary, the entire Limousin corridor *is* Poulidor country.

**Albert Bourlon (1916-2013)** — born Sancergues (Cher), but won the inaugural Grand Prix de Pompadour (Corrèze) in 1949. Holds the still-standing Tour record for longest solo breakaway: 253 km, Carcassonne-Luchon, 1947 Tour, ~8h10m at 31 km/h.

**Frédéric Brun (1957-2025)** — born Ribérac (Dordogne, adjacent). Won the Bol d'Or des Monédières at Chaumeil in 1988, multiple podiums 1984-86. 9 Tour starts.

#### Adjacent-department riders

*Adjacent context — design-phase decision flag.*

- **Luc Leblanc (1966-)** — Limoges, Haute-Vienne. World Road Champion 1994; 1991 wore yellow 3 days; 1994 Stage 12 winner at Hautacam beating Indurain in fog; 1994 Tour 4th. Won Tour de la Corrèze 1986 as an amateur; mentored by Poulidor. **The 2025 Tour renamed the Hautacam climb "montée Luc Leblanc."** Wikimedia Category:Luc_Leblanc has multiple CC BY-SA race photos.
- **Antonin Magne (1904-1983)** — Ytrac, Cantal. 2× Tour winner (1931, 1934). Won the Tour de la Corrèze 1929. Souvenir Antonin Magne held annually in the Aurillac / Limousin corridor.
- **Marc Durant (1955-)** — Saint-Sulpice-le-Guérétois, Creuse. 5 Tour starts (1981-85); best GC 30th in 1983.

The four-name corridor spine — **De Carvalho, Mazeaud, Brun, Leblanc** — covers 1962 to 1998 and lets the page tell a 36-year cycling-parish story without overreaching. Poulidor anchors the 1960s, Leblanc the 1990s, De Carvalho fills the gap. The Bol d'Or des Monédières at Chaumeil (1952-2002) is the connective tissue: **Robic, Coppi, Géminiani, Poulidor, Hinault, Fignon, Brun, Claveyrolat all rode this circuit on the actual 2026 Stage 9 route.**

## Wartime + post-war (sparingly)

**1942 — Circuit de France clipped Limoges.** Vichy-era propaganda race organised after Goddet refused to restart the Tour. Stage 3 (Limoges → Clermont-Ferrand, 163 km) crossed the northern Limousin. The corridor's nearest brush with stage-race cycling under occupation. (Detail in §Per-event corpus above.)

**1947 — first post-war Tour bypassed the corridor.** Despite reconciliation themes, the route ran the periphery and did not visit Limousin or Corrèze. The corridor had to wait. (Detail in §Per-event corpus above.)

Per publisher decision 2026-05-07 and subagent E recommendation: **do not write the 1996 Bastille Day Tulle stage as a Tulle-massacre commemoration.** No source supports the framing. The Massif Central mythology material (Tour treats it as "iconic but eccentric," not as the holy mountains alongside Alps and Pyrenees) is too thin for a section of its own; if the page wants it, a single sentence inside broader copy is the right register.

## Story arcs (design-phase menu)

Six candidate arcs; ranked best-first. Final selection deferred to design-phase planning.

### 1. Bol d'Or des Monédières as connective tissue (RECOMMENDED)

Robic, Coppi, Géminiani, Poulidor, Hinault, Fignon, Brun, Claveyrolat all rode the Chaumeil criterium on the actual 2026 Stage 9 route 1952-2002. Paris-Corrèze 2005-2012 inherited the same finish circuit (six confirmed editions at Chaumeil). The 2026 Stage 9 ascends the Suc au May 2 km from the Bol d'Or finish line at Chaumeil. **A 70-year continuous tradition that the 2026 Stage 9 is the latest chapter of, not an interruption of.** This is the strongest single arc the research surfaced — it ties seg 15 (the corridor's spiritual centre) to a roster of names the public knows, on roads they actually rode. The hero candidate `Le_sud_des_Monédières_vers_Chaumeil.JPG` (CC BY-SA 3.0, Babsy 2013) is a natural visual anchor.

### 2. Ussel's first Tour (RECOMMENDED)

Verified historical claim (two independent ledicodutour sources): Ussel has never been a Tour de France stage town. The 2009 Tour du Limousin opened with Limoges → Ussel, 159.6 km, won by Borut Božič — that's the closest precedent for the same finish line, at smaller scale, 17 years earlier. The 2026 Stage 9 finish on Avenue Thiers / Place Voltaire is genuinely Ussel's first appearance. **The finish-town narrative is intrinsically about waiting and arrival**, which fits a travelogue published over April-July 2026 building toward 12 July. Ussel hosted the Grand Prix d'Ussel in the 1950s (Molinéris 1953, Koblet 1955) and the Tour du Limousin 11 times — but the Tour proper is new.

### 3. The corridor's home circuit (RECOMMENDED)

The Tour du Limousin runs in mid-to-late August every year through these same roads. Hinault's 1976 and 1977 wins as a 21- and 22-year-old neo-pro on Gitane were the launching pad for his five Tour titles — formative wins on Stage 9 corridor roads. Marc Madiot, Charly Mottet, Pierrick Fédrigo, Sébastien Hinault (Bernard's nephew), Warren Barguil, Romain Grégoire all in the roll of honour. **The Tour de France is the rare tourist; the Tour du Limousin is the resident.** Frame Stage 9 2026 as the moment the resident's bigger cousin finally drops by, with the 2009 Tour du Limousin Limoges → Ussel as the exact-same-finish-line precedent.

### 4. Cycling parish, not cycling powerhouse

The Corrèze produced Alain De Carvalho (Ussel, 1978-81, four Tour finishes outside the top 45) and Claude Mazeaud (Vignols, Mercier 1962-64, never a Tour starter) — and that is the entire pro-cycling roster. Tulle Cyclisme Compétition, the L'Agglomérée sportive, and the Bol d'Or des Monédières at Chaumeil are all consumer-facing, not producer-facing. **The honest framing is scarcity:** the corridor is cycling-aware, intermittently visited, never the protagonist. Poulidor (Creuse-born) and Leblanc (Haute-Vienne) are the regional figureheads, both adjacent-department. This arc is the best fit if the publisher wants a tonally honest page rather than a triumphalist one. Lower-ranked here only because arcs 1-3 are stronger story material; cycling-parish is the *register* that sits underneath whichever arc is foregrounded.

### 5. The amateur came first

L'Agglomérée 4-5 April 2026, ~1,800 amateurs riding 40 km of the actual Stage 9 route 99 days before the pros. Same Suc au May climb that anchors segs 14-15. Tulle Cyclisme Compétition (organising club) as the road's actual steward. Lower-ranked because (a) the page launches in or after April 2026 so the arc becomes a lookback rather than a lookforward, and (b) the lack of CC-licensed L'Agglomérée imagery limits the page's visual options on this beat. Useful as a sidebar inside a larger arc.

### 6. Wartime + post-war framing

1942 Circuit de France clipped Limoges under Vichy propaganda; 1947 first post-war Tour bypassed the corridor. The corridor had to wait for the Tour to come. Per subagent E's recommendation, use sparingly — one paragraph each, not a section of their own. Lowest-ranked because the historical connection to the corridor is geographically weak (Limoges is in adjacent Haute-Vienne; both stages bypass the actual segs 1-26) and the framing risks tonal conflict with arcs 1-3. Worth keeping as a textual aside; not worth foregrounding.

**Top-3 ranked recommendation for design-phase decision: Bol d'Or des Monédières (arc 1) + Ussel's first Tour (arc 2) + The corridor's home circuit (arc 3), with cycling-parish (arc 4) as the underlying register and the amateur-came-first (arc 5) as a sidebar.** Wartime framing (arc 6) optional, one paragraph at most.

## Hero-image candidates (design-phase menu)

Five candidates with verified licences (one image per source category to give the design phase a real range). Per `reference_wikimedia_thumb_widths.md`: each entry records the File: page URL; no thumb width is asserted. Eventual rendering happens at draft phase.

### Candidate 1: Le sud des Monédières vers Chaumeil (RECOMMENDED for arc 1)

- **File**: https://commons.wikimedia.org/wiki/File:Le_sud_des_Mon%C3%A9di%C3%A8res_vers_Chaumeil.JPG
- **Licence**: CC BY-SA 3.0 Unported (verified 2026-05-07).
- **Attribution**: Babsy / CC BY-SA 3.0 / Wikimedia Commons.
- **Date**: 17 May 2013.
- **Original dimensions**: 3,456 × 2,304 px.
- **Segment relevance**: seg 15 (Chaumeil) viewed from Suc au May (segs 14-15). The exact view a rider has at the corridor's spiritual centre.
- **Why hero**: Anchors arc 1 (Bol d'Or as connective tissue) directly. Landscape framing with the village visible across the rolling Monédières — implies "this is the place," "this is where it always finishes."

### Candidate 2: Plateau limousin depuis le Suc au May (RECOMMENDED for arc 1 or arc 3)

- **File**: https://commons.wikimedia.org/wiki/File:Plateau_limousin_depuis_le_Suc_au_May.JPG
- **Licence**: CC BY-SA 3.0 Unported (verified 2026-05-07).
- **Attribution**: Babsy / CC BY-SA 3.0 / Wikimedia Commons.
- **Date**: 17 May 2013.
- **Original dimensions**: 3,456 × 2,304 px.
- **Segment relevance**: seg 14-15. Wide vista from Suc au May summit (908 m), the climb's payoff view.
- **Why hero**: Same photographer as Candidate 1, taken the same day; gives the design phase a wider-vista alternative that emphasises "open country." Stronger fit if the page foregrounds arc 3 (home-circuit / Tour du Limousin terrain) rather than arc 1 (specifically Chaumeil).

### Candidate 3: Passage Tour de France 2020 (Suc au May)

- **File**: https://commons.wikimedia.org/wiki/File:Passage_Tour_de_France_2020.jpg
- **Licence**: CC BY-SA 4.0 (verified 2026-05-07).
- **Attribution**: GAFUCRU / CC BY-SA 4.0 / Wikimedia Commons.
- **Date**: 26 July 2020.
- **Original dimensions**: 2,724 × 2,393 px.
- **Segment relevance**: seg 14-15 (Suc au May, 908 m). The 2020 Stage 12 Hirschi-breakaway-day passage of the corridor.
- **Why hero**: Live race-day photo on the actual climb that anchors the 2026 Stage 9 finish. Strongest fit for any layout that wants a "this is what race-day at Suc au May looks like" hero. Lower-ranked than Candidates 1-2 only because the framing is documentary-photographer rather than landscape-photographer; the Babsy panoramas read more like a magazine cover, the GAFUCRU shot reads more like a news image.

### Candidate 4: Les Monédières (panorama)

- **File**: https://commons.wikimedia.org/wiki/File:Les_Mon%C3%A9di%C3%A8res.jpg
- **Licence**: Free Art License (FAL) — copyleft, free for commercial and non-commercial use including redistribution and modification (verified 2026-05-07).
- **Attribution**: Phiffou / FAL / Wikimedia Commons.
- **Date**: 19 November 2004 (uploaded 27 August 2007).
- **Original dimensions**: 4,687 × 3,141 px (largest of any candidate).
- **Segment relevance**: segs 14-15 (Massif des Monédières range).
- **Why hero**: Highest-resolution candidate; sweeping range overview. FAL licence is more permissive than CC BY-SA but unfamiliar to many designers — flag the licence type to the publisher at design phase.

### Candidate 5: Raymond Poulidor portrait (Brive 2011 or 2012 signing)

- **File**: https://commons.wikimedia.org/wiki/File:Raymond_Poulidor_-_IMG_1906_(cropped)_(cropped).JPG
- **Licence**: CC BY-SA 3.0 (verified 2026-05-07).
- **Attribution**: Poudou99 / CC BY-SA 3.0 / Wikimedia Commons.
- **Date**: 3 April 2012.
- **Original dimensions**: 1,643 × 1,857 px.
- **Segment relevance**: regional figurehead; not segment-specific. Poulidor won the Bol d'Or des Monédières at Chaumeil in 1963, 1966, 1967 — so the figure connects to seg 15.
- **Why hero**: Best fit if the page leads on arc 4 (cycling parish) with Poulidor as the named anchor figure. Lower-ranked than landscape candidates because it's a 2012 signing-table portrait rather than racing imagery; the design phase will likely prefer landscape, but Poulidor-as-hero is a real option.

**Bol d'Or des Monédières Wikimedia category was opened during synthesis: it does not exist** (Commons search for "Bol d'Or des Monédières" returns no results; the EN Wikipedia article has zero photos). Period race photos likely exist in *L'Équipe* / Presse Sports archives but those are all-rights-reserved. **No CC-licensed Bol d'Or race imagery surfaced.** If the publisher wants Bol-d'Or-specific race photos rather than landscape proxies, the path is direct contact with Tulle Cyclisme Compétition / Cercle Laïque Tulliste Vélo / Club Rando Cyclo Chamboulive for archive photos under explicit release.

## Sources (consolidated)

Single deduped list grouped by topic. Bullets only.

### Corridor TdF stages (men's + Femmes)

- https://www.bikeraceinfo.com/tdf/tdf1951.html
- https://www.bikeraceinfo.com/tdf/tdf1964.html
- https://www.bikeraceinfo.com/tdf/tdf1969.html
- https://www.bikeraceinfo.com/tdf/tdf1973.html
- https://www.bikeraceinfo.com/tdf/tdf1976.html
- https://www.bikeraceinfo.com/tdf/tdf1987.html
- https://www.bikeraceinfo.com/tdf/tdf1998.html
- https://www.bikeraceinfo.com/tdf/tdf2001.html
- https://bikeraceinfo.com/tdf/2020-TDF-daily/tdf2020-stage-12.html
- https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html
- https://www.ledicodutour.com/villes_etapes/villes_t/tulle.htm
- https://www.ledicodutour.com/departements/departements_c/correze.html
- https://www.ledicodutour.com/statistiques/villes_etapes.html
- https://en.wikipedia.org/wiki/1947_Tour_de_France
- https://en.wikipedia.org/wiki/1976_Tour_de_France
- https://en.wikipedia.org/wiki/1996_Tour_de_France,_Stage_11_to_Stage_21
- https://en.wikipedia.org/wiki/1998_Tour_de_France,_Prologue_to_Stage_11
- https://en.wikipedia.org/wiki/2016_Tour_de_France
- https://www.procyclingstats.com/race/tour-de-france/1998/stage-7
- https://www.procyclingstats.com/race/tour-de-france/2001/stage-16/
- https://www.procyclingstats.com/race/tour-de-france/2012/stage-18
- https://www.procyclingstats.com/race/tour-de-france/2020/stage-12
- https://www.procyclingstats.com/race/tour-de-france/2023/stage-8
- https://www.procyclingstats.com/race/tour-de-france/2025/stage-10/result/
- https://www.procyclingstats.com/race/tour-de-france-femmes/2023/stage-2
- https://www.cyclingstage.com/tour-de-france-2016-route/stage-5-tdf-2016/
- https://www.cyclingstage.com/tour-de-france-2023-route/stage-8-tdf-2023/
- https://www.cyclingstage.com/tour-de-france-femmes-2023/stage-2-tdf-2023-women/
- https://www.cyclingnews.com/races/tour-de-france-2020/stage-12/results/
- https://lanternerouge.com/2025/07/14/pogacar-nearly-drops-vingegaard-before-the-big-mountains-tour-de-france-2025-stage-10/
- https://www.auvergnevolcansancy.com/en/tour-de-france-2025-ennezat-le-mont-dore-puy-de-sancy/
- http://www.memoire-du-cyclisme.eu/eta_tdf_1970_1979/tdf1976_19.php

### Tour du Limousin

- https://en.wikipedia.org/wiki/Tour_du_Limousin
- https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine
- https://fr.wikipedia.org/wiki/Tour_du_Limousin_1976
- https://fr.wikipedia.org/wiki/Tour_du_Limousin_2009
- https://fr.wikipedia.org/wiki/Tour_du_Limousin-P%C3%A9rigord-Nouvelle-Aquitaine_2023
- https://www.procyclingstats.com/race/tour-du-limousin
- https://www.procyclingstats.com/race/tour-du-limousin/1979/gc
- https://www.procyclingstats.com/race/tour-du-limousin/1987/gc/result/result
- https://www.procyclingstats.com/race/tour-du-limousin/1997/stage-2/result/result
- https://www.procyclingstats.com/race/tour-du-limousin/2024/stage-3
- https://www.procyclingstats.com/rider/pierrick-fedrigo
- https://tourdulimousin.com/
- https://tourdulimousin.com/les-etapes-2024/
- https://www.cyclingnews.com/races/42nd-tour-du-limousin-2-1/stage-1/results/
- https://www.cyclingnews.com/races/tour-du-limousin-perigord-nouvelle-aquitaine-2025/stage-3/results/
- https://www.directvelo.com/actualite/99818/
- https://www.directvelo.com/actualite/115025/tour-du-limousin-et-3-jefferson-cepeda-1er
- https://www.brive-tourisme.com/en/blog-en/the-tour-of-limousin/
- https://www.velowire.com/article/183/en/exclusive--the-stages-of-the-tour-du-limousin-2009-in-google-maps-google-earth-and-the-participating-teams.html
- https://decathlonag2rlamondialeteam.com/en/paul-lapeira-remporte-la-3e-etape-du-tour-du-limousin/
- https://france3-regions.franceinfo.fr/nouvelle-aquitaine/correze/brive/tour-du-limousin-2025-suivez-en-direct-l-arrivee-de-la-troisieme-etape-en-correze-3178875.html
- https://www.ici.fr/emissions/ici-limousin-sport/bernard-hinault-quintuple-vainqueur-du-tour-de-france-le-tour-du-limousin-ca-represente-beaucoup-5013613

### Paris-Corrèze

- https://en.wikipedia.org/wiki/Paris%E2%80%93Corr%C3%A8ze
- https://fr.wikipedia.org/wiki/Paris-Corr%C3%A8ze
- https://en.wikipedia.org/wiki/Bol_d%27Or_des_Mon%C3%A9di%C3%A8res
- https://autobus.cyclingnews.com/road.php?id=road%2F2007%2Faug07%2Fcorreze07%2Fcorreze072
- https://cqranking.com/men/asp/gen/race.asp?raceid=8246
- https://www.cyclingnews.com/races/9th-paris-correze-2-1/race-history/
- https://www.cyclingnews.com/races/10th-paris-correze-2-1/stage-1/results/
- https://www.procyclingstats.com/race/paris-correze/2011
- https://www.procyclingstats.com/race/paris-correze/2012/stage-2

### L'Agglomérée 2026

- https://lagglomeree.agglo-tulle.fr/
- https://www.tulleagglo.fr/actualites/lagglomeree-revient-les-4-5-avril-2026/
- https://www.velo-ouest.com/saison-2025/resultats-2025/cyclosportive-l-agglomeree.html
- https://www.directvelo.com/equipe/2271/tulle-cyclisme-competition

### Riders / Corrèze cycling biography

- https://en.wikipedia.org/wiki/Alain_De_Carvalho
- https://fr.wikipedia.org/wiki/Alain_De_Carvalho
- https://veloquercy.over-blog.com/2026/02/le-trophee-alain-de-carvalho-a-pompadour.html
- https://fr.wikipedia.org/wiki/Claude_Mazeaud
- https://www.memovelo.com/claude-mazeaud
- https://www.cyclisme-en-limousin.fr/coureur.php?id_coureur=8708
- https://en.wikipedia.org/wiki/Raymond_Poulidor
- https://en.wikipedia.org/wiki/Albert_Bourlon
- https://www.velo18.net/bourlon.html
- https://fr.wikipedia.org/wiki/Fr%C3%A9d%C3%A9ric_Brun_(cyclisme,_1957)
- https://en.wikipedia.org/wiki/Luc_Leblanc
- https://en.wikipedia.org/wiki/Antonin_Magne
- https://en.wikipedia.org/wiki/Marc_Durant

### Wartime + post-war

- https://fr.wikipedia.org/wiki/Circuit_de_France
- https://www.franceinfo.fr/tour-de-france/hommes/cyclisme-en-1942-sous-l-occupation-le-circuit-de-france-a-la-place-du-tour-de-france-pour-servir-la-propagande-de-vichy_5906849.html
- https://fr.wikipedia.org/wiki/Grand_Prix_du_Tour_de_France
- https://en.wikipedia.org/wiki/Tour_de_France_during_World_War_II
- https://en.wikipedia.org/wiki/Tulle_massacre
- https://en.wikipedia.org/wiki/Tour_de_France_records_and_statistics
- https://www.warhistoryonline.com/war-articles/tour-de-france.html
- https://origins.osu.edu/milestones/tour-de-france-and-yellow-jersey
- https://road.cc/content/feature/iconic-puy-de-dome-returns-tour-after-35-years-302331
- https://www.cyclist.co.uk/in-depth/tour-de-france-history-anquetil-and-poulidor-go-head-to-head
- https://www.jstor.org/stable/jj.18736045 (Christopher Thompson, *The Tour de France: A Cultural History*, UC Press 2006)

### Wikimedia Commons categories (image sourcing)

- https://commons.wikimedia.org/wiki/Category:Tour_du_Limousin
- https://commons.wikimedia.org/wiki/Category:Tour_du_Limousin_maps
- https://commons.wikimedia.org/wiki/Category:Chaumeil
- https://commons.wikimedia.org/wiki/Category:Suc_au_May
- https://commons.wikimedia.org/wiki/Category:Massif_des_Mon%C3%A9di%C3%A8res
- https://commons.wikimedia.org/wiki/Category:Ussel_(Corr%C3%A8ze)
- https://commons.wikimedia.org/wiki/Category:Raymond_Poulidor
- https://commons.wikimedia.org/wiki/Category:Luc_Leblanc
- https://commons.wikimedia.org/wiki/Category:Antonin_Magne

### Video sources

- https://www.dailymotion.com/video/x7zl61i (2020 Stage 12 ASO highlights — Hirschi)
- https://www.youtube.com/watch?v=WAcJxi8tEdA (2020 Stage 12 last km)
- https://www.dailymotion.com/video/x90ywby (2024 Stage 11 highlights — Massif Central)
- https://www.youtube.com/user/TourDuLimousin
- https://www.youtube.com/playlist?list=PL7CF7BC2A560171BF
- https://www.youtube.com/watch?v=jdYIrvDoHaQ (Warren Barguil 2021 winner interview)

## Carryforwards out of scope

### Umbrella issue body draft: "historical-tdf.json corridor expansion"

The publisher decision applied 2026-05-07 is **one umbrella tracker issue**, not individual issues. Draft body below; main session files this after PR open.

```
The /tour-history Session 2 dossier (PR #XXX) surfaced corridor-relevant Tour de France events that are not yet present in `data/historical-tdf.json`. This issue tracks adding them as a batch.

Each item below describes a gap (per `feedback_issues_describe_problems.md`). The data-add itself is a separate strand; this issue is the tracker. Each entry references the dossier's per-event corpus for narrative + segment-keying detail; segment keying uses polyline-distance verification per `feedback_on_route_checks.md`.

On-corridor events:

- [ ] 1951 Stage 10: Clermont-Ferrand → Brive (men's TdF; seg 1; pairs with already-corpus 1951 Stage 11 Koblet solo). Source: https://www.bikeraceinfo.com/tdf/tdf1951.html
- [ ] 1964 Stage 19: Bordeaux → Brive + Stage 20: Brive → Puy-de-Dôme (men's TdF; seg 1; Anquetil-Poulidor Puy-de-Dôme launch pad). Source: https://www.bikeraceinfo.com/tdf/tdf1964.html
- [ ] 1969 Stage 19: Libourne → Brive + Stage 20: Brive → Puy-de-Dôme (men's TdF; seg 1; Hoban + Matignon underdog). Source: https://www.bikeraceinfo.com/tdf/tdf1969.html
- [ ] 1973 Stage 17: Sainte-Foy-la-Grande → Brive + Stage 18: Brive → Puy-de-Dôme (men's TdF; seg 1; Ocaña era). Source: https://www.bikeraceinfo.com/tdf/tdf1973.html
- [ ] 1976 Stage 19: Sainte-Foy-la-Grande → Tulle (men's TdF; seg 10; pairs with already-corpus 1976 Stage 20). Source: https://www.bikeraceinfo.com/tdf/tdf1976.html
- [ ] 1987 Stage 12: Brive → Bordeaux (men's TdF; seg 1; Davis Phinney; pairs with #478's Chaumeil work). Source: https://www.bikeraceinfo.com/tdf/tdf1987.html
- [ ] 1998 Stage 6: La Châtre → Brive (men's TdF; seg 1; Cipollini). Source: https://www.bikeraceinfo.com/tdf/tdf1998.html
- [ ] 1998 Stage 7 ITT: Meyrignac-l'Église → Corrèze town (men's TdF; mid-corridor segs 12-13 vicinity; Ullrich + Festina expulsion). Source: https://www.procyclingstats.com/race/tour-de-france/1998/stage-7
- [ ] 1998 Stage 8: Brive → Montauban (men's TdF; seg 1; Jacky Durand). Source: https://www.bikeraceinfo.com/tdf/tdf1998.html
- [ ] 2001 Stage 17: Brive → Montluçon (men's TdF; seg 1; Serge Baguet). Source: https://www.bikeraceinfo.com/tdf/tdf2001.html
- [ ] Tour du Limousin 1979 Stage 5: Tulle → Tulle (regional race; seg 10).
- [ ] Tour du Limousin 1987 Stage 4: Tulle → Limoges (regional race; seg 10).
- [ ] Tour du Limousin 1997 Stage 2: Le Moutier-d'Ahun → Tulle (regional race; seg 10).
- [ ] Tour du Limousin 2009 Stage 1: Limoges → Ussel (regional race; seg 27 — same finish town as 2026 TdF Stage 9). Source: https://fr.wikipedia.org/wiki/Tour_du_Limousin_2009
- [ ] Tour du Limousin 2024 Stage 3: La Rivière de Mansac → Argentat (regional race; near seg 1).
- [ ] Tour du Limousin 2025 Stage 3: Saint-Jal → Masseret (regional race; corridor-adjacent north of seg 12-15).
- [ ] Paris-Corrèze 2007 / 2008 / 2009 / 2010 / 2011 / 2012 final stages at Chaumeil (regional race; seg 15). The existing `[25, 26, 27]` keying is wrong (see #503 + dossier §Paris-Corrèze); recommendation is to re-key to `[15]` and consider per-edition entries surfacing the 2008 (Brive start) and 2009 (Tulle → Chaumeil corridor-spanning) editions.

Closes when each event has been added to `data/historical-tdf.json` with verified segment keying. The exact polyline-keying for each event is in the dossier's per-event corpus.

Adjacent-only events (2016 Stage 5, 2020 Stage 12, 2023 Femmes Stage 2, 2023 Stages 8-9, 2025 Stage 10, Bort-les-Orgues passages, Sarran finishes, Le Mont-Dore stages) are NOT in this checklist — they are tagged design-phase decision flags in the dossier; the design phase decides whether they earn a `historical-tdf.json` row.
```

### #503 comment draft

Draft below; main session posts this on issue #503 after PR open.

```
Session 2 of the /tour-history feature research dossier (PR #XXX) computed the polyline distance from Chaumeil (data/town-coords.json: 45.4555541, 1.8808583) to the concatenated Stage 9 segment polyline. Result: 35 m at km 100.30, which falls in seg 15 (km 98-106 per data/segments.json).

The Bol d'Or des Monédières was held at Chaumeil 1952-2002, and the Paris-Corrèze 2005-2012 finishes inherited that corridor — six confirmed editions at Chaumeil (2007, 2008, 2009, 2010, 2011, 2012) per Wikipedia and the Bol d'Or article. The existing `[25, 26, 27]` keying does not match either the venue's polyline location or the segments.json km ranges (segs 25-27 are the Ussel approach + finish, ~80 km from Chaumeil).

Recommendation: re-key the Paris-Corrèze entry in `data/historical-tdf.json` from `[25, 26, 27]` to `[15]`. The JSON edit belongs to whichever strand resolves this issue; this is a recommendation only.
```

### Other carryforwards

Research follow-ups that don't belong in the umbrella tracker and aren't story-arc / hero-image / sources concerns:

- **ledicodutour.com Ussel page (404)** — `/villes_etapes/villes_u/ussel.htm` returned 404; the URL pattern wasn't exhausted. The statistics-page absence is strong enough on its own; if the eventual page wants a dedicated source, retry with pattern variations (`/villes-etapes/villes_etapes_u/ussel.html` is the pattern that works for Brive).
- **2026 L'Agglomérée per-distance podiums** — official results portal at `lagglomeree.agglo-tulle.fr` was 500-erroring during research. Retry closer to draft phase.
- **2024 TdF Stage 11 Corrèze touchpoint** — whether the Évaux-les-Bains → Le Lioran route actually crossed Corrèze department was not verified in raw notes. The route map suggests it stayed Creuse / Cantal. Worth a 5-minute confirmation if the corpus entry's segment keying is revisited.
- **2001 TdF Stage 16 routing through Tulle** — Castelsarrasin → Sarran via Tulle is geographically natural but not verified.
- **2001-2006 Paris-Corrèze finish-town data** — pre-Chaumeil era; archive trip needed to L'Équipe / La Montagne if anyone wants per-edition keying.
- **Tour du Limousin: Brive proper as ville-étape** — the Brive Basin agglomeration has hosted via La Rivière de Mansac (2009, 2024); whether Brive itself has been a start / finish town in any specific year was not confirmed. Tour du Limousin official archive at `tourdulimousin.com/parcours/` is the right place to check.
- **CC-licensed L'Agglomérée imagery** — none surfaced. If the eventual page wants imagery, the path is direct contact with Tulle Cyclisme Compétition or Tulle agglo communications under explicit release.
- **CC-licensed Bol d'Or des Monédières imagery** — none surfaced (Wikimedia category does not exist; EN Wikipedia article has zero photos). Same direct-contact path applies.
- **Wikimedia per-file licence verification** — Session 2 verified licences for the 5 hero candidates only. Full verification at draft phase (when more images are pulled in for body copy).
- **Contemporary (2010s-2020s) Corrèze-born WorldTour riders** — initial searches returned Tulle Cyclisme Compétition development riders only. Worth a targeted ProCyclingStats query if access can be arranged.

**CLAUDE.md Cipollini-2008 correction thread is CLOSED.** Subagent A flagged it; end-of-Session-1 grep confirmed the claim is not in CLAUDE.md. No correction filed.

## Verification log

### Phase 2 polyline keying (computed Session 2 by main session)

The raw notes' segment keying is approximate (town-based). The following polyline-distance numbers — computed via `processing/calculate_attraction_positions.py` helpers against the concatenated segment GPX — are authoritative and have been applied throughout the per-event corpus above.

| Coord | nearest_km | distance from polyline | Verdict |
|---|---|---|---|
| Sarran (45.3697, 1.9525) | 98.65 | **9.98 km** | ADJACENT only. The 1999/2001/2020 TdF stage finishes at Sarran are NOT corridor; closest seg is 15 but Sarran is 10 km north of the route. |
| Bort-les-Orgues (45.3997, 2.4944) | 181.92 | **20.93 km** | ADJACENT only. 2023 Femmes Stage 2 passage near Bort is NOT corridor; 21 km NE of Ussel. |
| Le Mont-Dore (45.5775, 2.8094) | 182.04 (end) | **40.79 km** | ADJACENT only. Auvergne mountains, deep adjacent. |
| Chaumeil (45.4555541, 1.8808583) | 100.30 | 35 m | seg 15 (km 98-106). Confirms #503 keying: Paris-Corrèze should re-key from `[25, 26, 27]` to `[15]`. |
| Tulle (45.2678347, 1.7706797) | 68.72 | 121 m | seg 10 (km 64-70). Confirms existing corpus. |

Stage 9 segment km ranges (from `data/segments.json`):
- seg 1: 0-8 (Malemort/Brive)
- seg 10: 64-70 (Tulle)
- seg 14: 92-98
- seg 15: 98-106 (Chaumeil)
- seg 26: 176-182 (Ussel approach)
- seg 27: 182-184.8 (Ussel finish)

**Application rule used during synthesis**: any event keyed in raw notes to "seg X" by town-name was checked against this table. If the town is in this table → verdict here applied. If the town isn't in this table but is on the corridor (Brive, Tulle, Naves, Treignac, Bugeat, Meymac, Ussel) → existing per-segment km range applied. If the town is off-corridor and not in this table → tagged adjacent-only and no segment key claimed.

### URL spot-check

**Session 1 (parent shell `curl -sIL -A "Mozilla/5.0" --max-time 12`)**: 26 / 30 returned HTTP 200. 4 / 30 returned DNS resolution failure — all four `bikeraceinfo.com` URLs (`tdf1951.html`, `tdf1976.html`, `tdf1998.html`, `tdf2001.html`).

**Session 2 (WebFetch re-test)**: All four bikeraceinfo URLs returned `ECONNREFUSED` from the WebFetch resolver as well. The subagents reached these URLs during research via a different path (their tool environment had successful resolution where the parent shell + WebFetch resolver both fail). Fact-claims drawn from these URLs are recorded as the subagents reported them; **dossier policy: treat bikeraceinfo as flaky-but-real**, retain the URL for source-of-record, and where alternatives exist (Wikipedia stage pages, ProCyclingStats stage URLs) the dossier cites both.

The four flaky URLs all have alternative coverage:
- 1951 Stage 10: covered by https://en.wikipedia.org/wiki/1951_Tour_de_France and https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html
- 1976 Stage 19: covered by https://en.wikipedia.org/wiki/1976_Tour_de_France, http://www.memoire-du-cyclisme.eu/eta_tdf_1970_1979/tdf1976_19.php, and https://www.ledicodutour.com/villes_etapes/villes_t/tulle.htm
- 1998 Stage 6/7/8: covered by https://en.wikipedia.org/wiki/1998_Tour_de_France,_Prologue_to_Stage_11 and https://www.procyclingstats.com/race/tour-de-france/1998/stage-7
- 2001 Stage 16: covered by https://www.procyclingstats.com/race/tour-de-france/2001/stage-16/ and https://www.ledicodutour.com/villes-etapes/villes_etapes_b/brive.html

### Hero-image licence verification (Session 2)

- `Le_sud_des_Monédières_vers_Chaumeil.JPG`: CC BY-SA 3.0 Unported (Babsy, 2013-05-17). Verified via Wikimedia file page.
- `Plateau_limousin_depuis_le_Suc_au_May.JPG`: CC BY-SA 3.0 Unported (Babsy, 2013-05-17). Verified.
- `Passage_Tour_de_France_2020.jpg`: CC BY-SA 4.0 (GAFUCRU, 2020-07-26). Verified.
- `Les_Monédières.jpg`: Free Art License — copyleft, free for commercial + non-commercial (Phiffou, photographed 2004-11-19). Verified.
- `Raymond_Poulidor_-_IMG_1906_(cropped)_(cropped).JPG`: CC BY-SA 3.0 (Poudou99, 2012-04-03). Verified.
