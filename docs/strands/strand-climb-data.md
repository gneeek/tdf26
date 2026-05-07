# Strand — Climb data corrections (#490 + #492)

**Start here:** [Roadmap → Now](https://github.com/gneeek/tdf26/wiki/Roadmap). This brief decided at planning session 2026-05-07. Follows [STRAND-BRIEF-TEMPLATE.md](STRAND-BRIEF-TEMPLATE.md). Closes [#490](https://github.com/gneeek/tdf26/issues/490) and [#492](https://github.com/gneeek/tdf26/issues/492).

## 1. Goal

Two paired data-layer corrections for climb data, bundled because they share the same files and the same per-source-assertion pattern:

- **#490** — Resolve the Côte des Naves gradient discrepancy (`data/points-config.json` says 5.6%; CLAUDE.md and ASO sources say ~6.7%; elevation-derived value should win). Add a per-source assertion that points-config climb gradients must match elevation-derived gradient within tolerance — extending the #474 pattern.
- **#492** — Add an `aso: true|false` flag to the points-config schema; document non-ASO regional climbs as first-class. Puy de Lachaud is the worked example (regional climb, on the route, not on the ASO categorised list).

Milestone v1.4.19. Companion to the CLAUDE.md deprecation strand (#491). Together these three issues are the data-layer regime expansion (#474/#475/#476 set the regime; #490/#491/#492 expand it).

## 2. Filesystem posture

Use the explicit-path worktree form:

```
git -C /home/jhs/code/tdf26 worktree add -b feature/issue-490-492-climb-data /home/jhs/code/tdf26-climb-data main
```

Run from outside the repo. Do not symlink `.claude/`. Verify branch with `git branch --show-current` before each `git add`/`git commit`.

## 3. Source-of-truth posture

- Read `data/elevation/segment-*.json` and `data/segments/segment-*.gpx` directly to compute elevation-derived gradients. These are the bedrock for #490's resolution.
- Read `data/points-config.json` for current values. **Do not** treat the points-config gradient as canonical when in doubt — that's exactly the source-of-truth framing problem at the heart of #490.
- Read CLAUDE.md "Categorized Climbs" only for cross-reference (treat as drift-prone per #491).
- Read external ASO climb data via web (the official Tour de France 2026 Stage 9 climb list, or per-stage announcements) only as a tie-breaker — capture the URL in the PR body.
- Verify against the segment polyline per `feedback_on_route_checks.md` when checking climb start/summit positions.

## 4. Target issues

- **Closes [#490](https://github.com/gneeek/tdf26/issues/490)** — Côte des Naves gradient + per-source assertion
- **Closes [#492](https://github.com/gneeek/tdf26/issues/492)** — `aso` flag schema + non-ASO posture
- **Read-only awareness** of #491 (CLAUDE.md deprecation, separate strand) and #474/#475/#476 (data-layer regime — assertions, schema, audit-trail). #475's schema work is the home for #492's `aso` flag.

## 5. Workflow

### #490 — Côte des Naves gradient

1. **Locate the climb in elevation data.** From `data/segments.json`, Côte des Naves is on segment 11 (km 70-78). Read `data/elevation/segment-11.json` for the climb's km span.
2. **Compute the elevation-derived gradient.** Climb start and summit positions per CLAUDE.md content notes / ASO references; use the polyline + elevation pairs to compute average gradient over the climb span. Document the math in PR body.
3. **Compare:**
   - `data/points-config.json` claims 5.6%
   - CLAUDE.md (drift-prone) claims 6.7% (text)
   - Elevation-derived: compute
   - ASO 2026 Stage 9 official: research; capture URL
4. **Decide canonical value.** Likely the elevation-derived value wins. If ASO disagrees significantly, flag as material disagreement (AskUserQuestion checkpoint) — could indicate climb-span definition disagreement (where does Côte des Naves start vs summit), not gradient error.
5. **Update `data/points-config.json`** with the canonical value.
6. **Add per-source assertion** in `tests/utils/` (mirrors PR #448's `tests/utils/stage-totals.test.ts` pattern):
   - For each climb in points-config, the assertion: `points_config[climb].gradient` must match elevation-derived gradient within tolerance (suggested ±0.3 percentage points; tune empirically).
   - Test fires red against pre-fix Naves value (5.6% vs ~6.7%); green after fix.

### #492 — `aso: true|false` flag

1. **Update points-config schema** (`tests/data/points-config.schema.json` or wherever #475 landed schemas — verify location) to add `aso: boolean` as a required field on each climb.
2. **Update `data/points-config.json`** with the flag for every climb. Determine ASO membership by checking the official ASO 2026 Stage 9 climb list:
   - On ASO list (set `aso: true`): expect to include Côte de Lagleygeolle, Côte de Miel, Côte des Naves, Suc au May, Côte de la Croix de Pey, Mont Bessou, Côte des Gardes (verify each).
   - Not on ASO list (set `aso: false`): Puy Boubou (verify), Puy de Lachaud (the worked example for #492).
3. **Update any code that consumes points-config** to handle the new field. Likely callers:
   - `utils/stage-totals.ts` (per PR #448's per-source assertion territory)
   - `processing/validate_points.py` (the spanning-climb invariant)
   - Any code that displays climb categorisation in the UI (search for `CATEGORIZED_CLIMBS` / `points-config` usage)
4. **Document non-ASO posture.** A short paragraph in the schema description, the relevant code's docstring, or the project wiki — pick the venue based on existing convention. Suggested text: "Non-ASO regional climbs are first-class entries in points-config; UI and per-segment narrative may treat them differently from ASO-categorised climbs (e.g., omit from the official KOM points display) but they remain in the data layer."

### Both — verification

5. Run validators; demonstrate red-green for both new assertions.

## 6. Verification commands

- `npm test` — must pass; specifically the new `tests/utils/<gradient>.test.ts` (or wherever the assertion lands).
- `python3 processing/validate_points.py` — must pass; spanning-climb invariant unaffected.
- `python3 scripts/validate_entries.py` — defensive (no entry frontmatter touched).
- `npm run build` — must pass (UI may consume points-config; defensive against the new schema field breaking things).

**Demonstrate red-green for both assertions:**

- #490: revert `data/points-config.json` Naves gradient to 5.6%, run gradient-tolerance test → red. Restore canonical value → green.
- #492: revert one climb's `aso` field, run schema validation → red. Restore → green.

Do not commit the artificial breakage — temporary local revert + rerun, restore before commit (per `feedback_strand_worktree_path.md` brief-rendering of the v1.4.11 Strand C technique).

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `data/points-config.json` — gradient correction + `aso` field on all climbs
  - `tests/data/points-config.schema.json` (or wherever #475 schemas live) — schema with new `aso` required field
  - `tests/utils/<new-gradient-assertion>.test.ts` — per-source assertion extending PR #448's pattern
  - `utils/stage-totals.ts` (only if it needs to consume the new `aso` field; likely yes)
  - Any documentation home for the non-ASO posture (schema description, README, or wiki)
- **What this strand reads:**
  - `data/segments.json`, `data/segments/segment-*.gpx`, `data/elevation/segment-*.json` — for elevation-derived gradient
  - CLAUDE.md "Categorized Climbs" — drift-prone, cross-reference only
  - External ASO climb list — research
  - `tests/utils/stage-totals.test.ts` — pattern reference
- **What this strand must NOT touch:**
  - `CLAUDE.md` — the deprecation strand (#491) owns it; do not edit even if the gradient narrative becomes stale.
  - `data/segments.json` — not in scope; if drift surfaces, file follow-up issue.
  - `data/elevation/segment-*.json` — read only (elevation source data does not change here).
  - `data/segments/segment-*.gpx` — master geometry, no edits.
- **Cross-strand collisions:**
  - **CLAUDE.md deprecation strand (#491)** runs concurrently in v1.4.19. It only reads `data/points-config.json` and writes CLAUDE.md. No file overlap with this strand. If the deprecation strand lands first, this strand's PR doesn't need to update CLAUDE.md (it's already pointer-only). If this strand lands first, the deprecation strand's pointer paragraph for "Categorized Climbs" should mention the new `aso` flag posture — that's a small text update on the second strand's side.
  - **Verification strands (#478, #498, #499, #500)** all run validate_points.py; if this strand's per-source-assertion test changes the points-config schema, the verification strands inherit the new requirement. Acceptable — they should be updating climb data anyway, and the assertion catches drift.

## 8. Scope discipline

- **Do not touch CLAUDE.md.** That's the deprecation strand's job.
- **Do not add or remove climbs from points-config.** Only correct the gradient on Côte des Naves and add the `aso` flag to all existing climbs. New climbs (e.g., a regional climb the route passes over that isn't currently in points-config) → file new issue.
- **Do not extend the per-source assertion to other gradient drift this strand notices.** Document the drift in PR body or new follow-up issues; the gradient-tolerance assertion catches all drift once it's in place anyway.
- AskUserQuestion at material disagreements:
  - Elevation-derived gradient differs significantly from ASO official.
  - Climb-span definition disagreement (e.g., where does Côte des Naves start).
  - Canonical posture for non-ASO climbs in UI (display them with the same chip as ASO? different style? omit?).

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`
- `feedback_on_route_checks.md` — polylines for spatial checks
- `feedback_strand_worktree_path.md`
- `feedback_shared_tree_branch_verification.md`
- `feedback_issues_describe_problems.md` — any new gradient drift surfaced gets filed as a problem, not fixed inline
- Per-source-of-truth detector (v1.4.8 retro rule, first instance landed in PR #448 — this strand's assertion is the second instance; worth naming in PR body)

## 10. Stop when

- `data/points-config.json` Côte des Naves gradient corrected to canonical (elevation-derived) value.
- `data/points-config.json` has `aso: true|false` on every climb; values verified against ASO official Stage 9 climb list.
- Schema (`tests/data/points-config.schema.json` or equivalent) updated with `aso` required boolean.
- Per-source assertion test exists in `tests/utils/`; demonstrates red-green against both #490 and #492 broken states.
- Non-ASO posture documented in agreed venue.
- All verification commands green.
- PR body audit table: per climb, ASO-or-not, current gradient, elevation-derived gradient, canonical value.
- PR open against milestone v1.4.19 closing #490 and #492.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-climb-data` once the PR has merged.
- Final report posted to publisher: PR link, audit-table summary, any open questions surfaced (e.g., further gradient drift caught by the new assertion).
