"""Tests for suggest_images.py — Wikimedia Commons image suggestions."""

import json
from unittest.mock import patch, MagicMock

import pytest

from processing.suggest_images import (
    geosearch,
    get_image_info,
    process_segment,
)


# --- geosearch ---

class TestGeosearch:
    def test_successful_search(self):
        mock_data = json.dumps({
            "query": {
                "geosearch": [
                    {"pageid": 1, "title": "File:Photo1.jpg", "lat": 45.0, "lon": 1.5},
                    {"pageid": 2, "title": "File:Photo2.jpg", "lat": 45.01, "lon": 1.51},
                ]
            }
        }).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = mock_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = geosearch(45.0, 1.5)

        assert len(results) == 2
        assert results[0]["title"] == "File:Photo1.jpg"

    def test_api_url_has_correct_params(self):
        with patch("urllib.request.urlopen", side_effect=Exception("test")) as mock_open:
            geosearch(45.1, 1.6, radius=3000, limit=25)

        req = mock_open.call_args[0][0]
        assert "gscoord=45.1%7C1.6" in req.full_url
        assert "gsradius=3000" in req.full_url
        assert "gslimit=25" in req.full_url
        assert "gsnamespace=6" in req.full_url

    def test_handles_failure(self):
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            results = geosearch(45.0, 1.5)
        assert results == []

    def test_handles_empty_response(self):
        mock_data = json.dumps({"query": {"geosearch": []}}).encode()
        mock_resp = MagicMock()
        mock_resp.read.return_value = mock_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = geosearch(45.0, 1.5)
        assert results == []


# --- get_image_info ---

class TestGetImageInfo:
    def _mock_imageinfo_response(self, pages):
        mock_data = json.dumps({"query": {"pages": pages}}).encode()
        mock_resp = MagicMock()
        mock_resp.read.return_value = mock_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    def test_filters_cc_licensed(self):
        pages = {
            "1": {
                "title": "File:CC_Photo.jpg",
                "imageinfo": [{
                    "url": "https://example.com/photo.jpg",
                    "thumburl": "https://example.com/thumb.jpg",
                    "descriptionurl": "https://commons.wikimedia.org/wiki/File:CC_Photo.jpg",
                    "mime": "image/jpeg",
                    "width": 800,
                    "height": 600,
                    "extmetadata": {
                        "LicenseShortName": {"value": "CC BY-SA 4.0"},
                        "Artist": {"value": "Test Author"},
                        "ImageDescription": {"value": "A photo"},
                    },
                }],
            },
            "2": {
                "title": "File:NonCC.jpg",
                "imageinfo": [{
                    "url": "https://example.com/noncc.jpg",
                    "mime": "image/jpeg",
                    "width": 800,
                    "height": 600,
                    "extmetadata": {
                        "LicenseShortName": {"value": "All rights reserved"},
                        "Artist": {"value": "Someone"},
                        "ImageDescription": {"value": ""},
                    },
                }],
            },
        }
        mock_resp = self._mock_imageinfo_response(pages)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = get_image_info(["File:CC_Photo.jpg", "File:NonCC.jpg"])

        assert len(results) == 1
        assert results[0]["license"] == "CC BY-SA 4.0"

    def test_filters_small_images(self):
        pages = {
            "1": {
                "title": "File:Tiny.jpg",
                "imageinfo": [{
                    "url": "https://example.com/tiny.jpg",
                    "mime": "image/jpeg",
                    "width": 200,
                    "height": 150,
                    "extmetadata": {
                        "LicenseShortName": {"value": "CC BY 4.0"},
                        "Artist": {"value": "Author"},
                        "ImageDescription": {"value": ""},
                    },
                }],
            },
        }
        mock_resp = self._mock_imageinfo_response(pages)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = get_image_info(["File:Tiny.jpg"])

        assert len(results) == 0

    def test_filters_svg(self):
        pages = {
            "1": {
                "title": "File:Map.svg",
                "imageinfo": [{
                    "url": "https://example.com/map.svg",
                    "mime": "image/svg+xml",
                    "width": 800,
                    "height": 600,
                    "extmetadata": {
                        "LicenseShortName": {"value": "CC BY-SA 4.0"},
                        "Artist": {"value": "Author"},
                        "ImageDescription": {"value": ""},
                    },
                }],
            },
        }
        mock_resp = self._mock_imageinfo_response(pages)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = get_image_info(["File:Map.svg"])

        assert len(results) == 0

    def test_empty_titles(self):
        results = get_image_info([])
        assert results == []

    def test_output_structure(self):
        pages = {
            "1": {
                "title": "File:Test.jpg",
                "imageinfo": [{
                    "url": "https://example.com/full.jpg",
                    "thumburl": "https://example.com/thumb.jpg",
                    "descriptionurl": "https://commons.wikimedia.org/wiki/File:Test.jpg",
                    "mime": "image/jpeg",
                    "width": 1024,
                    "height": 768,
                    "extmetadata": {
                        "LicenseShortName": {"value": "CC BY 2.0"},
                        "Artist": {"value": "Photographer"},
                        "ImageDescription": {"value": "Nice photo"},
                    },
                }],
            },
        }
        mock_resp = self._mock_imageinfo_response(pages)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = get_image_info(["File:Test.jpg"])

        assert len(results) == 1
        img = results[0]
        assert img["title"] == "File:Test.jpg"
        assert img["url"] == "https://example.com/thumb.jpg"
        assert img["full_url"] == "https://example.com/full.jpg"
        assert img["width"] == 1024
        assert img["height"] == 768
        assert img["license"] == "CC BY 2.0"
        assert img["artist"] == "Photographer"
        assert img["description"] == "Nice photo"

    def test_accepts_public_domain(self):
        pages = {
            "1": {
                "title": "File:PD.jpg",
                "imageinfo": [{
                    "url": "https://example.com/pd.jpg",
                    "mime": "image/jpeg",
                    "width": 800,
                    "height": 600,
                    "extmetadata": {
                        "LicenseShortName": {"value": "Public domain"},
                        "Artist": {"value": "Old Author"},
                        "ImageDescription": {"value": ""},
                    },
                }],
            },
        }
        mock_resp = self._mock_imageinfo_response(pages)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            results = get_image_info(["File:PD.jpg"])

        assert len(results) == 1


