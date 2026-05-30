#!/usr/bin/env bats
#
# #618 idempotent merge gate (merge_frontmatter_commit in scripts/publish.sh).
#
# Regression intent: when the publish branch's frontmatter work is already on
# main, a re-run must NOT attempt a second commit/merge/push. In the live
# pipeline the equivalent guard is the gh-PR-state re-query (Step 9): an
# already-MERGED reconciliation PR is treated as success so the run proceeds to
# tag/release instead of dying under set -e. merge_frontmatter_commit models
# that "already merged -> skip" decision locally via `git merge-base
# --is-ancestor <branch> main`, which is what makes it unit-testable.
#
# Red-green: sed out the --is-ancestor early-return -> the function falls
# through to git add/commit/push even when already merged, the stub log records
# them, and this test goes red; git checkout -- restores green.
#
# The git PATH-shim stub records every invocation to a TEMPFILE (not an
# in-memory variable): merge_frontmatter_commit runs git inside `$(...)` /
# `if` subshells, and a variable mutated in a subshell would be lost in the
# parent. (Known project gotcha: reference_shell_stub_subshell_state.)

load test_helper

setup() {
    TMPDIR_TEST="$(mktemp -d)"
    BIN_DIR="$TMPDIR_TEST/bin"
    mkdir -p "$BIN_DIR"
    GIT_LOG_FILE="$TMPDIR_TEST/git-calls.log"
    : > "$GIT_LOG_FILE"

    # git PATH-shim: records args to the tempfile, returns success for the
    # ancestry check (simulating "already merged"), success for everything else.
    cat > "$BIN_DIR/git" <<EOF
#!/usr/bin/env bash
echo "\$@" >> "$GIT_LOG_FILE"
if [ "\$1" = "merge-base" ] && [ "\$2" = "--is-ancestor" ]; then
    exit 0   # branch IS an ancestor of main -> already merged
fi
exit 0
EOF
    chmod +x "$BIN_DIR/git"

    ORIG_PATH="$PATH"
    PATH="$BIN_DIR:$PATH"
}

teardown() {
    PATH="$ORIG_PATH"
    rm -rf "$TMPDIR_TEST"
}

@test "already-merged branch skips commit/merge/push" {
    entry="$TMPDIR_TEST/09-test.md"
    make_entry "$entry" "false"

    # shellcheck disable=SC1090
    source "$PUBLISH_SH"
    run merge_frontmatter_commit "$entry"

    [ "$status" -eq 0 ]
    [[ "$output" == *"already merged; skipping"* ]]

    # The only git call should be the ancestry check. No mutating commands.
    ! grep -q 'commit' "$GIT_LOG_FILE"
    ! grep -q 'merge --no-ff' "$GIT_LOG_FILE"
    ! grep -qw 'push' "$GIT_LOG_FILE"

    # Sanity: the ancestry check itself WAS made (proves the stub ran).
    grep -q 'merge-base --is-ancestor' "$GIT_LOG_FILE"
}
