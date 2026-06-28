"""Byte-identical migration proof for the #326 parser consolidation.

This module pins what "byte-identical" meant when the hand-rolled regex
frontmatter parsers were removed. It embeds the *exact* pre-#326 extraction
and write logic from each Python consumer (validate_entries, weather,
pick_entry_thumbnails, scripts/publish.sh) and asserts the canonical parser
produces identical results on **every current content/entries/*.md**.

Per the strand brief (§5/§6) the migration must not change any consumer's
observable behaviour. These tests are the durable regression guard for that:
if a future change to processing/frontmatter.py drifts from the old
behaviour, the relevant assertion fails. The embedded `old_*` functions are
intentionally frozen copies of deleted code -- do not "modernise" them.
"""

import json
import os
import re

from processing import frontmatter as fm

ENTRIES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'content', 'entries')


def _entries():
    for name in sorted(os.listdir(ENTRIES_DIR)):
        if name.endswith('.md'):
            path = os.path.join(ENTRIES_DIR, name)
            with open(path) as f:
                yield name, path, f.read()


# --- frozen pre-#326 implementations ---------------------------------------

def old_validate_parse(content):
    """validate_entries.parse_frontmatter, verbatim (pre-#326)."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    out = {}
    for line in match.group(1).split('\n'):
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == 'true':
                out[key] = True
            elif val == 'false':
                out[key] = False
            elif val == 'null':
                out[key] = None
            elif val == '[]':
                out[key] = []
            elif val.startswith('[') and val.endswith(']') and val != '[]':
                out[key] = val
            else:
                out[key] = val
    return out


def old_weather_seg(content):
    m = re.search(r'^segment:\s*(\d+)', content, re.MULTILINE)
    return int(m.group(1)) if m else None


def old_weather_pubdate(content):
    m = re.search(r'^publishDate:\s*(\S+)', content, re.MULTILINE)
    return m.group(1) if m else None


def old_weather_is_draft(content):
    m = re.search(r'^draft:\s*(\S+)', content, re.MULTILINE)
    return m.group(1).lower() == 'true' if m else False


def old_datacutoff(content):
    m = re.search(r'^dataCutoff:\s*(\S+)', content, re.MULTILINE)
    return m.group(1) if m else ''


def old_set_images_optional(content):
    match = re.match(r'^(---\n)(.*?)(\n---)', content, re.DOTALL)
    if not match:
        return content
    return match.group(1) + match.group(2) + '\nimagesOptional: true' + match.group(3) + content[match.end():]


def old_weather_inject(content, weather_data):
    weather_yaml = json.dumps(weather_data)
    return re.sub(r'^weather:.*$', f'weather: {weather_yaml}', content, count=1, flags=re.MULTILINE)


def old_datacutoff_write(content, value):
    parts = content.split('---', 2)
    if len(parts) >= 3:
        parts[1] = parts[1].rstrip() + f'\ndataCutoff: {value}\n'
        return '---'.join(parts)
    return content


def old_draft_flip(content):
    out, _ = re.subn(r'^draft:\s*true\s*$', 'draft: false', content, count=1, flags=re.MULTILINE)
    return out


# --- read parity -----------------------------------------------------------

def test_read_parity_on_every_entry():
    """Each field every consumer reads matches the old extraction exactly."""
    mismatches = []
    for name, _path, content in _entries():
        new = fm.parse(content)
        old = old_validate_parse(content)

        # segment / publishDate / draft (weather.py + publish.sh selection)
        if new.get('segment') != old_weather_seg(content):
            mismatches.append(f'{name}: segment {new.get("segment")!r} != {old_weather_seg(content)!r}')
        if new.get('publishDate') != old_weather_pubdate(content):
            mismatches.append(f'{name}: publishDate {new.get("publishDate")!r} != {old_weather_pubdate(content)!r}')
        if (new.get('draft') is True) != old_weather_is_draft(content):
            mismatches.append(f'{name}: draft decision differs')

        # dataCutoff (publish.sh get) -- canonical empty -> '' like the old code
        new_dc = new.get('dataCutoff')
        new_dc = '' if new_dc is None else str(new_dc)
        if new_dc != old_datacutoff(content):
            mismatches.append(f'{name}: dataCutoff {new_dc!r} != {old_datacutoff(content)!r}')

        # validate_entries "has images" decision
        new_has_images = bool(new.get('images'))
        old_images = old.get('images', [])
        old_has_images = (isinstance(old_images, str) and old_images.startswith('[')) or \
                         (isinstance(old_images, list) and len(old_images) > 0)
        if new_has_images != old_has_images:
            mismatches.append(f'{name}: has-images decision differs')

        # draft / imagesOptional booleans the old validate parser produced
        for key in ('draft', 'imagesOptional'):
            if key in old and isinstance(old[key], bool):
                if new.get(key) != old[key]:
                    mismatches.append(f'{name}: {key} {new.get(key)!r} != {old[key]!r}')

    assert not mismatches, 'Read parity broken:\n' + '\n'.join(mismatches)


# --- write parity ----------------------------------------------------------

def test_set_images_optional_byte_identical():
    # The real caller -- validate_entries.set_images_optional, gated by
    # find_entries_without_images -- only ever runs on entries that do NOT
    # already declare imagesOptional. On that domain the canonical set_field
    # (append-when-absent) is byte-identical to the old appender, which is the
    # behaviour this migration must preserve. The two legitimately diverge only
    # when the field is already present: the old impl blindly appends a second
    # (duplicate) line, while set_field replaces in place. That case cannot
    # occur in production, and set_field's replace-in-place behaviour is covered
    # directly by test_frontmatter.TestSetField. So assert parity only over the
    # production input domain.
    for name, _path, content in _entries():
        if fm.parse(content).get('imagesOptional') is not None:
            continue
        assert fm.set_field(content, 'imagesOptional', 'true') == old_set_images_optional(content), name


def test_weather_inject_byte_identical():
    weather = {
        'fetchedAt': '2026-05-30',
        'current': {'temp': 17, 'conditions': 'Clear sky', 'wind': '3 km/h ESE'},
        'forecast': None,
    }
    for name, _path, content in _entries():
        if re.search(r'^weather:', content, re.MULTILINE):
            new = fm.set_field(content, 'weather', json.dumps(weather))
            assert new == old_weather_inject(content, weather), name


def test_datacutoff_insert_byte_identical():
    for name, _path, content in _entries():
        if not re.search(r'^dataCutoff:', content, re.MULTILINE):
            new = fm.set_field(content, 'dataCutoff', '2026-05-30')
            assert new == old_datacutoff_write(content, '2026-05-30'), name


def test_draft_flip_byte_identical():
    for name, _path, content in _entries():
        if re.search(r'^draft:\s*true\s*$', content, re.MULTILINE):
            assert fm.set_field(content, 'draft', 'false') == old_draft_flip(content), name
