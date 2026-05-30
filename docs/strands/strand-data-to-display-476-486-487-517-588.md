# Strand: data-to-display reconciliation (#517 / #588 / #486 / #487 / #476)

The "data reaches readers" strand. Climb-data corrections in `points-config.json` do **not** currently reach the rendered pages — two Vue components hold hardcoded climb maps that duplicate and disagree with the canonical data. This strand removes the parallel copies so the data layer is the single source the UI renders, adds drift-detection assertions so the two can never silently re-diverge, and closes the two related parallel-source gaps (#487 town-coords completeness, #476 verification audit-trail).

> **Runs after `strand-geometry-drift-551-554-555-589-590-591.md` merges.** Geometry-drift corrects the canonical climb summit-km / length / gradient in `points-config.json` and resolves the `segments.json` regen (#639). This strand makes those corrected numbers reach readers — so it must consolidate *against the final numbers*, not the pre-correction ones, and against a clean regenerated `segments.json`. Branch only after geometry-drift is on `main` (see §2).

## 1. Goal

Land the data-to-display reconciliation cluster that `docs/planning/v1.4.20-scope.md` named as the **candidate spine for the next milestone**: make `StageDetails.vue` and `ElevationChart.vue` derive climb length/gradient/summit-km from `data/competition/points-config.json` instead of hand-maintained literals (#517, #588, #486), assert that every town/climb name declared in `segments.json` and `points-config.json` has a `town-coords.json` entry (#487), and give verified segment data an audit-trail so edits can't silently undo verification (#476). The unifying problem: a fix to the data layer is invisible to readers because the render path reads a parallel copy. **No milestone is assigned yet** — planning parked this cluster as the next cycle's candidate spine; treat this brief as publisher-requested scaffolding ahead of scheduling, and flag at close whether planning should formally milestone it.

Worked as one strand session, opened as **coherent PRs** (recommended split below), not one mega-PR: (a) the component consolidation + drift assertion (#517/#588/#486), (b) the town-coords completeness assertion (#487), (c) the verification audit-trail (#476). (a) is the heart and should land first.

## 2. Filesystem posture

- Explicit-path worktree, run from outside the repo, **branched after geometry-drift has merged**:
  ```
  git -C /home/jhs/code/tdf26 worktree add -b feature/data-to-display /home/jhs/code/tdf26-data-to-display main
  ```
  Before branching, `git fetch && git log origin/main --oneline` and confirm the geometry-drift PR landed (look for the corrected climbs / #639 regen). If it has not, **stop and surface** — consolidating against pre-correction `points-config.json` would bake the wrong numbers into the render path. Do **not** use the nesting in-repo worktree form; do **not** add a `.claude` symlink (`feedback_strand_worktree_path.md`).
- **Branch verification:** before each `git add` / `git commit`, run `git branch --show-current` and confirm `feature/data-to-display` (`feedback_shared_tree_branch_verification.md`).
- Seed gitignored rider data before any `npm run build`: `for f in daily-log points stats; do cp -n data/riders/$f.example.json data/riders/$f.json; done` (`feedback_ci_seed_ordering.md`).

## 3. Source-of-truth posture

- **`data/competition/points-config.json` is the single source of truth** for climb identity, summit km (`km`), `length_km`, and `gradient`. The render path must read it, not a copy. Precedent already in the repo: `tests/utils/*.ts` import `~/data/competition/points-config.json` directly; `components/StageDetails.vue` already imports `~/data/segments.json` and `~/utils/stage-totals.ts` (`CATEGORIZED_CLIMBS`). The consolidation extends that pattern — it does not invent a new one.
- **Do not edit `points-config.json` climb values** — geometry-drift owns them and will have just corrected them. This strand *reads* them. Per `feedback_source_of_truth_framing.md`, the component is a consumer, not a second source.
- **Lookup keys are accent- and rename-sensitive.** `ElevationChart.vue`'s `climbSummitKm` keeps both ASCII and accented key variants for fallback; #517 notes the keys broke under the Naves rename. Before any name-keyed change, **grep every extension** (`.vue`, `.ts`, `.py`, `.json`) for the climb name (`feedback_rename_scope_grep.md`). Deriving from `points-config.json` by the canonical `name` is the fix that removes the key-drift surface entirely.

## 4. Target issues

| # | Surface | Current state | Fix |
|---|---------|---------------|-----|
| #517 | `StageDetails.vue:47-56` `climbData`, `ElevationChart.vue:236-247` `climbSummitKm` | hardcoded maps duplicating points-config | Derive both from `points-config.json` (directly or via a `utils/` helper) |
| #588 | `StageDetails.vue` climb `length`/`gradient` map | disagrees with points-config on every gradient + ≥1 length (table in issue) | Subsumed by #517's StageDetails consolidation |
| #486 | both components + points-config | umbrella: drift across UI surfaces | Closed by the consolidation + a drift assertion |
| #487 | `town-coords.json` keys vs `segments.json` towns + `points-config` climb names | no assertion every declared name has a coords entry | Add a vitest completeness assertion |
| #476 | verified segment data (no metadata) | edits can silently undo verification | Add an audit-trail metadata convention + an assertion |

`#517`, `#588`, `#486` are the same fix viewed three ways — do them together; `#487` and `#476` are independent assertions/conventions.

## 5. Workflow per issue

1. **#517 / #588 / #486 — the consolidation (do first).** Replace `StageDetails.vue`'s `climbData` and `ElevationChart.vue`'s `climbSummitKm` with values derived from `points-config.json`, keyed by the canonical `name`. Recommended shape: a single small helper in `utils/` (alongside `stage-totals.ts`) that maps climb name → `{ length_km, gradient, km }` from the imported `points-config.json`, consumed by both components — so there is exactly one derivation. **Checkpoint (AskUserQuestion)** if the helper shape is non-obvious (e.g. extend `stage-totals.ts` vs new `utils/climb-display.ts`); otherwise proceed and note the choice in the PR. Confirm the rendered "Xkm @ Y%" and the chart summit labels now match `points-config.json` exactly.
2. **Drift assertion (closes #486 durably).** Add a vitest assertion that the values the components render equal `points-config.json` (the parallel-source-of-truth detector pattern, `feedback_parallel_source_of_truth_detector.md`). After consolidation there is no second source, so the natural form asserts "no hardcoded climb literal remains / the helper output equals points-config" — design it so it would fire red if someone re-introduces a literal. Hand-check its diagnostic against the bug (`feedback_assertion_bug_class.md`).
3. **#487 — town-coords completeness.** Add a vitest assertion: every name in `segments.json[].towns[]` and every `points-config.json#climbs[].name` has a key in `town-coords.json`. Test-only; no data edit unless the assertion surfaces a genuine missing coord (file that as its own finding).
4. **#476 — verification audit-trail (most independent; may split or, if the strand runs long, defer with a note).** Add a metadata convention recording that a segment's data was verified (date / PR / source), so a later edit to a verified field is detectable. **Checkpoint (AskUserQuestion):** the metadata shape and where it lives (a `verified` block in `segments.json`, a sidecar file, or a manifest) is a design decision, not a determinate fix — present options. Add an assertion that flags edits to verified fields without a re-audit bump. Keep the audit-trail mechanical, not prose.

## 6. Verification commands

- `npm test` — the vitest suite where the new assertions live. **Red-green for the consolidation:** an assertion comparing the *pre-consolidation* `climbData`/`climbSummitKm` literals to `points-config.json` fires **red** (they disagree on every gradient per #588's table); after the components derive from points-config it goes **green**. Demonstrate the transition; do not commit artificial breakage — the red state is the literals as they exist on `main` today.
- `npm run build` (`nuxt generate`) — confirm `StageDetails.vue` and `ElevationChart.vue` render the derived values without error on entry pages and the stage-details card (seed rider data first, §2). Spot-check a segment whose number geometry-drift corrected (e.g. Croix de Pey / Côte des Gardes) renders the corrected figure.
- `python3 processing/validate_points.py` — only if #476 touches data files; otherwise N/A.
- `npm run typecheck` does **not** exist in this repo — do not list it.

## 7. Cross-strand sharing notes

- **What this strand owns (write):** `components/StageDetails.vue`, `components/ElevationChart.vue`, a new/extended helper in `utils/`, new vitest files under `tests/utils/`, and — for #476 — the verification-metadata surface (shape TBD at the checkpoint).
- **What this strand reads:** `data/competition/points-config.json`, `data/segments.json`, `data/town-coords.json`, `utils/stage-totals.ts`.
- **What this strand must NOT touch:** climb values in `points-config.json` (geometry-drift owns them), the GPX polylines, and `tests/utils/climb-summit-km.test.ts`'s `KNOWN_FAILING` map (geometry-drift empties it). This strand consumes the corrected data; it does not re-derive or re-correct it.
- **Hard dependency on geometry-drift (the load-bearing note).** This strand must branch *after* geometry-drift merges, because (a) consolidating the render path against pre-correction climb numbers would bake stale values in, and (b) `StageDetails.vue` imports `segments.json`, whose clean regeneration is geometry-drift's #639 deliverable — a stale `segments.json` would make the town/climb derivation and the #487 assertion test against the wrong data. If geometry-drift is still running, **wait**; do not start against current `main`. Forecast: the most likely collision is racing geometry-drift and asserting drift against numbers that are about to change — the sequencing rule removes it.
- **`town-positions`:** both components import `~/data/town-positions`, which is adjacent to the #639 `town_positions` regen. Confirm after geometry-drift lands that `town-positions` is consistent before building the #487 assertion on it.

## 8. Scope discipline

- File new issues for any genuinely-missing town/climb coord the #487 assertion surfaces; do not patch data silently inside a component strand.
- Record the two design checkpoints (helper shape for #517; metadata shape for #476) in the PR body with the option chosen and why (`feedback_issues_describe_problems.md`).
- If #476's audit-trail design balloons, split it to its own PR or surface to planning rather than blocking the #517/#487 wins — the consolidation is the reader-facing payoff and should not wait on the metadata-regime design.

## 9. Memories that apply

- `feedback_parallel_source_of_truth_detector.md` — this strand *is* an instance of the pattern; the drift assertion is the deliverable (PR #448 / #516 are the named prior instances).
- `feedback_source_of_truth_framing.md` — the component is a consumer of points-config, never a second source.
- `feedback_rename_scope_grep.md` — grep `.vue` / `.ts` / `.py` / `.json` for any name-keyed climb before changing it; the lookup keys broke under the Naves rename.
- `feedback_assertion_bug_class.md` — hand-compute each new assertion's diagnostic against the bug it guards.
- `feedback_shared_tree_branch_verification.md`, `feedback_strand_worktree_path.md`, `feedback_ci_seed_ordering.md`, `feedback_issues_describe_problems.md`.

## 10. Stop when

- PR(s) open: component consolidation + drift assertion (#517/#588/#486), town-coords completeness assertion (#487), and verification audit-trail (#476, or split/deferred-with-note); `npm test` green with the drift assertion demonstrated red→green; `npm run build` renders the derived (corrected) values on entry pages.
- The two design checkpoints recorded in the PR body.
- A corrected climb figure from geometry-drift verified as actually reaching the rendered page (the whole point of the strand).
- Final report to publisher: PR link(s), the design decisions, any missing-coord finding from #487, the #476 disposition (landed / split / deferred), and a recommendation on whether planning should milestone this cluster.
- **Retro inputs written to `project_next_planning_notes.md` at close** under a new section header (e.g. `## Items surfaced during data-to-display execution (<date>)`): decision-actionable observations (incl. the milestone recommendation and any #476 scope movement), light-tier pattern observations, and numeric stats (`git diff --stat`, commits, AskUserQuestion checkpoints fired, approx wall-clock).
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove /home/jhs/code/tdf26-data-to-display` once the PR(s) have merged.
