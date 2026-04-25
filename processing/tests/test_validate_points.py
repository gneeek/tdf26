"""Tests for validate_points.py — cross-check between points-config and segments.json."""

import json
import os

import pytest

from processing.validate_points import (
    elevation_at_km,
    load_elevation_track,
    validate,
    validate_elevation,
)


@pytest.fixture
def minimal_segments():
    return [
        {"segment": 1, "km_start": 0.0, "km_end": 8.0, "climbs": []},
        {"segment": 2, "km_start": 8.0, "km_end": 14.0, "climbs": []},
        {"segment": 3, "km_start": 14.0, "km_end": 22.0, "climbs": []},
        {"segment": 4, "km_start": 22.0, "km_end": 28.0, "climbs": []},
        {"segment": 5, "km_start": 28.0, "km_end": 36.0, "climbs": []},
    ]


class TestClimbValidation:
    def test_summit_in_declared_segment_passes(self, minimal_segments):
        minimal_segments[4]["climbs"] = ["Puy Boubou"]
        config = {"climbs": [{"name": "Puy Boubou", "segment": 5, "km": 32.8, "length_km": 2.8}]}
        assert validate(config, minimal_segments) == []

    def test_summit_outside_declared_segment_fails(self, minimal_segments):
        minimal_segments[3]["climbs"] = ["Puy Boubou"]
        config = {"climbs": [{"name": "Puy Boubou", "segment": 4, "km": 32.8, "length_km": 2.8}]}
        errors = validate(config, minimal_segments)
        assert any("falls outside declared segment 4" in e for e in errors)

    def test_climb_missing_from_segment_fails(self, minimal_segments):
        config = {"climbs": [{"name": "Puy Boubou", "segment": 5, "km": 32.8, "length_km": 2.8}]}
        errors = validate(config, minimal_segments)
        assert any("missing from segments" in e for e in errors)

    def test_summit_only_climb_passes(self, minimal_segments):
        minimal_segments[0]["climbs"] = ["Côte de Malemort"]
        config = {"climbs": [{"name": "Côte de Malemort", "segment": 1, "km": 5, "length_km": None}]}
        assert validate(config, minimal_segments) == []

    def test_spanning_climb_requires_both_segments(self, minimal_segments):
        # Span from km 30 to 32.8 crosses only segment 5 (28-36), so only seg 5 required
        minimal_segments[4]["climbs"] = ["Puy Boubou"]
        config = {"climbs": [{"name": "Puy Boubou", "segment": 5, "km": 32.8, "length_km": 2.8}]}
        assert validate(config, minimal_segments) == []

        # A climb with span crossing segments 6 and 7 must appear on both
        segs = [
            {"segment": 6, "km_start": 36.0, "km_end": 42.0, "climbs": ["Côte de Lagleygeolle"]},
            {"segment": 7, "km_start": 42.0, "km_end": 50.0, "climbs": []},
        ]
        config = {"climbs": [{"name": "Côte de Lagleygeolle", "segment": 7, "km": 43.2, "length_km": 5.2}]}
        errors = validate(config, segs)
        assert any("missing from segments [7]" in e for e in errors)


class TestSprintValidation:
    def test_sprint_in_segment_passes(self, minimal_segments):
        config = {"sprints": [{"name": "Sprint - Brive", "segment": 1, "km": 3}]}
        assert validate(config, minimal_segments) == []

    def test_sprint_outside_segment_fails(self, minimal_segments):
        config = {"sprints": [{"name": "Sprint - Brive", "segment": 2, "km": 3}]}
        errors = validate(config, minimal_segments)
        assert any("falls outside declared segment 2" in e for e in errors)


class TestRealData:
    """Integration test against the project's real data files."""

    def test_real_data_validates(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        points_path = os.path.join(root, "data", "competition", "points-config.json")
        segments_path = os.path.join(root, "data", "segments.json")
        if not (os.path.exists(points_path) and os.path.exists(segments_path)):
            pytest.skip("real data files not found")
        with open(points_path) as f:
            points = json.load(f)
        with open(segments_path) as f:
            segments = json.load(f)
        errors = validate(points, segments)
        assert errors == [], f"real data has divergences: {errors}"


class TestElevationAtKm:
    @pytest.fixture
    def synthetic_track(self):
        # Climb from 0 to 5 km gaining 100 m, then descend to 10 km losing 100 m.
        return [(0.0, 200.0), (2.5, 250.0), (5.0, 300.0), (7.5, 250.0), (10.0, 200.0)]

    def test_interpolates_between_vertices(self, synthetic_track):
        assert elevation_at_km(synthetic_track, 1.25) == pytest.approx(225.0)

    def test_clamps_below_first(self, synthetic_track):
        assert elevation_at_km(synthetic_track, -1) == 200.0

    def test_clamps_above_last(self, synthetic_track):
        assert elevation_at_km(synthetic_track, 100) == 200.0


class TestValidateElevation:
    @pytest.fixture
    def good_track(self):
        # Symmetric climb peaking at km 5 (300 m), descending to km 10 (200 m).
        return [(float(i), 200.0 + (100 - abs(50 - i * 10) * 2)) for i in range(11)]

    def test_summit_on_descending_flank_fails(self, good_track):
        # Track peaks at km 5; declare summit at km 7 (descending side).
        climbs = [{"name": "Test Climb", "km": 7.0, "length_km": 1.0, "gradient": 5.0}]
        errors = validate_elevation(climbs, good_track)
        assert any("descending flank" in e for e in errors)

    def test_summit_at_actual_peak_passes(self, good_track):
        # Climb of 1km at 4% (rising 40m); track at peak is 300, at km 4 is 280.
        climbs = [{"name": "Test Climb", "km": 5.0, "length_km": 1.0, "gradient": 4.0}]
        errors = validate_elevation(climbs, good_track)
        # Filter to the rising-into-summit error; gradient consistency is a separate concern.
        assert not any("descending flank" in e for e in errors)

    def test_gradient_consistency_passes_at_match(self, good_track):
        # km 5 ele 300, km 4 ele 280 → 20m gain over 1km = 2% gradient.
        climbs = [{"name": "Match Climb", "km": 5.0, "length_km": 1.0, "gradient": 2.0}]
        errors = validate_elevation(climbs, good_track)
        assert not any("expects" in e for e in errors)

    def test_gradient_consistency_fails_when_inflated(self, good_track):
        # Declare 10% gradient when actual is 2%.
        climbs = [{"name": "Inflated Climb", "km": 5.0, "length_km": 1.0, "gradient": 10.0}]
        errors = validate_elevation(climbs, good_track)
        assert any("Inflated Climb" in e and "expects" in e for e in errors)

    def test_point_summit_skips_gradient_check(self, good_track):
        # length_km=None: only the rising-into-summit check applies.
        climbs = [{"name": "Point Summit", "km": 5.0, "length_km": None, "gradient": 5.0}]
        errors = validate_elevation(climbs, good_track)
        assert errors == []

    def test_real_data_passes(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        points_path = os.path.join(root, "data", "competition", "points-config.json")
        segments_path = os.path.join(root, "data", "segments.json")
        elev_dir = os.path.join(root, "data", "elevation")
        if not (os.path.exists(points_path) and os.path.exists(segments_path) and os.path.isdir(elev_dir)):
            pytest.skip("real data not found")
        with open(points_path) as f:
            points = json.load(f)
        with open(segments_path) as f:
            segments = json.load(f)
        track = load_elevation_track(elev_dir, segments)
        errors = validate_elevation(points.get("climbs", []), track)
        assert errors == [], f"real climbs have elevation divergences: {errors}"
