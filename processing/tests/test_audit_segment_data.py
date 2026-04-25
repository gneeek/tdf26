"""Tests for audit_segment_data.py — closest-approach km for places along the route."""

import json
import os
import subprocess
import sys

import pytest

from processing.audit_segment_data import (
    build_master_track,
    build_report_dict,
    nearest_km_and_distance,
    project_onto_segment,
)


class TestProjectOntoSegment:
    """Project a query point onto a single polyline segment."""

    def test_projection_lies_within_segment(self):
        # Segment from (45.0, 1.5) to (45.0, 1.6) with A at km 0 and B at km ~7.85.
        # Query point (45.0, 1.55) is exactly on the segment at midpoint.
        A = (45.0, 1.5, 0.0)
        B = (45.0, 1.6, 7.85)
        km, dist_m = project_onto_segment(45.0, 1.55, *A, *B)
        assert km == pytest.approx(3.925, abs=0.01)
        assert dist_m == pytest.approx(0.0, abs=1.0)

    def test_projection_clamps_before_a(self):
        # Query west of A -> closest point is A itself.
        A = (45.0, 1.5, 0.0)
        B = (45.0, 1.6, 7.85)
        km, _ = project_onto_segment(45.0, 1.4, *A, *B)
        assert km == pytest.approx(0.0, abs=0.001)

    def test_projection_clamps_after_b(self):
        A = (45.0, 1.5, 0.0)
        B = (45.0, 1.6, 7.85)
        km, _ = project_onto_segment(45.0, 1.7, *A, *B)
        assert km == pytest.approx(7.85, abs=0.001)

    def test_perpendicular_distance(self):
        # Query 1 km north of segment midpoint should report ~1000m distance.
        A = (45.0, 1.5, 0.0)
        B = (45.0, 1.6, 7.85)
        lat_offset = 1.0 / 111.0  # ~1 km north
        _, dist_m = project_onto_segment(45.0 + lat_offset, 1.55, *A, *B)
        assert dist_m == pytest.approx(1000.0, rel=0.01)


class TestBuildMasterTrack:
    def test_track_spans_full_route(self, segments_dir):
        track = build_master_track(segments_dir)
        assert len(track) > 1000, "expected a dense polyline"
        total_km = track[-1][2]
        assert total_km == pytest.approx(185.0, abs=5.0)

    def test_track_cum_km_is_monotonic(self, segments_dir):
        track = build_master_track(segments_dir)
        for i in range(1, len(track)):
            assert track[i][2] >= track[i - 1][2]


class TestNearestKmAndDistance:
    """Integration test against the real master track."""

    def test_beynat_lands_at_km_46_23(self, segments_dir):
        # Fixture answer established in town-positions.ts (verified 2026-04-21).
        # Beynat village centre at 45.1268, 1.7362 -> route km 46.23, ~75 m from route.
        track = build_master_track(segments_dir)
        km, dist_m = nearest_km_and_distance(track, 45.1268, 1.7362)
        assert km == pytest.approx(46.23, abs=0.1)
        assert dist_m == pytest.approx(75.0, abs=30.0)

    def test_malemort_lands_near_start(self, segments_dir):
        # Malemort at 45.13834, 1.54947 is the start of the route.
        track = build_master_track(segments_dir)
        km, dist_m = nearest_km_and_distance(track, 45.13834, 1.54947)
        assert km < 1.0
        assert dist_m < 100.0


class TestJsonOutput:
    """The --json flag emits a structured document the next two issues can consume."""

    def test_build_report_dict_shape(self):
        # Synthetic rows; just check the dict structure round-trips through JSON.
        town_rows = [{
            "name": "Test Town", "stored_km": 10.0, "computed_km": 10.05,
            "distance_m": 50, "computed_segment": 2, "stored_segments": [2],
            "notes": "ok",
        }]
        report = build_report_dict(
            as_of="2026-04-25",
            track_len=100,
            total_km=185.0,
            town_rows=town_rows,
            climb_rows=[],
            sprint_rows=[],
            attraction_rows=[],
            notable_rows=[],
        )
        assert report["as_of"] == "2026-04-25"
        assert report["track"]["points"] == 100
        assert report["track"]["total_km"] == pytest.approx(185.0)
        assert report["towns"] == town_rows
        for key in ("climbs", "sprints", "attractions", "notable_points"):
            assert report[key] == []
        # Round-trips through JSON.
        assert json.loads(json.dumps(report)) == report

    def test_json_flag_emits_valid_json(self, segments_dir, tmp_path):
        repo_root = os.path.join(os.path.dirname(__file__), "..", "..")
        out = tmp_path / "audit.json"
        subprocess.run(
            [
                sys.executable, os.path.join(repo_root, "processing", "audit_segment_data.py"),
                "--json", "--output", str(out),
            ],
            check=True,
        )
        data = json.loads(out.read_text())
        assert "towns" in data and isinstance(data["towns"], list)
        assert "climbs" in data and isinstance(data["climbs"], list)
        assert data["track"]["points"] > 1000


@pytest.fixture
def segments_dir():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    path = os.path.join(root, "data", "segments")
    if not os.path.isdir(path):
        pytest.skip("data/segments not present")
    return path
