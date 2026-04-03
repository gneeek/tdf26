#!/usr/bin/env python3
"""Query Wikimedia Commons for CC-licensed images near each segment's location."""

import argparse
import json
import os
import time
import urllib.request
import urllib.parse


COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "CorrezeTravelogue/1.0 (cycling travelogue project)"


def geosearch(lat, lng, radius=5000, limit=50):
    """Search Wikimedia Commons for files near a coordinate."""
    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{lat}|{lng}",
        "gsradius": str(radius),
        "gsnamespace": "6",  # File namespace
        "gslimit": str(limit),
        "format": "json",
    }
    url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("query", {}).get("geosearch", [])
    except Exception as e:
        print(f"    Warning: geosearch failed: {e}")
        return []


def get_image_info(titles):
    """Get image URLs, licenses, and descriptions for a list of file titles."""
    if not titles:
        return []

    # API has a limit per request, batch in groups of 20
    results = []
    for i in range(0, len(titles), 20):
        batch = titles[i:i + 20]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "imageinfo|categories",
            "iiprop": "url|extmetadata|size|mime",
            "iiurlwidth": "800",
            "format": "json",
        }
        url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                pages = data.get("query", {}).get("pages", {})
                for page_id, page in pages.items():
                    if page_id == "-1":
                        continue
                    info = page.get("imageinfo", [{}])[0]
                    extmeta = info.get("extmetadata", {})

                    # Filter: only images, skip SVGs and tiny files
                    mime = info.get("mime", "")
                    if not mime.startswith("image/") or mime == "image/svg+xml":
                        continue
                    width = info.get("width", 0)
                    if width < 400:
                        continue

                    license_short = extmeta.get("LicenseShortName", {}).get("value", "Unknown")
                    artist = extmeta.get("Artist", {}).get("value", "Unknown")
                    description = extmeta.get("ImageDescription", {}).get("value", "")

                    # Only include CC or public domain
                    license_lower = license_short.lower()
                    if not any(kw in license_lower for kw in ["cc", "public domain", "pd"]):
                        continue

                    results.append({
                        "title": page.get("title", ""),
                        "url": info.get("thumburl") or info.get("url", ""),
                        "full_url": info.get("url", ""),
                        "description_url": info.get("descriptionurl", ""),
                        "width": width,
                        "height": info.get("height", 0),
                        "license": license_short,
                        "artist": artist,
                        "description": description[:200] if description else "",
                    })
        except Exception as e:
            print(f"    Warning: imageinfo failed: {e}")

        time.sleep(0.5)  # Be nice to the API

    return results


def process_segment(segment, radius=5000):
    """Find CC images near a segment's midpoint."""
    mid_lat = (segment["start_lat"] + segment["end_lat"]) / 2
    mid_lng = (segment["start_lng"] + segment["end_lng"]) / 2

    # Search near midpoint
    geo_results = geosearch(mid_lat, mid_lng, radius=radius)

    if not geo_results:
        return []

    titles = [r["title"] for r in geo_results]
    images = get_image_info(titles)

    # Sort by width (prefer larger images)
    images.sort(key=lambda x: x["width"], reverse=True)

    return images


def main():
    parser = argparse.ArgumentParser(description="Suggest CC images from Wikimedia Commons")
    parser.add_argument("--segments-json", default="data/segments.json", help="Path to segments.json")
    parser.add_argument("--output-dir", default="data/image-suggestions", help="Output directory")
    parser.add_argument("--radius", type=int, default=5000, help="Search radius in meters")
    parser.add_argument("--segment", type=int, help="Process a single segment (1-26)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.segments_json, "r") as f:
        segments = json.load(f)

    if args.segment:
        segments = [s for s in segments if s["segment"] == args.segment]

    for seg in segments:
        seg_num = seg["segment"]
        seg_str = str(seg_num).zfill(2)
        print(f"Segment {seg_num} ({', '.join(seg['towns']) or 'no towns'})...")

        images = process_segment(seg, radius=args.radius)
        print(f"  Found {len(images)} CC images")

        output_path = os.path.join(args.output_dir, f"segment-{seg_str}.json")
        with open(output_path, "w") as f:
            json.dump({
                "segment": seg_num,
                "towns": seg["towns"],
                "climbs": seg["climbs"],
                "image_count": len(images),
                "images": images,
            }, f, indent=2, ensure_ascii=False)

        time.sleep(1)  # Rate limiting between segments

    print(f"\nWrote suggestions to {args.output_dir}/")
    print("Review the suggestions and manually select the best images for each segment.")


if __name__ == "__main__":
    main()
