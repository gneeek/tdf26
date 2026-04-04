"""Tests for elevation_profile.py — elevation profiles, gradients, and power estimates."""

import json
import os
import tempfile

import pytest

from processing.elevation_profile import (
    calculate_power,
    format_time,
    haversine,
    process_segment,
)


# Minimal GPX for a segment with some elevation change
SEGMENT_GPX = """\
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test"
     xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>Test Segment</name>
    <trkseg>
      <trkpt lat="45.0" lon="1.5"><ele>200</ele></trkpt>
      <trkpt lat="45.001" lon="1.5"><ele>210</ele></trkpt>
      <trkpt lat="45.002" lon="1.5"><ele>220</ele></trkpt>
      <trkpt lat="45.003" lon="1.5"><ele>230</ele></trkpt>
      <trkpt lat="45.004" lon="1.5"><ele>240</ele></trkpt>
      <trkpt lat="45.005" lon="1.5"><ele>250</ele></trkpt>
      <trkpt lat="45.006" lon="1.5"><ele>245</ele></trkpt>
      <trkpt lat="45.007" lon="1.5"><ele>260</ele></trkpt>
      <trkpt lat="45.008" lon="1.5"><ele>270</ele></trkpt>
      <trkpt lat="45.009" lon="1.5"><ele>280</ele></trkpt>
    </trkseg>
  </trk>
</gpx>
"""


@pytest.fixture
def segment_gpx_file(tmp_path):
    path = tmp_path / "segment-01.gpx"
    path.write_text(SEGMENT_GPX)
    return str(path)


# --- calculate_power ---

class TestCalculatePower:
    def test_flat_road_positive_power(self):
        power = calculate_power(0.0, 35)
        assert power > 0

    def test_uphill_more_power_than_flat(self):
        flat = calculate_power(0.0, 35)
        uphill = calculate_power(5.0, 35)
        assert uphill > flat

    def test_steeper_requires_more_power(self):
        mild = calculate_power(3.0, 35)
        steep = calculate_power(8.0, 35)
        assert steep > mild

    def test_faster_requires_more_power(self):
        slow = calculate_power(0.0, 30)
        fast = calculate_power(0.0, 50)
        assert fast > slow

    def test_downhill_can_be_zero(self):
        # Steep enough downhill at low speed should return 0 (freewheeling)
        power = calculate_power(-10.0, 10)
        assert power == 0

    def test_returns_non_negative(self):
        for gradient in [-15, -10, -5, 0, 5, 10]:
            for speed in [20, 30, 40, 50]:
                assert calculate_power(gradient, speed) >= 0

    def test_reasonable_flat_power_at_35kmh(self):
        # A 78kg rider+bike at 35km/h on flat should need ~150-300W
        power = calculate_power(0.0, 35)
        assert 100 < power < 400


# --- format_time ---

class TestFormatTime:
    def test_whole_minutes(self):
        assert format_time(10.0) == "10:00"

    def test_fractional_minutes(self):
        assert format_time(10.5) == "10:30"

    def test_small_value(self):
        assert format_time(1.25) == "1:15"


# --- haversine ---

class TestHaversine:
    def test_same_point(self):
        assert haversine(45.0, 1.5, 45.0, 1.5) == 0.0

    def test_known_distance(self):
        dist = haversine(45.0, 1.5, 46.0, 1.5)
        assert 110_000 < dist < 112_000


# --- process_segment ---

class TestProcessSegment:
    def test_returns_expected_keys(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        expected_keys = {
            "segment", "distance", "elevation", "gradient",
            "power_30kmh", "power_35kmh", "power_40kmh", "power_50kmh",
            "summary",
        }
        assert expected_keys == set(result.keys())

    def test_segment_number_preserved(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 7)
        assert result["segment"] == 7

    def test_arrays_same_length(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        n = len(result["distance"])
        assert len(result["elevation"]) == n
        assert len(result["gradient"]) == n
        assert len(result["power_30kmh"]) == n
        assert len(result["power_35kmh"]) == n
        assert len(result["power_40kmh"]) == n
        assert len(result["power_50kmh"]) == n

    def test_distance_starts_at_zero(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        assert result["distance"][0] == 0.0

    def test_distance_increases(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        for i in range(1, len(result["distance"])):
            assert result["distance"][i] >= result["distance"][i - 1]

    def test_summary_has_required_fields(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        summary = result["summary"]
        required = {
            "avg_gradient", "max_gradient", "elevation_gain", "elevation_loss",
            "avg_power_30kmh", "avg_power_35kmh", "avg_power_40kmh", "avg_power_50kmh",
            "estimated_time_30kmh", "estimated_time_35kmh",
            "estimated_time_40kmh", "estimated_time_50kmh",
        }
        assert required.issubset(summary.keys())

    def test_elevation_gain_positive_for_uphill(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        # Our test GPX goes mostly uphill
        assert result["summary"]["elevation_gain"] > 0

    def test_power_increases_with_speed(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        s = result["summary"]
        assert s["avg_power_30kmh"] < s["avg_power_35kmh"]
        assert s["avg_power_35kmh"] < s["avg_power_40kmh"]
        assert s["avg_power_40kmh"] < s["avg_power_50kmh"]

    def test_estimated_time_format(self, segment_gpx_file):
        result = process_segment(segment_gpx_file, 1)
        import re
        for key in ["estimated_time_30kmh", "estimated_time_35kmh",
                     "estimated_time_40kmh", "estimated_time_50kmh"]:
            assert re.match(r"^\d+:\d{2}$", result["summary"][key])


# --- Integration with real data ---

class TestRealElevationData:
    """Tests using actual generated elevation data (skipped if not available)."""

    @pytest.fixture
    def real_elevation(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "elevation", "segment-01.json"
        )
        if not os.path.exists(path):
            pytest.skip("data/elevation/segment-01.json not found")
        with open(path) as f:
            return json.load(f)

    def test_output_structure(self, real_elevation):
        assert real_elevation["segment"] == 1
        assert len(real_elevation["distance"]) == len(real_elevation["elevation"])

    def test_power_in_reasonable_range(self, real_elevation):
        s = real_elevation["summary"]
        # Average power at 35km/h should be 100-600W for any segment
        assert 100 < s["avg_power_35kmh"] < 600

    def test_gradient_in_reasonable_range(self, real_elevation):
        s = real_elevation["summary"]
        assert 0 <= s["avg_gradient"] < 15
        assert s["max_gradient"] < 25
