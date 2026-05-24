# Strand: Suc au May points-config fix (#513)

Auto-mode data-correctness strand to resolve the three-field disagreement (`category`, `gradient`, `points`) for the Suc au May climb in `data/competition/points-config.json`. Authored 2026-05-24 as part of the v1.4.19 close-out parallel slate.

## 1. Goal

Land the canonical Suc au May entry in `data/competition/points-config.json` consistent with the ASO 2026 Stage 9 official categorisation and the TdF polka-dot points scale, before the seg 15 publish window opens. Seg 15 IS Suc au May — a wrong category, gradient, or points array shows up on the seg 15 entry page's PowerStats card the moment publish.sh runs.

Closes #513. Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/52). Runs in **auto-mode** per the v1.4.18 retro learning (data-fix suits auto-mode). One mandatory AskUserQuestion checkpoint: which of the three contested category values is canonical (see §5 step 2). The points array follows mechanically from the category once it is fixed.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/513-suc-au-may-points-config /home/jhs/code/tdf26-513 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `data/competition/points-config.json` is the canonical source for climb categorisation, length, gradient, points — `processing/split_gpx.py` imports from here, and `data/segments.json` climb assignments are generated downstream. Per CLAUDE.md § Categorized Climbs: "Single source of truth: `processing/split_gpx.py` imports from here, and `data/segments.json` climb assignments are generated accordingly." Fix this file; do not patch `segments.json` directly.
- The `points-config` schema constrains the points array to match the category per TdF polka-dot rules:
  - Cat 4: `[1]`
  - Cat 3: `[2, 1]`
  - Cat 2: `[5, 3, 2, 1]`
  - Cat 1: `[10, 8, 6, 4, 2, 1]`
  - HC: `[20, 15, 12, 10, 8, 6, 4, 2]`
