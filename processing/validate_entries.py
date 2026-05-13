"""Validate entry frontmatter before publishing.

Checks that entries being published today have at least one image,
or have imagesOptional: true set in frontmatter. Also checks all
non-draft entries for unbalanced MDC blocks (`::name{...}` opens
without matching `::` closes) which render as broken pages.
"""

import argparse
import os
import re
import sys
from datetime import date

MDC_OPEN_RE = re.compile(r'^(::+)([A-Za-z][A-Za-z0-9_-]*)(\s*\{.*\})?\s*$')
MDC_CLOSE_RE = re.compile(r'^(::+)\s*$')
CODE_FENCE_RE = re.compile(r'^(```+|~~~+)')
FRONTMATTER_FENCE = '---'


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file. Returns a dict."""
    with open(filepath) as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    for line in match.group(1).split('\n'):
        # Simple key: value parsing
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == 'true':
                fm[key] = True
            elif val == 'false':
                fm[key] = False
            elif val == 'null':
                fm[key] = None
            elif val == '[]':
                fm[key] = []
            elif val.startswith('[') and val.endswith(']') and val != '[]':
                fm[key] = val  # non-empty array, keep as string marker
            else:
                fm[key] = val
    return fm


def find_entries_to_validate(entries_dir, today=None):
    """Find entries published today that need image validation.

    Returns a list of dicts with 'filename', 'filepath', 'needs_prompt'.
    Only returns entries that have no images and no imagesOptional: true.
    """
    if today is None:
        today = date.today()

    today_str = today.isoformat()
    results = []

    for filename in sorted(os.listdir(entries_dir)):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(entries_dir, filename)
        fm = parse_frontmatter(filepath)

        # Skip drafts
        if fm.get('draft') is True:
            continue

        # Only check entries published today
        publish_date = fm.get('publishDate', '')
        if str(publish_date) != today_str:
            continue

        # Skip if imagesOptional is set
        if fm.get('imagesOptional') is True:
            continue

        # Skip if images is a non-empty array
        images = fm.get('images', [])
        if isinstance(images, str) and images.startswith('['):
            # Non-empty array string like [{src: ...}]
            continue
        if isinstance(images, list) and len(images) > 0:
            continue

        results.append({
            'filename': filename,
            'filepath': filepath,
            'needs_prompt': True,
        })

    return results


def mdc_balance_check(filepath):
    """Scan an entry body for unbalanced MDC block markers.

    Returns a list of error strings (empty when balanced).
    """
    with open(filepath) as f:
        lines = f.read().splitlines()

    in_frontmatter = False
    frontmatter_done = False
    code_fence = None
    stack = []
    errors = []

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip()

        if not frontmatter_done:
            if lineno == 1 and line == FRONTMATTER_FENCE:
                in_frontmatter = True
                continue
            if in_frontmatter:
                if line == FRONTMATTER_FENCE:
                    in_frontmatter = False
                    frontmatter_done = True
                continue
            frontmatter_done = True

        fence_match = CODE_FENCE_RE.match(line)
        if fence_match:
            fence_char = fence_match.group(1)[0]
            if code_fence is None:
                code_fence = fence_char
            elif code_fence == fence_char:
                code_fence = None
            continue
        if code_fence is not None:
            continue

        open_match = MDC_OPEN_RE.match(line)
        close_match = MDC_CLOSE_RE.match(line)
        if open_match:
            stack.append((open_match.group(2), lineno))
        elif close_match:
            if not stack:
                errors.append(
                    f'{filepath}:{lineno}: unmatched MDC close `::` with no open block'
                )
            else:
                stack.pop()

    for name, opened_at in stack:
        errors.append(
            f'{filepath}:{opened_at}: unclosed MDC block `::{name}` (no matching `::`)'
        )

    return errors


def find_entries_for_mdc_check(entries_dir):
    """Return absolute paths of every non-draft markdown entry."""
    paths = []
    for filename in sorted(os.listdir(entries_dir)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(entries_dir, filename)
        fm = parse_frontmatter(filepath)
        if fm.get('draft') is True:
            continue
        paths.append(filepath)
    return paths


def set_images_optional(filepath):
    """Add imagesOptional: true to an entry's frontmatter."""
    with open(filepath) as f:
        content = f.read()

    # Insert imagesOptional: true before the closing ---
    # Find the end of frontmatter
    match = re.match(r'^(---\n)(.*?)(\n---)', content, re.DOTALL)
    if not match:
        return

    before = match.group(1)
    fm_content = match.group(2)
    after = match.group(3)
    rest = content[match.end():]

    new_content = before + fm_content + '\nimagesOptional: true' + after + rest

    with open(filepath, 'w') as f:
        f.write(new_content)


def main():
    parser = argparse.ArgumentParser(description='Validate entries before publishing')
    parser.add_argument('--entries-dir', required=True, help='Path to content/entries directory')
    parser.add_argument('--non-interactive', action='store_true',
                        help='Fail instead of prompting (for CI)')
    args = parser.parse_args()

    mdc_errors = []
    for filepath in find_entries_for_mdc_check(args.entries_dir):
        mdc_errors.extend(mdc_balance_check(filepath))

    if mdc_errors:
        print('Unbalanced MDC blocks detected:')
        for err in mdc_errors:
            print(f'  {err}')
        sys.exit(1)

    entries = find_entries_to_validate(args.entries_dir)

    if not entries:
        print('All entries have images or are marked imagesOptional; MDC blocks balanced.')
        return

    for entry in entries:
        print(f'\nWARNING: {entry["filename"]} has no images.')

        if args.non_interactive:
            print('Failing (--non-interactive mode).')
            sys.exit(1)

        response = input('Publish without images? [y/N] ').strip().lower()
        if response == 'y':
            set_images_optional(entry['filepath'])
            print(f'  Set imagesOptional: true in {entry["filename"]}')
        else:
            print('Exiting. Add images and try again.')
            sys.exit(1)


if __name__ == '__main__':
    main()
