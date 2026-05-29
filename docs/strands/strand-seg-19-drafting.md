# Strand: seg 19 drafting — Lestards, the Croix de Pey crest, the Plateau threshold

Publisher-paced single-segment drafting strand (deviation: "Workflow" lists the publisher checkpoints, not the prose-writing steps; cadence is publisher-driven). Mirrors the seg 15 / seg 16 / seg 17 / seg 18 drafting strands.

## 1. Goal

Draft `content/entries/19-*.md` (currently the stub `19-bugeat-gateway-to-millevaches.md`) for the **Sun 2026-06-07** publish slot, 800–1,200 words, from `content/research/segs-17-19-block-research.md` ("Segment 19" section). Seg 19 climbs the upper Croix de Pey grade onto the open **Lestards** plateau and is the segment where the *paysage* crosses from Vézère gorge to Plateau de Millevaches (segments.json: seg 19 km 126–134, `towns: ["Lestards"]`, `climbs: ["Côte de la Croix de Pey"]`). **The stub is mis-titled** `19-bugeat-gateway-to-millevaches` — **Bugeat is seg 21 and all Bugeat material is reserved for it** (the dossier is explicit). Seg 19's verified content is Lestards + the climb's crest + the Plateau *threshold*. Retitle at the anchor checkpoint to a Lestards / thatched-church / Plateau-threshold anchor; seg 19 names the *gateway*, it is not the destination.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/seg-19-draft /home/jhs/code/tdf26-seg-19 main
```

- Explicit-path worktree; no nesting, no `.claude` symlink. `git branch --show-current` → `feature/seg-19-draft` before each commit.
- Rename the stub via `git mv` once the new slug is chosen (per the seg 12/13/17 precedent), don't create a second file.
- Fresh worktree: `npm ci` + seed rider data (`cp data/riders/*.example.json` to non-example names, per `feedback_ci_seed_ordering.md`) before any `npm run build` / dev preview.
- **Single-strand, orchestrator-session only — do not spawn sub-agents for the drafting itself** (per the seg-13 finding).
- **Image frontmatter: inline-JSON form, not YAML list** (per #479 / the seg-9 crash history).

## 3. Source-of-truth posture

- **Verify named on-route anchors against `data/town-coords.json` + the seg-19 GPX polyline before writing prose around them.** The dossier puts **Lestards bourg 12 m off the polyline at ~km 131.6 — firmly on-route** (the Église Saint-Martial is the strongest on-route set-piece in the block); confirm.
- The dossier is scaffolding, not bedrock (`feedback_brief_content_is_carryforward.md`) — re-verify load-bearing claims. The dossier flags these:
  - **The thatched-roof church is "the only thatched-roof church in France" per Wikipedia FR + Office de Tourisme.** Write it that way. **Do NOT write the brief's earlier "one of two in France" claim** — the dossier could not corroborate a second (no Bénodet, no Saint-Aignan church surfaced); it is likely a confusion with the broader category of thatched religious *buildings*. Footnote the "two" reading as unverified if you mention it at all.
  - **The "1977" thatch-rebuild date was not corroborated this round** — flag for verification before asserting any specific restoration date. The **June 2015 commemorative postage stamp** (premier-jour 26 June 2015) *is* verified.
  - The **Croix de Pey climb numbers (#551) and summit km (#591) are contested** — write the crest as a *paysage* beat (the moment the Plateau opens, the trees thin, the horizon widens), **not** as a km-precise GPS moment. The road's literal high point (851 m, ~km 132.52) is past the polka-dot line, inside seg 19.
- Per `feedback_corridor_commune_name_collisions.md`: disambiguate Lestards against same-named places (dept 19 + adjacency) in any search.
- Do NOT transcribe CLAUDE.md tabular data. Narrative project context only.

## 4. Anchors available (from the dossier)

- **The Plateau threshold (the segment's geographic beat).** Treignac's Vézère gorge (granite walls, deciduous forest, half-timbered houses) gives way to the Plateau de Millevaches's *landes* (open heath), *tourbières* (peat bogs — the Plateau is the *château d'eau de la France*), and 20th-c. conifer plantations (Douglas-fir, sitka — the *fermeture paysagère*). The rider crests the climb, the trees thin, the horizon opens. The watershed framing: the catchment-wise transition from Vézère-immediate (gorges, fast water) to Vézère-source-country (plateau peat, slow water) happens precisely here.
- **The thatched-roof church (the set-piece).** Église Saint-Martial — Romanesque supports/barrel vaults late 12th–early 13th c.; clocher-mur with four corner buttresses; inscribed MH 1998, classified 2002; on-route (12 m off polyline). **The only thatched-roof church in France** (Wikipedia FR + Office de Tourisme), roofed in **rye straw (paille de seigle), Limousin technique** (bundles tied to joists with twisted straw cords, not metal bars; Armand Klavun among the last masters). 2015 postage stamp. The single most-photographed object in the Treignac–Bugeat corridor.
- **The medieval rye-mission foundation.** Lestards appears in the record in **1315**; around **1300** the **Ordre de Saint-Antoine-de-Viennois** established a *commanderie* here, charged with care for *ergotisme* (Saint Anthony's fire — the gangrenous/hallucinogenic disease from rye-ergot infection). The choice was not random: rye was the Plateau's staple, ergotism a recurring upland-rye epidemic. Transferred to the Knights Hospitaller via a 1766 decree. **The material connection is the beat:** the village's foundation is a rye-grain medical mission, and the surviving church is itself rye-strawed.
- **Cycling: the polka-dot crest + the naming-history beat.** The Croix de Pey *crest* (the classification-points moment) falls in seg 19 — the points-king beat, even with length/gradient/category/summit-km all contested. **"Côte de Lestards" = "Côte de la Croix de Pey"** — same road, two names (the 2017 Tour du Limousin Stage 3, Cyril Gautier win, used *Lestards*; the 2020 Tour de France, Hirschi win, and 2026 use *Croix de Pey*; Inner Ring's 2020 preview: "98% of the Col de Lestards"). 2026 is the first Tour to *climb* through Lestards (2020 descended it). A writable naming-history beat with two confirmed pro-cycling shadows on one road.
- **Cuisine shift at the threshold.** Below the crest: *bas-Limousin* (cattle, chestnut, *farcidure*). Above: *mountain Limousin* (myrtilles, mushroom cookery, rye flour/bread — the Antonine rye logic returns as a culinary trace, *clafoutis aux myrtilles*). Seg 19 is where the first upland markers (rye, myrtille) appear on village ground.
- **Local people are genuinely thin** — no documented historical figure born/formed in Lestards. The natural local-person anchor is **back to Treignac** (Lachaud, Sangnier, Tapissier — *all spent in seg 18*) or **forward to Bugeat** (Mimoun, Lestang — *reserved for seg 21*). **Accept the thinness and lean into the church-and-Plateau material**; do not borrow seg 18's or seg 21's people. (Christophe Petit, Lestards mayor since 2001, is available but lightweight.)

## 5. Workflow (publisher checkpoints — the cadence)

Fire these as AskUserQuestion in the orchestrator session; iterate in free-form chat between them.

1. **Anchor/title checkpoint (run first, before voice):** confirm the retitle (Lestards / thatched-church / Plateau-threshold, **not** Bugeat — that is seg 21) and the lead anchor (the thatched church? the Plateau threshold? the rye-mission/church pairing?). Confirm seg 19 owns the climb *crest* and inherits the *base* from seg 18.
2. **Voice register:** pre-read candidate register SKILL.md briefs *before* firing (per `feedback_voice_checkpoint_prep.md`). Seg 19 is the last entry before the Plateau body (segs 20–22) — present continuity vs a register shift into the upland material as a genuine fork.
3. **Promises-inherited check:** enumerate forward-looking promises segs 17–18 made that seg 19 must honour or defer (the climb-crest handed up from seg 18; the Plateau named-as-threshold but its *body* reserved for segs 20–22; Bugeat reserved for seg 21). Confirm pick-up vs hand-on — seg 19 names the gateway, the Plateau interior is reserved.
4. **First-draft review.**
5. **Fact-duplication audit pass** between draft revisions and Sources/disclosure.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive`
- `npm test`
- `npm run build` then a `nuxt generate` preview (not the SSR runtime, per `feedback_production_preview.md`); entry stays `draft: true` through drafting — do NOT flip `draft: false` in the drafting PR.
- MDC balance: rely on the validator's directive check (PR #563) or grep `::name{...}` opens vs closes.

## 7. Cross-strand sharing notes

- **Owns (write):** `content/entries/19-*.md` (the renamed seg 19 entry) only; possibly `data/historical-tdf.json` *only if* the 2020 Stage 12 / 2017 Tour du Limousin card needs a seg-19 key (verify not already keyed; if adding, sibling PR, not in the draft).
- **Reads:** the 17-19 dossier, `data/segments.json`, `data/town-coords.json`, seg-19 GPX, `data/attractions.json`.
- **Must NOT touch:** any other `content/entries/*.md` (`feedback_content_change_rule.md`); the seg 17/18 entries; the seg 20+ stubs; `data/` beyond an optional historical-tdf card. Out-of-scope edits open as **sibling PRs** off main (`feedback_interpolated_pr_pattern.md`).
- **Reserved material — do NOT use** (dossier "Reserved" list): Bugeat (seg 21); the Plateau de Millevaches *body* — peat bogs, *néo-paysan* movement, 2004 PNR creation, *mille sources* etymology (segs 20–22); Mont Bessou "highest in Corrèze" (seg 22). Seg 19 is the threshold, not the interior.
- **Data corrections:** #551 / #591 (Croix de Pey) — do not fix inline; write per the dossier's *paysage*-beat recommendation. The thatch-date and "only/​two churches" framing — write the verified consensus, file nothing unless `data/attractions.json` carries the unverified claim.
- **Parallel-safety:** orthogonal to the pipeline strands (touches `content/`, not `scripts/`); safe alongside the gate/spine/ceremony. Safe alongside seg 18 drafting (different entry file) — but the two share the climb: agree the **base (seg 18) vs crest (seg 19)** split at the anchor checkpoint so the Croix de Pey isn't written twice.

## 8. Scope discipline

- File new issues for findings outside the entry write-set; don't over-scope.
- Style tics to actively avoid (cross-entry grep before sign-off): the **"the X the Y will not Z" shape** (`feedback_will_not_shape.md`), **"polyline" in prose** (`feedback_avoid_polyline_in_prose.md`), em-dashes and exclamation marks (project standard: zero), internal-data citations in Sources (`feedback_sources_no_internal.md`).
- Literary references get proper footnotes (`feedback_literary_footnotes.md`); optional `## Sources` (`feedback_sources_section.md`); per-entry disclosure footer (`project_disclosure_practice.md`).

## 9. Memories that apply

- `feedback_content_change_rule.md`, `feedback_brief_content_is_carryforward.md`, `feedback_pre_publish_scrutiny.md`, `feedback_voice_checkpoint_prep.md`, `feedback_literary_footnotes.md`, `feedback_sources_section.md`, `feedback_sources_no_internal.md`, `project_disclosure_practice.md`, `feedback_will_not_shape.md`, `feedback_avoid_polyline_in_prose.md`, `feedback_interpolated_pr_pattern.md`, `feedback_on_route_checks.md`, `feedback_corridor_commune_name_collisions.md`, `feedback_ci_seed_ordering.md`, `feedback_shared_tree_branch_verification.md`, `feedback_strand_session_self_cleanup.md`. (Barthes arc spent at seg 15. Meymac/saintsbury voice is seg 25, not here.)

## 10. Stop when

- Renamed seg 19 entry drafted (800–1,200 words), validators green, dev preview confirmed by publisher; PR open against `main` (open a seg-19 tracking issue if none exists; `Refs #N`).
- Entry left `draft: true` (publisher flips at publish time).
- **Cleanup (you run these):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-seg-19` once merged.
- Final report: PR link, chosen slug (confirming the move off the Bugeat mis-title), voice register, the base/crest split agreed with seg 18, promises picked-up vs deferred to seg 20, any issue filed.
- **Retro inputs written to `project_next_planning_notes.md`** under `## Items surfaced during seg-19-drafting strand execution (<date>)`: decision-actionable observations, light-tier pattern observations, numeric stats (word count, footnotes, MDC directives, em-dash/exclamation counts, checkpoint cycles, wall-clock).
