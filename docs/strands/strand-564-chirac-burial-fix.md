# Strand: Chirac burial-location fix (#564)

Auto-mode small data-correctness strand to fix the Musée du Président Jacques Chirac entry in `data/attractions.json`, which currently asserts Chirac is buried at Sarran. He is buried at Cimetière du Montparnasse, Paris 14e. Authored 2026-05-24 as part of the v1.4.19 close-out parallel slate.

## 1. Goal

Land a corrected description for the Musée du Président Jacques Chirac entry in `data/attractions.json` before the seg 15 publish window opens. The seg 15 drafting strand reaches into the Sarran/Chirac adjacency thread for the Monédières corridor; the wrong burial framing must not bleed into the entry.

Closes #564. Milestone: [v1.4.19](https://github.com/gneeek/tdf26/milestone/52). Runs in **auto-mode** per the v1.4.18 retro learning (small data fix suits auto-mode). No checkpoints — the recommended-fix language is in the issue body and is mechanical to apply.

## 2. Filesystem posture

```
git -C /home/jhs/code/tdf26 worktree add -b feature/564-chirac-burial /home/jhs/code/tdf26-564 main
```

- Run from outside the repo, or use `git -C`. Do not run `git worktree add ...` from inside the repo (per `feedback_strand_worktree_path.md`).
- Do **not** add `ln -s ../tdf26/.claude .claude` — `.claude/` is tracked.
- Branch verification: run `git branch --show-current` immediately before each `git add` / `git commit` (per `feedback_shared_tree_branch_verification.md`).

## 3. Source-of-truth posture

- `data/attractions.json` is the canonical reader-facing attractions index. The entry in question is `Musée du Président Jacques Chirac`.
- **External source for the correction** (verify before quoting in PR body): `fr.wikipedia.org/wiki/Jacques_Chirac` — the Sépulture infobox names *Cimetière du Montparnasse, Paris 14e*. Cross-check against `en.wikipedia.org/wiki/Jacques_Chirac` for English-language confirmation.
- The legitimate Sarran connections that survive the fix:
  - Château de Bity (Chirac family château, in the Sarran commune).
  - Bernadette Chirac as a municipal councillor of Sarran.
  - The Musée du Président Jacques Chirac itself (the gifts-museum at Sarran).
  - The October 2019 memorial gathering at Sarran (a *memorial*, not an interment).
- Per `feedback_source_of_truth_framing.md`: French Wikipedia is the canonical source for French biographical details, not English-language travel sites that may have transcribed the Sarran-memorial conflation.

## 4. Target issues

**Closes #564** — use `Closes #564` in PR body (per `feedback_pr_closure_keywords.md`).

If the audit surfaces other attractions with similar factual issues, file separate issues per finding — do not expand scope.

## 5. Workflow

Single-issue strand; collapse "Target issues" + "Workflow per issue" into one cadence.

1. **Read the current entry.** Locate `Musée du Président Jacques Chirac` in `data/attractions.json`. Capture the pre-fix description verbatim for the PR body.
2. **Verify the correction** against `fr.wikipedia.org/wiki/Jacques_Chirac` (Sépulture infobox + biographical body). Confirm the cemetery name and arrondissement; confirm the Sarran/Bity/Bernadette framing is accurate.
3. **Rewrite the description.** Drop the "buried in Sarran communal cemetery" sentence (or clause). Replace with framing along the lines of: "Sarran was the Chirac family home — the Château de Bity is here, and Bernadette Chirac served as a municipal councillor of the commune. Chirac is buried at Cimetière du Montparnasse in Paris; Sarran hosted a memorial gathering in October 2019." Adapt to the entry's existing voice and length budget — do not lengthen materially.
4. **Audit-trail metadata.** If the entry has any `verified` / `lastVerified` / `source` fields per #476 conventions, update them to reflect this fix's verification date and the Wikipedia source URL. If no such fields exist, skip — #476 is a separate v1.4.20 strand and adding the fields ad hoc would prejudge its design.
5. **PR open against `main`.** Title `fix(attractions): Chirac burial location at Montparnasse, not Sarran (closes #564)`. Body shows pre-fix and post-fix description; lists external source URL verified; notes the Sarran connections retained.

## 6. Verification commands

- `python3 processing/validate_entries.py --entries-dir content/entries --non-interactive` — green (attractions changes don't typically touch entry validation, but confirm no schema regression).
- `npm test` — green pre-fix, green post-fix.
- `npm run build` — production build succeeds.
- **Spot-check** the seg 13 / 14 / 15 entry pages in dev for any place the attractions entry surfaces in card or detail form — confirm the new text renders.

## 7. Cross-strand sharing notes

- **What this strand owns (write):**
  - `data/attractions.json` — the Musée du Président Jacques Chirac entry only.
- **What this strand reads:**
  - External: `fr.wikipedia.org/wiki/Jacques_Chirac`.
  - `content/research/segs-14-16-block-research.md` (the dossier flagged this error; cross-check the recommended fix against the dossier framing).
- **What this strand must NOT touch:**
  - Other attractions entries — file separate issues per finding.
  - `content/entries/*` — published entries are fixed (per `feedback_content_change_rule.md`).
  - `data/competition/points-config.json` — owned by #513 strand.
  - `tests/utils/*.test.ts` — owned by #518 strand.
  - `components/EntryCard.vue` — owned by #535 strand.
- **Cross-strand collisions and rebasing rules:**
  - **Seg 15 drafting strand fires in parallel.** Its brief instructs it to avoid the burial framing; no collision expected, but the seg 15 draft may want to land after this fix so its Sarran/Chirac thread reads against the corrected entry. Merge order recommendation: this strand merges first.
  - **No collision with #513 or #518.** Different files.

## 8. Scope discipline

- **Single-entry fix.** Do not audit other attractions; if anything else looks wrong, file an issue and move on.
- **No checkpoints.** The recommended-fix language is in #564's body; apply mechanically.
- **If the recommended fix produces an entry that reads awkwardly, propose two phrasings in the PR body and let review decide** — do not over-design.

## 9. Memories that apply

- `feedback_source_of_truth_framing.md`.
- `feedback_content_change_rule.md`.
- `feedback_strand_worktree_path.md`.
- `feedback_shared_tree_branch_verification.md`.
- `feedback_pr_closure_keywords.md`.
- `feedback_issues_describe_problems.md`.

## 10. Stop when

- PR opened against `main`, `Closes #564` in body.
- Pre-fix and post-fix description both shown in PR body.
- External source URL (`fr.wikipedia.org/wiki/Jacques_Chirac`) verified and linked.
- `npm test` + entry validators green; `npm run build` green.
- Spot-check of any reader surface using the attractions entry confirms the new text renders.
- **Cleanup (you run these, do not hand off):** `git -C /home/jhs/code/tdf26 worktree remove tdf26-564` once the PR has merged.
- Final report posted to publisher: PR link, pre/post description, source verified, any follow-up issues filed.
- **Retro inputs written to `project_next_planning_notes.md` at close.** Section `## Items surfaced during 564-chirac-burial strand execution (<date>)`:
  - **Decision-actionable observations:** any other attractions entries found to have similar issues during the audit, any audit-trail metadata gaps surfaced.
  - **Light-tier pattern observations:** dossier-flagged-error workflow shape, source-authority precedent.
  - **Numeric stats:** files-touched, commits on branch, AskUserQuestion checkpoints fired (likely zero), approximate wall-clock.