- The current `[10, 8, 6, 4]` array does not match any of these — confirm by reading the `validate_points.py` invariants before fixing.
- **External sources to cross-check** (verify each URL fetches before quoting in the PR body):
  - Tourisme Corrèze official 2026 Stage 9 announcement (named in #513 as the dissenting source — find the URL, verify, attach to PR body).
  - ASO official Stage 9 climb categorisation (the 2026 stage page; may not name Suc au May explicitly until closer to July).
  - The L'Agglomérée cyclosportive route notes (per CLAUDE.md § Cycling References: the cyclosportive uses Suc au May; its notes may name the climb category).
- Per `feedback_source_of_truth_framing.md`: trace each source's provenance before treating it as bedrock. Tourisme Corrèze is a tourism office, not ASO; ASO is the official categorisation authority for the actual stage.
- **Climb-summit-km is out of scope here** — that's #518's territory. Do not touch `summit_km`. (The Suc au May audit confirmed the road-summit km 105.15 is correct; the *mountain* summit is 19m higher than the road and 200m off the route, which is a future content-clarification, not a data error.)

## 4. Target issues

**Closes #513** — use `Closes #513` in PR body (per `feedback_pr_closure_keywords.md`).

If the strand surfaces a fourth disagreement (e.g., `length_km` also doesn't match ASO), fix inline only if scope-bounded; otherwise file a separate issue.

## 5. Workflow

Single-issue strand; collapse "Target issues" + "Workflow per issue" into one cadence.

1. **Survey current state.** Read the `Suc au May` entry in `data/competition/points-config.json`. Read every external source named in #513 (Tourisme Corrèze, CLAUDE.md categorized climbs, direct measurement from `data/elevation/segment-15.json`). Tabulate the disagreement matrix in the PR draft body up-front.
2. **Category resolution checkpoint (AskUserQuestion).** Present the candidate categories with the evidence each rests on:
   - **HC** — current points-config value; not supported by any external source surveyed. Almost certainly wrong (no climb of this length/gradient is HC).
   - **Cat 2** — CLAUDE.md § Categorized Climbs lists Cat 2; consistent with the 2.22 km length × ~5.7% gradient. Points array `[5, 3, 2, 1]`.
   - **Cat 3** — possible per Tourisme Corrèze "Cat 4 or Cat 3" range; if the gradient measurement is at the higher end (7-8% sustained), this is plausible. Points array `[2, 1]`.
   - **Cat 4** — Tourisme Corrèze's primary value; consistent with a 2.22 km × ~5.7% averaged gradient. Points array `[1]`.
   The publisher decides which authority is canonical. **Default recommendation: Cat 2** per CLAUDE.md narrative project context (which has survived prior data-layer audits as a content reference), pending ASO confirmation closer to July. If the publisher prefers to wait for ASO confirmation, the fallback is to leave Cat 2 as a placeholder with a code comment naming the open question and the planned recheck date.
3. **Fix the three fields together.** Once category is fixed, `points` follows mechanically from the scale. `gradient` — pick the value most defensible from the elevation data: re-measure from `data/elevation/segment-15.json` over the declared `[summit_km - length_km, summit_km]` window and use that value (round to one decimal place). If the new gradient disagrees with the existing `length_km`, fix `length_km` too — but flag in the PR body.
4. **Re-run validators.** `python3 processing/validate_points.py` must remain green. `npm test` must remain green. Any failure is the strand's responsibility to resolve before merge.
5. **Regression test addition.** Add an assertion that the points array for a climb matches the canonical points scale for its declared category. If `processing/validate_points.py` already has this invariant, confirm it would have caught the current `[10, 8, 6, 4]` mismatch (it should — `[10, 8, 6, 4]` is a Cat 1 prefix); if not, add it. Per the v1.4.18 parallel-source-of-truth-detector pattern (`feedback_parallel_source_of_truth_detector.md`): when two values must agree (category + points array), write the assertion that catches drift.
6. **PR open against `main`.** Title `fix(points-config): Suc au May category, gradient, and points (closes #513)`. Body lists: pre-fix values, post-fix values, source URLs verified, validator output before/after, any related issues filed.

## 6. Verification commands

- `python3 processing/validate_points.py` — green pre-fix (existing baseline), green post-fix.
- `npm test` — green pre-fix, green post-fix.
- **Red-green for the new assertion:** if step 5 adds a category↔points assertion, demonstrate it fires red against the pre-fix `[10, 8, 6, 4]` + HC state, green against the post-fix combination.
- `npm run build` — production build succeeds.
- **Spot-check the seg 15 entry page** in dev: PowerStats card reflects the new category/gradient/points; no rendering regressions.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `data/competition/points-config.json` (the Suc au May entry only — do not touch other climbs).
  - `processing/validate_points.py` if step 5 needs the new assertion.
  - `processing/tests/test_validate_points.py` (or wherever the existing points-config tests live) if a regression test is added.
- **What this strand reads:**
  - `data/elevation/segment-15.json` (gradient re-measurement).
  - `data/segments/segment-15.gpx` (route polyline).
  - `data/segments.json` (climb assignment to seg 15 — read-only, do not patch).
  - External: Tourisme Corrèze, ASO, L'Agglomérée notes.
- **What this strand must NOT touch:**
  - Other climbs in `points-config.json` — #518 owns the summit-km drift assertion that may surface follow-ups elsewhere.
  - `content/entries/15-*` — owned by seg 15 drafting strand.
  - `data/segments.json` climb assignments — generated from points-config; do not edit by hand.
  - `data/attractions.json` — owned by #564 strand.
  - `components/EntryCard.vue` — owned by #535 strand.
- **Cross-strand collisions and rebasing rules:**
  - **Seg 15 drafting strand fires in parallel.** That strand's brief instructs it to avoid quoting category/gradient in prose precisely because of this fix; the entry's PowerStats card auto-updates from points-config so no entry-side rebase is needed.
  - **#518 climb summit-km assertion strand fires in parallel.** It may add a new invariant that fires red against a pre-existing summit-km drift on a *different* climb; that does not block this strand. If #518 lands first and its assertion catches a drift in Suc au May's summit km (unlikely per the #513 discovery context), file it as a follow-up issue and resolve under #518's review window, not here.
  - Likely merge order: this strand merges first (smallest scope), then #518, then seg 15 drafting once both data fixes land.

## 8. Scope discipline

- **Do not expand to other climbs.** Suc au May only. #518 is the sibling assertion strand; sister-climb fixes will surface from it.
- **Do not retitle or restructure `points-config.json`.** Field-value edits only.
- **AskUserQuestion fires once at the category resolution.** Implementation after that is mechanical.
- **If the publisher prefers to defer:** acceptable outcome is "category-resolution checkpoint fires, publisher chooses 'leave as Cat 2 placeholder, recheck after ASO publishes'". Land the placeholder + the code comment + the recheck-date plan.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md` (Tourisme Corrèze vs ASO authority).
- `feedback_parallel_source_of_truth_detector.md` (category↔points assertion).
- `feedback_assertion_bug_class.md` (compute the assertion's diagnostic by hand before writing it).
- `feedback_strand_worktree_path.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_pr_closure_keywords.md`.
- `feedback_issues_describe_problems.md`.

## 10. Stop when

- PR opened against `main`, `Closes #513` in body.
- Category resolution checkpoint fired and answered; chosen value + rationale documented in PR body.
- All three contested fields (`category`, `gradient`, `points`) consistent with each other and with the chosen authority.
- `validate_points.py` and `npm test` green.
- Regression assertion added (or existing one's coverage of this mismatch confirmed); red-green demonstrated.
- Spot-check of seg 15 entry page in dev shows correct PowerStats.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-513` once the PR has merged.
- Final report posted to publisher: PR link, chosen category, source authority, validator state, any follow-up issues filed.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during 513-suc-au-may-points-config strand execution (<date>)`:
  - **Decision-actionable observations:** any other climbs found to share the same disagreement pattern, source-authority precedent set for ASO-vs-Tourisme conflicts.
  - **Light-tier pattern observations:** assertion-shape findings, sibling-strand interlock surprises.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock.