# --- process_segment ---

class TestProcessSegment:
    def test_uses_midpoint_coordinates(self):
        segment = {
            "start_lat": 45.0, "end_lat": 45.1,
            "start_lng": 1.5, "end_lng": 1.6,
        }

        with patch("processing.suggest_images.geosearch", return_value=[]) as mock_geo:
            process_segment(segment)

        mock_geo.assert_called_once()
        call_lat, call_lng = mock_geo.call_args[0][:2]
        assert call_lat == pytest.approx(45.05)
        assert call_lng == pytest.approx(1.55)

    def test_sorts_by_width(self):
        segment = {
            "start_lat": 45.0, "end_lat": 45.1,
            "start_lng": 1.5, "end_lng": 1.6,
        }

        geo_results = [
            {"title": "File:Small.jpg"},
            {"title": "File:Large.jpg"},
        ]

        image_results = [
            {"title": "File:Small.jpg", "width": 400, "height": 300,
             "url": "", "full_url": "", "description_url": "",
             "license": "CC BY 4.0", "artist": "", "description": ""},
            {"title": "File:Large.jpg", "width": 1200, "height": 900,
             "url": "", "full_url": "", "description_url": "",
             "license": "CC BY 4.0", "artist": "", "description": ""},
        ]

        with patch("processing.suggest_images.geosearch", return_value=geo_results), \
             patch("processing.suggest_images.get_image_info", return_value=image_results):
            results = process_segment(segment)

        assert results[0]["width"] >= results[1]["width"]

    def test_empty_geosearch(self):
        segment = {
            "start_lat": 45.0, "end_lat": 45.1,
            "start_lng": 1.5, "end_lng": 1.6,
        }

        with patch("processing.suggest_images.geosearch", return_value=[]):
            results = process_segment(segment)

        assert results == []
