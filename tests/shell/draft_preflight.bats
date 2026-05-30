#!/usr/bin/env bats
#
# #617 draft pre-flight gate (preflight_draft_check in scripts/publish.sh).
#
# Regression intent: a draft:true entry must NOT reach the build untouched. The
# shipped gate auto-flips draft:true -> draft:false in place (the publisher
# chose auto-flip over abort, per PR #629), so production never 404s on a
# silently-excluded entry. A draft:false entry is left unchanged.
#
# Red-green: sed preflight_draft_check to `return 0` (no flip) -> the draft:true
# entry stays draft:true and this test goes red; git checkout -- restores green.
#
# NOTE (deviation from the #508 brief): the brief described preflight_draft_check
# as returning exit 3 with "refusing to publish". The code actually shipped on
# main (b857802 / PR #629) auto-flips instead of refusing. The test asserts the
# real shipped behaviour. See the report for the full reconciliation.

load test_helper

setup() {
    TMPDIR_TEST="$(mktemp -d)"
    PY="$(pick_python)"
}

teardown() {
    rm -rf "$TMPDIR_TEST"
}

@test "draft:true entry is flipped to draft:false (not left as draft)" {
    entry="$TMPDIR_TEST/09-test.md"
    make_entry "$entry" "true"

    # shellcheck disable=SC1090
    source "$PUBLISH_SH"
    run preflight_draft_check "$PY" "$entry" 9

    [ "$status" -eq 0 ]
    # The gate must have changed the on-disk draft field.
    grep -q '^draft: false' "$entry"
    ! grep -q '^draft: true' "$entry"
}

@test "draft:false entry passes untouched" {
    entry="$TMPDIR_TEST/09-test.md"
    make_entry "$entry" "false"
    before="$(md5sum "$entry" | cut -d' ' -f1)"

    # shellcheck disable=SC1090
    source "$PUBLISH_SH"
    run preflight_draft_check "$PY" "$entry" 9

    [ "$status" -eq 0 ]
    after="$(md5sum "$entry" | cut -d' ' -f1)"
    [ "$before" = "$after" ]
}

@test "missing entry file aborts the publish (non-zero exit)" {
    # shellcheck disable=SC1090
    source "$PUBLISH_SH"
    run preflight_draft_check "$PY" "$TMPDIR_TEST/does-not-exist.md" 9

    [ "$status" -ne 0 ]
    [[ "$output" == *"Cannot publish"* ]]
}
