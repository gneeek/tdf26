# Reference: Creative Commons Image Sources

Relocated from `CLAUDE.md` (issue #627 context-budget prune). This is cross-cutting operational reference for image sourcing across all segments; no per-segment research dossier owns it. Consult it when selecting images for an entry. `processing/suggest_images.py` automates the Wikimedia Commons geosearch query below.

## Wikimedia Commons Categories (all CC BY-SA)

Primary location categories to query for each segment:

| Segment(s) | Wikimedia Commons Category | Notes |
|------------|---------------------------|-------|
| 1–2 | Category:Malemort, Category:Brive-la-Gaillarde | Town views, river Corrèze |
| 3 | Category:Turenne (Corrèze) | Castle ruins, hilltop village, panoramic views |
| 4 | Category:Collonges-la-Rouge | Extensive collection; red sandstone architecture |
| 5–6 | Category:Beynat | Smaller collection |
| 9–10 | Category:Tulle | River valley, cathedral, town views |
| 11–12 | Category:Naves, Corrèze | Limited |
| 15 | Category:Monédières | Suc au May area, heathland panoramas |
| 17 | Category:Treignac | Medieval bridge, granite town |
| 18–20 | Category:Plateau de Millevaches | Heathland, forests, remote landscapes |
| 19–20 | Category:Bugeat | Small town, Millevaches gateway |
| 22 | Category:Mont Bessou | Summit views (highest point in Corrèze) |
| 25 | Category:Meymac | Benedictine abbey, medieval town |
| 27 | Category:Ussel, Corrèze | Town centre, Place Voltaire |

## Confirmed CC-Licensed Photographers on Commons

These photographers have Corrèze-specific content confirmed as CC BY-SA:
- **E gargadennec** — Collonges-la-Rouge header images
- **Alertomalibu** — Collonges village streets, Castel de Vassinhac
- **Accrochoc** — Collonges architectural details, tympanum
- **Sail over** — Maison de la Sirène, Collonges

## Other CC/Open Image Sources

- **Unsplash** — search "Corrèze", "Limousin", "Dordogne valley" for landscape photography (Unsplash license, free for all uses)
- **Flickr Creative Commons** — search by geographic coordinates for each segment; filter by CC BY or CC BY-SA
- **Wikimedia Commons geosearch API** — `suggest_images.py` should query: `https://commons.wikimedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=5000&gsnamespace=6&gslimit=50`

## Video Sources

- **Dailymotion / Tour de France official channel** — ASO publishes stage highlight videos. Embeddable but check redistribution terms per video:
  - 2024 TdF Stage 11 highlights (Massif Central): dailymotion.com/video/x90ywby
  - 2024 TdF Stage 11 route preview: dailymotion.com/video/x9sik7s (check — may be 2026 stage 9 preview)
  - 2025 TdF highlights reel: dailymotion.com/video/x9npbe4
- **YouTube** — search "cycling Corrèze", "vélo Corrèze", "Suc au May cycling", "Plateau de Millevaches vélo" for amateur ride-along videos. Many cycling YouTubers post CC-licensed or embeddable content.
- **Tour du Limousin** — official race footage may be available via France 3 Nouvelle-Aquitaine archives or the race's social media channels.
