#!/usr/bin/env python3
"""Geocode towns and climbs to get accurate coordinates using OpenStreetMap Nominatim."""

import json
import time
import urllib.parse
import urllib.request

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "CorrezeTravelogue/1.0 (cycling travelogue project)"

# Known towns with search hints for disambiguation
TOWN_SEARCH = {
    "Malemort": "Malemort-sur-Corrèze, Corrèze, France",
    "Brive-la-Gaillarde": "Brive-la-Gaillarde, Corrèze, France",
    "Turenne": "Turenne, Corrèze, France",
    "Collonges-la-Rouge": "Collonges-la-Rouge, Corrèze, France",
    "Beynat": "Beynat, Corrèze, France",
    "Tulle": "Tulle, Corrèze, France",
    "Naves": "Naves, Corrèze, France",
    "Chaumeil": "Chaumeil, Corrèze, France",
    "Treignac": "Treignac, Corrèze, France",
    "Bugeat": "Bugeat, Corrèze, France",
    "Meymac": "Meymac, Corrèze, France",
    "Ussel": "Ussel, Corrèze, France",
}

# Known climbs with search hints
CLIMB_SEARCH = {
    "Puy Boubou": "Puy Boubou, Corrèze, France",
    "Côte de Lagleygeolle": "Lagleygeolle, Corrèze, France",
    "Côte de Miel": "Miel, Corrèze, France",
    "Côte des Naves": "Naves, Corrèze, France",
    "Puy de Lachaud": "Lachaud, Corrèze, France",
    "Suc au May": "Suc au May, Corrèze, France",
    "Côte de la Croix de Pey": "Croix de Pey, Corrèze, France",
    "Mont Bessou": "Mont Bessou, Corrèze, France",
    "Côte des Gardes": "Les Gardes, Corrèze, France",
}


def geocode(query):
    """Look up coordinates for a place name using Nominatim."""
    params = {
        "q": query,
        "format": "json",
        "limit": "1",
        "countrycodes": "fr",
    }
    url = f"{NOMINATIM_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data:
                return {
                    "lat": float(data[0]["lat"]),
                    "lng": float(data[0]["lon"]),
                    "display_name": data[0].get("display_name", ""),
                }
    except Exception as e:
        print(f"    Warning: geocode failed for '{query}': {e}")
    return None


def main():
    output_path = "data/town-coords.json"
    coords = {}

    print("Geocoding towns...")
    for name, query in TOWN_SEARCH.items():
        result = geocode(query)
        if result:
            coords[name] = {
                "type": "town",
                "lat": result["lat"],
                "lng": result["lng"],
            }
            print(f"  {name}: {result['lat']:.5f}, {result['lng']:.5f}")
        else:
            print(f"  {name}: NOT FOUND")
        time.sleep(1)  # Nominatim rate limit: 1 req/sec

    print("\nGeocoding climbs...")
    for name, query in CLIMB_SEARCH.items():
        result = geocode(query)
        if result:
            coords[name] = {
                "type": "climb",
                "lat": result["lat"],
                "lng": result["lng"],
            }
            print(f"  {name}: {result['lat']:.5f}, {result['lng']:.5f}")
        else:
            print(f"  {name}: NOT FOUND")
        time.sleep(1)

    with open(output_path, "w") as f:
        json.dump(coords, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(coords)} coordinates to {output_path}")


if __name__ == "__main__":
    main()
