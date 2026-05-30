"""Tests for the canonical frontmatter parser (processing/frontmatter.py, #326).

Covers the read path, the surgical byte-preserving write path, the publish.sh
helper logic (current_segment / find_entry_path), and -- the drift guard that
makes the shared schema load-bearing on the Python side -- validation of every
real content/entries/*.md against schemas/frontmatter.schema.json.
"""

import os

import pytest

from processing import frontmatter as fm

ENTRIES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'content', 'entries')


def _entry_files():
    return sorted(
        os.path.join(ENTRIES_DIR, f)
        for f in os.listdir(ENTRIES_DIR)
        if f.endswith('.md')
    )


# --- parse -----------------------------------------------------------------

class TestParse:
    def test_basic_fields_and_types(self):
        d = fm.parse('---\nsegment: 3\nkmEnd: 7.1\ndraft: false\nweather: null\n---\n\nbody')
        assert d['segment'] == 3 and isinstance(d['segment'], int)
        assert d['kmEnd'] == 7.1 and isinstance(d['kmEnd'], float)
        assert d['draft'] is False
        assert d['weather'] is None

    def test_bare_iso_date_stays_string(self):
        # The whole reason for the custom loader: YAML would coerce this to a
        # date object, but downstream code compares publishDate as a string.
        d = fm.parse('---\npublishDate: 2026-04-05\n---\n')
        assert d['publishDate'] == '2026-04-05'
        assert isinstance(d['publishDate'], str)

    def test_inline_json_images_becomes_list(self):
        d = fm.parse('---\nimages: [{"src": "/a.jpg", "alt": "a"}]\n---\n')
        assert d['images'] == [{'src': '/a.jpg', 'alt': 'a'}]

    def test_no_frontmatter_returns_empty(self):
        assert fm.parse('# just a heading\n') == {}

    def test_non_mapping_returns_empty(self):
        assert fm.parse('---\n- a\n- b\n---\n') == {}

    def test_parse_file(self, tmp_path):
        p = tmp_path / 'e.md'
        p.write_text('---\nsegment: 9\n---\nbody\n')
        assert fm.parse_file(str(p))['segment'] == 9


# --- split_frontmatter -----------------------------------------------------

class TestSplitFrontmatter:
    def test_splits_raw_and_body(self):
        raw, body = fm.split_frontmatter('---\nsegment: 1\n---\n\n# Title\n')
        assert raw == 'segment: 1'
        assert body == '\n\n# Title\n'

    def test_no_frontmatter(self):
        raw, body = fm.split_frontmatter('# Title\n')
        assert raw is None
        assert body == '# Title\n'


# --- set_field -------------------------------------------------------------

class TestSetField:
    def test_replaces_existing_line(self):
        out = fm.set_field('---\nweather: null\ndraft: false\n---\nbody', 'weather', '{"t": 1}')
        assert 'weather: {"t": 1}' in out
        assert 'weather: null' not in out
        assert out.endswith('---\nbody')

    def test_inserts_before_closing_fence_when_absent(self):
        out = fm.set_field('---\nsegment: 1\n---\nbody', 'imagesOptional', 'true')
        assert out == '---\nsegment: 1\nimagesOptional: true\n---\nbody'

    def test_value_with_backslash_not_treated_as_backreference(self):
        out = fm.set_field('---\nweather: null\n---\n', 'weather', r'{"p": "a\1b"}')
        assert r'weather: {"p": "a\1b"}' in out

    def test_no_frontmatter_returned_unchanged(self):
        content = '# no frontmatter\n'
        assert fm.set_field(content, 'draft', 'false') == content

    def test_draft_flip_byte_exact(self):
        out = fm.set_field('---\nsegment: 9\ndraft: true\n---\n\nbody', 'draft', 'false')
        assert out == '---\nsegment: 9\ndraft: false\n---\n\nbody'


# --- publish.sh helpers ----------------------------------------------------

class TestPublishHelpers:
    def _dir(self, tmp_path, entries):
        for name, body in entries.items():
            (tmp_path / name).write_text(body)
        return str(tmp_path)

    def test_current_segment_picks_highest_published(self, tmp_path):
        d = self._dir(tmp_path, {
            '01.md': '---\nsegment: 1\npublishDate: 2026-04-05\ndraft: false\n---\n',
            '02.md': '---\nsegment: 2\npublishDate: 2026-04-08\ndraft: false\n---\n',
            '03.md': '---\nsegment: 3\npublishDate: 2026-09-01\ndraft: false\n---\n',
        })
        assert fm.current_segment(d, today='2026-04-10') == 2

    def test_current_segment_skips_drafts(self, tmp_path):
        d = self._dir(tmp_path, {
            '01.md': '---\nsegment: 1\npublishDate: 2026-04-05\ndraft: false\n---\n',
            '02.md': '---\nsegment: 2\npublishDate: 2026-04-08\ndraft: true\n---\n',
        })
        assert fm.current_segment(d, today='2026-04-10') == 1

    def test_current_segment_none_qualifies(self, tmp_path):
        d = self._dir(tmp_path, {
            '01.md': '---\nsegment: 1\npublishDate: 2026-09-01\ndraft: false\n---\n',
        })
        assert fm.current_segment(d, today='2026-04-10') == 0

    def test_find_entry_path(self, tmp_path):
        d = self._dir(tmp_path, {
            '01.md': '---\nsegment: 1\n---\n',
            '07.md': '---\nsegment: 7\n---\n',
        })
        assert fm.find_entry_path(d, 7) == os.path.join(d, '07.md')
        assert fm.find_entry_path(d, 99) is None


# --- _format_scalar (the `get` CLI rendering) ------------------------------

class TestFormatScalar:
    @pytest.mark.parametrize('value,expected', [
        (None, ''),
        (True, 'true'),
        (False, 'false'),
        (9, '9'),
        ('2026-04-05', '2026-04-05'),
    ])
    def test_render(self, value, expected):
        assert fm._format_scalar(value) == expected


# --- schema drift guard ----------------------------------------------------

class TestSchemaConformance:
    def test_every_entry_conforms_to_shared_schema(self):
        failures = []
        for path in _entry_files():
            errors = fm.validate(fm.parse_file(path))
            if errors:
                failures.append(f'{os.path.basename(path)}: {"; ".join(errors)}')
        assert not failures, 'Entries violate frontmatter schema:\n' + '\n'.join(failures)

    def test_validate_flags_a_bad_entry(self):
        # segment is required and must be an integer; a string must fail.
        errors = fm.validate({'segment': 'not-an-int'})
        assert errors
