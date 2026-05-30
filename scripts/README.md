# scripts/

Operational shell scripts for the publish pipeline and repo housekeeping.

| Script | Purpose |
|--------|---------|
| `publish.sh` | Publish-day pipeline: stats, points, snapshot, weather, build, deploy, frontmatter reconciliation, tag/release. |
| `add-rider-data.sh` | Append a day's rider distances and regenerate stats. |
| `create-release.sh` | Tag + GitHub Release helper (called by `publish.sh` and the `/release` ceremony). |
| `list-stale-branches.sh` | Report merged/stale branches. |
| `setup-vm.sh` | One-time production VM provisioning. |

## Testing shell scripts

Shell logic in `scripts/` gets regression coverage with [bats-core](https://github.com/bats-core/bats-core)
under `tests/shell/`. The rule:

- **Every load-bearing gate in a shell script gets a bats test.** The publish
  pipeline's safety gates (draft pre-flight #617, idempotent merge #618, and
  weather single-entry isolation #619, which lives in `processing/weather.py`)
  are covered in `tests/shell/`.
- **Write the test red against a restored-broken state before relying on green.**
  For each gate, transiently mutate the source so it exhibits the pre-gate bug
  (e.g. `sed` `preflight_draft_check` to `return 0`), confirm the test fails,
  then `git checkout -- <file>` and confirm it passes. Never commit the
  breakage. A test that has only ever been seen green is not yet trusted.
- **Run the suite with `npm run test:shell`** (equivalently `npx bats tests/shell`).
  It also runs in CI after `npm ci`.

`publish.sh` defines its gate logic in sourceable functions
(`preflight_draft_check`, `merge_frontmatter_commit`) and a source-guard
(`[ "${BASH_SOURCE[0]}" != "${0}" ] && return 0`) so the tests can source the
file and call those functions without driving a full publish. Keep that guard
in place when editing the script.
