"""Regression tests for stats-pipeline temporal coupling (issues #541, #328).

Two assertions trap the bug class:

1. `calculate_stats` does not consult `datetime.now()` at all — its output
   depends only on the daily log, the rider config, and an explicit
   `reference_date` argument. Same-day runs at different hours produce
   identical output.

2. Regenerating stats and points for the seg 11 publish date (2026-05-11)
   from the snapshot's frozen log produces values byte-identical to the
   hotfixed seg 11 snapshot (see issue #541 for the hotfix narrative).
"""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from processing.calculate_points import calculate_points
from processing.rider_stats import calculate_stats

SNAPSHOT_11_PATH = Path(__file__).resolve().parents[2] / "data" / "riders" / "snapshots" / "snapshot-11.json"


def _load_snapshot_11():
    with open(SNAPSHOT_11_PATH) as f:
        return json.load(f)


def _standard_rider_config():
    """The production rider-config.json shape — mirrors `data/riders/rider-config.json`."""
    return {
        "riders": [
            {"id": "justin", "name": "Justin", "color": "#DAA520"},
            {"id": "marian", "name": "Marian", "color": "#4682B4"},
            {"id": "nan", "name": "Nan", "color": "#FF00FF"},
            {"id": "wally", "name": "Wally", "color": "#8B0000"},
        ],
        "totalDistance": 185,
        "dailyCap": 2,
        "startDate": "2026-04-02",
    }


class TestNoDatetimeNowInStats:
    """`calculate_stats` must not call `datetime.now()` — it depends only on its
    inputs. This was the root cause of the #541 time-of-day finish-date bug."""

    def test_calculate_stats_does_not_call_datetime_now(self, monkeypatch):
        """Monkey-patch datetime in rider_stats so any `.now()` call raises."""
        from processing import rider_stats

        class _Forbidden:
            @classmethod
            def now(cls, *a, **kw):
                raise AssertionError(
                    "calculate_stats must not call datetime.now() — pass reference_date instead"
                )

            @classmethod
            def today(cls, *a, **kw):
                raise AssertionError(
                    "calculate_stats must not call datetime.today() — pass reference_date instead"
                )

        monkeypatch.setattr(rider_stats, "datetime", _Forbidden)

        log = {
            "entries": [
                {"date": "2026-04-02", "distances": {"justin": 2.0, "marian": 1.0, "nan": 2.0, "wally": 1.5}},
                {"date": "2026-04-03", "distances": {"justin": 2.0, "marian": 2.0, "nan": 2.0, "wally": 2.0}},
            ]
        }
        result = calculate_stats(log, _standard_rider_config(), reference_date=date(2026, 4, 3))
        assert result["asOf"] == "2026-04-03"
        assert result["entryNumber"] == 2

    def test_calculate_stats_output_independent_of_clock(self):
        """Two runs with the same reference_date must produce byte-identical output,
        regardless of when the clock ticks. This is the direct #541 assertion."""
        log = {
            "entries": [
                {"date": "2026-05-08", "distances": {"justin": 1.5, "marian": 1.0, "nan": 2.0, "wally": 1.5}},
                {"date": "2026-05-09", "distances": {"justin": 2.0, "marian": 2.0, "nan": 2.0, "wally": 2.0}},
            ]
        }
        config = _standard_rider_config()
        ref = date(2026, 5, 11)
        first = calculate_stats(log, config, reference_date=ref)
        second = calculate_stats(log, config, reference_date=ref)
        assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


class TestSegment11Regeneration:
    """Regenerate seg 11 stats + points from the frozen snapshot log; outputs must
    match the hotfixed snapshot values per #541.

    Reference_date = the segment's dataCutoff (2026-05-11). The snapshot's `asOf`
    is overridden downstream by snapshot_stats.py to the last log-entry date
    (2026-05-09); we assert against the per-rider values, which are computed by
    calculate_stats itself."""

    DATA_CUTOFF = date(2026, 5, 11)

    @pytest.fixture
    def snapshot(self):
        if not SNAPSHOT_11_PATH.exists():
            pytest.skip(f"Snapshot fixture not present at {SNAPSHOT_11_PATH}")
        return _load_snapshot_11()

    def test_stats_regenerate_matches_snapshot(self, snapshot):
        log = snapshot["log"]
        config = _standard_rider_config()
        result = calculate_stats(log, config, reference_date=self.DATA_CUTOFF)

        # Per-rider numeric fields must match the snapshot exactly. The snapshot's
        # asOf was overridden downstream — we don't assert on top-level asOf here.
        for rider_id in ("justin", "marian", "nan", "wally"):
            expected = snapshot["stats"]["riders"][rider_id]
            actual = result["riders"][rider_id]
            for field in (
                "totalDistanceCapped", "dailyAverageActual", "dailyAverageCapped",
                "longestDay", "shortestDay", "daysBelowThreeKm",
                "consistencyStdev", "bestThreeDayCombo", "recentFiveDayAverage",
                "distanceRemaining", "estimatedDaysToFinish", "estimatedFinishDate",
                "place",
            ):
                assert actual[field] == expected[field], (
                    f"{rider_id}.{field}: regenerated {actual[field]!r} != snapshot {expected[field]!r}"
                )

    def test_points_regenerate_matches_snapshot(self, snapshot):
        log = snapshot["log"]
        config = _standard_rider_config()
        points_config_path = Path(__file__).resolve().parents[2] / "data" / "competition" / "points-config.json"
        with open(points_config_path) as f:
            points_config = json.load(f)

        # calculate_points takes no reference_date — its only temporal input is
        # the daily log. The snapshot's log is the truth; regenerated points
        # must match.
        result = calculate_points(log, config, points_config, seed=42)

        for rider_id in ("justin", "marian", "nan", "wally"):
            expected = snapshot["points"]["riders"][rider_id]
            actual = result["riders"][rider_id]
            assert actual == expected, (
                f"{rider_id} points: regenerated {actual} != snapshot {expected}"
            )


class TestEstimatedFinishConsistency:
    """The displayed days and date must be derivable from one another via the
    chosen rounding rule — picking `floor` per the seg 11 hotfix (see PR body).
    For any rider: cutoff + estimatedDaysToFinish days == estimatedFinishDate."""

    def test_days_and_date_agree(self):
        log = {
            "entries": [
                # 50 days at 2 km/day capped → 100 km of 185. Remaining 85, avg 2.0, est 42.5 days.
                {"date": f"2026-04-{i+1:02d}" if i < 30 else f"2026-05-{i-29:02d}",
                 "distances": {"justin": 2.0, "marian": 2.0, "nan": 2.0, "wally": 2.0}}
                for i in range(50)
            ]
        }
        config = _standard_rider_config()
        ref = date(2026, 5, 20)
        result = calculate_stats(log, config, reference_date=ref)
        for rider_id in ("justin", "marian", "nan", "wally"):
            r = result["riders"][rider_id]
            days = r["estimatedDaysToFinish"]
            finish = r["estimatedFinishDate"]
            expected_finish = (ref + timedelta(days=days)).isoformat()
            assert finish == expected_finish, (
                f"{rider_id}: cutoff {ref} + {days} days = {expected_finish}, got {finish}"
            )
