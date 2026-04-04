"""Tests for generate_narrative.py - race narrative generation."""

from processing.generate_narrative import (
    format_category,
    format_rest,
    generate_narrative,
    rider_name,
)

CONFIG = {
    "riders": [
        {"id": "alice", "name": "Alice", "color": "#FF0000"},
        {"id": "bob", "name": "Bob", "color": "#0000FF"},
    ],
}


def make_points(locations):
    return {"riders": {}, "locations": locations}


class TestRiderName:
    def test_found(self):
        assert rider_name("alice", CONFIG) == "Alice"

    def test_fallback(self):
        assert rider_name("unknown", CONFIG) == "unknown"


class TestFormatCategory:
    def test_hc(self):
        assert format_category("HC") == "Hors Categorie"

    def test_numbered(self):
        assert format_category(2) == "Cat 2"


class TestFormatRest:
    def test_no_others(self):
        awards = [{"place": 1, "rider": "alice", "points": 20}]
        assert "No other riders" in format_rest(awards, CONFIG)

    def test_one_other(self):
        awards = [
            {"place": 1, "rider": "alice", "points": 20},
            {"place": 2, "rider": "bob", "points": 17},
        ]
        result = format_rest(awards, CONFIG)
        assert "Bob" in result
        assert "17" in result

    def test_zero_points_excluded(self):
        awards = [
            {"place": 1, "rider": "alice", "points": 6},
            {"place": 2, "rider": "bob", "points": 0},
        ]
        result = format_rest(awards, CONFIG)
        assert "Bob" not in result


class TestGenerateNarrative:
    def test_no_locations_in_segment(self):
        points = make_points([
            {"name": "Sprint 1", "type": "sprint", "segment": 5, "km": 30,
             "reached": True, "awards": [{"place": 1, "rider": "alice", "points": 20}]},
        ])
        result = generate_narrative(points, CONFIG, segment=1)
        assert "no" in result.lower() or "No" in result

    def test_sprint_narrative(self):
        points = make_points([
            {"name": "Sprint - Turenne", "type": "sprint", "segment": 3, "km": 17,
             "reached": True, "awards": [
                 {"place": 1, "rider": "alice", "points": 20},
                 {"place": 2, "rider": "bob", "points": 17},
             ]},
        ])
        result = generate_narrative(points, CONFIG, segment=3)
        assert "Alice" in result
        assert "20" in result
        assert "Turenne" in result

    def test_climb_narrative(self):
        points = make_points([
            {"name": "Suc au May", "type": "climb", "segment": 15, "km": 104.8,
             "category": "HC", "reached": True, "awards": [
                 {"place": 1, "rider": "bob", "points": 10},
                 {"place": 2, "rider": "alice", "points": 8},
             ]},
        ])
        result = generate_narrative(points, CONFIG, segment=15)
        assert "Bob" in result
        assert "10" in result
        assert "Suc au May" in result
        assert "Hors Categorie" in result or "HC" in result

    def test_not_reached(self):
        points = make_points([
            {"name": "Sprint - Bugeat", "type": "sprint", "segment": 19, "km": 130,
             "reached": False, "awards": []},
        ])
        result = generate_narrative(points, CONFIG, segment=19)
        assert "Bugeat" in result
        assert "await" in result.lower() or "unclaimed" in result.lower()

    def test_seed_consistency(self):
        points = make_points([
            {"name": "Test Sprint", "type": "sprint", "segment": 1, "km": 5,
             "reached": True, "awards": [{"place": 1, "rider": "alice", "points": 20}]},
        ])
        r1 = generate_narrative(points, CONFIG, segment=1, seed=42)
        r2 = generate_narrative(points, CONFIG, segment=1, seed=42)
        assert r1 == r2

    def test_multiple_locations_in_segment(self):
        points = make_points([
            {"name": "Sprint A", "type": "sprint", "segment": 3, "km": 15,
             "reached": True, "awards": [{"place": 1, "rider": "alice", "points": 20}]},
            {"name": "Climb B", "type": "climb", "segment": 3, "km": 18,
             "category": 3, "reached": True, "awards": [{"place": 1, "rider": "bob", "points": 4}]},
        ])
        result = generate_narrative(points, CONFIG, segment=3)
        assert "Sprint A" in result
        assert "Climb B" in result

    def test_empty_points_data(self):
        result = generate_narrative({"riders": {}, "locations": []}, CONFIG, segment=1)
        assert len(result) > 0
