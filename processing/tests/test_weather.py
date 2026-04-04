"""Tests for weather.py — weather fetching and frontmatter injection."""

import json
from unittest.mock import MagicMock, patch

from processing.weather import (
    degree_to_compass,
    find_current_entry,
    get_weather,
    inject_weather_into_entry,
)

# --- degree_to_compass ---

class TestDegreeToCompass:
    def test_north(self):
        assert degree_to_compass(0) == "N"
        assert degree_to_compass(360) == "N"

    def test_east(self):
        assert degree_to_compass(90) == "E"

    def test_south(self):
        assert degree_to_compass(180) == "S"

    def test_west(self):
        assert degree_to_compass(270) == "W"

    def test_intermediate(self):
        assert degree_to_compass(45) == "NE"
        assert degree_to_compass(135) == "SE"
        assert degree_to_compass(225) == "SW"
        assert degree_to_compass(315) == "NW"


# --- get_weather ---

class TestGetWeather:
    def test_successful_fetch(self):
        mock_response = json.dumps({
            "main": {"temp": 18.3},
            "weather": [{"description": "broken clouds"}],
            "wind": {"speed": 3.5, "deg": 180},
        }).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = mock_response
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = get_weather(45.0, 1.5, "fake-key")

        assert result is not None
        assert result["current"]["temp"] == 18
        assert result["current"]["conditions"] == "Broken clouds"
        assert "km/h" in result["current"]["wind"]
        assert result["forecast"] is None

    def test_api_url_construction(self):
        """Verify the API is called with correct parameters."""
        with patch("urllib.request.urlopen", side_effect=Exception("test")) as mock_open:
            result = get_weather(45.1, 1.6, "my-key")

        assert result is None
        # Verify the request was made
        call_args = mock_open.call_args
        req = call_args[0][0]
        assert "lat=45.1" in req.full_url
        assert "lon=1.6" in req.full_url
        assert "appid=my-key" in req.full_url
        assert "units=metric" in req.full_url

    def test_handles_api_failure(self):
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            result = get_weather(45.0, 1.5, "fake-key")
        assert result is None


# --- inject_weather_into_entry ---

class TestInjectWeather:
    def test_replaces_weather_field(self, tmp_path):
        entry = tmp_path / "01-test.md"
        entry.write_text(
            "---\n"
            "segment: 1\n"
            "title: Test\n"
            "weather: null\n"
            "draft: false\n"
            "---\n"
            "# Content here\n"
        )

        weather = {"current": {"temp": 20, "conditions": "Clear", "wind": "5 km/h N"}, "forecast": None}
        inject_weather_into_entry(str(entry), weather)

        content = entry.read_text()
        assert '"temp": 20' in content
        assert "weather: null" not in content

    def test_preserves_other_fields(self, tmp_path):
        entry = tmp_path / "01-test.md"
        entry.write_text(
            "---\n"
            "segment: 1\n"
            "title: My Title\n"
            "weather: null\n"
            "draft: false\n"
            "---\n"
            "# Content here\n"
        )

        weather = {"current": {"temp": 15}, "forecast": None}
        inject_weather_into_entry(str(entry), weather)

        content = entry.read_text()
        assert "segment: 1" in content
        assert 'title: My Title' in content
        assert "draft: false" in content
        assert "# Content here" in content

    def test_replaces_existing_weather(self, tmp_path):
        entry = tmp_path / "01-test.md"
        entry.write_text(
            "---\n"
            "segment: 1\n"
            'weather: {"current": {"temp": 10}}\n'
            "draft: false\n"
            "---\n"
        )

        weather = {"current": {"temp": 25}, "forecast": None}
        inject_weather_into_entry(str(entry), weather)

        content = entry.read_text()
        assert '"temp": 25' in content
        assert '"temp": 10' not in content

    def test_no_change_when_weather_is_none(self, tmp_path):
        entry = tmp_path / "01-test.md"
        original = "---\nsegment: 1\nweather: null\n---\n"
        entry.write_text(original)

        inject_weather_into_entry(str(entry), None)

        assert entry.read_text() == original


# --- find_current_entry ---

class TestFindCurrentEntry:
    def test_finds_most_recent_published(self, tmp_path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()

        (entries_dir / "01-first.md").write_text(
            "---\nsegment: 1\npublishDate: 2026-01-01\ndraft: false\n---\n"
        )
        (entries_dir / "02-second.md").write_text(
            "---\nsegment: 2\npublishDate: 2026-01-05\ndraft: false\n---\n"
        )
        (entries_dir / "03-draft.md").write_text(
            "---\nsegment: 3\npublishDate: 2026-01-10\ndraft: true\n---\n"
        )

        segments = [
            {"segment": 1, "start_lat": 45.0, "end_lat": 45.1, "start_lng": 1.5, "end_lng": 1.6},
            {"segment": 2, "start_lat": 45.1, "end_lat": 45.2, "start_lng": 1.6, "end_lng": 1.7},
            {"segment": 3, "start_lat": 45.2, "end_lat": 45.3, "start_lng": 1.7, "end_lng": 1.8},
        ]
        seg_json = tmp_path / "segments.json"
        seg_json.write_text(json.dumps(segments))

        result = find_current_entry(str(entries_dir), str(seg_json))

        assert result is not None
        assert result["segment"] == 2
        assert result["lat"] is not None
        assert result["lng"] is not None

    def test_skips_drafts(self, tmp_path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()

        (entries_dir / "01-draft.md").write_text(
            "---\nsegment: 1\npublishDate: 2026-01-01\ndraft: true\n---\n"
        )

        seg_json = tmp_path / "segments.json"
        seg_json.write_text("[]")

        result = find_current_entry(str(entries_dir), str(seg_json))
        assert result is None

    def test_empty_directory(self, tmp_path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()

        seg_json = tmp_path / "segments.json"
        seg_json.write_text("[]")

        result = find_current_entry(str(entries_dir), str(seg_json))
        assert result is None
