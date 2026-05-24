# Strand: Climb summit-km drift assertion (#518)

Auto-mode code/test strand to add an assertion that catches drift between a climb's declared `summit_km` and the actual GPX local elevation maximum. Authored 2026-05-24 as part of the v1.4.19 close-out parallel slate. Retro v1.4.19 promoted this from candidate to must-have (five-instance carry: Lachaud, Naves, Mont Bessou, Croix de Pey, Côte des Gardes).

## 1. Goal

Land an assertion that, for each climb with a declared `summit_km`, the GPX local elevation maximum in a tolerance window around the declared summit is within an acceptable offset. The existing validators (invariant 3 "rising into summit" and invariant 4 "length × gradient ≈ GPX gain") are structurally blind to a declared summit km that sits on a rising flank — PR #516's Naves fix was caught by manual audit, not by automation.

Closes #518. Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/52). Runs in **auto-mode** per the v1.4.18 retro learning (code-refactor / test addition suits auto-mode). One mandatory AskUserQuestion checkpoint: the tolerance window's size (see §5 step 3). If the assertion catches drift on any of the five named climbs (Lachaud, Naves, Mont Bessou, Croix de Pey, Côte des Gardes), file a follow-up issue per climb and resolve under separate scope — do not expand this strand.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/518-summit-km-assertion /home/jhs/code/tdf26-518 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `data/competition/points-config.json` declares each climb's `summit_km` and `length_km`. Read this directly; do not transcribe.
- `data/elevation/segment-NN.json` carries the per-segment elevation profile (distance + elevation arrays) the assertion will scan. The existing `tests/utils/climb-gradient.test.ts` (added in PR #516) already loads these files — model the new assertion on its loader pattern.
- The known failure mode: a declared summit km that sits short of the actual GPX peak by a non-trivial distance (Naves was 860m short). The actual peak is typically slightly higher than the declared point (Naves was +30m higher).
- **Tolerance design problem:** elevation data is smoothed; the GPX argmax may not exactly equal the declared summit even when both are correct. A reasonable tolerance is ~100m of km along the route and ~5m of elevation — but this is a guess; tune against the five named climbs and any other climb in `points-config.json` that the assertion runs against. The publisher checkpoint at §5 step 3 picks the values.
- Per `feedback_assertion_bug_class.md`: before writing the assertion, compute its diagnostic for the Naves pre-fix state by hand. If the assertion as drafted would not have caught Naves's 860m / +30m drift, the assertion is wrong — redesign before writing.

## 4. Target issues

**Closes #518** — use `Closes #518` in PR body (per `feedback_pr_closure_keywords.md`).

If the assertion catches drift on any of the five named climbs:
- **Lachaud, Naves, Mont Bessou, Croix de Pey, Côte des Gardes** — file one follow-up issue per climb that fails; resolve under separate scope. Naves was already fixed by PR #516 and should pass; if it still fails, the assertion or PR #516 is wrong and needs investigation, but do not roll the fix into this strand.

If the assertion catches drift on a climb *not* in the five named, file a follow-up issue too — the strand's deliverable is the assertion, not the data fixes.

## 5. Workflow

Single-issue strand; collapse "Target issues" + "Workflow per issue" into one cadence.

1. **Survey the existing test infrastructure.** Read `tests/utils/climb-gradient.test.ts` end-to-end. Understand: how it loads `points-config.json`, how it loads `data/elevation/segment-NN.json`, how it asserts, how it reports failures, how it skips climbs without `length_km`.
2. **Sketch the assertion shape.** Pseudocode:
   ```
   for each climb in points-config.climbs:
     if climb.length_km is null: skip
     window = [climb.summit_km - climb.length_km, climb.summit_km + tolerance_km]
     samples = elevation_data for segment(climb), filtered to window
     gpx_argmax_km, gpx_argmax_elev = argmax(samples by elevation)
     assert abs(gpx_argmax_km - climb.summit_km) <= tolerance_km
     assert abs(gpx_argmax_elev - elevation_at(climb.summit_km)) <= tolerance_m
   ```
   Naves's pre-fix state: argmax_km - summit_km = +0.86, argmax_elev - elev_at_summit_km = +30. Any tolerance below 0.86 km catches it.
3. **Tolerance checkpoint (AskUserQuestion).** Present three tolerance regimes:
   - **Tight (tolerance_km = 0.1, tolerance_m = 5)** — fires on most real drift; risks false positives on smoothed elevation data.
   - **Moderate (tolerance_km = 0.3, tolerance_m = 10)** — catches Naves-class drift comfortably; some false-positive resilience.
   - **Loose (tolerance_km = 0.5, tolerance_m = 20)** — only catches egregious drift; misses borderline cases.
   The publisher decides. **Default recommendation: Moderate** (caught Naves with margin, low false-positive risk against smoothed data).
4. **Implement the assertion.** Add to `tests/utils/climb-gradient.test.ts` or a sibling `tests/utils/climb-summit-km.test.ts` — pick the cleaner factoring. Both are acceptable per #518's body ("Could be folded into the same file or split out — either is fine"). Reuse the existing loader pattern.
5. **Demonstrate red-green by hand.** With the assertion at the chosen tolerance, run it against `main` (post-PR-#516 state). It should be green on all climbs in `points-config.json` if all are correctly declared. To demonstrate red, temporarily edit a climb's `summit_km` to the pre-fix Naves value (or any value 1km off the true summit) — show the assertion fires red. Revert before commit.
6. **If the assertion fires red on any of the five named climbs at the chosen tolerance**, **stop and file follow-up issues per climb**, then proceed to merge the assertion with those climbs documented as known-failing (or, more conservatively, with a temporary skip-list for the named climbs to keep CI green until the follow-up fixes land). Discuss with the publisher via AskUserQuestion if this happens; do not silently skip.
7. **PR open against `main`.** Title `test(climbs): assertion catches summit-km drift from GPX peak (closes #518)`. Body lists: tolerance chosen, red-green demonstration, climbs that pass, climbs that fire red (if any), follow-up issues filed.

## 6. Verification commands

- `npm test` — green pre-change (existing baseline), green post-change if no climb fires red.
- `npm test -- climb-summit-km` (or similar, scoped to the new test) — runs the new assertion in isolation.
- **Red-green for the new assertion:** as in §5 step 5, demonstrate with a temporary `summit_km` edit; revert before commit.
- `python3 processing/validate_points.py` — green (this validator is separate; new assertion is in tests/, not validators/).
- `npm run build` — production build succeeds.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `tests/utils/climb-gradient.test.ts` (extend) **or** a new sibling `tests/utils/climb-summit-km.test.ts`.
  - Possibly a small shared loader if the existing one is too tied to the gradient calc — refactor minimally.
- **What this strand reads:**
  - `data/competition/points-config.json` (read-only — #513 owns mutation of the Suc au May entry, this strand reads what's there).
  - `data/elevation/segment-*.json` (all segments).
  - `data/segments/segment-*.gpx` (only if elevation JSON is insufficient — should not be needed).
- **What this strand must NOT touch:**
  - `data/competition/points-config.json` itself — even if the assertion fires red on a climb, fix via follow-up issue, not this strand.
  - `processing/validate_points.py` — only extend the JS-side test surface; this matches #518's discovery context.
  - `content/entries/*` — out of scope.
  - `data/attractions.json` — owned by #564 strand.
  - `components/EntryCard.vue` — owned by #535 strand.
- **Cross-strand collisions and rebasing rules:**
  - **#513 fires in parallel.** If #513 changes Suc au May's `length_km` or `summit_km` (it should not touch `summit_km` per #513's brief, but `length_km` may move), the assertion's window for Suc au May shifts. Re-run the assertion after #513 lands; if Suc au May now fires red, file as follow-up issue per §5 step 6.
  - **Seg 15 drafting strand** does not touch this strand's files; no collision.
  - **#564 strand** does not touch this strand's files; no collision.
  - **#535 strand** does not touch this strand's files; no collision.
  - Likely merge order: #513 and #564 merge first, then this strand (so the assertion runs against the post-fix `points-config.json`), then seg 15 drafting.

## 8. Scope discipline

- **Do not fix climbs.** Even if the assertion catches Lachaud / Mont Bessou / Croix de Pey / Côte des Gardes drift, file follow-up issues and merge the assertion with the failing climbs either documented or temporarily skipped (with publisher consent via AskUserQuestion).
- **Do not generalise the assertion** to also check `length_km` consistency or `gradient` consistency — those have separate assertions (invariant 4 + the climb-gradient test). This strand owns only the summit-km drift bug class.
- **AskUserQuestion fires at tolerance + only re-fires if step 6 hits a red climb.** Implementation in between is mechanical.

## 9. Memories that apply

- `feedback_assertion_bug_class.md` (compute the assertion's diagnostic by hand against Naves before writing).
- `feedback_parallel_source_of_truth_detector.md` (this assertion is exactly that pattern: declared summit km vs GPX argmax).
- `feedback_source_of_truth_framing.md`.
- `feedback_strand_worktree_path.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_pr_closure_keywords.md`.
- `feedback_issues_describe_problems.md`.

## 10. Stop when

- PR opened against `main`, `Closes #518` in body.
- Tolerance checkpoint fired and answered; chosen values + rationale documented.
- Assertion implemented; red-green demonstrated in PR body.
- All climbs in `points-config.json` either pass the assertion or have follow-up issues filed (with publisher consent via AskUserQuestion).
- `npm test` green; `npm run build` green.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-518` once the PR has merged.
- Final report posted to publisher: PR link, tolerance chosen, climbs passing / firing red, follow-up issues filed.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during 518-summit-km-assertion strand execution (<date>)`:
  - **Decision-actionable observations:** how many of the five named climbs fired red, any unnamed climbs that also fired red, tolerance precedent for future assertions of the same shape.
  - **Light-tier pattern observations:** assertion-by-hand-diagnostic exercise findings, test-file-factoring decisions.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired, approximate wall-clock.
