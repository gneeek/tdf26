"""Tests for validate_points.py — cross-check between points-config and segments.json."""

import json
import os

import pytest

from processing.validate_points import validate


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
