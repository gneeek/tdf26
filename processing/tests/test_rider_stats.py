"""Tests for rider_stats.py — rider statistics calculations."""


from processing.rider_stats import calculate_stats


def make_config(daily_cap=2, total_distance=185):
    return {
        "riders": [
            {"id": "alice", "name": "Alice", "color": "#FF0000"},
            {"id": "bob", "name": "Bob", "color": "#0000FF"},
        ],
        "totalDistance": total_distance,
        "dailyCap": daily_cap,
        "startDate": "2026-04-02",
    }


def make_log(alice_dists, bob_dists=None):
    """Build a daily-log from distance lists, one entry per day."""
    if bob_dists is None:
        bob_dists = [0] * len(alice_dists)
    entries = []
    for i, (a, b) in enumerate(zip(alice_dists, bob_dists)):
        entries.append({
            "date": f"2026-04-{(i + 2):02d}",
            "distances": {"alice": a, "bob": b},
        })
    return {"entries": entries}


# --- Empty / edge cases ---

class TestEdgeCases:
    def test_empty_log(self):
        result = calculate_stats({"entries": []}, make_config())
        assert result["entryNumber"] == 0
        assert result["riders"] == {}

    def test_single_entry(self):
        log = make_log([1.5], [0.5])
        result = calculate_stats(log, make_config())
        alice = result["riders"]["alice"]
        assert alice["longestDay"] == 1.5
        assert alice["shortestDay"] == 1.5
        assert alice["bestThreeDayCombo"] == 1.5

    def test_all_zeros(self):
        log = make_log([0, 0, 0], [0, 0, 0])
        result = calculate_stats(log, make_config())
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 0
        assert alice["longestDay"] == 0
        assert alice["shortestDay"] == 0
        assert alice["estimatedDaysToFinish"] is None
        assert alice["estimatedFinishDate"] is None


# --- Rolling cap with carry-over ---

class TestRollingCap:
    def test_basic_carry(self):
        # Day 1: ride 1km, cap 2 -> credited 1, carry 1
        # Day 2: ride 3km, cap 2+1=3 -> credited 3, carry 0
        log = make_log([1.0, 3.0])
        result = calculate_stats(log, make_config(daily_cap=2))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 4.0

    def test_exceed_cap_no_carry(self):
        # Day 1: ride 5km, cap 2 -> credited 2, carry 0
        log = make_log([5.0])
        result = calculate_stats(log, make_config(daily_cap=2))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 2.0

    def test_multi_day_carry_accumulation(self):
        # Day 1: ride 0, cap 2 -> credited 0, carry 2
        # Day 2: ride 0, cap 2+2=4 -> credited 0, carry 4
        # Day 3: ride 6, cap 2+4=6 -> credited 6, carry 0
        log = make_log([0, 0, 6.0])
        result = calculate_stats(log, make_config(daily_cap=2))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 6.0

    def test_carry_caps_at_available(self):
        # Day 1: ride 0, carry 2
        # Day 2: ride 0, carry 4
        # Day 3: ride 10, available 6 -> credited 6
        log = make_log([0, 0, 10.0])
        result = calculate_stats(log, make_config(daily_cap=2))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 6.0

    def test_daily_rides_under_cap(self):
        # Ride 1km each day for 4 days, cap 2 -> credited 1 each, carry grows
        # Day 1: ride 1, cap 2, cred 1, carry 1
        # Day 2: ride 1, cap 3, cred 1, carry 2
        # Day 3: ride 1, cap 4, cred 1, carry 3
        # Day 4: ride 1, cap 5, cred 1, carry 4
        log = make_log([1, 1, 1, 1])
        result = calculate_stats(log, make_config(daily_cap=2))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 4.0


# --- Actual distance stats ---

