"""Canonical frontmatter parser for content/entries/*.md (issue #326).

Single source of read/write logic for every Python consumer of entry
frontmatter: validate_entries.py, weather.py, pick_entry_thumbnails.py, and
the inline reads in scripts/publish.sh. Replaces the per-module hand-rolled
regex parsers those files used to carry, each of which drifted independently
(the class of fragility behind the seg-9 publish-day crash).

Field definitions live in schemas/frontmatter.schema.json -- the shared schema
the TypeScript canonical parser (server/utils/frontmatter.ts) reads too. This
module loads that schema for its field registry so neither language re-derives
frontmatter field shapes.

YAML quirk handled here once: PyYAML (like js-yaml's default schema) parses a
bare ISO date such as `publishDate: 2026-04-05` into a datetime.date. The
hand-rolled regex parsers kept those as strings, and downstream code compares
them as strings (e.g. `pub_date <= today`). So this loader strips the YAML 1.1
timestamp resolver, keeping bare dates as strings -- matching the TypeScript
side, which loads with js-yaml JSON_SCHEMA for the same reason.
"""

import argparse
import json
import os
import re

import yaml

# The frontmatter fence: group 1 the opening `---\n`, group 2 the YAML body
# (non-greedy, so it stops at the first closing fence), group 3 the `\n---`.
# This is the exact pattern validate_entries.set_images_optional used, so the
# surgical writer below stays byte-identical to the code it replaces.
_FENCE_RE = re.compile(r'^(---\n)(.*?)(\n---)', re.DOTALL)
_HEAD_RE = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'schemas', 'frontmatter.schema.json'
)


class _Loader(yaml.SafeLoader):
    """SafeLoader that keeps bare ISO dates as strings (see module docstring)."""


_Loader.yaml_implicit_resolvers = {
    ch: [(tag, regexp) for (tag, regexp) in mappers
         if tag != 'tag:yaml.org,2002:timestamp']
    for ch, mappers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


SCHEMA = _load_schema()
FIELDS = tuple(SCHEMA['properties'].keys())
REQUIRED = tuple(SCHEMA['required'])


def split_frontmatter(content):
    """Split a markdown string into (raw_frontmatter, body).

    Returns (None, content) when there is no leading `---` frontmatter block.
    The raw frontmatter is the unparsed text between the fences -- the shared
    primitive the entry-content editor round-trip relies on.
    """
    m = _FENCE_RE.match(content)
    if not m:
        return None, content
    return m.group(2), content[m.end():]


def parse(content):
    """Parse the YAML frontmatter of a markdown string into a dict.

    Returns {} when there is no frontmatter block, or it is not a mapping.
    Bare ISO dates stay strings (see module docstring).
    """
    m = _HEAD_RE.match(content)
    if not m:
        return {}
    data = yaml.load(m.group(1), Loader=_Loader)
    return data if isinstance(data, dict) else {}


def parse_file(path):
    """Parse frontmatter from a markdown file path."""
    with open(path) as f:
        return parse(f.read())


def set_field(content, key, value):
    """Return content with frontmatter field `key` set to the literal `value`.

    Surgical and byte-preserving: if a `key:` line exists in the frontmatter
    block it is replaced in place; otherwise the field is appended as the last
    frontmatter line, before the closing `---`. `value` is inserted verbatim
    -- already formatted by the caller (e.g. `true`, an ISO date, or a compact
    JSON string) -- so the rest of the file is untouched. This unifies the
    three hand-rolled writers it replaces: validate_entries' imagesOptional
    insert, weather's weather-line rewrite, and publish.sh's dataCutoff insert
    and draft flip.

    Content with no frontmatter block is returned unchanged.
    """
    m = _FENCE_RE.match(content)
    if not m:
        return content
    head, fm_body, tail = m.group(1), m.group(2), m.group(3)
    rest = content[m.end():]
    line_re = re.compile(r'^' + re.escape(key) + r':.*$', re.MULTILINE)
    new_line = f'{key}: {value}'
    if line_re.search(fm_body):
        # Replace via a function so the literal value is never interpreted as a
        # regex backreference (e.g. a `\1` inside a URL or JSON string).
        fm_body = line_re.sub(lambda _m: new_line, fm_body, count=1)
    else:
        fm_body = f'{fm_body}\n{new_line}'
    return f'{head}{fm_body}{tail}{rest}'


def validate(frontmatter):
    """Validate a parsed frontmatter dict against the shared schema.

    Returns a list of human-readable error strings (empty when valid). Imports
    jsonschema lazily so the parse/write path never needs it -- only callers
    that opt into validation (the test suite) pull the dependency in.
    """
    import jsonschema

    validator = jsonschema.Draft7Validator(SCHEMA)
    return [
        f'{"/".join(str(p) for p in err.absolute_path) or "<root>"}: {err.message}'
        for err in sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.absolute_path))
    ]


def current_segment(entries_dir, today=None):
    """Return the highest segment number whose entry is published on/before today.

    "Published" means draft is false and publishDate <= today (string compare on
    ISO dates). Returns 0 when nothing qualifies. Replaces publish.sh's inline
    segment auto-detect.
    """
    if today is None:
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
    best = None
    for fname in sorted(os.listdir(entries_dir)):
        if not fname.endswith('.md'):
            continue
        fm = parse_file(os.path.join(entries_dir, fname))
        seg = fm.get('segment')
        pub = fm.get('publishDate')
        if seg is not None and pub and fm.get('draft') is False and pub <= today:
            if best is None or seg > best:
                best = seg
    return best if best is not None else 0


def find_entry_path(entries_dir, segment):
    """Return the path of the entry whose frontmatter segment equals `segment`.

    Returns None when no entry matches. Replaces publish.sh's inline entry-file
    resolve.
    """
    for fname in sorted(os.listdir(entries_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(entries_dir, fname)
        if parse_file(path).get('segment') == segment:
            return path
    return None


def _format_scalar(value):
    """Render a frontmatter scalar for shell consumption (the `get` CLI).

    None -> empty string; booleans -> lowercase `true`/`false` (matching the
    publish.sh comparisons this replaces); everything else -> str().
    """
    if value is None:
        return ''
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return str(value)


def _main(argv=None):
    parser = argparse.ArgumentParser(
        description='Frontmatter operations for content/entries/*.md (issue #326).'
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_get = sub.add_parser('get', help='print a frontmatter field value')
    p_get.add_argument('file')
    p_get.add_argument('field')

    p_set = sub.add_parser('set', help='set a frontmatter field in place')
    p_set.add_argument('file')
    p_set.add_argument('field')
    p_set.add_argument('value')

    p_cur = sub.add_parser('current-segment', help='highest published segment number')
    p_cur.add_argument('entries_dir')
    p_cur.add_argument('--today', default=None)

    p_find = sub.add_parser('find-entry', help='path of the entry for a segment')
    p_find.add_argument('entries_dir')
    p_find.add_argument('segment', type=int)

    args = parser.parse_args(argv)

    if args.cmd == 'get':
        print(_format_scalar(parse_file(args.file).get(args.field)))
    elif args.cmd == 'set':
        with open(args.file) as f:
            content = f.read()
        with open(args.file, 'w') as f:
            f.write(set_field(content, args.field, args.value))
    elif args.cmd == 'current-segment':
        print(current_segment(args.entries_dir, args.today))
    elif args.cmd == 'find-entry':
        print(find_entry_path(args.entries_dir, args.segment) or '')


if __name__ == '__main__':
    _main()
