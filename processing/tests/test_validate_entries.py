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