class TestActualDistanceStats:
    def test_longest_day(self):
        log = make_log([1.0, 5.0, 3.0, 2.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["longestDay"] == 5.0

    def test_shortest_day_excludes_zero(self):
        log = make_log([0, 1.5, 3.0, 0, 2.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["shortestDay"] == 1.5

    def test_best_three_day_combo(self):
        log = make_log([1.0, 2.0, 5.0, 3.0, 1.0])
        result = calculate_stats(log, make_config())
        # Best 3 consecutive: 2+5+3 = 10
        assert result["riders"]["alice"]["bestThreeDayCombo"] == 10.0

    def test_best_three_day_with_two_entries(self):
        log = make_log([3.0, 4.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["bestThreeDayCombo"] == 7.0

    def test_recent_five_day_average(self):
        log = make_log([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
        result = calculate_stats(log, make_config())
        # Last 5: 3, 4, 5, 6, 7 -> avg 5.0
        assert result["riders"]["alice"]["recentFiveDayAverage"] == 5.0

    def test_recent_five_day_with_fewer_entries(self):
        log = make_log([2.0, 4.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["recentFiveDayAverage"] == 3.0

    def test_consistency_stdev(self):
        # Same distance every day -> stdev 0
        log = make_log([3.0, 3.0, 3.0, 3.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["consistencyStdev"] == 0.0

    def test_consistency_stdev_varies(self):
        log = make_log([1.0, 5.0, 1.0, 5.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["consistencyStdev"] > 0

    def test_days_below_three_km(self):
        log = make_log([1.0, 4.0, 2.5, 3.0, 0])
        result = calculate_stats(log, make_config())
        # Days below 3km: 1.0, 2.5, 0 = 3 days
        assert result["riders"]["alice"]["daysBelowThreeKm"] == 3

    def test_daily_average_actual(self):
        log = make_log([2.0, 4.0, 6.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["alice"]["dailyAverageActual"] == 4.0


# --- Capped stats ---

class TestCappedStats:
    def test_distance_remaining(self):
        log = make_log([2.0, 2.0, 2.0])
        result = calculate_stats(log, make_config(daily_cap=2, total_distance=10))
        alice = result["riders"]["alice"]
        assert alice["totalDistanceCapped"] == 6.0
        assert alice["distanceRemaining"] == 4.0

    def test_distance_remaining_never_negative(self):
        log = make_log([2.0] * 100)
        result = calculate_stats(log, make_config(daily_cap=2, total_distance=10))
        alice = result["riders"]["alice"]
        assert alice["distanceRemaining"] == 0.0

    def test_estimated_days_to_finish(self):
        log = make_log([2.0, 2.0])
        result = calculate_stats(log, make_config(daily_cap=2, total_distance=10))
        alice = result["riders"]["alice"]
        # Capped avg = 2.0, remaining = 6.0, est days = 3
        assert alice["estimatedDaysToFinish"] == 3

    def test_estimated_finish_date_present(self):
        log = make_log([2.0, 2.0])
        result = calculate_stats(log, make_config(daily_cap=2, total_distance=10))
        alice = result["riders"]["alice"]
        assert alice["estimatedFinishDate"] is not None
        # Should be a valid date string
        assert len(alice["estimatedFinishDate"]) == 10  # YYYY-MM-DD


# --- Rankings ---

class TestRankings:
    def test_correct_order_by_capped_distance(self):
        log = make_log([1.0, 1.0], [2.0, 2.0])
        result = calculate_stats(log, make_config())
        assert result["riders"]["bob"]["place"] == 1
        assert result["riders"]["alice"]["place"] == 2

    def test_all_riders_have_place(self):
        log = make_log([1.0], [2.0])
        result = calculate_stats(log, make_config())
        for rider_stats in result["riders"].values():
            assert "place" in rider_stats

    def test_entry_count(self):
        log = make_log([1.0, 2.0, 3.0])
        result = calculate_stats(log, make_config())
        assert result["entryNumber"] == 3


# --- Output structure ---

class TestOutputStructure:
    def test_rider_stats_have_all_fields(self):
        log = make_log([2.0, 3.0, 1.0])
        result = calculate_stats(log, make_config())
        expected_fields = {
            "totalDistanceCapped", "dailyAverageActual", "dailyAverageCapped",
            "longestDay", "shortestDay", "daysBelowThreeKm",
            "consistencyStdev", "bestThreeDayCombo", "recentFiveDayAverage",
            "distanceRemaining", "estimatedDaysToFinish", "estimatedFinishDate",
            "place",
        }
        alice = result["riders"]["alice"]
        assert expected_fields.issubset(alice.keys())

    def test_result_has_top_level_fields(self):
        log = make_log([1.0])
        result = calculate_stats(log, make_config())
        assert "asOf" in result
        assert "entryNumber" in result
        assert "riders" in result
