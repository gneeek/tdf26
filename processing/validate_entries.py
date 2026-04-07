"""Validate entry frontmatter before publishing.

Checks that entries being published today have at least one image,
or have imagesOptional: true set in frontmatter.
"""

import argparse
import os
import re
import sys
from datetime import date


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
    parser = argparse.ArgumentParser(description='Validate entry images before publishing')
    parser.add_argument('--entries-dir', required=True, help='Path to content/entries directory')
    parser.add_argument('--non-interactive', action='store_true',
                        help='Fail instead of prompting (for CI)')
    args = parser.parse_args()

    entries = find_entries_to_validate(args.entries_dir)

    if not entries:
        print('All entries have images or are marked imagesOptional.')
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
