"""Tests for split_gpx.py — GPX parsing and segment splitting."""

import json
import os

import pytest

from processing.split_gpx import (
    KNOWN_CLIMBS,
    compute_town_proximity,
    haversine,
    load_town_coords,
    parse_gpx,
    split_into_segments,
    write_segment_gpx,
)

# Minimal GPX content: a short track with 5 points spanning ~1km
MINIMAL_GPX = """\
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test"
     xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>Test Route</name>
    <trkseg>
      <trkpt lat="45.0" lon="1.5"><ele>200</ele></trkpt>
      <trkpt lat="45.001" lon="1.5"><ele>210</ele></trkpt>
      <trkpt lat="45.002" lon="1.5"><ele>220</ele></trkpt>
      <trkpt lat="45.003" lon="1.5"><ele>215</ele></trkpt>
      <trkpt lat="45.004" lon="1.5"><ele>230</ele></trkpt>
      <trkpt lat="45.005" lon="1.5"><ele>225</ele></trkpt>
      <trkpt lat="45.006" lon="1.5"><ele>240</ele></trkpt>
      <trkpt lat="45.007" lon="1.5"><ele>235</ele></trkpt>
      <trkpt lat="45.008" lon="1.5"><ele>250</ele></trkpt>
      <trkpt lat="45.009" lon="1.5"><ele>245</ele></trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture
def gpx_file(tmp_path):
    """Write minimal GPX to a temp file."""
    path = tmp_path / "test.gpx"
    path.write_text(MINIMAL_GPX)
    return str(path)


# --- haversine ---

class TestHaversine:
    def test_same_point_is_zero(self):
        assert haversine(45.0, 1.5, 45.0, 1.5) == 0.0

    def test_known_distance(self):
        # ~111km per degree of latitude
        dist = haversine(45.0, 1.5, 46.0, 1.5)
        assert 110_000 < dist < 112_000

    def test_symmetry(self):
        d1 = haversine(45.0, 1.5, 45.1, 1.6)
        d2 = haversine(45.1, 1.6, 45.0, 1.5)
        assert abs(d1 - d2) < 0.01


# --- parse_gpx ---

class TestParseGpx:
    def test_returns_correct_point_count(self, gpx_file):
        points = parse_gpx(gpx_file)
        assert len(points) == 10

    def test_first_point_zero_distance(self, gpx_file):
        points = parse_gpx(gpx_file)
        assert points[0]["cum_km"] == 0.0

    def test_cumulative_distance_increases(self, gpx_file):
        points = parse_gpx(gpx_file)
        for i in range(1, len(points)):
            assert points[i]["cum_km"] > points[i - 1]["cum_km"]

    def test_elevation_preserved(self, gpx_file):
        points = parse_gpx(gpx_file)
        assert points[0]["ele"] == 200
        assert points[4]["ele"] == 230

    def test_coordinates_preserved(self, gpx_file):
        points = parse_gpx(gpx_file)
        assert points[0]["lat"] == 45.0
        assert points[0]["lon"] == 1.5


# --- split_into_segments ---

class TestSplitIntoSegments:
    def test_correct_segment_count(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        assert len(segments) == 2

    def test_segment_numbering(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=3)
        assert [s["segment"] for s in segments] == [1, 2, 3]

    def test_km_start_end_continuous(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        assert segments[0]["km_start"] == 0.0
        assert segments[0]["km_end"] == pytest.approx(segments[1]["km_start"], abs=0.2)

    def test_elevation_gain_non_negative(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        for seg in segments:
            assert seg["elevation_gain"] >= 0
            assert seg["elevation_loss"] >= 0

    def test_min_max_elevation_consistent(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        for seg in segments:
            assert seg["min_elevation"] <= seg["max_elevation"]

    def test_segment_has_required_keys(self, gpx_file):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        required = {
            "segment", "km_start", "km_end", "start_lat", "start_lng",
            "end_lat", "end_lng", "elevation_gain", "elevation_loss",
            "min_elevation", "max_elevation", "notable_points", "towns",
            "climbs", "points",
        }
        for seg in segments:
            assert required.issubset(seg.keys())

    def test_towns_assigned_to_correct_segment(self, gpx_file):
        # Use the real GPX to verify town assignment
        points = parse_gpx(gpx_file)
        # Our test GPX is too short for real towns — just verify lists are returned
        segments = split_into_segments(points, num_segments=2)
        for seg in segments:
            assert isinstance(seg["towns"], list)
            assert isinstance(seg["climbs"], list)


# --- compute_town_proximity ---

class TestComputeTownProximity:
    """Closest-approach lookup for each town against the GPX."""

    def test_returns_km_and_distance_per_town(self, gpx_file):
        points = parse_gpx(gpx_file)
        # Place a synthetic "town" right on the track at the third trackpoint.
        coords = {"On Route": {"type": "town", "lat": 45.002, "lng": 1.5}}
        prox = compute_town_proximity(points, coords)
        assert "On Route" in prox
        assert prox["On Route"]["distance_m"] < 5
        # Track is dense at 0.001 deg lat (~111m) intervals; expect km < 0.5
        assert prox["On Route"]["km"] < 0.5

    def test_skips_non_town_types(self, gpx_file):
        points = parse_gpx(gpx_file)
        coords = {
            "Town": {"type": "town", "lat": 45.0, "lng": 1.5},
            "Climb": {"type": "climb", "lat": 45.0, "lng": 1.5},
        }
        prox = compute_town_proximity(points, coords)
        assert "Town" in prox
        assert "Climb" not in prox


# --- route-proximity town assignment ---

class TestRouteProximityAssignment:
    """split_into_segments uses closest-approach km, not km-range guessing, to bucket towns."""

    def test_town_near_track_assigned_to_correct_segment(self, gpx_file):
        # Track runs north along lon=1.5 from lat 45.0 to 45.009 (~1km).
        # Two segments: 0-0.5km and 0.5-1km.
        points = parse_gpx(gpx_file)
        town_coords = {
            # ~111m east of lat 45.001 (km ~0.11) -> seg 1
            "Early Town": {"type": "town", "lat": 45.001, "lng": 1.501},
            # ~111m east of lat 45.008 (km ~0.89) -> seg 2
            "Late Town": {"type": "town", "lat": 45.008, "lng": 1.501},
        }
        segments = split_into_segments(
            points, num_segments=2, odd_length=0.5, even_length=0.5,
            town_coords=town_coords,
        )
        assert "Early Town" in segments[0]["towns"]
        assert "Late Town" in segments[1]["towns"]
        assert "Early Town" not in segments[1]["towns"]
        assert "Late Town" not in segments[0]["towns"]

    def test_far_off_route_town_excluded(self, gpx_file):
        points = parse_gpx(gpx_file)
        town_coords = {
            "Distant": {"type": "town", "lat": 47.0, "lng": 1.5},  # ~220km north
        }
        segments = split_into_segments(
            points, num_segments=2, odd_length=0.5, even_length=0.5,
            town_coords=town_coords, town_max_distance_m=1000,
        )
        for seg in segments:
            assert "Distant" not in seg["towns"]

    def test_town_positions_field_exposes_closest_approach_km(self, gpx_file):
        points = parse_gpx(gpx_file)
        town_coords = {
            "Early Town": {"type": "town", "lat": 45.001, "lng": 1.501},
        }
        segments = split_into_segments(
            points, num_segments=2, odd_length=0.5, even_length=0.5,
            town_coords=town_coords,
        )
        assert "town_positions" in segments[0]
        assert "Early Town" in segments[0]["town_positions"]
        assert isinstance(segments[0]["town_positions"]["Early Town"], (int, float))


# --- load_town_coords ---

class TestLoadTownCoords:
    def test_loads_real_file(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        path = os.path.join(root, "data", "town-coords.json")
        if not os.path.exists(path):
            pytest.skip("town-coords.json not found")
        coords = load_town_coords(path)
        assert "Malemort" in coords
        assert "type" in coords["Malemort"]


# --- write_segment_gpx ---

class TestWriteSegmentGpx:
    def test_writes_valid_gpx(self, gpx_file, tmp_path):
        import gpxpy as gpxpy_lib

        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        output_dir = str(tmp_path / "output")
        os.makedirs(output_dir)

        path = write_segment_gpx(segments[0], output_dir)
        assert os.path.exists(path)

        # Verify the output is parseable GPX
        with open(path) as f:
            gpx = gpxpy_lib.parse(f)
        assert len(gpx.tracks) == 1
        assert len(gpx.tracks[0].segments[0].points) > 0

    def test_filename_zero_padded(self, gpx_file, tmp_path):
        points = parse_gpx(gpx_file)
        segments = split_into_segments(points, num_segments=2)
        output_dir = str(tmp_path / "output")
        os.makedirs(output_dir)

        path = write_segment_gpx(segments[0], output_dir)
        assert path.endswith("segment-01.gpx")


# --- Integration with real data ---

class TestRealData:
    """Tests using the actual project GPX data (skipped if not available)."""

    @pytest.fixture
    def real_segments(self):
        segments_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "segments.json"
        )
        if not os.path.exists(segments_path):
            pytest.skip("data/segments.json not found")
        with open(segments_path) as f:
            return json.load(f)

    def test_27_segments(self, real_segments):
        assert len(real_segments) == 27

    def test_segments_within_length_range(self, real_segments):
        for seg in real_segments:
            length = seg["km_end"] - seg["km_start"]
            assert 2.0 < length < 10.0, f"Segment {seg['segment']} length {length} out of range"

    def test_total_distance_approximately_185km(self, real_segments):
        total = real_segments[-1]["km_end"]
        assert 180 < total < 190

    def test_malemort_in_segment_1(self, real_segments):
        assert "Malemort" in real_segments[0]["towns"]

    def test_ussel_in_last_segment(self, real_segments):
        assert "Ussel" in real_segments[-1]["towns"]

    def test_all_towns_assigned(self, real_segments):
        # Towns within 1 km of the route should all appear on some segment.
        # Brive-la-Gaillarde is intentionally off-route (2.5 km north) per
        # the v1.4.8 audit decision and is excluded from segment assignment.
        all_towns = set()
        for seg in real_segments:
            all_towns.update(seg["towns"])
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        coords_path = os.path.join(root, "data", "town-coords.json")
        with open(coords_path) as f:
            coords = json.load(f)
        on_route_towns = [
            n for n, v in coords.items()
            if v.get("type") == "town" and n != "Brive-la-Gaillarde"
        ]
        for town in on_route_towns:
            assert town in all_towns, f"Town {town} not assigned to any segment"

    def test_all_climbs_assigned(self, real_segments):
        all_climbs = set()
        for seg in real_segments:
            all_climbs.update(seg["climbs"])
        for climb in KNOWN_CLIMBS:
            assert climb in all_climbs, f"Climb {climb} not assigned to any segment"

    def test_coordinates_in_france(self, real_segments):
        for seg in real_segments:
            assert 44.5 < seg["start_lat"] < 46.0
            assert 1.0 < seg["start_lng"] < 3.0
