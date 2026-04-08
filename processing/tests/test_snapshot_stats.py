"""Tests for snapshot_stats.py - per-segment stats snapshots."""

import json
import os

from processing.snapshot_stats import create_snapshot


class TestCreateSnapshot:
    def test_creates_snapshot_file(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats.write_text(json.dumps({"asOf": "2026-04-04", "riders": {}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": []}))

        path = create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))

        assert os.path.exists(path)
        assert path.endswith("snapshot-01.json")

    def test_snapshot_contains_all_data(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats_data = {"asOf": "2026-04-04", "riders": {"alice": {"place": 1}}}
        points_data = {"riders": {"alice": {"sprintPoints": 5}}, "locations": []}
        log_data = {"entries": [{"date": "2026-04-02", "distances": {"alice": 2.0}}]}

        stats.write_text(json.dumps(stats_data))
        points.write_text(json.dumps(points_data))
        log.write_text(json.dumps(log_data))

        path = create_snapshot(str(stats), str(points), str(log), 3, str(output_dir))

        with open(path) as f:
            snapshot = json.load(f)

        assert snapshot["segment"] == 3
        expected_stats = {**stats_data, "asOf": "2026-04-02"}  # overridden to last log entry
        assert snapshot["stats"] == expected_stats
        assert snapshot["points"] == points_data
        assert snapshot["log"] == log_data

    def test_missing_points_file_uses_empty(self, tmp_path):
        stats = tmp_path / "stats.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"
        missing_points = tmp_path / "nonexistent.json"

        stats.write_text(json.dumps({"riders": {}}))
        log.write_text(json.dumps({"entries": []}))

        path = create_snapshot(str(stats), str(missing_points), str(log), 0, str(output_dir))

        with open(path) as f:
            snapshot = json.load(f)

        assert snapshot["points"] == {"riders": {}, "locations": []}

    def test_segment_zero_padded_filename(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats.write_text(json.dumps({"riders": {}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": []}))

        path = create_snapshot(str(stats), str(points), str(log), 5, str(output_dir))
        assert "snapshot-05.json" in path

        path = create_snapshot(str(stats), str(points), str(log), 26, str(output_dir))
        assert "snapshot-26.json" in path

    def test_creates_output_directory(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "deep" / "nested" / "snapshots"

        stats.write_text(json.dumps({"riders": {}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": []}))

        path = create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))
        assert os.path.exists(path)

    def test_asof_date_matches_last_log_entry(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats.write_text(json.dumps({"asOf": "2026-04-07", "riders": {}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": [
            {"date": "2026-04-01", "distances": {}},
            {"date": "2026-04-04", "distances": {}},
        ]}))

        path = create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))

        with open(path) as f:
            snapshot = json.load(f)

        assert snapshot["stats"]["asOf"] == "2026-04-04"

    def test_asof_unchanged_when_no_log_entries(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats.write_text(json.dumps({"asOf": "2026-04-07", "riders": {}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": []}))

        path = create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))

        with open(path) as f:
            snapshot = json.load(f)

        assert snapshot["stats"]["asOf"] == "2026-04-07"

    def test_overwrites_existing_snapshot(self, tmp_path):
        stats = tmp_path / "stats.json"
        points = tmp_path / "points.json"
        log = tmp_path / "log.json"
        output_dir = tmp_path / "snapshots"

        stats.write_text(json.dumps({"riders": {"v": 1}}))
        points.write_text(json.dumps({"riders": {}, "locations": []}))
        log.write_text(json.dumps({"entries": []}))

        create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))

        stats.write_text(json.dumps({"riders": {"v": 2}}))
        path = create_snapshot(str(stats), str(points), str(log), 1, str(output_dir))

        with open(path) as f:
            snapshot = json.load(f)

        assert snapshot["stats"]["riders"]["v"] == 2
