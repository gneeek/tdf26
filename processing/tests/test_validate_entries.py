"""Tests for validate_entries.py - entry image validation."""

import os
import tempfile
from datetime import date

import pytest


def write_entry(dir_path, filename, frontmatter_lines):
    """Helper to write a markdown entry file with frontmatter."""
    path = os.path.join(dir_path, filename)
    content = "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# Test Entry\n"
    with open(path, "w") as f:
        f.write(content)
    return path


@pytest.fixture
def entries_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


class TestFindEntriesToValidate:
    """Test which entries are selected for validation."""

    def test_entry_published_today_is_checked(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            "images: []",
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 1
        assert results[0]["filename"] == "01-test.md"

    def test_entry_published_yesterday_is_skipped(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-06",
            "images: []",
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 0

    def test_future_publish_date_is_skipped(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-08",
            "images: []",
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 0

    def test_draft_entry_is_skipped(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            "images: []",
            "draft: true",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 0


class TestImageValidation:
    """Test image presence checks."""

    def test_entry_with_images_passes(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            'images: [{src: "/img/test.jpg", alt: "Test", attribution: "CC"}]',
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 0

    def test_entry_with_images_optional_passes(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            "images: []",
            "imagesOptional: true",
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 0

    def test_entry_without_images_needs_prompt(self, entries_dir):
        from validate_entries import find_entries_to_validate

        write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            "images: []",
            "draft: false",
        ])
        results = find_entries_to_validate(entries_dir, today=date(2026, 4, 7))
        assert len(results) == 1
        assert results[0]["needs_prompt"] is True


class TestFrontmatterUpdate:
    """Test writing imagesOptional to frontmatter."""

    def test_sets_images_optional_in_frontmatter(self, entries_dir):
        from validate_entries import set_images_optional

        path = write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            "title: Test",
            "publishDate: 2026-04-07",
            "images: []",
            "draft: false",
        ])
        set_images_optional(path)
        with open(path) as f:
            content = f.read()
        assert "imagesOptional: true" in content

    def test_preserves_existing_frontmatter(self, entries_dir):
        from validate_entries import set_images_optional

        path = write_entry(entries_dir, "01-test.md", [
            "segment: 1",
            'title: "Test Entry"',
            "publishDate: 2026-04-07",
            "images: []",
            "draft: false",
        ])
        set_images_optional(path)
        with open(path) as f:
            content = f.read()
        assert "segment: 1" in content
        assert 'title: "Test Entry"' in content
        assert "draft: false" in content
        assert "# Test Entry" in content


def write_body(dir_path, filename, body, draft=False):
    """Write an entry with arbitrary body content under standard frontmatter."""
    path = os.path.join(dir_path, filename)
    fm = [
        "segment: 99",
        'title: "Test"',
        "publishDate: 2000-01-01",
        "images: []",
        "imagesOptional: true",
        f"draft: {'true' if draft else 'false'}",
    ]
    content = "---\n" + "\n".join(fm) + "\n---\n\n" + body + "\n"
    with open(path, "w") as f:
        f.write(content)
    return path


class TestMdcBalanceCheck:
    """Test the per-file MDC block balance scan."""

    def test_balanced_single_block_no_errors(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          '::inline-figure{src="/x.jpg"}\n::\n')
        assert mdc_balance_check(path) == []

    def test_unbalanced_open_reports_opener_line(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          '::inline-figure{src="/x.jpg"}\n\nBody text never closed.\n')
        errors = mdc_balance_check(path)
        assert len(errors) == 1
        assert "unclosed MDC block `::inline-figure`" in errors[0]
        assert ":10:" in errors[0]  # opener is on line 10 after 8-line frontmatter + blank

    def test_orphan_close_reports_close_line(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          'No open block here.\n\n::\n')
        errors = mdc_balance_check(path)
        assert len(errors) == 1
        assert "unmatched MDC close" in errors[0]

    def test_nested_balanced_no_errors(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          '::card\n::inline-figure{src="/x.jpg"}\n::\n::\n')
        assert mdc_balance_check(path) == []

    def test_inline_form_not_counted_as_open(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          'Some :inline-figure{src="/x.jpg"} text with a single colon.\n')
        assert mdc_balance_check(path) == []

    def test_code_fence_skipped(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          '```md\n::inline-figure{src="/x.jpg"}\n```\n')
        assert mdc_balance_check(path) == []

    def test_frontmatter_dash_does_not_open_block(self, entries_dir):
        from validate_entries import mdc_balance_check

        # Standard frontmatter is already in write_body; just confirm a body
        # with no MDC markers returns no errors.
        path = write_body(entries_dir, "01.md", 'Plain prose only.\n')
        assert mdc_balance_check(path) == []

    def test_multiple_opens_unbalanced_lists_each(self, entries_dir):
        from validate_entries import mdc_balance_check

        path = write_body(entries_dir, "01.md",
                          '::card\n\n::figure\n\nbody\n')
        errors = mdc_balance_check(path)
        assert len(errors) == 2
        assert any("`::card`" in e for e in errors)
        assert any("`::figure`" in e for e in errors)


class TestMdcCliIntegration:
    """Test the CLI main loop aggregates MDC errors and exits non-zero."""

    def test_cli_green_on_balanced_dir(self, entries_dir, capsys):
        import validate_entries as ve

        write_body(entries_dir, "01.md",
                   '::inline-figure{src="/x.jpg"}\n::\n')
        # Stub argv
        import sys
        old_argv = sys.argv
        sys.argv = ["validate_entries", "--entries-dir", entries_dir, "--non-interactive"]
        try:
            ve.main()
        finally:
            sys.argv = old_argv
        out = capsys.readouterr().out
        assert "MDC blocks balanced" in out

    def test_cli_red_on_unbalanced_dir(self, entries_dir, capsys):
        import validate_entries as ve

        write_body(entries_dir, "01.md",
                   '::inline-figure{src="/x.jpg"}\n\nbody never closed.\n')
        import sys
        old_argv = sys.argv
        sys.argv = ["validate_entries", "--entries-dir", entries_dir, "--non-interactive"]
        try:
            with pytest.raises(SystemExit) as exc:
                ve.main()
            assert exc.value.code == 1
        finally:
            sys.argv = old_argv
        out = capsys.readouterr().out
        assert "Unbalanced MDC blocks detected" in out

    def test_cli_skips_draft_entries(self, entries_dir, capsys):
        import validate_entries as ve

        write_body(entries_dir, "01.md",
                   '::inline-figure{src="/x.jpg"}\n\nbody never closed.\n',
                   draft=True)
        import sys
        old_argv = sys.argv
        sys.argv = ["validate_entries", "--entries-dir", entries_dir, "--non-interactive"]
        try:
            ve.main()
        finally:
            sys.argv = old_argv
        out = capsys.readouterr().out
        assert "Unbalanced" not in out
