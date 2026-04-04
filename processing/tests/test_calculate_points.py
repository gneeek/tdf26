"""Tests for calculate_points.py - sprint and climbing point calculations."""

from processing.calculate_points import (
    calculate_capped_distances,
    calculate_points,
    find_arrival_day,
)


def make_config(daily_cap=2):
    return {
        "riders": [
            {"id": "alice", "name": "Alice", "color": "#FF0000"},
            {"id": "bob", "name": "Bob", "color": "#0000FF"},
        ],
        "totalDistance": 185,
        "dailyCap": daily_cap,
        "startDate": "2026-04-02",
    }


def make_log(alice_dists, bob_dists=None):
    if bob_dists is None:
        bob_dists = [0] * len(alice_dists)
    entries = []
    for i, (a, b) in enumerate(zip(alice_dists, bob_dists)):
        entries.append({
            "date": f"2026-04-{(i + 2):02d}",
            "distances": {"alice": a, "bob": b},
        })
    return {"entries": entries}


SIMPLE_POINTS_CONFIG = {
    "sprints": [
        {"name": "Sprint 1", "segment": 1, "km": 5, "points": [20, 17, 15, 13]},
    ],
    "climbs": [
        {"name": "Climb 1", "segment": 2, "km": 10, "points": [6, 4, 2, 1]},
    ],
}


class TestCappedDistances:
    def test_basic_accumulation(self):
        log = make_log([2.0, 2.0, 2.0], [1.0, 1.0, 1.0])
        result = calculate_capped_distances(log, make_config(daily_cap=2))
        alice = result["alice"]
        assert alice[-1]["cumulative_km"] == 6.0
        bob = result["bob"]
        assert bob[-1]["cumulative_km"] == 3.0

    def test_cap_applied(self):
        log = make_log([10.0], [10.0])
        result = calculate_capped_distances(log, make_config(daily_cap=2))
        assert result["alice"][-1]["cumulative_km"] == 2.0

    def test_carry_over(self):
        # Day 1: ride 0, carry 2. Day 2: ride 4, available 4, credited 4.
        log = make_log([0, 4.0])
        result = calculate_capped_distances(log, make_config(daily_cap=2))
        assert result["alice"][-1]["cumulative_km"] == 4.0


class TestFindArrivalDay:
    def test_finds_first_day_past_mark(self):
        progress = [
            {"date": "2026-04-02", "cumulative_km": 2.0},
            {"date": "2026-04-03", "cumulative_km": 4.0},
            {"date": "2026-04-04", "cumulative_km": 6.0},
        ]
        date, km = find_arrival_day(progress, 5.0)
        assert date == "2026-04-04"
        assert km == 6.0

    def test_exact_match(self):
        progress = [
            {"date": "2026-04-02", "cumulative_km": 5.0},
        ]
        date, km = find_arrival_day(progress, 5.0)
        assert date == "2026-04-02"

    def test_not_yet_reached(self):
        progress = [
            {"date": "2026-04-02", "cumulative_km": 2.0},
        ]
        assert find_arrival_day(progress, 10.0) is None

    def test_empty_progress(self):
        assert find_arrival_day([], 5.0) is None


class TestCalculatePoints:
    def test_no_points_when_not_reached(self):
        log = make_log([1.0])
        result = calculate_points(log, make_config(), SIMPLE_POINTS_CONFIG)
        assert result["riders"]["alice"]["totalPoints"] == 0
        assert result["locations"][0]["reached"] is False

    def test_sprint_points_awarded(self):
        # Alice reaches km 5 first (day 3), Bob reaches day 4
        log = make_log([2.0, 2.0, 2.0, 2.0], [1.0, 1.0, 1.0, 2.0])
        config = make_config(daily_cap=2)
        result = calculate_points(log, config, SIMPLE_POINTS_CONFIG)
        alice = result["riders"]["alice"]
        bob = result["riders"]["bob"]
        # Alice arrives day 3 (6km), Bob arrives day 4 (5km)
        assert alice["sprintPoints"] == 20
        assert bob["sprintPoints"] == 17

    def test_climb_points_awarded(self):
        # Both reach km 10 eventually
        log = make_log([2.0] * 6, [2.0] * 6)
        config = make_config(daily_cap=2)
        result = calculate_points(log, config, SIMPLE_POINTS_CONFIG)
        # Both arrive on same day (day 5, 10km) - tiebreak is random but seeded
        alice_climb = result["riders"]["alice"]["climbPoints"]
        bob_climb = result["riders"]["bob"]["climbPoints"]
        assert {alice_climb, bob_climb} == {6, 4}

    def test_only_reached_locations_have_awards(self):
        log = make_log([2.0, 2.0, 2.0])  # 6km - past sprint at 5, not climb at 10
        result = calculate_points(log, make_config(), SIMPLE_POINTS_CONFIG)
        sprint = result["locations"][0]
        climb = result["locations"][1]
        assert sprint["reached"] is True
        assert len(sprint["awards"]) > 0
        assert climb["reached"] is False
        assert len(climb["awards"]) == 0

    def test_seed_produces_consistent_results(self):
        log = make_log([2.0] * 6, [2.0] * 6)
        config = make_config(daily_cap=2)
        r1 = calculate_points(log, config, SIMPLE_POINTS_CONFIG, seed=42)
        r2 = calculate_points(log, config, SIMPLE_POINTS_CONFIG, seed=42)
        assert r1 == r2

    def test_different_seed_may_change_tiebreak(self):
        log = make_log([2.0] * 6, [2.0] * 6)
        config = make_config(daily_cap=2)
        # With identical progress, tiebreak depends on seed
        r1 = calculate_points(log, config, SIMPLE_POINTS_CONFIG, seed=1)
        r2 = calculate_points(log, config, SIMPLE_POINTS_CONFIG, seed=2)
        # At least one location should potentially differ (not guaranteed but likely)
        # Just verify both are valid
        assert r1["riders"]["alice"]["totalPoints"] + r1["riders"]["bob"]["totalPoints"] > 0
        assert r2["riders"]["alice"]["totalPoints"] + r2["riders"]["bob"]["totalPoints"] > 0

    def test_empty_log(self):
        log = {"entries": []}
        result = calculate_points(log, make_config(), SIMPLE_POINTS_CONFIG)
        assert result["riders"]["alice"]["totalPoints"] == 0
        assert all(not loc["reached"] for loc in result["locations"])

    def test_total_points_is_sum(self):
        log = make_log([2.0] * 6, [1.0] * 10)
        config = make_config(daily_cap=2)
        result = calculate_points(log, config, SIMPLE_POINTS_CONFIG)
        for rider_id, totals in result["riders"].items():
            assert totals["totalPoints"] == totals["sprintPoints"] + totals["climbPoints"]

    def test_location_results_structure(self):
        log = make_log([2.0] * 3)
        result = calculate_points(log, make_config(), SIMPLE_POINTS_CONFIG)
        for loc in result["locations"]:
            assert "name" in loc
            assert "type" in loc
            assert loc["type"] in ("sprint", "climb")
            assert "segment" in loc
            assert "km" in loc
            assert "reached" in loc
            assert "awards" in loc
