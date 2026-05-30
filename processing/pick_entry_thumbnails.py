#!/usr/bin/env python3
"""Pick the most landscape-shaped image per entry and write a thumbnail manifest.

For each entry in content/entries/, reads the images frontmatter and resolves
each image's width/height. Local images are read with PIL; remote Wikimedia
Commons images are batched through the MediaWiki imageinfo API (up to 50
titles per call) and cached locally.

The chosen thumbnail is the image whose aspect ratio is closest to the target
landscape ratio (3:2). Portrait images are never picked. If no landscape
candidate exists, the manifest falls back to images[0] so the rendering does
not regress. The Vue EntryCard reads this manifest at render time and falls
back to entry.images[0] when no entry exists for a segment.

Run as a pre-publish step when new images are added. Output is committed so
the build does not depend on network availability.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import frontmatter
import requests
from PIL import Image

WIKIMEDIA_PREFIX = "https://upload.wikimedia.org/"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "tdf26-thumbnail-picker/1.0 "
    "(https://github.com/gneeek/tdf26; gneeek@proton.me)"
)
TARGET_RATIO = 1.5  # 3:2 wins ties; portraits are rejected outright
OBJECT_POSITION_BONUS = 0.05
API_BATCH_SIZE = 50
API_SLEEP_SECONDS = 1.0


def wikimedia_filename(url):
    """Extract the File:Name.ext title from any upload.wikimedia.org URL."""
    if not url.startswith(WIKIMEDIA_PREFIX):
        return None
    # Thumbnail URL: .../commons/thumb/X/XX/Filename.jpg/WIDTHpx-Filename.jpg
    # Original URL:  .../commons/X/XX/Filename.jpg
    parts = url.split("/")
    if "thumb" in parts:
        idx = parts.index("thumb")
        # Filename is two segments after the hex hash dirs
        if idx + 3 < len(parts):
            return unquote(parts[idx + 3])
    else:
        return unquote(parts[-1])
    return None


def get_local_dimensions(public_dir, src):
    rel = src.lstrip("/")
    path = Path(public_dir) / rel
    if not path.exists():
        return None
    try:
        with Image.open(path) as img:
            return img.size
    except Exception as e:
        print(f"  local read failed for {path}: {e}", file=sys.stderr)
        return None


def fetch_wikimedia_dimensions(filenames, cache):
    """Batch-query the Commons imageinfo API. Updates cache in place."""
    pending = [f for f in filenames if f and f not in cache]
    if not pending:
        return
    for i in range(0, len(pending), API_BATCH_SIZE):
        batch = pending[i : i + API_BATCH_SIZE]
        titles = "|".join(f"File:{name}" for name in batch)
        try:
            resp = requests.get(
                COMMONS_API,
                params={
                    "action": "query",
                    "format": "json",
                    "prop": "imageinfo",
                    "iiprop": "size",
                    "titles": titles,
                },
                headers={"User-Agent": USER_AGENT},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  API batch failed: {e}", file=sys.stderr)
            for name in batch:
                cache[name] = [None, None]
            continue
        # API returns a normalized title map and pages; build a name->info lookup
        norms = {n["from"]: n["to"] for n in data.get("query", {}).get("normalized", [])}
        pages = data.get("query", {}).get("pages", {}) or {}
        results = {}
        for page in pages.values():
            title = page.get("title", "")
            ii = page.get("imageinfo") or []
            if title.startswith("File:") and ii:
                results[title[len("File:") :]] = (ii[0].get("width"), ii[0].get("height"))
        for name in batch:
            normalized = norms.get(f"File:{name}", f"File:{name}")
            key = normalized[len("File:") :] if normalized.startswith("File:") else normalized
            if key in results:
                w, h = results[key]
                cache[name] = [w, h]
            else:
                cache[name] = [None, None]
        if i + API_BATCH_SIZE < len(pending):
            time.sleep(API_SLEEP_SECONDS)


def cost_for(ratio, has_object_position):
    cost = abs(ratio - TARGET_RATIO)
    if has_object_position:
        cost -= OBJECT_POSITION_BONUS
    return cost


def resolve_dimensions(img, public_dir, remote_cache):
    src = img.get("src", "")
    if src.startswith("/"):
        return get_local_dimensions(public_dir, src)
    if src.startswith(WIKIMEDIA_PREFIX):
        name = wikimedia_filename(src)
        if name and name in remote_cache:
            entry = remote_cache[name]
            if entry and entry[0] and entry[1]:
                return tuple(entry)
    return None


def pick_thumbnail(images, public_dir, remote_cache):
    landscape_candidates = []
    for idx, img in enumerate(images):
        dims = resolve_dimensions(img, public_dir, remote_cache)
        if dims is None:
            continue
        w, h = dims
        if not w or not h:
            continue
        ratio = w / h
        if ratio < 1.0:
            continue  # never pick a portrait
        has_op = bool(img.get("objectPosition"))
        landscape_candidates.append((cost_for(ratio, has_op), idx, img, ratio))
    if not landscape_candidates:
        if images:
            return images[0], "fallback-no-landscape"
        return None, "no-images"
    landscape_candidates.sort(key=lambda t: (t[0], t[1]))
    _, idx, img, ratio = landscape_candidates[0]
    return img, f"landscape ratio={ratio:.2f} idx={idx}"


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--entries-dir", default="content/entries")
    p.add_argument("--public-dir", default="public")
    p.add_argument("--output", default="data/entry-thumbnails.json")
    p.add_argument("--cache", default="data/.thumbnail-dimension-cache.json")
    p.add_argument("--segment", type=int, help="Process only this segment number")
    p.add_argument("--min-segment", type=int, help="Only process segments >= this")
    return p.parse_args()


def main():
    args = parse_args()
    entries_dir = Path(args.entries_dir)
    public_dir = Path(args.public_dir)
    output_path = Path(args.output)
    cache_path = Path(args.cache)

    remote_cache = {}
    if cache_path.exists():
        remote_cache = json.loads(cache_path.read_text())

    # Pass 1: collect entries and the full set of Wikimedia filenames to resolve.
    entries_to_process = []
    needed_filenames = set()
    for filename in sorted(os.listdir(entries_dir)):
        if not filename.endswith(".md"):
            continue
        filepath = entries_dir / filename
        fm = frontmatter.parse_file(filepath)
        seg = fm.get("segment")
        if seg is None or seg <= 0:
            continue
        if args.segment is not None and seg != args.segment:
            continue
        if args.min_segment is not None and seg < args.min_segment:
            continue
        images = fm.get("images") or []
        entries_to_process.append((seg, images))
        for img in images:
            name = wikimedia_filename(img.get("src", ""))
            if name:
                needed_filenames.add(name)

    fetch_wikimedia_dimensions(sorted(needed_filenames), remote_cache)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(remote_cache, indent=2, sort_keys=True) + "\n")

    existing = {}
    if output_path.exists():
        existing = json.loads(output_path.read_text())

    for seg, images in entries_to_process:
        if existing.get(str(seg), {}).get("manual"):
            print(f"seg {seg:>2}: manual override preserved")
            continue
        if not images:
            print(f"seg {seg:>2}: no images, skipping")
            existing.pop(str(seg), None)
            continue
        chosen, reason = pick_thumbnail(images, public_dir, remote_cache)
        if chosen is None:
            existing.pop(str(seg), None)
            print(f"seg {seg:>2}: {reason}")
            continue
        previous = existing.get(str(seg), {}).get("src")
        existing[str(seg)] = {"src": chosen["src"], "reason": reason}
        marker = "" if previous == chosen["src"] else "  *CHANGED*"
        match_first = " (=images[0])" if chosen["src"] == images[0].get("src", "") else ""
        print(f"seg {seg:>2}: {reason}{match_first}{marker}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n")
    print(f"\nWrote {output_path} ({len(existing)} entries)")


if __name__ == "__main__":
    main()
